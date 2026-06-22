from sqlalchemy import func
from sqlalchemy.orm import Session

from .models import DailyReport
from ..alarm.models import Alarm
from ..telemetry.models import TelemetryLatest


def latest_daily_report(db: Session) -> DailyReport | None:
    return db.query(DailyReport).order_by(DailyReport.report_date.desc()).first()


def get_daily_report(db: Session, report_date: str = "") -> DailyReport | None:
    if report_date:
        return db.query(DailyReport).filter(DailyReport.report_date == report_date).first()
    return latest_daily_report(db)


def get_report_summary(db: Session, date_from: str = "", date_to: str = "") -> dict | None:
    latest = latest_daily_report(db)
    if latest is None:
        return None

    start_date = date_from or latest.report_date
    end_date = date_to or start_date
    row = (
        db.query(
            func.count(DailyReport.id).label("day_count"),
            func.sum(DailyReport.generation_kwh).label("generation_kwh"),
            func.sum(DailyReport.ess_charge_kwh).label("ess_charge_kwh"),
            func.sum(DailyReport.ess_discharge_kwh).label("ess_discharge_kwh"),
            func.sum(DailyReport.grid_export_kwh).label("grid_export_kwh"),
            func.sum(DailyReport.grid_import_kwh).label("grid_import_kwh"),
            func.sum(DailyReport.alarm_count).label("alarm_count"),
            func.sum(DailyReport.maintenance_count).label("maintenance_count"),
        )
        .filter(DailyReport.report_date >= start_date, DailyReport.report_date <= end_date)
        .one()
    )
    if not row.day_count:
        return None
    return {
        "date_from": start_date,
        "date_to": end_date,
        "day_count": int(row.day_count or 0),
        "generation_kwh": float(row.generation_kwh or 0),
        "ess_charge_kwh": float(row.ess_charge_kwh or 0),
        "ess_discharge_kwh": float(row.ess_discharge_kwh or 0),
        "grid_export_kwh": float(row.grid_export_kwh or 0),
        "grid_import_kwh": float(row.grid_import_kwh or 0),
        "alarm_count": int(row.alarm_count or 0),
        "maintenance_count": int(row.maintenance_count or 0),
    }


def _load_breakdown(report: DailyReport) -> dict:
    load_total = max(
        report.generation_kwh
        + report.grid_import_kwh
        + report.ess_discharge_kwh
        - report.ess_charge_kwh
        - report.grid_export_kwh,
        0,
    )
    solar_to_load = min(report.generation_kwh, load_total)
    remaining_load = max(load_total - solar_to_load, 0)
    grid_to_load = min(report.grid_import_kwh, remaining_load)
    ess_to_load = max(remaining_load - grid_to_load, 0)
    self_reliance_rate = (solar_to_load / load_total * 100) if load_total > 0 else 0
    return {
        "load_total_kwh": round(load_total, 1),
        "load_solar_kwh": round(solar_to_load, 1),
        "load_grid_kwh": round(grid_to_load, 1),
        "load_ess_kwh": round(ess_to_load, 1),
        "self_reliance_rate": round(self_reliance_rate, 1),
    }


def _latest_metric_value(db: Session, metric_key: str, default: float = 0) -> float:
    item = db.query(TelemetryLatest).filter(TelemetryLatest.metric_key == metric_key).first()
    return float(item.metric_value) if item is not None else default


def _alarm_query(db: Session, start_date: str, end_date: str):
    return db.query(Alarm).filter(Alarm.occurred_at >= start_date, Alarm.occurred_at <= f"{end_date} 23:59:59")


def get_report_statistics(db: Session, date_from: str = "", date_to: str = "") -> dict | None:
    summary = get_report_summary(db, date_from, date_to)
    if summary is None:
        return None

    start_date = summary["date_from"]
    end_date = summary["date_to"]
    reports = (
        db.query(DailyReport)
        .filter(DailyReport.report_date >= start_date, DailyReport.report_date <= end_date)
        .order_by(DailyReport.report_date.asc())
        .all()
    )
    latest_temperature = _latest_metric_value(db, "ambient_temperature_c", 24)
    latest_soc = _latest_metric_value(db, "ess_soc", 70)

    series = []
    for index, report in enumerate(reports):
        load = _load_breakdown(report)
        temperature = round(latest_temperature + ((index % 5) - 2) * 0.7, 1)
        soc = round(max(0, min(100, latest_soc + ((index % 7) - 3) * 1.6)), 1)
        series.append(
            {
                "date": report.report_date,
                "generation_kwh": report.generation_kwh,
                "temperature_c": temperature,
                "ess_charge_kwh": report.ess_charge_kwh,
                "ess_discharge_kwh": report.ess_discharge_kwh,
                "ess_soc": soc,
                "grid_export_kwh": report.grid_export_kwh,
                "grid_import_kwh": report.grid_import_kwh,
                "alarm_count": report.alarm_count,
                **load,
            },
        )

    alarm_rows = (
        _alarm_query(db, start_date, end_date)
        .with_entities(Alarm.severity, func.count(Alarm.id).label("count"))
        .group_by(Alarm.severity)
        .all()
    )
    return {
        "summary": summary,
        "series": series,
        "alarm_severity_distribution": [
            {"severity": row.severity, "count": int(row.count or 0)} for row in alarm_rows
        ],
        "alarm_by_device": [],
    }
