from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_tenant, require_role

from app.services.analytics_service import (
    get_dashboard_data,
    get_monthly_revenue,
    get_student_growth,
    get_pending_trend,
    get_insights
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


# =========================
# 📊 BASIC DASHBOARD
# =========================
@router.get("/admin")
def admin_dashboard(
    db: Session = Depends(get_db),
    tenant=Depends(get_current_tenant),
    user=Depends(require_role(["institute_admin"]))
):
    data = get_dashboard_data(db, tenant.id)

    return {
        "message": "Dashboard data",
        "data": data
    }


# =========================
# 🚀 PREMIUM DASHBOARD
# =========================
@router.get("/admin/premium")
def premium_dashboard(
    db: Session = Depends(get_db),
    tenant=Depends(get_current_tenant),
    user=Depends(require_role(["institute_admin"]))
):
    return {
        "message": "Premium dashboard",
        "data": {
            "revenue_trend": get_monthly_revenue(db, tenant.id),
            "student_growth": get_student_growth(db, tenant.id),
            "pending_trend": get_pending_trend(db, tenant.id),
            "insights": get_insights(db, tenant.id)
        }
    }