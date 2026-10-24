from datetime import datetime

from ...shared.schemas import OrmModel


# 장비 또는 장비 미지정 계측값 응답
class TelemetryOut(OrmModel):
    id: int  # 계측 ID
    device_id: int | None  # 연결 장비 ID; None이면 특정 장비를 지정하지 않음
    metric_key: str  # 계측 지표 키
    metric_value: float  # 계측값; 단위는 unit 기준
    unit: str | None  # 계측 단위
    measured_at: datetime  # 계측 시각
