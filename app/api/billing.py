from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import extract
import uuid
from datetime import datetime, timedelta

from app.api.deps import get_db, get_current_tenant, require_role
from app.models.billing_cycle import BillingCycle
from app.models.invoice import Invoice

from app.services.billing_service import calculate_bill
from app.services.payment_service import create_razorpay_order


router = APIRouter(prefix="/billing", tags=["Billing"])


# =========================
# 🧾 GENERATE BILL (MANUAL)
# =========================
@router.post("/generate")
def generate_bill(
    db: Session = Depends(get_db),
    tenant=Depends(get_current_tenant),
    user=Depends(require_role(["institute_admin"]))
):
    # =========================
    # 🔍 VALIDATE TENANT CONFIG
    # =========================
    if not tenant.slab_limit or not tenant.plan:
        raise HTTPException(status_code=400, detail="Tenant billing config missing")

    now = datetime.utcnow()

    # =========================
    # 🔒 PREVENT DUPLICATE BILLING (MONTHLY)
    # =========================
    existing = db.query(BillingCycle).filter(
        BillingCycle.tenant_id == tenant.id,
        extract("month", BillingCycle.created_at) == now.month,
        extract("year", BillingCycle.created_at) == now.year
    ).first()

    if existing:
        return {
            "message": "Billing already generated for this month",
            "billing_id": existing.id,
            "amount": existing.total_amount
        }

    # =========================
    # 💰 CALCULATE BILL (FIXED)
    # =========================
    result = calculate_bill(
        db,
        tenant.id,
        tenant.slab_limit,
        tenant.plan
    )

    # =========================
    # 🧾 CREATE BILLING CYCLE
    # =========================
    bill = BillingCycle(
        id=str(uuid.uuid4()),
        tenant_id=tenant.id,
        slab=result["slab"],
        plan=result["plan"],
        peak_students=result["peak_students"],
        extra_students=result["extra_students"],
        base_amount=result["base_amount"],
        extra_amount=result["extra_amount"],
        total_amount=result["total_amount"],
    )

    db.add(bill)

    # =========================
    # 🧾 CREATE INVOICE (FULL SNAPSHOT)
    # =========================
    invoice = Invoice(
        id=str(uuid.uuid4()),
        tenant_id=tenant.id,
        amount=result["total_amount"],

        slab=result["slab"],
        peak_students=result["peak_students"],
        extra_students=result["extra_students"],
        base_amount=result["base_amount"],
        extra_amount=result["extra_amount"],

        status="pending",
        due_date=datetime.utcnow() + timedelta(days=7)
    )

    db.add(invoice)
    db.flush()  # get invoice.id

    # =========================
    # 💳 CREATE RAZORPAY ORDER
    # =========================
    try:
        order = create_razorpay_order(
            amount=invoice.amount,
            receipt=invoice.id
        )

        invoice.razorpay_order_id = order["id"]

    except Exception:
        invoice.status = "failed"
        invoice.payment_method = "razorpay_error"

    # =========================
    # 💾 COMMIT
    # =========================
    db.commit()

    return {
        "message": "Billing + Invoice generated successfully",
        "billing": result,
        "invoice": {
            "invoice_id": invoice.id,
            "amount": invoice.amount,
            "status": invoice.status,
            "razorpay_order_id": invoice.razorpay_order_id
        }
    }