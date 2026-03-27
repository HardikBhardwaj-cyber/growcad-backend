import uuid
from sqlalchemy import Column, String, Integer, Date, Index
from app.db.base import Base


class UsageLog(Base):
    __tablename__ = "usage_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    tenant_id = Column(String, index=True)

    # 🔥 CHANGE: use DATE (not string)
    date = Column(Date, index=True)

    # 🔥 CHANGE: rename for clarity
    active_student_count = Column(Integer, nullable=False)


# 🔥 INDEX for fast peak queries
Index("idx_usage_tenant_date", UsageLog.tenant_id, UsageLog.date)