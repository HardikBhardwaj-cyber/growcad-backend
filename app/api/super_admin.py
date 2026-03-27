from fastapi import APIRouter, Depends
from app.api.deps import require_role

router = APIRouter(prefix="/super-admin", tags=["Super Admin"])


@router.get("/dashboard")
def super_admin_dashboard(user=Depends(require_role(["super_admin"]))):
    return {
        "panel": "Super Admin",
        "features": [
            "all institutes",
            "billing",
            "usage",
            "feature flags"
        ]
    }