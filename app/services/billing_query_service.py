from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.invoice import Invoice
from app.services.usage_service import get_peak_usage_last_30_days


# =========================
# 📊 CURRENT BILLING
# =========================
def get_current_billing(db: Session, tenant_id: str):

    invoice = db.query(Invoice).filter(
        Invoice.tenant_id == tenant_id
    ).order_by(desc(Invoice.created_at)).first()

    if not invoice:
        return None

    return {
        "invoice_id": invoice.id,
        "amount": invoice.amount,
        "status": invoice.status,
        "due_date": invoice.due_date,
        "created_at": invoice.created_at,

        # breakdown
        "slab": invoice.slab,
        "peak_students": invoice.peak_students,
        "extra_students": invoice.extra_students,
        "base_amount": invoice.base_amount,
        "extra_amount": invoice.extra_amount,
    }


# =========================
# 📜 BILLING HISTORY
# =========================
def get_billing_history(
    db: Session,
    tenant_id: str,
    skip: int = 0,
    limit: int = 20
):

    invoices = db.query(Invoice).filter(
        Invoice.tenant_id == tenant_id
    ).order_by(desc(Invoice.created_at)).offset(skip).limit(limit).all()

    return [
        {
            "invoice_id": i.id,
            "amount": i.amount,
            "status": i.status,
            "created_at": i.created_at,
            "due_date": i.due_date,
        }
        for i in invoices
    ]


# =========================
# 📄 INVOICE DETAILS
# =========================
def get_invoice_detail(db: Session, tenant_id: str, invoice_id: str):

    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id,
        Invoice.tenant_id == tenant_id
    ).first()

    if not invoice:
        return None

    return {
        "invoice_id": invoice.id,
        "amount": invoice.amount,
        "status": invoice.status,
        "payment_method": invoice.payment_method,
        "created_at": invoice.created_at,
        "due_date": invoice.due_date,
        "paid_at": invoice.paid_at,

        # breakdown
        "slab": invoice.slab,
        "peak_students": invoice.peak_students,
        "extra_students": invoice.extra_students,
        "base_amount": invoice.base_amount,
        "extra_amount": invoice.extra_amount,
    }


# =========================
# 📈 CURRENT USAGE (TRUST)
# =========================
def get_current_usage(db: Session, tenant_id: str):

    peak = get_peak_usage_last_30_days(db, tenant_id)

    return {
        "peak_students_last_30_days": peak
    }