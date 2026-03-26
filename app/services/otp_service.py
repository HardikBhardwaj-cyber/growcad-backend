import random
from datetime import datetime, timedelta

otp_store = {}
otp_requests = {}


def can_request_otp(identifier: str):
    now = datetime.utcnow()

    if identifier in otp_requests:
        if now - otp_requests[identifier] < timedelta(seconds=30):
            return False

    otp_requests[identifier] = now
    return True


def generate_otp(identifier: str):
    otp = str(random.randint(100000, 999999))
    expiry = datetime.utcnow() + timedelta(minutes=5)

    otp_store[identifier] = {
        "otp": otp,
        "expiry": expiry
    }

    return otp


def verify_otp(identifier: str, otp: str):
    record = otp_store.get(identifier)

    if not record:
        return False

    if record["otp"] != otp:
        return False

    if datetime.utcnow() > record["expiry"]:
        return False

    return True