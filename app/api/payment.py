from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.payment_service import handle_payment_webhook

router = APIRouter(prefix="/payments", tags=["Payments"])


# =========================
# 🔔 RAZORPAY WEBHOOK
# =========================
@router.post("/webhook")
async def razorpay_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    body = await request.body()
    signature = request.headers.get("X-Razorpay-Signature")

    return handle_payment_webhook(db, body, signature)