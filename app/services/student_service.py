from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.student import Student
from app.services.usage_service import log_daily_usage
from app.crud.student import create_student as crud_create_student


# =========================
# ➕ CREATE STUDENT
# =========================
def create_student(
    db: Session,
    tenant_id: str,
    name: str,
    phone: Optional[str] = None,
):
    student = crud_create_student(
        db,
        {"name": name, "phone": phone},
        tenant_id
    )

    db.commit()
    db.refresh(student)

    # 🔥 CRITICAL: update usage
    log_daily_usage(db, tenant_id)

    return student


# =========================
# 🔍 GET STUDENT
# =========================
def get_student(
    db: Session,
    tenant_id: str,
    student_id: str
):
    return db.query(Student).filter(
        Student.id == student_id,
        Student.tenant_id == tenant_id
    ).first()


# =========================
# 📋 LIST STUDENTS
# =========================
def list_students(
    db: Session,
    tenant_id: str,
    skip: int = 0,
    limit: int = 50,
    active_only: bool = False
):
    query = db.query(Student).filter(
        Student.tenant_id == tenant_id
    )

    if active_only:
        query = query.filter(Student.is_active.is_(True))

    return query.offset(skip).limit(limit).all()


# =========================
# ✏️ UPDATE STUDENT
# =========================
def update_student(
    db: Session,
    tenant_id: str,
    student_id: str,
    name: Optional[str] = None,
    phone: Optional[str] = None,
):
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.tenant_id == tenant_id
    ).first()

    if not student:
        return None

    if name is not None:
        student.name = name

    if phone is not None:
        student.phone = phone

    db.commit()
    db.refresh(student)

    return student


# =========================
# 🔁 ACTIVATE / DEACTIVATE
# =========================
def set_student_active_status(
    db: Session,
    tenant_id: str,
    student_id: str,
    is_active: bool
):
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.tenant_id == tenant_id
    ).first()

    if not student:
        return None

    # No change → skip
    if student.is_active == is_active:
        return student

    student.is_active = is_active

    db.commit()
    db.refresh(student)

    # 🔥 CRITICAL: anti-cheat usage tracking
    log_daily_usage(db, tenant_id)

    return student


# =========================
# 📦 BULK CREATE STUDENTS
# =========================
def bulk_create_students(
    db: Session,
    tenant_id: str,
    students: List[dict]
):
    created_students = []

    for data in students:
        student = crud_create_student(db, data, tenant_id)
        created_students.append(student)

    db.commit()

    # 🔥 CRITICAL: log usage once after bulk
    log_daily_usage(db, tenant_id)

    return created_students


# =========================
# ❌ SOFT DELETE
# =========================
def delete_student(
    db: Session,
    tenant_id: str,
    student_id: str
):
    """
    We DO NOT hard delete.
    We deactivate.
    """

    student = db.query(Student).filter(
        Student.id == student_id,
        Student.tenant_id == tenant_id
    ).first()

    if not student:
        return None

    if not student.is_active:
        return student

    student.is_active = False

    db.commit()
    db.refresh(student)

    # 🔥 CRITICAL: update usage
    log_daily_usage(db, tenant_id)

    return student