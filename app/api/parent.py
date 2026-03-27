from fastapi import APIRouter, Depends
from app.api.deps import require_role

router = APIRouter(prefix="/parent", tags=["Parent"])


@router.get("/dashboard")
def parent_dashboard(user=Depends(require_role(["parent"]))):
    return {
        "panel": "Parent",
        "features": [
            "child performance",
            "fees",
            "attendance"
        ]
    }