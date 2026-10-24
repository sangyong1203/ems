from sqlalchemy import or_
from sqlalchemy.orm import Session

from .models import InverterPvStringLink, PvString
from ..device.models import Device


# 스트링 정보에 선택적인 인버터와 MPPT·채널 연결 정보를 합칩니다.
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


# 스트링을 연결 정보와 결합하고 상태·검색어·연결 여부로 필터링합니다.
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


# 스트링과 인버터 연결 정보를 조회하며 없으면 None을 반환합니다.
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


# 스트링을 생성·커밋한 뒤 연결 정보를 포함하여 다시 조회합니다.
def create_pv_string(db: Session, payload: dict) -> dict:
    item = PvString(**payload)
    db.add(item)
    db.commit()
    db.refresh(item)
    return get_pv_string(db, item.id) or {}


# 스트링 필드를 갱신·커밋한 뒤 다시 조회하며 대상이 없으면 None을 반환합니다.
def update_pv_string(db: Session, pv_string_id: int, payload: dict) -> dict | None:
    item = db.query(PvString).filter(PvString.id == pv_string_id).first()
    if item is None:
        return None
    for key, value in payload.items():
        setattr(item, key, value)
    db.commit()
    return get_pv_string(db, pv_string_id)


# 스트링의 인버터 연결을 먼저 지운 뒤 스트링을 삭제하고 커밋합니다.
def delete_pv_string(db: Session, pv_string_id: int) -> bool:
    item = db.query(PvString).filter(PvString.id == pv_string_id).first()
    if item is None:
        return False
    db.query(InverterPvStringLink).filter(InverterPvStringLink.pv_string_id == pv_string_id).delete()
    db.delete(item)
    db.commit()
    return True


# 인버터의 스트링 연결을 MPPT·채널·스트링 이름 순으로 조회합니다.
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


# 기존 연결을 전부 교체하며 다른 인버터의 동일 스트링 연결도 해제합니다. 커밋은 호출자가 처리합니다.
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
