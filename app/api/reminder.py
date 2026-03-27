from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.reminder_service import send_payment_reminders

router = APIRouter(prefix="/reminders", tags=["Reminders"])


@router.post("/run")
def run_reminders(db: Session = Depends(get_db)):
    return send_payment_reminders(db)