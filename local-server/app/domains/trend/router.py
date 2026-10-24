from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .service import get_trend_overview


router = APIRouter(prefix="/api/trend", tags=["trend"])  # 이 도메인의 API 경로와 문서 태그


# 사업장과 첫 ESS 시스템의 트렌드 요약 및 시계열을 반환합니다.
@router.get("/overview")
def trend_overview(db: Session = Depends(get_db)):
    return ok(get_trend_overview(db))
