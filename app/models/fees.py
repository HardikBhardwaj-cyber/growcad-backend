import uuid
from sqlalchemy import Column, String, Integer
from app.db.base import Base


class Fees(Base):
    __tablename__ = "fees"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    student_id = Column(String, nullable=False)
    total_amount = Column(Integer, nullable=False)
    paid_amount = Column(Integer, default=0)