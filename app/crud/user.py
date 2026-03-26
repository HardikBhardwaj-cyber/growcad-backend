from sqlalchemy.orm import Session
from app.models.user import User


def get_user_by_identifier(db: Session, identifier: str):
    return db.query(User).filter(
        (User.email == identifier) | (User.phone == identifier)
    ).first()


def create_user(db: Session, identifier: str, tenant_id: str):
    user = User(
        email=identifier if "@" in identifier else None,
        phone=identifier if "@" not in identifier else None,
        tenant_id=tenant_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user