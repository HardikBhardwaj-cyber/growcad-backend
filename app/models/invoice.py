import uuid
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    tenant_id = Column(String, index=True)

    # 💰 FINAL AMOUNT
    amount = Column(Integer, nullable=False)

    # 🔥 BILLING SNAPSHOT
    slab = Column(Integer)
    peak_students = Column(Integer)
    extra_students = Column(Integer)
    base_amount = Column(Integer)
    extra_amount = Column(Integer)

    # 🔥 STATUS
    status = Column(String, default="pending")  # pending / paid / failed

    # 💳 PAYMENT
    payment_method = Column(String, nullable=True)

    razorpay_order_id = Column(String, nullable=True, index=True)
    razorpay_payment_id = Column(String, nullable=True)
    razorpay_signature = Column(String, nullable=True)  # ✅ NEW

    # 📅 TIME
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    due_date = Column(DateTime, nullable=True)
    paid_at = Column(DateTime, nullable=True)