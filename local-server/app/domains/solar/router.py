from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .service import get_solar_overview


router = APIRouter(prefix="/api/solar", tags=["solar"])  # 이 도메인의 API 경로와 문서 태그


# 태양광 요약 지표와 인버터별 출력·발전 이력을 반환합니다.
@router.get("/overview")
def solar_overview(db: Session = Depends(get_db)):
    return ok(get_solar_overview(db))
