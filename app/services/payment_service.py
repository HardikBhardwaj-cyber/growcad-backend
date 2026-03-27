import razorpay
import os
import hmac
import hashlib
import json
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.invoice import Invoice


client = razorpay.Client(
    auth=(os.getenv("RAZORPAY_KEY"), os.getenv("RAZORPAY_SECRET"))
)


# =========================
# 🧾 CREATE ORDER
# =========================
def create_razorpay_order(amount: int, receipt: str):

    order = client.order.create({
        "amount": amount * 100,  # rupees → paisa
        "currency": "INR",
        "receipt": receipt
    })

    return order


# =========================
# 🔐 VERIFY WEBHOOK SIGNATURE
# =========================
def verify_signature(body: bytes, signature: str):

    secret = os.getenv("RAZORPAY_WEBHOOK_SECRET")

    generated = hmac.new(
        bytes(secret, "utf-8"),
        body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(generated, signature):
        raise HTTPException(status_code=400, detail="Invalid signature")


# =========================
# 💳 HANDLE WEBHOOK
# =========================
def handle_payment_webhook(db: Session, body: bytes, signature: str):

    # 🔥 Step 1: verify signature
    verify_signature(body, signature)

    payload = json.loads(body)

    event = payload.get("event")

    # We only care about successful payments
    if event != "payment.captured":
        return {"status": "ignored"}

    payment = payload["payload"]["payment"]["entity"]

    razorpay_payment_id = payment["id"]
    razorpay_order_id = payment["order_id"]
    amount = payment["amount"] // 100  # paisa → rupees

    # 🔥 Step 2: find invoice
    invoice = db.query(Invoice).filter(
        Invoice.razorpay_order_id == razorpay_order_id
    ).first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    # 🔥 Step 3: idempotency (avoid double processing)
    if invoice.status == "paid":
        return {"status": "already_processed"}

    # 🔥 Step 4: amount validation
    if invoice.amount != amount:
        raise HTTPException(status_code=400, detail="Amount mismatch")

    # 🔥 Step 5: mark paid
    invoice.status = "paid"
    invoice.payment_method = "razorpay"
    invoice.razorpay_payment_id = razorpay_payment_id
    invoice.razorpay_signature = signature
    invoice.paid_at = datetime.utcnow()

    db.commit()

    return {"status": "success"}