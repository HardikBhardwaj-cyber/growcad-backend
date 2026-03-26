import uuid
from sqlalchemy import Column, String
from app.db.base import Base


class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    role_id = Column(String, nullable=False)