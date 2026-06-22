from sqlalchemy import or_
from sqlalchemy.orm import Session

from .models import InverterPvStringLink, PvString
from ..device.models import Device


def _pv_string_row(item: PvString, link: InverterPvStringLink | None, inverter: Device | None) -> dict:
    return {
        "id": item.id,
        "name": item.name,
        "panel_count": item.panel_count,
        "panel_capacity_kw": item.panel_capacity_kw,
        "rated_capacity_kw": item.rated_capacity_kw,
        "install_location": item.install_location,
        "status": item.status,
        "is_active": item.is_active,
        "memo": item.memo,
        "inverter_device_id": link.inverter_device_id if link else None,
        "inverter_name": inverter.name if inverter else None,
        "mppt_no": link.mppt_no if link else None,
        "channel_no": link.channel_no if link else None,
    }


def list_pv_strings(db: Session, status: str = "", keyword: str = "", connection: str = "") -> list[dict]:
    query = (
        db.query(PvString, InverterPvStringLink, Device)
        .outerjoin(InverterPvStringLink, InverterPvStringLink.pv_string_id == PvString.id)
        .outerjoin(Device, Device.id == InverterPvStringLink.inverter_device_id)
        .order_by(PvString.name.asc())
    )
    if status:
        query = query.filter(PvString.status == status)
    keyword = keyword.strip()
    if keyword:
        keyword_pattern = f"%{keyword}%"
        query = query.filter(
            or_(
                PvString.name.ilike(keyword_pattern),
                PvString.install_location.ilike(keyword_pattern),
                Device.name.ilike(keyword_pattern),
            ),
        )
    if connection == "LINKED":
        query = query.filter(InverterPvStringLink.id.isnot(None))
    if connection == "UNLINKED":
        query = query.filter(InverterPvStringLink.id.is_(None))
    return [_pv_string_row(item, link, inverter) for item, link, inverter in query.all()]


def get_pv_string(db: Session, pv_string_id: int) -> dict | None:
    row = (
        db.query(PvString, InverterPvStringLink, Device)
        .outerjoin(InverterPvStringLink, InverterPvStringLink.pv_string_id == PvString.id)
        .outerjoin(Device, Device.id == InverterPvStringLink.inverter_device_id)
        .filter(PvString.id == pv_string_id)
        .first()
    )
    if row is None:
        return None
    item, link, inverter = row
    return _pv_string_row(item, link, inverter)


def create_pv_string(db: Session, payload: dict) -> dict:
    item = PvString(**payload)
    db.add(item)
    db.commit()
    db.refresh(item)
    return get_pv_string(db, item.id) or {}


def update_pv_string(db: Session, pv_string_id: int, payload: dict) -> dict | None:
    item = db.query(PvString).filter(PvString.id == pv_string_id).first()
    if item is None:
        return None
    for key, value in payload.items():
        setattr(item, key, value)
    db.commit()
    return get_pv_string(db, pv_string_id)


def delete_pv_string(db: Session, pv_string_id: int) -> bool:
    item = db.query(PvString).filter(PvString.id == pv_string_id).first()
    if item is None:
        return False
    db.query(InverterPvStringLink).filter(InverterPvStringLink.pv_string_id == pv_string_id).delete()
    db.delete(item)
    db.commit()
    return True


def list_inverter_links(db: Session, inverter_device_id: int) -> list[dict]:
    rows = (
        db.query(InverterPvStringLink, PvString, Device)
        .join(PvString, PvString.id == InverterPvStringLink.pv_string_id)
        .join(Device, Device.id == InverterPvStringLink.inverter_device_id)
        .filter(InverterPvStringLink.inverter_device_id == inverter_device_id)
        .order_by(InverterPvStringLink.mppt_no.asc(), InverterPvStringLink.channel_no.asc(), PvString.name.asc())
        .all()
    )
    return [
        {
            "id": link.id,
            "inverter_device_id": link.inverter_device_id,
            "pv_string_id": link.pv_string_id,
            "mppt_no": link.mppt_no,
            "channel_no": link.channel_no,
            "pv_string_name": pv_string.name,
            "inverter_name": inverter.name,
        }
        for link, pv_string, inverter in rows
    ]


def replace_inverter_links(db: Session, inverter_device_id: int, links: list[dict]) -> None:
    db.query(InverterPvStringLink).filter(InverterPvStringLink.inverter_device_id == inverter_device_id).delete()
    for item in links:
        db.query(InverterPvStringLink).filter(
            InverterPvStringLink.pv_string_id == item["pv_string_id"],
        ).delete()
        db.add(
            InverterPvStringLink(
                inverter_device_id=inverter_device_id,
                pv_string_id=item["pv_string_id"],
                mppt_no=item.get("mppt_no"),
                channel_no=item.get("channel_no"),
            )
        )
