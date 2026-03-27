from pydantic import BaseModel


# 🔐 OTP
class SendOTPRequest(BaseModel):
    phone: str


class VerifyOTPRequest(BaseModel):
    phone: str
    otp: str


# 🔁 Refresh
class RefreshTokenRequest(BaseModel):
    token: str


# 🏢 Register Institute
class RegisterInstitute(BaseModel):
    name: str
    subdomain: str
    slab: str
    plan: str
    phone: str