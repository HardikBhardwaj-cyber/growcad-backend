from fastapi import APIRouter, Depends
from app.api.deps import require_role

router = APIRouter(prefix="/faculty", tags=["Faculty"])


@router.get("/dashboard")
def faculty_dashboard(user=Depends(require_role(["faculty"]))):
    return {
        "panel": "Faculty",
        "features": [
            "attendance",
            "tests",
            "materials"
        ]
    }