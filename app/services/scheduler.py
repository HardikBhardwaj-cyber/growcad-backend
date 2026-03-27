from sqlalchemy.orm import Session
from sqlalchemy import extract
import uuid
from datetime import datetime, timedelta

from app.crud.tenant import get_all_tenants
from app.services.billing_service import calculate_bill
from app.models.billing_cycle import BillingCycle
from app.models.invoice import Invoice
from app.services.payment_service import create_razorpay_order


def run_auto_billing(db: Session):

    tenants = get_all_tenants(db)
    results = []

    now = datetime.utcnow()

    for tenant in tenants:

        print(f"[Billing] Processing tenant: {tenant.name}")

        if not tenant.slab_limit or not tenant.plan:
            continue

        # 🔥 SAFE DUPLICATE CHECK (FIXED)
        existing_invoice = db.query(Invoice).filter(
            Invoice.tenant_id == tenant.id,
            extract("day", Invoice.created_at) == now.day,
            extract("month", Invoice.created_at) == now.month,
            extract("year", Invoice.created_at) == now.year
        ).first()

        if existing_invoice:
            continue

        # 🔥 BILLING
        result = calculate_bill(
            db,
            tenant.id,
            tenant.slab_limit,
            tenant.plan
        )

        # 🔥 BILLING CYCLE
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

        # 🔥 INVOICE
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
        db.flush()

        # 🔥 PAYMENT ORDER
        try:
            order = create_razorpay_order(
                amount=invoice.amount,
                receipt=invoice.id
            )

            invoice.razorpay_order_id = order["id"]

        except Exception as e:
            print(f"[Payment Error] Tenant {tenant.name}: {str(e)}")
            invoice.status = "failed"
            invoice.payment_method = "razorpay_error"

        results.append({
            "tenant": tenant.name,
            "amount": result["total_amount"]
        })

    db.commit()

    return results