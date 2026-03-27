from sqlalchemy.orm import Session

from app.crud.user import get_user_by_identifier, create_user
from app.models.user_role import UserRole
from app.models.role import Role
from app.constants.roles import INSTITUTE_ADMIN
from app.utils.jwt import create_access_token, create_refresh_token


# 🔥 Assign default role
def assign_default_role(db: Session, user):

    role = db.query(Role).filter(Role.name == INSTITUTE_ADMIN).first()

    if not role:
        raise Exception("Default role not found in DB")

    user_role = UserRole(
        user_id=user.id,
        role_id=role.id
    )

    db.add(user_role)
    db.commit()


# 🔥 Fetch user role
def get_user_role(db: Session, user_id: str):
    role = (
        db.query(Role.name)
        .join(UserRole, Role.id == UserRole.role_id)
        .filter(UserRole.user_id == user_id)
        .first()
    )

    if not role:
        raise Exception("User role not found")

    return role[0]


# 🔥 Main login flow
def login_or_create_user(db: Session, identifier: str, tenant):
    user = get_user_by_identifier(db, identifier)

    if not user:
        user = create_user(db, identifier, tenant.id)
        assign_default_role(db, user)

    # 🔥 get role
    role_name = get_user_role(db, user.id)

    token_data = {
        "user_id": user.id,
        "tenant_id": tenant.id,
        "role": role_name
    }

    return {
        "access_token": create_access_token(token_data),
        "refresh_token": create_refresh_token(token_data)
    }