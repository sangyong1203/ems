from sqlalchemy.orm import Session

from .models import (
    EssSystemTelemetryHistory,
    EssSystemTelemetryLatest,
    SiteTelemetryHistory,
    SiteTelemetryLatest,
    TelemetryHistory,
    TelemetryLatest,
)


# 장비 구분 없이 최신 테이블을 지표 키로 묶으며 같은 키는 뒤에서 읽은 행으로 덮어씁니다.
def latest_map(db: Session) -> dict[str, TelemetryLatest]:
    return {item.metric_key: item for item in db.query(TelemetryLatest).all()}


# 사업장 최신 계측 테이블을 지표 키로 묶습니다.
def latest_site_map(db: Session) -> dict[str, SiteTelemetryLatest]:
    return {item.metric_key: item for item in db.query(SiteTelemetryLatest).all()}


# 사업장 지표 중 계측 시각이 가장 최근인 행을 조회합니다.
def latest_site_metric(db: Session, metric_key: str) -> SiteTelemetryLatest | None:
    return (
        db.query(SiteTelemetryLatest)
        .filter(SiteTelemetryLatest.metric_key == metric_key)
        .order_by(SiteTelemetryLatest.measured_at.desc())
        .first()
    )


# 지정 ESS 시스템과 지표의 가장 최근 계측값을 조회합니다.
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


# 지정 장비의 최신 지표를 조회하며 장비 ID 생략 시 장비가 없는 행만 조회합니다.
def latest_metric(db: Session, metric_key: str, device_id: int | None = None) -> TelemetryLatest | None:
    query = db.query(TelemetryLatest).filter(TelemetryLatest.metric_key == metric_key)
    if device_id is None:
        query = query.filter(TelemetryLatest.device_id.is_(None))
    else:
        query = query.filter(TelemetryLatest.device_id == device_id)
    return query.order_by(TelemetryLatest.measured_at.desc()).first()


# 장비 ID와 지표에 해당하는 최신 계측값 조회를 위임합니다.
def latest_device_metric(db: Session, device_id: int, metric_key: str) -> TelemetryLatest | None:
    return latest_metric(db, metric_key, device_id)


# 장비를 제한하지 않고 해당 지표의 가장 최근 계측값을 조회합니다.
def latest_metric_any_device(db: Session, metric_key: str) -> TelemetryLatest | None:
    return (
        db.query(TelemetryLatest)
        .filter(TelemetryLatest.metric_key == metric_key)
        .order_by(TelemetryLatest.measured_at.desc())
        .first()
    )


# 장비별 지표 이력을 최신순으로 제한 조회하며 장비 ID 생략 시 장비가 없는 행만 조회합니다.
def history_by_metric(db: Session, metric_key: str, limit: int = 48, device_id: int | None = None) -> list[TelemetryHistory]:
    query = db.query(TelemetryHistory).filter(TelemetryHistory.metric_key == metric_key)
    if device_id is None:
        query = query.filter(TelemetryHistory.device_id.is_(None))
    else:
        query = query.filter(TelemetryHistory.device_id == device_id)
    return query.order_by(TelemetryHistory.measured_at.desc()).limit(limit).all()


# 사업장 지표 이력을 계측 시각 내림차순으로 지정 개수까지 조회합니다.
def site_history_by_metric(db: Session, metric_key: str, limit: int = 48) -> list[SiteTelemetryHistory]:
    return (
        db.query(SiteTelemetryHistory)
        .filter(SiteTelemetryHistory.metric_key == metric_key)
        .order_by(SiteTelemetryHistory.measured_at.desc())
        .limit(limit)
        .all()
    )


# ESS 시스템별 지표 이력을 최신순으로 지정 개수까지 조회합니다.
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


# 장비 구분 없이 지표 이력을 최신순으로 지정 개수까지 조회합니다.
def history_by_metric_any_device(db: Session, metric_key: str, limit: int = 48) -> list[TelemetryHistory]:
    return (
        db.query(TelemetryHistory)
        .filter(TelemetryHistory.metric_key == metric_key)
        .order_by(TelemetryHistory.measured_at.desc())
        .limit(limit)
        .all()
    )
