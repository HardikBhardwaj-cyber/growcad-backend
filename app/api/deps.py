from fastapi import Depends, Request, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.db.session import SessionLocal
from app.models.user import User
from app.models.user_role import UserRole
from app.models.role import Role
from app.utils.jwt import decode_token

security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_tenant(request: Request):
    if not request.state.tenant:
        raise HTTPException(status_code=400, detail="Invalid tenant")
    return request.state.tenant


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
    tenant=Depends(get_current_tenant)
):
    token = credentials.credentials
    payload = decode_token(token)

    user = db.query(User).filter(User.id == payload["user_id"]).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.tenant_id != tenant.id:
        raise HTTPException(status_code=403, detail="Tenant mismatch")

    print("USER ROLE:", user.role)
    return user


def require_role(required_role: str):
    def role_checker(
        user=Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        role = (
            db.query(Role.name)
            .join(UserRole, Role.id == UserRole.role_id)
            .filter(UserRole.user_id == user.id)
            .first()
        )

        if not role or role[0] != required_role:
            raise HTTPException(status_code=403, detail="Access denied")

        return user

    return role_checker