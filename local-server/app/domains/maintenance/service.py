from fastapi import HTTPException
from sqlalchemy.orm import Session

from .repository import (
    create_maintenance,
    delete_maintenance,
    get_maintenance,
    list_maintenance,
    update_maintenance,
)
from .schemas import MaintenanceOut, MaintenanceSaveBody


def get_maintenance_list(
    db: Session,
    keyword: str = "",
    device_id: int | None = None,
    maintenance_type: str = "",
    status: str = "",
    date_from: str = "",
    date_to: str = "",
) -> dict:
    items = list_maintenance(
        db,
        keyword=keyword,
        device_id=device_id,
        maintenance_type=maintenance_type,
        status=status,
        date_from=date_from,
        date_to=date_to,
    )
    return {"list": [_maintenance_to_dict(item, device) for item, device in items], "totalCount": len(items)}


def get_maintenance_detail(db: Session, maintenance_id: int) -> dict:
    item = get_maintenance(db, maintenance_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    return _maintenance_to_dict(item)


def add_maintenance(db: Session, body: MaintenanceSaveBody) -> dict:
    item = create_maintenance(db, body.model_dump())
    return _maintenance_to_dict(item)


def save_maintenance(db: Session, maintenance_id: int, body: MaintenanceSaveBody) -> dict:
    item = update_maintenance(db=db, maintenance_id=maintenance_id, payload=body.model_dump())
    if item is None:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    return _maintenance_to_dict(item)


def remove_maintenance(db: Session, maintenance_id: int) -> dict:
    if not delete_maintenance(db, maintenance_id):
        raise HTTPException(status_code=404, detail="Maintenance not found")
    return {"deleted": True}


def _maintenance_to_dict(item, device=None) -> dict:
    data = MaintenanceOut.model_validate(item).model_dump()
    data["device_name"] = device.name if device else None
    data["device_type"] = device.device_type if device else None
    return data
