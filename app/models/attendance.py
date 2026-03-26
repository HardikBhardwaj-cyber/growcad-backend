import uuid
from sqlalchemy import Column, String, Date, Boolean
from app.db.base import Base


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    student_id = Column(String, nullable=False)
    batch_id = Column(String, nullable=False)

    date = Column(Date, nullable=False)

    present = Column(Boolean, default=True)