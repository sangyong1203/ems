from datetime import datetime

from sqlalchemy.orm import Session

from .models import TelemetryHistory, TelemetryLatest
from .repository import history_by_metric, history_by_metric_any_device, latest_map
from .schemas import TelemetryOut


def telemetry_value(latest: dict, key: str, default: float = 0) -> float:
    item = latest.get(key)
    if item is None:
        return default
    return item.metric_value


def telemetry_time(latest: dict, key: str) -> str:
    item = latest.get(key)
    if item is None:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return item.measured_at.strftime("%Y-%m-%d %H:%M:%S")


def metric_value(item: TelemetryLatest | None) -> float:
    return round(float(item.metric_value), 1) if item else 0


def metric_time(item: TelemetryLatest | None) -> str | None:
    return item.measured_at.isoformat() if item else None


def history_points(items: list[TelemetryHistory]) -> list[dict]:
    return [
        {
            "id": item.id,
            "device_id": getattr(item, "device_id", None),
            "ess_system_id": getattr(item, "ess_system_id", None),
            "metric_key": item.metric_key,
            "metric_value": round(float(item.metric_value), 1),
            "unit": item.unit,
            "measured_at": item.measured_at.isoformat(),
        }
        for item in reversed(items)
    ]


def get_latest_telemetry(db: Session) -> list[dict]:
    return [TelemetryOut.model_validate(item).model_dump() for item in latest_map(db).values()]


def get_telemetry_history(db: Session, metric_key: str = "solar_power_kw", limit: int = 48) -> list[dict]:
    items = history_by_metric(db, metric_key, limit)
    if not items:
        items = history_by_metric_any_device(db, metric_key, limit)
    return [TelemetryOut.model_validate(item).model_dump() for item in reversed(items)]


def get_telemetry_power_flow(db: Session) -> dict:
    from ..power_flow.service import get_power_flow_overview

    return get_power_flow_overview(db)
