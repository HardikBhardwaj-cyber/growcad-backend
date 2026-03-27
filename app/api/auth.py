from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

# deps
from app.api.deps import get_db, get_current_tenant

# services
from app.services.otp_service import generate_otp, verify_otp, can_request_otp
from app.services.auth_service import (
    login_or_create_user,
    assign_default_role
)

# crud
from app.crud.user import create_user, get_user_by_identifier

# utils
from app.utils.jwt import decode_token, create_access_token

# schemas
from app.schemas.auth import (
    SendOTPRequest,
    VerifyOTPRequest,
    RefreshTokenRequest,
    RegisterInstitute
)

# models
from app.models.tenant import Tenant

# constants
from app.constants.slabs import SLABS

router = APIRouter(prefix="/auth", tags=["Auth"])


# =========================
# 📲 SEND OTP
# =========================
@router.post("/send-otp")
def send_otp(payload: SendOTPRequest):
    phone = payload.phone

    if not can_request_otp(phone):
        raise HTTPException(status_code=429, detail="Too many requests")

    generate_otp(phone)

    return {"message": "OTP sent"}


# =========================
# 🔐 VERIFY OTP (LOGIN)
# =========================
@router.post("/verify-otp")
def verify(
    payload: VerifyOTPRequest,
    db: Session = Depends(get_db),
    tenant=Depends(get_current_tenant)
):
    phone = payload.phone
    otp = payload.otp

    if not verify_otp(phone, otp):
        raise HTTPException(status_code=400, detail="Invalid OTP")

    tokens = login_or_create_user(db, phone, tenant)

    return tokens


# =========================
# 🔁 REFRESH TOKEN
# =========================
@router.post("/refresh")
def refresh_token(payload: RefreshTokenRequest):
    token = payload.token

    payload_data = decode_token(token)

    new_access = create_access_token({
        "user_id": payload_data["user_id"],
        "tenant_id": payload_data["tenant_id"],
        "role": payload_data.get("role")  # preserve role
    })

    return {"access_token": new_access}


# =========================
# 🏢 REGISTER INSTITUTE (FINAL)
# =========================
@router.post("/register-institute")
def register_institute(
    payload: RegisterInstitute,
    db: Session = Depends(get_db)
):
    # 🔍 validate slab
    if payload.slab not in SLABS:
        raise HTTPException(status_code=400, detail="Invalid slab")

    # 🔍 check subdomain
    existing = db.query(Tenant).filter(
        Tenant.subdomain == payload.subdomain
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Subdomain already taken")

    # 🔍 check if user already exists
    existing_user = get_user_by_identifier(db, payload.phone)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # 🔥 CREATE TENANT
    tenant = Tenant(
        id=str(uuid.uuid4()),
        name=payload.name,
        subdomain=payload.subdomain,
        slab_name=payload.slab,
        slab_limit=SLABS[payload.slab],
        plan=payload.plan
    )

    db.add(tenant)
    db.commit()

    # 🔥 CREATE OWNER USER (ADMIN)
    user = create_user(db, payload.phone, tenant.id)

    # 🔥 ASSIGN ADMIN ROLE
    assign_default_role(db, user)

    return {
        "message": "Institute + Admin created successfully",
        "tenant_id": tenant.id,
        "admin_phone": payload.phone,
        "subdomain": tenant.subdomain,
        "slab": tenant.slab_name,
        "plan": tenant.plan
    }