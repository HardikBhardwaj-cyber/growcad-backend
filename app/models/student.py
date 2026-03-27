import uuid
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.base import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # 🔥 MULTI-TENANT
    tenant_id = Column(String, nullable=False, index=True)

    # 👨‍🎓 BASIC INFO
    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)

    # 🔥 STATUS (VERY IMPORTANT FOR BILLING)
    is_active = Column(Boolean, default=True)

    # 🔥 TRACK WHEN ACTIVATED (ANTI-CHEAT FUTURE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())