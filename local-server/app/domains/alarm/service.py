from fastapi import HTTPException
from sqlalchemy.orm import Session

from .repository import (
    acknowledge_alarm,
    create_alarm_maintenance,
    get_alarm_with_device,
    list_alarms,
    resolve_alarm,
)
from .schemas import AlarmOut
from ..maintenance.schemas import MaintenanceOut


def get_alarm_list(
    db: Session,
    keyword: str = "",
    device_id: int | None = None,
    severity: str = "",
    alarm_type: str = "",
    status: str = "",
    date_from: str = "",
    date_to: str = "",
) -> dict:
    items = list_alarms(
        db,
        keyword=keyword,
        device_id=device_id,
        severity=severity,
        alarm_type=alarm_type,
        status=status,
        date_from=date_from,
        date_to=date_to,
    )
    return {
        "list": [_alarm_to_dict(alarm, device, maintenance) for alarm, device, maintenance in items],
        "totalCount": len(items),
    }


def get_alarm_detail(db: Session, alarm_id: int) -> dict:
    result = get_alarm_with_device(db, alarm_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Alarm not found")
    alarm, device, maintenance = result
    return _alarm_to_dict(alarm, device, maintenance)


def ack_alarm(db: Session, alarm_id: int) -> dict:
    alarm = acknowledge_alarm(db, alarm_id)
    if alarm is None:
        raise HTTPException(status_code=404, detail="Alarm not found")
    return get_alarm_detail(db, alarm_id)


def complete_alarm(db: Session, alarm_id: int) -> dict:
    alarm = resolve_alarm(db, alarm_id)
    if alarm is None:
        raise HTTPException(status_code=404, detail="Alarm not found")
    return get_alarm_detail(db, alarm_id)


def add_alarm_maintenance(db: Session, alarm_id: int) -> dict:
    maintenance = create_alarm_maintenance(db, alarm_id)
    if maintenance is None:
        raise HTTPException(status_code=404, detail="Alarm not found")
    return MaintenanceOut.model_validate(maintenance).model_dump()


def _alarm_to_dict(alarm, device=None, maintenance=None) -> dict:
    data = AlarmOut.model_validate(alarm).model_dump()
    data["device_name"] = device.name if device else None
    data["device_type"] = device.device_type if device else None
    data["maintenance_id"] = maintenance.id if maintenance else None
    data["maintenance_status"] = maintenance.status if maintenance else None
    data["maintenance_title"] = maintenance.title if maintenance else None
    data["maintenance_date"] = maintenance.maintenance_date if maintenance else None
    return data
