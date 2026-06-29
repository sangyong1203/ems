from sqlalchemy.orm import Session

from .models import EssSystem, EssSystemBatteryRack
from ..device.models import Device


def list_ess_systems(db: Session) -> list[EssSystem]:
    return db.query(EssSystem).order_by(EssSystem.id.asc()).all()


def get_ess_system(db: Session, system_id: int) -> EssSystem | None:
    return db.query(EssSystem).filter(EssSystem.id == system_id).first()


def first_ess_system(db: Session) -> EssSystem | None:
    return db.query(EssSystem).order_by(EssSystem.id.asc()).first()


def list_battery_racks(db: Session, system_id: int) -> list[tuple[EssSystemBatteryRack, Device]]:
    return (
        db.query(EssSystemBatteryRack, Device)
        .join(Device, Device.id == EssSystemBatteryRack.rack_device_id)
        .filter(EssSystemBatteryRack.ess_system_id == system_id)
        .order_by(EssSystemBatteryRack.display_order.asc(), EssSystemBatteryRack.rack_no.asc())
        .all()
    )
