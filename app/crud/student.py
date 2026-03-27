from sqlalchemy.orm import Session
from app.models.student import Student


def create_student(db: Session, data: dict, tenant_id: str):
    """
    ⚠️ INTERNAL USE ONLY (should be used inside service)
    """
    student = Student(
        tenant_id=tenant_id,
        name=data.get("name"),
        phone=data.get("phone"),
        is_active=True  # 🔥 enforce active
    )

    db.add(student)
    db.flush()  # 🔥 no commit here

    return student


def get_students(db: Session, tenant_id: str, skip: int = 0, limit: int = 50):
    return db.query(Student).filter(
        Student.tenant_id == tenant_id
    ).offset(skip).limit(limit).all()