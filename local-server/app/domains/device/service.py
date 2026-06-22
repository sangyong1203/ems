from fastapi import HTTPException
from sqlalchemy.orm import Session

from .repository import create_device, delete_device, get_device, list_devices, update_device
from .schemas import DeviceOut, DeviceSaveBody
from ..pv_string.repository import list_inverter_links


def get_device_list(db: Session, device_type: str = "", status: str = "", keyword: str = "") -> dict:
    items = list_devices(db, device_type=device_type, status=status, keyword=keyword)
    return {"list": [_device_out(item, db) for item in items], "totalCount": len(items)}


def get_device_detail(db: Session, device_id: int) -> dict:
    device = get_device(db, device_id)
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return _device_out(device, db)


def add_device(db: Session, body: DeviceSaveBody) -> dict:
    payload = body.model_dump()
    pv_string_links = payload.pop("pv_string_links", [])
    device = create_device(db, payload, pv_string_links=pv_string_links)
    return _device_out(device, db)


def save_device(db: Session, device_id: int, body: DeviceSaveBody) -> dict:
    payload = body.model_dump()
    pv_string_links = payload.pop("pv_string_links", [])
    device = update_device(db, device_id, payload, pv_string_links=pv_string_links)
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return _device_out(device, db)


def remove_device(db: Session, device_id: int) -> dict:
    if not delete_device(db, device_id):
        raise HTTPException(status_code=404, detail="Device not found")
    return {"deleted": True}


def _device_out(device, db: Session) -> dict:
    data = DeviceOut.model_validate(device).model_dump()
    data["pv_string_links"] = list_inverter_links(db, device.id) if device.device_type == "INVERTER" else []
    return data
