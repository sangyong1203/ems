from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .service import get_ess_overview, get_ess_system_overview, get_ess_systems


router = APIRouter(prefix="/api/ess", tags=["ess"])  # 이 도메인의 API 경로와 문서 태그


# 첫 ESS 시스템의 상세 모니터링 정보를 반환합니다.
@router.get("/overview")
def ess_overview(db: Session = Depends(get_db)):
    return ok(get_ess_overview(db))


# ESS 시스템 목록과 전체 집계를 반환합니다.
@router.get("/systems")
def ess_systems(db: Session = Depends(get_db)):
    return ok(get_ess_systems(db))


# 선택한 ESS 시스템의 상세 모니터링 정보를 반환합니다.
@router.get("/systems/{system_id}/overview")
def ess_system_overview(system_id: int, db: Session = Depends(get_db)):
    return ok(get_ess_system_overview(db, system_id))
