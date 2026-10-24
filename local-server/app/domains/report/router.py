from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .service import (
    get_daily_report_response,
    get_report_statistics_response,
    get_report_summary_response,
)


router = APIRouter(prefix="/api/reports", tags=["reports"])  # 이 도메인의 API 경로와 문서 태그


# 요청 일자의 리포트를 반환하며 날짜 생략 시 최신 리포트를 사용합니다.
@router.get("/daily")
def daily_report(date: str = Query(default=""), db: Session = Depends(get_db)):
    return ok(get_daily_report_response(db, date))


# 기간 쿼리를 서비스에 전달하여 리포트 합계를 반환합니다.
@router.get("/summary")
def report_summary(
    dateFrom: str = Query(default=""),
    dateTo: str = Query(default=""),
    db: Session = Depends(get_db),
):
    return ok(get_report_summary_response(db, dateFrom, dateTo))


# 기간 쿼리를 서비스에 전달하여 시계열과 알림 통계를 반환합니다.
@router.get("/statistics")
def report_statistics(
    dateFrom: str = Query(default=""),
    dateTo: str = Query(default=""),
    db: Session = Depends(get_db),
):
    return ok(get_report_statistics_response(db, dateFrom, dateTo))
