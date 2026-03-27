from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_tenant
from app.services.usage_service import log_daily_usage

router = APIRouter(prefix="/usage", tags=["Usage"])


@router.post("/log")
def log_usage(
    db: Session = Depends(get_db),
    tenant=Depends(get_current_tenant)
):
    log_daily_usage(db, tenant.id)
    return {"message": "Usage logged"}