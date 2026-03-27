import os


# =========================
# 📩 SEND SMS (MSG91 READY)
# =========================
def send_sms(phone: str, message: str):
    """
    Placeholder for SMS integration (MSG91 / Fast2SMS)
    """

    # 🔥 For now: simple log (replace later with API call)
    print(f"[SMS] To: {phone} | Message: {message}")

    return True


# =========================
# 📧 SEND EMAIL (FUTURE)
# =========================
def send_email(email: str, subject: str, body: str):

    print(f"[EMAIL] To: {email} | Subject: {subject}")

    return True


# =========================
# 💬 SEND WHATSAPP (FUTURE)
# =========================
def send_whatsapp(phone: str, message: str):

    print(f"[WHATSAPP] To: {phone} | Message: {message}")

    return True