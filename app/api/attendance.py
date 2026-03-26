from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.api.deps import get_db, get_current_tenant, require_role
from app.constants.roles import INSTITUTE_ADMIN
from app.models.attendance import Attendance
from app.models.student_batch import StudentBatch
from app.schemas.attendance import AttendanceRequest

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("/mark")
def mark_attendance(
    payload: AttendanceRequest,
    db: Session = Depends(get_db),
    tenant=Depends(get_current_tenant),
    user=Depends(require_role(INSTITUTE_ADMIN))
):
    today = date.today()

    students = db.query(StudentBatch).filter(
        StudentBatch.batch_id == payload.batch_id
    ).all()

    records = []

    for s in students:
        present = s.student_id not in payload.absent_student_ids

        record = Attendance(
            student_id=s.student_id,
            batch_id=payload.batch_id,
            date=today,
            present=present
        )

        records.append(record)

    db.bulk_save_objects(records)
    db.commit()

    return {
        "message": "Attendance marked successfully",
        "total_students": len(students),
        "absent": len(payload.absent_student_ids)
    }