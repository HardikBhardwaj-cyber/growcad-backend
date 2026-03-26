from sqlalchemy.orm import declarative_base

Base = declarative_base()

# 🔥 IMPORT ALL MODELS HERE (MANDATORY)
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