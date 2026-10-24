from sqlalchemy import or_
from sqlalchemy.orm import Session

from .models import MaintenanceRecord
from ..device.models import Device


# 정비일 내림차순으로 최근 정비를 지정 개수까지 조회합니다.
def recent_maintenance(db: Session, limit: int = 5) -> list[MaintenanceRecord]:
    return db.query(MaintenanceRecord).order_by(MaintenanceRecord.maintenance_date.desc()).limit(limit).all()


# 정비에 장비 정보를 결합하고 검색어·장비·유형·상태·기간 조건을 적용합니다.
def list_maintenance(
    db: Session,
    keyword: str = "",
    device_id: int | None = None,
    maintenance_type: str = "",
    status: str = "",
    date_from: str = "",
    date_to: str = "",
) -> list[tuple[MaintenanceRecord, Device | None]]:
    query = (
        db.query(MaintenanceRecord, Device)
        .outerjoin(Device, MaintenanceRecord.device_id == Device.id)
        .order_by(MaintenanceRecord.maintenance_date.desc(), MaintenanceRecord.id.desc())
    )
    if device_id:
        query = query.filter(MaintenanceRecord.device_id == device_id)
    if maintenance_type:
        query = query.filter(MaintenanceRecord.maintenance_type == maintenance_type)
    if status:
        query = query.filter(MaintenanceRecord.status == status)
    if date_from:
        query = query.filter(MaintenanceRecord.maintenance_date >= date_from)
    if date_to:
        query = query.filter(MaintenanceRecord.maintenance_date <= date_to)
    keyword = keyword.strip()
    if keyword:
        keyword_pattern = f"%{keyword}%"
        query = query.filter(
            or_(
                MaintenanceRecord.title.ilike(keyword_pattern),
                MaintenanceRecord.description.ilike(keyword_pattern),
                MaintenanceRecord.action_taken.ilike(keyword_pattern),
                MaintenanceRecord.manager_name.ilike(keyword_pattern),
                Device.name.ilike(keyword_pattern),
            ),
        )
    return query.all()


# 정비 ID로 단건 조회하며 없으면 None을 반환합니다.
def get_maintenance(db: Session, maintenance_id: int) -> MaintenanceRecord | None:
    return db.query(MaintenanceRecord).filter(MaintenanceRecord.id == maintenance_id).first()


# 정비와 선택적인 연결 장비를 함께 조회하며 없으면 None을 반환합니다.
def get_maintenance_with_device(db: Session, maintenance_id: int) -> tuple[MaintenanceRecord, Device | None] | None:
    return (
        db.query(MaintenanceRecord, Device)
        .outerjoin(Device, MaintenanceRecord.device_id == Device.id)
        .filter(MaintenanceRecord.id == maintenance_id)
        .first()
    )


# 정비 기록을 생성·커밋하고 저장된 객체를 반환합니다.
def create_maintenance(db: Session, payload: dict) -> MaintenanceRecord:
    item = MaintenanceRecord(**payload)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


# 정비 필드를 갱신·커밋하며 없으면 None을 반환합니다.
def update_maintenance(db: Session, maintenance_id: int, payload: dict) -> MaintenanceRecord | None:
    item = get_maintenance(db, maintenance_id)
    if item is None:
        return None
    for key, value in payload.items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


# 정비 기록을 삭제·커밋하며 없으면 False를 반환합니다.
def delete_maintenance(db: Session, maintenance_id: int) -> bool:
    item = get_maintenance(db, maintenance_id)
    if item is None:
        return False
    db.delete(item)
    db.commit()
    return True
