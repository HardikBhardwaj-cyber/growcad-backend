from fastapi import FastAPI

# middleware
from app.middleware.tenant import TenantMiddleware

# core routers
from app.api.auth import router as auth_router
from app.api.test_secure import router as test_router

# core modules
from app.api.student import router as student_router
from app.api.batch import router as batch_router
from app.api.attendance import router as attendance_router

# panels
from app.api.admin import router as admin_router
from app.api.faculty import router as faculty_router
from app.api.student_panel import router as student_panel_router
from app.api.parent import router as parent_router
from app.api.super_admin import router as super_admin_router

# billing & usage
from app.api.billing import router as billing_router
from app.api.usage import router as usage_router

# payments & cron
from app.api.payment import router as payment_router
from app.api.cron import router as cron_router

# dashboard
from app.api.dashboard import router as dashboard_router

# reminders (✅ FIXED IMPORT)
from app.api.reminder import router as reminder_router

# DB
from app.db.init_db import init_db


# 🔥 INIT DB
init_db()

app = FastAPI(title="Growcad API")

# 🔥 MIDDLEWARE
app.add_middleware(TenantMiddleware)


# =========================
# 🔐 AUTH
# =========================
app.include_router(auth_router)

# =========================
# 🧪 TEST
# =========================
app.include_router(test_router)

# =========================
# 📦 CORE
# =========================
app.include_router(student_router)
app.include_router(batch_router)
app.include_router(attendance_router)

# =========================
# 🏢 PANELS
# =========================
app.include_router(admin_router)
app.include_router(faculty_router)
app.include_router(student_panel_router)
app.include_router(parent_router)
app.include_router(super_admin_router)

# =========================
# 💰 BILLING
# =========================
app.include_router(billing_router)
app.include_router(usage_router)

# =========================
# 💳 PAYMENTS
# =========================
app.include_router(payment_router)
app.include_router(cron_router)

# =========================
# 📊 DASHBOARD
# =========================
app.include_router(dashboard_router)

# =========================
# 🔔 REMINDERS
# =========================
app.include_router(reminder_router)


# =========================
# ❤️ HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}


# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {
        "message": "Growcad API running",
        "modules": [
            "auth",
            "students",
            "batches",
            "attendance",
            "billing",
            "payments",
            "reminders",
            "dashboard"
        ]
    }