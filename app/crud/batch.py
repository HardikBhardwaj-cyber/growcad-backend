from sqlalchemy.orm import Session
from app.models.batch import Batch


def create_batch(db: Session, name, tenant_id):
    batch = Batch(name=name, tenant_id=tenant_id)
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch