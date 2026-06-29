from sqlalchemy.orm import Session

from .models import (
    EssSystemTelemetryHistory,
    EssSystemTelemetryLatest,
    SiteTelemetryHistory,
    SiteTelemetryLatest,
    TelemetryHistory,
    TelemetryLatest,
)


def latest_map(db: Session) -> dict[str, TelemetryLatest]:
    return {item.metric_key: item for item in db.query(TelemetryLatest).all()}


def latest_site_map(db: Session) -> dict[str, SiteTelemetryLatest]:
    return {item.metric_key: item for item in db.query(SiteTelemetryLatest).all()}


def latest_site_metric(db: Session, metric_key: str) -> SiteTelemetryLatest | None:
    return (
        db.query(SiteTelemetryLatest)
        .filter(SiteTelemetryLatest.metric_key == metric_key)
        .order_by(SiteTelemetryLatest.measured_at.desc())
        .first()
    )


def latest_system_metric(db: Session, ess_system_id: int, metric_key: str) -> EssSystemTelemetryLatest | None:
    return (
        db.query(EssSystemTelemetryLatest)
        .filter(
            EssSystemTelemetryLatest.ess_system_id == ess_system_id,
            EssSystemTelemetryLatest.metric_key == metric_key,
        )
        .order_by(EssSystemTelemetryLatest.measured_at.desc())
        .first()
    )


def latest_metric(db: Session, metric_key: str, device_id: int | None = None) -> TelemetryLatest | None:
    query = db.query(TelemetryLatest).filter(TelemetryLatest.metric_key == metric_key)
    if device_id is None:
        query = query.filter(TelemetryLatest.device_id.is_(None))
    else:
        query = query.filter(TelemetryLatest.device_id == device_id)
    return query.order_by(TelemetryLatest.measured_at.desc()).first()


def latest_device_metric(db: Session, device_id: int, metric_key: str) -> TelemetryLatest | None:
    return latest_metric(db, metric_key, device_id)


def latest_metric_any_device(db: Session, metric_key: str) -> TelemetryLatest | None:
    return (
        db.query(TelemetryLatest)
        .filter(TelemetryLatest.metric_key == metric_key)
        .order_by(TelemetryLatest.measured_at.desc())
        .first()
    )


def history_by_metric(db: Session, metric_key: str, limit: int = 48, device_id: int | None = None) -> list[TelemetryHistory]:
    query = db.query(TelemetryHistory).filter(TelemetryHistory.metric_key == metric_key)
    if device_id is None:
        query = query.filter(TelemetryHistory.device_id.is_(None))
    else:
        query = query.filter(TelemetryHistory.device_id == device_id)
    return query.order_by(TelemetryHistory.measured_at.desc()).limit(limit).all()


def site_history_by_metric(db: Session, metric_key: str, limit: int = 48) -> list[SiteTelemetryHistory]:
    return (
        db.query(SiteTelemetryHistory)
        .filter(SiteTelemetryHistory.metric_key == metric_key)
        .order_by(SiteTelemetryHistory.measured_at.desc())
        .limit(limit)
        .all()
    )


def system_history_by_metric(
    db: Session,
    ess_system_id: int,
    metric_key: str,
    limit: int = 48,
) -> list[EssSystemTelemetryHistory]:
    return (
        db.query(EssSystemTelemetryHistory)
        .filter(
            EssSystemTelemetryHistory.ess_system_id == ess_system_id,
            EssSystemTelemetryHistory.metric_key == metric_key,
        )
        .order_by(EssSystemTelemetryHistory.measured_at.desc())
        .limit(limit)
        .all()
    )


def history_by_metric_any_device(db: Session, metric_key: str, limit: int = 48) -> list[TelemetryHistory]:
    return (
        db.query(TelemetryHistory)
        .filter(TelemetryHistory.metric_key == metric_key)
        .order_by(TelemetryHistory.measured_at.desc())
        .limit(limit)
        .all()
    )
