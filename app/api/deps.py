from fastapi import Depends, Request, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.db.session import SessionLocal
from app.models.user import User
from app.utils.jwt import decode_token

security = HTTPBearer()


# DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Tenant
def get_current_tenant(request: Request):
    if not hasattr(request.state, "tenant") or not request.state.tenant:
        raise HTTPException(status_code=400, detail="Invalid tenant")
    return request.state.tenant


# 🔥 Current user
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

    # 🔥 attach role from JWT
    user.role = payload.get("role")

    return user


# 🔥 Role guard (FINAL)
def require_role(allowed_roles: list):
    def role_checker(user=Depends(get_current_user)):

        # super admin override
        if user.role == "super_admin":
            return user

        if user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Access denied")

        return user

    return role_checker