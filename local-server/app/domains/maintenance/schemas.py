from pydantic import BaseModel

from ...shared.schemas import OrmModel


class MaintenanceOut(OrmModel):
    id: int
    device_id: int | None
    alarm_id: int | None
    maintenance_type: str
    title: str
    description: str | None
    action_taken: str | None
    status: str
    maintenance_date: str | None
    next_maintenance_date: str | None
    manager_name: str | None
    cause: str | None = None
    before_status: str | None = None
    after_status: str | None = None
    contractor_name: str | None = None
    cost: float | None = None
    memo: str | None = None
    device_name: str | None = None
    device_type: str | None = None


class MaintenanceSaveBody(BaseModel):
    device_id: int | None = None
    alarm_id: int | None = None
    maintenance_type: str
    title: str
    description: str | None = None
    action_taken: str | None = None
    status: str = "SCHEDULED"
    maintenance_date: str | None = None
    next_maintenance_date: str | None = None
    manager_name: str | None = None
    memo: str | None = None
