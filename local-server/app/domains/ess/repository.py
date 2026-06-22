from sqlalchemy.orm import Session

from .models import EssSystem


def list_ess_systems(db: Session) -> list[EssSystem]:
    return db.query(EssSystem).order_by(EssSystem.id.asc()).all()


def get_ess_system(db: Session, system_id: int) -> EssSystem | None:
    return db.query(EssSystem).filter(EssSystem.id == system_id).first()


def first_ess_system(db: Session) -> EssSystem | None:
    return db.query(EssSystem).order_by(EssSystem.id.asc()).first()
