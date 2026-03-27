import uuid
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class BillingCycle(Base):
    __tablename__ = "billing_cycles"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # 🔥 MULTI-TENANT (INDEXED FOR PERFORMANCE)
    tenant_id = Column(String, index=True)

    # 📊 BILL CONFIG
    slab = Column(Integer)            # e.g. 250
    plan = Column(String)             # basic / academic / advanced

    # 👥 USAGE
    peak_students = Column(Integer)
    extra_students = Column(Integer)

    # 💰 BILLING
    base_amount = Column(Integer)
    extra_amount = Column(Integer)
    total_amount = Column(Integer)

    # 🔄 STATUS
    status = Column(String, default="pending")  # pending / paid

    # 📅 TIMESTAMP (USED FOR MONTHLY BILLING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())