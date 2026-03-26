from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_tenant, require_role
from app.constants.roles import INSTITUTE_ADMIN
from app.crud.student import create_student, get_students

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/")
def add_student(
    data: dict,
    db: Session = Depends(get_db),
    tenant=Depends(get_current_tenant),
    user=Depends(require_role(INSTITUTE_ADMIN))
):
    return create_student(db, data, tenant.id)


@router.get("/")
def list_students(
    db: Session = Depends(get_db),
    tenant=Depends(get_current_tenant),
    user=Depends(require_role(INSTITUTE_ADMIN))
):
    return get_students(db, tenant.id)