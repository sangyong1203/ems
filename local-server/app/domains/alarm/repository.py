from datetime import datetime

from typing import cast

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from .models import Alarm
from ..device.models import Device
from ..maintenance.models import MaintenanceRecord

AlarmDetailRow = tuple[Alarm, Device | None, MaintenanceRecord | None]


def recent_alarms(db: Session, limit: int = 5) -> list[Alarm]:
    return db.query(Alarm).order_by(Alarm.occurred_at.desc()).limit(limit).all()


def count_open_alarms(db: Session) -> int:
    return db.query(Alarm).filter(Alarm.status != "RESOLVED").count()


def list_alarms(
    db: Session,
    keyword: str = "",
    device_id: int | None = None,
    severity: str = "",
    alarm_type: str = "",
    status: str = "",
    date_from: str = "",
    date_to: str = "",
) -> list[AlarmDetailRow]:
    latest_maintenance = (
        db.query(
            MaintenanceRecord.alarm_id.label("alarm_id"),
            func.max(MaintenanceRecord.id).label("maintenance_id"),
        )
        .filter(MaintenanceRecord.alarm_id.isnot(None))
        .group_by(MaintenanceRecord.alarm_id)
        .subquery()
    )
    query = (
        db.query(Alarm, Device, MaintenanceRecord)
        .outerjoin(Device, Alarm.device_id == Device.id)
        .outerjoin(latest_maintenance, latest_maintenance.c.alarm_id == Alarm.id)
        .outerjoin(MaintenanceRecord, MaintenanceRecord.id == latest_maintenance.c.maintenance_id)
        .order_by(Alarm.occurred_at.desc(), Alarm.id.desc())
    )
    if device_id:
        query = query.filter(Alarm.device_id == device_id)
    if severity:
        query = query.filter(Alarm.severity == severity)
    if alarm_type:
        query = query.filter(Alarm.alarm_type == alarm_type)
    if status:
        if status == "OPEN":
            query = query.filter(Alarm.status == "OPEN")
        elif status == "ACKED":
            query = query.filter(Alarm.status == "ACKED", MaintenanceRecord.id.is_(None))
        else:
            query = query.filter(MaintenanceRecord.status == status)
    if date_from:
        query = query.filter(Alarm.occurred_at >= date_from)
    if date_to:
        query = query.filter(Alarm.occurred_at <= f"{date_to} 23:59:59")
    keyword = keyword.strip()
    if keyword:
        keyword_pattern = f"%{keyword}%"
        query = query.filter(
            or_(
                Alarm.alarm_type.ilike(keyword_pattern),
                Alarm.message.ilike(keyword_pattern),
                Device.name.ilike(keyword_pattern),
                Device.manufacturer.ilike(keyword_pattern),
                Device.model_name.ilike(keyword_pattern),
            ),
        )
    return cast(list[AlarmDetailRow], query.all())


def get_alarm(db: Session, alarm_id: int) -> Alarm | None:
    return db.query(Alarm).filter(Alarm.id == alarm_id).first()


def get_alarm_with_device(db: Session, alarm_id: int) -> AlarmDetailRow | None:
    latest_maintenance = (
        db.query(
            MaintenanceRecord.alarm_id.label("alarm_id"),
            func.max(MaintenanceRecord.id).label("maintenance_id"),
        )
        .filter(MaintenanceRecord.alarm_id.isnot(None))
        .group_by(MaintenanceRecord.alarm_id)
        .subquery()
    )
    result = (
        db.query(Alarm, Device, MaintenanceRecord)
        .outerjoin(Device, Alarm.device_id == Device.id)
        .outerjoin(latest_maintenance, latest_maintenance.c.alarm_id == Alarm.id)
        .outerjoin(MaintenanceRecord, MaintenanceRecord.id == latest_maintenance.c.maintenance_id)
        .filter(Alarm.id == alarm_id)
        .first()
    )
    return cast(AlarmDetailRow | None, result)


def acknowledge_alarm(db: Session, alarm_id: int) -> Alarm | None:
    alarm = get_alarm(db, alarm_id)
    if alarm is None:
        return None
    if alarm.status == "RESOLVED":
        return alarm
    alarm.status = "ACKED"
    alarm.acknowledged_at = alarm.acknowledged_at or datetime.now()
    db.commit()
    db.refresh(alarm)
    return alarm


def resolve_alarm(db: Session, alarm_id: int) -> Alarm | None:
    alarm = get_alarm(db, alarm_id)
    if alarm is None:
        return None
    alarm.status = "RESOLVED"
    alarm.acknowledged_at = alarm.acknowledged_at or datetime.now()
    alarm.resolved_at = datetime.now()
    db.commit()
    db.refresh(alarm)
    return alarm


def create_alarm_maintenance(db: Session, alarm_id: int) -> MaintenanceRecord | None:
    alarm = get_alarm(db, alarm_id)
    if alarm is None:
        return None
    existing = (
        db.query(MaintenanceRecord)
        .filter(MaintenanceRecord.alarm_id == alarm.id)
        .order_by(MaintenanceRecord.id.desc())
        .first()
    )
    if existing is not None:
        return existing
    maintenance = MaintenanceRecord(
        device_id=alarm.device_id,
        alarm_id=alarm.id,
        maintenance_type="장애점검",
        title=f"{alarm.alarm_type} 조치",
        description=f"{alarm.message}\n발생 시간: {alarm.occurred_at}",
        action_taken=None,
        status="SCHEDULED",
        maintenance_date=datetime.now().date().isoformat(),
        manager_name="O&M 담당자",
        memo="알림 이력에서 생성",
    )
    db.add(maintenance)
    if alarm.status == "OPEN":
        alarm.status = "ACKED"
        alarm.acknowledged_at = datetime.now()
    db.commit()
    db.refresh(maintenance)
    return maintenance
