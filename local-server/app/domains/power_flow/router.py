from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .service import get_power_flow_overview


router = APIRouter(prefix="/api/power-flow", tags=["power-flow"])  # 이 도메인의 API 경로와 문서 태그


# 계산된 전력 흐름과 갱신 주기를 공통 성공 응답으로 반환합니다.
@router.get("/overview")
def power_flow_overview(db: Session = Depends(get_db)):
    return ok(get_power_flow_overview(db))
