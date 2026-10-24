from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .service import (
    generate_alarm_data,
    generate_last_7_days_data,
    generate_maintenance_data,
    generate_today_data,
    reset_data,
)


router = APIRouter(prefix="/api/simulator", tags=["simulator"])  # 이 도메인의 API 경로와 문서 태그


# 오늘의 가상 운전 데이터 재생성을 요청하고 생성 시각을 반환합니다.
@router.post("/generate-today")
def generate_today(db: Session = Depends(get_db)):
    return ok(generate_today_data(db))


# 오늘 데이터와 최근 7일 리포트의 재생성을 요청합니다.
@router.post("/generate-last-7-days")
def generate_last_7_days(db: Session = Depends(get_db)):
    return ok(generate_last_7_days_data(db))


# 기존 알림을 샘플 알림으로 교체합니다.
@router.post("/generate-alarms")
def generate_alarms(db: Session = Depends(get_db)):
    return ok(generate_alarm_data(db))


# 기존 정비 기록을 샘플 정비로 교체합니다.
@router.post("/generate-maintenance")
def generate_maintenance(db: Session = Depends(get_db)):
    return ok(generate_maintenance_data(db))


# 운전 데이터 전체 삭제를 요청하고 초기화 결과를 반환합니다.
@router.post("/reset")
def reset(db: Session = Depends(get_db)):
    return ok(reset_data(db))
