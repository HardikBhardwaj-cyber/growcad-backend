from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_tenant, require_role
from app.constants.roles import INSTITUTE_ADMIN
from app.crud.batch import create_batch

router = APIRouter(prefix="/batches", tags=["Batches"])


@router.post("/")
def add_batch(
    name: str,
    db: Session = Depends(get_db),
    tenant=Depends(get_current_tenant),
    user=Depends(require_role(INSTITUTE_ADMIN))
):
    return create_batch(db, name, tenant.id)