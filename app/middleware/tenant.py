from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from app.db.session import SessionLocal
from app.models.tenant import Tenant


class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        host = request.headers.get("host", "")
        request.state.tenant = None

        # =========================
        # 🔥 EXTRACT SUBDOMAIN
        # =========================
        subdomain = host.split(".")[0] if host else None

        # =========================
        # 🔥 SKIP SYSTEM DOMAINS
        # =========================
        if subdomain in ["api", "www", "localhost", "127", None]:
            return await call_next(request)

        # =========================
        # 🔥 DB SAFE BLOCK
        # =========================
        try:
            db = SessionLocal()

            tenant = db.query(Tenant).filter(
                Tenant.subdomain == subdomain
            ).first()

            if tenant:
                request.state.tenant = tenant

            db.close()

        except Exception as e:
            # ❌ Never crash middleware
            print(f"[Tenant Middleware Error] {str(e)}")

        # =========================
        # 🔥 CONTINUE REQUEST
        # =========================
        response = await call_next(request)
        return response