from app.db.base import Base
from app.db.session import engine

# 🔥 IMPORT ALL MODELS HERE (SAFE PLACE)
from app.models.tenant import Tenant
from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole
from app.models.student import Student
from app.models.batch import Batch
from app.models.student_batch import StudentBatch
from app.models.attendance import Attendance
from app.models.fees import Fees
from app.models.payment import Payment


def init_db():
    Base.metadata.create_all(bind=engine)