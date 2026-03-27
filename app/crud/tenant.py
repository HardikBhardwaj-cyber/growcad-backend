from sqlalchemy.orm import Session
from app.models.tenant import Tenant


# 🔍 Get by subdomain (USED BY MIDDLEWARE)
def get_tenant_by_subdomain(db: Session, subdomain: str):
    return db.query(Tenant).filter(
        Tenant.subdomain == subdomain
    ).first()


# 🔥 Get by ID
def get_tenant_by_id(db: Session, tenant_id: str):
    return db.query(Tenant).filter(
        Tenant.id == tenant_id
    ).first()


# 🔥 Get all tenants (USED FOR AUTO BILLING)
def get_all_tenants(db: Session):
    return db.query(Tenant).all()


# 🔥 Update tenant plan (UPGRADE / DOWNGRADE)
def update_tenant_plan(db: Session, tenant_id: str, plan: str):
    tenant = get_tenant_by_id(db, tenant_id)

    if not tenant:
        return None

    tenant.plan = plan
    db.commit()
    db.refresh(tenant)

    return tenant


# 🔥 Update slab (important for scaling)
def update_tenant_slab(db: Session, tenant_id: str, slab_name: str, slab_limit: int):
    tenant = get_tenant_by_id(db, tenant_id)

    if not tenant:
        return None

    tenant.slab_name = slab_name
    tenant.slab_limit = slab_limit

    db.commit()
    db.refresh(tenant)

    return tenant