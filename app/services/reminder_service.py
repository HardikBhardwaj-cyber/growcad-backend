from sqlalchemy.orm import Session
from datetime import datetime

from app.models.invoice import Invoice
from app.models.tenant import Tenant
from app.services.communication_service import send_sms


def get_due_invoices(db: Session):

    now = datetime.utcnow()

    return db.query(Invoice).filter(
        Invoice.status == "pending",
        Invoice.due_date != None,
        Invoice.due_date <= now
    ).all()


def send_payment_reminders(db: Session):

    invoices = get_due_invoices(db)
    results = []

    for inv in invoices:

        tenant = db.query(Tenant).filter(
            Tenant.id == inv.tenant_id
        ).first()

        if not tenant or not tenant.phone:
            continue

        message = (
            f"Growcad Reminder:\n"
            f"Invoice ₹{inv.amount} is due.\n"
            f"Please pay to avoid service interruption."
        )

        send_sms(tenant.phone, message)

        results.append({
            "tenant": tenant.name,
            "amount": inv.amount
        })

    return {
        "total_reminders_sent": len(results),
        "details": results
    }