from datetime import datetime

from typing import cast

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from .models import Alarm
from ..device.models import Device
from ..maintenance.models import MaintenanceRecord

AlarmDetailRow = tuple[Alarm, Device | None, MaintenanceRecord | None]  # 알림과 선택적인 장비·연결 정비의 조회 결과


# 발생 시각 내림차순으로 최근 알림을 지정 개수까지 조회합니다.
def recent_alarms(db: Session, limit: int = 5) -> list[Alarm]:
    return db.query(Alarm).order_by(Alarm.occurred_at.desc()).limit(limit).all()


# 상태가 RESOLVED가 아닌 모든 미해결 알림의 수를 셉니다.
def count_open_alarms(db: Session) -> int:
    return db.query(Alarm).filter(Alarm.status != "RESOLVED").count()


# 장비와 ID가 가장 큰 연결 정비를 결합하여 조회하며 상태에 따라 알림 또는 정비 상태를 필터링합니다.
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
    # 정비 ID가 가장 큰 기록 한 건만 연결하여 정비가 여러 건이어도 알림 행이 중복되지 않게 합니다.
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
        # ACKED 검색은 연결 정비가 없는 확인 알림만, 그 외 정비 상태는 연결 정비를 기준으로 조회합니다.
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


# 알림 ID로 단건 조회하며 없으면 None을 반환합니다.
def get_alarm(db: Session, alarm_id: int) -> Alarm | None:
    return db.query(Alarm).filter(Alarm.id == alarm_id).first()


# 알림에 연결 장비와 ID가 가장 큰 정비를 결합하며 없으면 None을 반환합니다.
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


# 해결된 알림은 유지하고 나머지는 확인 상태와 최초 확인 시각을 저장·커밋합니다.
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


# 알림을 해결 상태로 바꾸고 확인·해결 시각을 저장한 뒤 커밋합니다.
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


# 이미 연결된 정비는 재사용하고, 없으면 정비를 생성하며 미확인 알림도 확인 처리합니다.
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
