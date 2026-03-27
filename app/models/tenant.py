import uuid
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.sql import func
from app.db.base import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # basic info
    name = Column(String, nullable=False)
    subdomain = Column(String, unique=True, nullable=False)

    # 🔥 BILLING CONFIG (CRITICAL)
    slab_name = Column(String)       # "151-250"
    slab_limit = Column(Integer)     # 250

    plan = Column(String)            # basic / academic / advanced

    # 🔥 USAGE TRACKING (optional future)
    max_students_seen = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())