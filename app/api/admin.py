from fastapi import APIRouter, Depends
from app.api.deps import require_role

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard")
def admin_dashboard(user=Depends(require_role(["institute_admin"]))):
    return {
        "panel": "Admin",
        "features": [
            "students",
            "batches",
            "fees",
            "attendance",
            "reports"
        ]
    }