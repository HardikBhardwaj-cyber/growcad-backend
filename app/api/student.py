from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_tenant, require_role
from app.constants.roles import INSTITUTE_ADMIN

# 🔥 USE SERVICE (NOT CRUD)
from app.services.student_service import (
    create_student,
    list_students
)

router = APIRouter(prefix="/students", tags=["Students"])


# =========================
# ➕ ADD STUDENT
# =========================
@router.post("/")
def add_student(
    data: dict,
    db: Session = Depends(get_db),
    tenant=Depends(get_current_tenant),
    user=Depends(require_role([INSTITUTE_ADMIN]))
):
    student = create_student(
        db=db,
        tenant_id=tenant.id,
        name=data.get("name"),
        phone=data.get("phone")
    )

    return student


# =========================
# 📋 LIST STUDENTS
# =========================
@router.get("/")
def list_students_api(
    db: Session = Depends(get_db),
    tenant=Depends(get_current_tenant),
    user=Depends(require_role([INSTITUTE_ADMIN]))
):
    return list_students(db, tenant.id)