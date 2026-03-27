from fastapi import APIRouter, Depends
from app.api.deps import require_role

router = APIRouter(prefix="/student", tags=["Student Panel"])


# =========================
# 🎓 STUDENT DASHBOARD
# =========================
@router.get("/dashboard")
def student_dashboard(user=Depends(require_role(["student"]))):
    return {
        "panel": "Student",
        "features": [
            "attendance",
            "courses",
            "tests",
            "performance",
            "notifications"
        ]
    }