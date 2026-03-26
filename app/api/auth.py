from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_tenant
from app.services.otp_service import generate_otp, verify_otp, can_request_otp
from app.services.auth_service import login_or_create_user
from app.utils.jwt import decode_token, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/send-otp")
def send_otp(identifier: str):
    if not can_request_otp(identifier):
        raise HTTPException(status_code=429, detail="Too many requests")

    otp = generate_otp(identifier)

    return {"message": "OTP sent"}  # never expose OTP in prod


@router.post("/verify-otp")
def verify(
    identifier: str,
    otp: str,
    request: Request,
    db: Session = Depends(get_db),
    tenant=Depends(get_current_tenant)
):
    if not verify_otp(identifier, otp):
        raise HTTPException(status_code=400, detail="Invalid OTP")

    tokens = login_or_create_user(db, identifier, tenant)

    return tokens


@router.post("/refresh")
def refresh_token(token: str):
    payload = decode_token(token)

    new_access = create_access_token({
        "user_id": payload["user_id"],
        "tenant_id": payload["tenant_id"]
    })

    return {"access_token": new_access}