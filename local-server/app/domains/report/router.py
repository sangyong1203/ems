from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .service import (
    get_daily_report_response,
    get_report_statistics_response,
    get_report_summary_response,
)


router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/daily")
def daily_report(date: str = Query(default=""), db: Session = Depends(get_db)):
    return ok(get_daily_report_response(db, date))


@router.get("/summary")
def report_summary(
    dateFrom: str = Query(default=""),
    dateTo: str = Query(default=""),
    db: Session = Depends(get_db),
):
    return ok(get_report_summary_response(db, dateFrom, dateTo))


@router.get("/statistics")
def report_statistics(
    dateFrom: str = Query(default=""),
    dateTo: str = Query(default=""),
    db: Session = Depends(get_db),
):
    return ok(get_report_statistics_response(db, dateFrom, dateTo))
