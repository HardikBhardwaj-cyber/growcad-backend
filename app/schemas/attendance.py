from pydantic import BaseModel
from typing import List


class AttendanceRequest(BaseModel):
    batch_id: str
    absent_student_ids: List[str]