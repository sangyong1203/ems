from datetime import datetime

from sqlalchemy.orm import Session

from .models import TelemetryHistory, TelemetryLatest
from .repository import history_by_metric, history_by_metric_any_device, latest_map
from .schemas import TelemetryOut


# 지표 사전에서 계측값을 읽고 누락 시 전달된 기본값을 사용합니다.
def telemetry_value(latest: dict, key: str, default: float = 0) -> float:
    item = latest.get(key)
    if item is None:
        return default
    return item.metric_value


# 계측 시각을 초 단위 문자열로 반환하며 지표가 없으면 현재 서버 시각을 사용합니다.
def telemetry_time(latest: dict, key: str) -> str:
    item = latest.get(key)
    if item is None:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return item.measured_at.strftime("%Y-%m-%d %H:%M:%S")


# 계측값을 소수점 한 자리로 반환하며 계측 객체가 없으면 0을 사용합니다.
def metric_value(item: TelemetryLatest | None) -> float:
    return round(float(item.metric_value), 1) if item else 0


# 계측 시각을 ISO 문자열로 반환하며 계측 객체가 없으면 None을 사용합니다.
def metric_time(item: TelemetryLatest | None) -> str | None:
    return item.measured_at.isoformat() if item else None


# 최신순 조회 결과를 뒤집고 계측값을 반올림하여 시간 오름차순 응답을 구성합니다.
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


# 지표 키로 묶인 최신 계측값을 응답 스키마로 변환합니다.
def get_latest_telemetry(db: Session) -> list[dict]:
    return [TelemetryOut.model_validate(item).model_dump() for item in latest_map(db).values()]


# 장비가 없는 지표 이력을 먼저 조회하고 없으면 장비 구분 없이 조회하여 시간순으로 반환합니다.
def get_telemetry_history(db: Session, metric_key: str = "solar_power_kw", limit: int = 48) -> list[dict]:
    items = history_by_metric(db, metric_key, limit)
    if not items:
        items = history_by_metric_any_device(db, metric_key, limit)
    return [TelemetryOut.model_validate(item).model_dump() for item in reversed(items)]


# 호출 시 전력 흐름 서비스를 가져와 계산 결과를 반환합니다.
def get_telemetry_power_flow(db: Session) -> dict:
    from ..power_flow.service import get_power_flow_overview

    return get_power_flow_overview(db)
