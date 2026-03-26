from fastapi import APIRouter, Depends
from app.api.deps import require_role
from app.constants.roles import INSTITUTE_ADMIN

router = APIRouter(prefix="/test", tags=["Test"])


@router.get("/secure")
def secure_data(user=Depends(require_role(INSTITUTE_ADMIN))):
    return {
        "message": "Authorized access",
        "user_id": user.id
    }