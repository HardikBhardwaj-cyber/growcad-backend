from sqlalchemy.orm import Session

from app.crud.user import get_user_by_identifier, create_user
from app.models.user_role import UserRole
from app.models.role import Role
from app.constants.roles import INSTITUTE_ADMIN
from app.utils.jwt import create_access_token, create_refresh_token


def assign_default_role(db: Session, user):
    role = db.query(Role).filter(Role.name == INSTITUTE_ADMIN).first()

    user_role = UserRole(
        user_id=user.id,
        role_id=role.id
    )

    db.add(user_role)
    db.commit()


def login_or_create_user(db: Session, identifier: str, tenant):
    user = get_user_by_identifier(db, identifier)

    if not user:
        user = create_user(db, identifier, tenant.id)
        assign_default_role(db, user)

    token_data = {
        "user_id": user.id,
        "tenant_id": tenant.id
    }

    return {
        "access_token": create_access_token(token_data),
        "refresh_token": create_refresh_token(token_data)
    }