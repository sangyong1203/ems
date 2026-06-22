from datetime import datetime

from ...shared.schemas import OrmModel


class AlarmOut(OrmModel):
    id: int
    device_id: int | None
    severity: str
    alarm_type: str
    message: str
    status: str
    occurred_at: datetime
    acknowledged_at: datetime | None
    resolved_at: datetime | None
    device_name: str | None = None
    device_type: str | None = None
    maintenance_id: int | None = None
    maintenance_status: str | None = None
    maintenance_title: str | None = None
    maintenance_date: str | None = None
