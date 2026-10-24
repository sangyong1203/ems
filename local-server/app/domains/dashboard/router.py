from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .service import (
    get_dashboard_summary,
    get_power_flow,
    get_recent_alarm_ids,
    get_recent_maintenance_ids,
)


router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])  # 이 도메인의 API 경로와 문서 태그


# 대시보드의 설비·계측·알림·정비 요약을 반환합니다.
@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    return ok(get_dashboard_summary(db))


# 대시보드용 전력 흐름 계산 결과를 반환합니다.
@router.get("/power-flow")
def power_flow(db: Session = Depends(get_db)):
    return ok(get_power_flow(db))


# 최근 알림의 ID 목록을 반환합니다.
@router.get("/recent-alarms")
def dashboard_recent_alarms(db: Session = Depends(get_db)):
    return ok(get_recent_alarm_ids(db))


# 최근 정비의 ID 목록을 반환합니다.
@router.get("/recent-maintenance")
def dashboard_recent_maintenance(db: Session = Depends(get_db)):
    return ok(get_recent_maintenance_ids(db))
