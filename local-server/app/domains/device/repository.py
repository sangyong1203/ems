from sqlalchemy import or_
from sqlalchemy.orm import Session

from .models import Device
from ..alarm.models import Alarm
from ..ess.models import EssSystem, EssSystemBatteryRack
from ..maintenance.models import MaintenanceRecord
from ..power_flow.models import PowerFlowLayoutNode
from ..pv_string.models import InverterPvStringLink
from ..pv_string.repository import replace_inverter_links
from ..telemetry.models import TelemetryHistory, TelemetryLatest


# 종류·상태·검색어로 장비를 필터링하고 종류와 이름 순으로 조회합니다.
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


# 활성 여부나 종류를 제한하지 않고 모든 장비를 조회합니다.
def list_all_devices(db: Session) -> list[Device]:
    return db.query(Device).all()


# 종류에 해당하는 장비를 이름 또는 ID 오름차순으로 조회합니다.
def list_devices_by_type(db: Session, device_type: str, order_by_id: bool = False) -> list[Device]:
    query = db.query(Device).filter(Device.device_type == device_type)
    if order_by_id:
        query = query.order_by(Device.id.asc())
    else:
        query = query.order_by(Device.name.asc())
    return query.all()


# 종류가 일치하는 첫 장비를 조회하며 없으면 None을 반환합니다.
def first_device_by_type(db: Session, device_type: str) -> Device | None:
    return db.query(Device).filter(Device.device_type == device_type).first()


# 장비 ID로 단건 조회하며 없으면 None을 반환합니다.
def get_device(db: Session, device_id: int) -> Device | None:
    return db.query(Device).filter(Device.id == device_id).first()


# 장비를 커밋한 뒤 전달된 스트링 연결을 저장하며 인버터 외 장비의 연결은 비웁니다.
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


# 장비와 전달된 스트링 연결을 갱신·커밋하며 연결 인자가 None이면 기존 연결을 유지합니다.
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


# ESS·스트링·배치·계측·알림·정비에서 장비를 참조하는 항목을 수집합니다.
def device_delete_blockers(db: Session, device_id: int) -> list[str]:
    blockers: list[str] = []
    if (
        db.query(EssSystem)
        .filter(
            or_(
                EssSystem.pcs_device_id == device_id,
                EssSystem.bms_device_id == device_id,
                EssSystem.battery_device_id == device_id,
            )
        )
        .first()
        is not None
    ):
        blockers.append("ESS system")
    if db.query(EssSystemBatteryRack).filter(EssSystemBatteryRack.rack_device_id == device_id).first() is not None:
        blockers.append("ESS battery rack")
    if db.query(InverterPvStringLink).filter(InverterPvStringLink.inverter_device_id == device_id).first() is not None:
        blockers.append("PV string connection")
    if db.query(PowerFlowLayoutNode).filter(PowerFlowLayoutNode.device_id == device_id).first() is not None:
        blockers.append("Power Flow layout")
    if db.query(TelemetryLatest).filter(TelemetryLatest.device_id == device_id).first() is not None:
        blockers.append("latest telemetry")
    if db.query(TelemetryHistory).filter(TelemetryHistory.device_id == device_id).first() is not None:
        blockers.append("telemetry history")
    if db.query(Alarm).filter(Alarm.device_id == device_id).first() is not None:
        blockers.append("alarm history")
    if db.query(MaintenanceRecord).filter(MaintenanceRecord.device_id == device_id).first() is not None:
        blockers.append("maintenance history")
    return blockers


# 장비를 삭제하고 커밋하며 참조 여부 검사는 호출 서비스에서 수행합니다.
def delete_device(db: Session, device_id: int) -> bool:
    device = get_device(db, device_id)
    if device is None:
        return False
    db.delete(device)
    db.commit()
    return True
