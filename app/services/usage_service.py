from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.usage_log import UsageLog
from app.models.student import Student


def log_daily_usage(db: Session, tenant_id: str):
    """
    Logs usage ONCE per day per tenant.
    Prevents duplicates.
    """

    today = date.today()

    # ✅ Prevent duplicate log for same day
    existing = db.query(UsageLog).filter(
        UsageLog.tenant_id == tenant_id,
        UsageLog.date == today
    ).first()

    if existing:
        return existing

    # ✅ Count ONLY active students
    active_count = db.query(func.count(Student.id)).filter(
        Student.tenant_id == tenant_id,
        Student.is_active.is_(True)
    ).scalar() or 0

    usage = UsageLog(
        tenant_id=tenant_id,
        date=today,
        active_student_count=active_count
    )

    db.add(usage)
    db.commit()
    db.refresh(usage)

    return usage


def get_peak_usage_last_30_days(db: Session, tenant_id: str):
    """
    🔥 CORE BILLING FUNCTION
    Returns peak active students in last 30 days
    """

    today = date.today()
    last_30_days = today - timedelta(days=30)

    peak = db.query(func.max(UsageLog.active_student_count)).filter(
        UsageLog.tenant_id == tenant_id,
        UsageLog.date >= last_30_days
    ).scalar()

    return peak or 0