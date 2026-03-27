from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.student import Student
from app.models.invoice import Invoice
from app.models.attendance import Attendance


# =========================
# 📊 BASIC DASHBOARD
# =========================
def get_dashboard_data(db: Session, tenant_id: str):

    # 👨‍🎓 Students
    total_students = db.query(Student).filter(
        Student.tenant_id == tenant_id
    ).count()

    # 💰 Revenue (paid)
    total_revenue_data = db.query(Invoice.amount).filter(
        Invoice.tenant_id == tenant_id,
        Invoice.status == "paid"
    ).all()

    total_revenue = sum([r[0] for r in total_revenue_data]) if total_revenue_data else 0

    # ⏳ Pending
    pending_data = db.query(Invoice.amount).filter(
        Invoice.tenant_id == tenant_id,
        Invoice.status == "pending"
    ).all()

    pending_amount = sum([p[0] for p in pending_data]) if pending_data else 0

    # 📊 Attendance
    total_attendance = db.query(Attendance).filter(
        Attendance.tenant_id == tenant_id
    ).count()

    present_attendance = db.query(Attendance).filter(
        Attendance.tenant_id == tenant_id,
        Attendance.status == "present"
    ).count()

    attendance_percentage = (
        (present_attendance / total_attendance) * 100
        if total_attendance > 0 else 0
    )

    return {
        "total_students": total_students,
        "total_revenue": total_revenue,
        "pending_amount": pending_amount,
        "attendance_percentage": round(attendance_percentage, 2)
    }


# =========================
# 📈 MONTHLY REVENUE
# =========================
def get_monthly_revenue(db: Session, tenant_id: str):
    data = db.query(
        func.date_trunc('month', Invoice.created_at).label("month"),
        func.sum(Invoice.amount)
    ).filter(
        Invoice.tenant_id == tenant_id,
        Invoice.status == "paid"
    ).group_by("month").order_by("month").all()

    return [
        {
            "month": str(d[0])[:7],
            "revenue": int(d[1] or 0)
        }
        for d in data
    ]


# =========================
# 👨‍🎓 STUDENT GROWTH
# =========================
def get_student_growth(db: Session, tenant_id: str):
    data = db.query(
        func.date_trunc('month', Student.created_at).label("month"),
        func.count(Student.id)
    ).filter(
        Student.tenant_id == tenant_id
    ).group_by("month").order_by("month").all()

    return [
        {
            "month": str(d[0])[:7],
            "students": d[1]
        }
        for d in data
    ]


# =========================
# ⚠️ PENDING TREND
# =========================
def get_pending_trend(db: Session, tenant_id: str):
    data = db.query(
        func.date_trunc('month', Invoice.created_at).label("month"),
        func.sum(Invoice.amount)
    ).filter(
        Invoice.tenant_id == tenant_id,
        Invoice.status == "pending"
    ).group_by("month").order_by("month").all()

    return [
        {
            "month": str(d[0])[:7],
            "pending": int(d[1] or 0)
        }
        for d in data
    ]


# =========================
# 🧠 SMART INSIGHTS
# =========================
def get_insights(db: Session, tenant_id: str):

    revenue = get_monthly_revenue(db, tenant_id)
    students = get_student_growth(db, tenant_id)

    insights = []

    # Revenue trend
    if len(revenue) >= 2:
        if revenue[-1]["revenue"] > revenue[-2]["revenue"]:
            insights.append("📈 Revenue is growing this month")
        else:
            insights.append("⚠️ Revenue dropped this month")

    # Student trend
    if len(students) >= 2:
        if students[-1]["students"] > students[-2]["students"]:
            insights.append("🎓 Student base is increasing")
        else:
            insights.append("⚠️ Student growth slowing down")

    if not insights:
        insights.append("🚀 Keep growing your institute!")

    return insights