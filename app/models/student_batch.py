import uuid
from sqlalchemy import Column, String
from app.db.base import Base


class StudentBatch(Base):
    __tablename__ = "student_batches"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String, nullable=False)
    batch_id = Column(String, nullable=False)