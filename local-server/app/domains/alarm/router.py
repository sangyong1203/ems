from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .service import (
    ack_alarm,
    add_alarm_maintenance,
    complete_alarm,
    get_alarm_detail,
    get_alarm_list,
)


router = APIRouter(prefix="/api/alarms", tags=["alarms"])  # 이 도메인의 API 경로와 문서 태그


# 검색 조건의 쿼리 필드명을 서비스 인자로 매핑하여 알림 목록을 반환합니다.
@router.get("")
def alarms(
    keyword: str = Query(default=""),
    deviceId: int | None = Query(default=None),
    severity: str = Query(default=""),
    alarmType: str = Query(default=""),
    status: str = Query(default=""),
    dateFrom: str = Query(default=""),
    dateTo: str = Query(default=""),
    db: Session = Depends(get_db),
):
    return ok(
        get_alarm_list(
            db,
            keyword=keyword,
            device_id=deviceId,
            severity=severity,
            alarm_type=alarmType,
            status=status,
            date_from=dateFrom,
            date_to=dateTo,
        )
    )


# 알림 ID에 해당하는 장비·정비 포함 상세를 성공 응답으로 반환합니다.
@router.get("/{alarm_id}")
def alarm_detail(alarm_id: int, db: Session = Depends(get_db)):
    return ok(get_alarm_detail(db, alarm_id))


# 알림 확인 처리를 요청하고 갱신된 상세를 반환합니다.
@router.put("/{alarm_id}/ack")
def acknowledge(alarm_id: int, db: Session = Depends(get_db)):
    return ok(ack_alarm(db, alarm_id))


# 알림 해결 처리를 요청하고 갱신된 상세를 반환합니다.
@router.put("/{alarm_id}/resolve")
def resolve(alarm_id: int, db: Session = Depends(get_db)):
    return ok(complete_alarm(db, alarm_id))


# 알림에 연결할 정비의 생성 또는 재사용 결과를 반환합니다.
@router.post("/{alarm_id}/maintenance")
def create_maintenance_from_alarm(alarm_id: int, db: Session = Depends(get_db)):
    return ok(add_alarm_maintenance(db, alarm_id))
