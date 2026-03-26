import uuid
from sqlalchemy import Column, String, Integer
from app.db.base import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    student_id = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)

    method = Column(String)  # cash / razorpay
    status = Column(String)  # pending / approved