from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_tenant
from app.services.otp_service import generate_otp, verify_otp, can_request_otp
from app.services.auth_service import login_or_create_user
from app.utils.jwt import decode_token, create_access_token

from app.schemas.auth import SendOTPRequest, VerifyOTPRequest, RefreshTokenRequest

router = APIRouter(prefix="/auth", tags=["Auth"])


# ✅ SEND OTP (BODY BASED)
@router.post("/send-otp")
def send_otp(
    payload: SendOTPRequest,
):
    phone = payload.phone

    if not can_request_otp(phone):
        raise HTTPException(status_code=429, detail="Too many requests")

    generate_otp(phone)

    return {"message": "OTP sent"}


# ✅ VERIFY OTP (BODY BASED)
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


# ✅ REFRESH TOKEN (BODY BASED)
@router.post("/refresh")
def refresh_token(payload: RefreshTokenRequest):
    token = payload.token

    payload_data = decode_token(token)

    new_access = create_access_token({
        "user_id": payload_data["user_id"],
        "tenant_id": payload_data["tenant_id"]
    })

    return {"access_token": new_access}