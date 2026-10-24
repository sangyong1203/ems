from sqlalchemy.orm import Session

from .models import EssSystem, EssSystemBatteryRack
from ..device.models import Device


# 전체 ESS 시스템을 ID 오름차순으로 조회합니다.
def list_ess_systems(db: Session) -> list[EssSystem]:
    return db.query(EssSystem).order_by(EssSystem.id.asc()).all()


# ESS 시스템 ID로 조회하며 없으면 None을 반환합니다.
def get_ess_system(db: Session, system_id: int) -> EssSystem | None:
    return db.query(EssSystem).filter(EssSystem.id == system_id).first()


# ID가 가장 작은 ESS 시스템을 조회하며 없으면 None을 반환합니다.
def first_ess_system(db: Session) -> EssSystem | None:
    return db.query(EssSystem).order_by(EssSystem.id.asc()).first()


# ESS에 연결된 랙과 장비를 표시 순서·랙 번호 순으로 조회합니다.
def list_battery_racks(db: Session, system_id: int) -> list[tuple[EssSystemBatteryRack, Device]]:
    return (
        db.query(EssSystemBatteryRack, Device)
        .join(Device, Device.id == EssSystemBatteryRack.rack_device_id)
        .filter(EssSystemBatteryRack.ess_system_id == system_id)
        .order_by(EssSystemBatteryRack.display_order.asc(), EssSystemBatteryRack.rack_no.asc())
        .all()
    )
