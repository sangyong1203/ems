from sqlalchemy import or_
from sqlalchemy.orm import Session

from .models import Device
from ..pv_string.models import InverterPvStringLink
from ..pv_string.repository import replace_inverter_links


def list_devices(db: Session, device_type: str = "", status: str = "", keyword: str = "") -> list[Device]:
    query = db.query(Device).order_by(Device.device_type.asc(), Device.name.asc())
    if device_type:
        query = query.filter(Device.device_type == device_type)
    if status:
        query = query.filter(Device.status == status)
    keyword = keyword.strip()
    if keyword:
        keyword_pattern = f"%{keyword}%"
        query = query.filter(
            or_(
                Device.name.ilike(keyword_pattern),
                Device.manufacturer.ilike(keyword_pattern),
                Device.model_name.ilike(keyword_pattern),
                Device.serial_number.ilike(keyword_pattern),
                Device.install_location.ilike(keyword_pattern),
            ),
        )
    return query.all()


def list_all_devices(db: Session) -> list[Device]:
    return db.query(Device).all()


def list_devices_by_type(db: Session, device_type: str, order_by_id: bool = False) -> list[Device]:
    query = db.query(Device).filter(Device.device_type == device_type)
    if order_by_id:
        query = query.order_by(Device.id.asc())
    else:
        query = query.order_by(Device.name.asc())
    return query.all()


def first_device_by_type(db: Session, device_type: str) -> Device | None:
    return db.query(Device).filter(Device.device_type == device_type).first()


def get_device(db: Session, device_id: int) -> Device | None:
    return db.query(Device).filter(Device.id == device_id).first()


def create_device(db: Session, payload: dict, pv_string_links: list[dict] | None = None) -> Device:
    device = Device(**payload)
    db.add(device)
    db.commit()
    db.refresh(device)
    if pv_string_links is not None:
        if device.device_type != "INVERTER":
            pv_string_links = []
        replace_inverter_links(db, device.id, pv_string_links)
        db.commit()
        db.refresh(device)
    return device


def update_device(db: Session, device_id: int, payload: dict, pv_string_links: list[dict] | None = None) -> Device | None:
    device = get_device(db, device_id)
    if device is None:
        return None
    for key, value in payload.items():
        setattr(device, key, value)
    if pv_string_links is not None:
        if device.device_type != "INVERTER":
            pv_string_links = []
        replace_inverter_links(db, device.id, pv_string_links)
    db.commit()
    db.refresh(device)
    return device


def delete_device(db: Session, device_id: int) -> bool:
    device = get_device(db, device_id)
    if device is None:
        return False
    db.query(InverterPvStringLink).filter(InverterPvStringLink.inverter_device_id == device_id).delete()
    db.delete(device)
    db.commit()
    return True
