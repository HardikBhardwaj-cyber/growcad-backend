from sqlalchemy.orm import Session
from app.models.tenant import Tenant


def get_tenant_by_subdomain(db: Session, subdomain: str):
    return db.query(Tenant).filter(Tenant.subdomain == subdomain).first()