from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.scheduler import run_auto_billing
from app.services.reminder_service import send_payment_reminders

router = APIRouter(prefix="/cron", tags=["Cron"])


@router.post("/run-billing")
def run_billing(db: Session = Depends(get_db)):
    result = run_auto_billing(db)
    return {"billing_done": result}


@router.post("/send-reminders")
def reminders(db: Session = Depends(get_db)):
    result = send_payment_reminders(db)
    return result