from sqlalchemy.orm import Session
from app.models.student import Student


def create_student(db: Session, data, tenant_id):
    student = Student(**data, tenant_id=tenant_id)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def get_students(db: Session, tenant_id):
    return db.query(Student).filter(Student.tenant_id == tenant_id).all()