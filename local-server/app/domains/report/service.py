from sqlalchemy.orm import Session

from .repository import get_daily_report, get_report_statistics, get_report_summary
from .schemas import DailyReportOut, ReportStatisticsOut, ReportSummaryOut


def get_daily_report_response(db: Session, date: str = "") -> dict | None:
    report = get_daily_report(db, date)
    return DailyReportOut.model_validate(report).model_dump() if report else None


def get_report_summary_response(db: Session, date_from: str = "", date_to: str = "") -> dict | None:
    report = get_report_summary(db, date_from, date_to)
    return ReportSummaryOut.model_validate(report).model_dump() if report else None


def get_report_statistics_response(db: Session, date_from: str = "", date_to: str = "") -> dict | None:
    report = get_report_statistics(db, date_from, date_to)
    return ReportStatisticsOut.model_validate(report).model_dump() if report else None
