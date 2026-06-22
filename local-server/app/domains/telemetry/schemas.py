from datetime import datetime

from ...shared.schemas import OrmModel


class TelemetryOut(OrmModel):
    id: int
    device_id: int | None
    metric_key: str
    metric_value: float
    unit: str | None
    measured_at: datetime
