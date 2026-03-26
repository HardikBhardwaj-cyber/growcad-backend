from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from app.db.session import SessionLocal
from app.models.tenant import Tenant


class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        host = request.headers.get("host")

        request.state.tenant = None

        if host:
            subdomain = host.split(".")[0]

            db = SessionLocal()
            tenant = db.query(Tenant).filter(Tenant.subdomain == subdomain).first()
            db.close()

            if tenant:
                request.state.tenant = tenant

        response = await call_next(request)
        return response