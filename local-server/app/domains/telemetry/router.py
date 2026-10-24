from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .service import get_latest_telemetry, get_telemetry_history, get_telemetry_power_flow


router = APIRouter(prefix="/api/telemetry", tags=["telemetry"])  # 이 도메인의 API 경로와 문서 태그


# 최신 계측값 목록을 공통 성공 응답으로 반환합니다.
@router.get("/latest")
def latest(db: Session = Depends(get_db)):
    return ok(get_latest_telemetry(db))


# 지표 키와 조회 개수를 전달하여 계측 이력을 반환합니다.
@router.get("/history")
def history(metricKey: str = Query(default="solar_power_kw"), limit: int = Query(default=48), db: Session = Depends(get_db)):
    return ok(get_telemetry_history(db, metricKey, limit))


# 전력 흐름 서비스의 계산 결과를 반환합니다.
@router.get("/power-flow")
def telemetry_power_flow(db: Session = Depends(get_db)):
    return ok(get_telemetry_power_flow(db))
