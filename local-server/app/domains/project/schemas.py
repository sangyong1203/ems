from pydantic import BaseModel

from ...shared.schemas import OrmModel


class ProjectConfigOut(OrmModel):
    id: int
    project_name: str
    site_name: str
    location: str | None
    customer_name: str | None
    contractor_name: str | None
    solar_capacity_kw: float
    ess_capacity_kwh: float
    system_name: str
    background_image_path: str | None
    logo_image_path: str | None
    data_refresh_interval: int
    dashboard_refresh_interval: int
    solar_refresh_interval: int
    ess_refresh_interval: int
    power_flow_refresh_interval: int
    trend_refresh_interval: int
    device_counts: dict[str, int]
    active_device_counts: dict[str, int]
    equipment_capacities: dict[str, float]


class ProjectConfigSaveBody(BaseModel):
    project_name: str
    site_name: str
    location: str | None = None
    customer_name: str | None = None
    contractor_name: str | None = None
    solar_capacity_kw: float
    ess_capacity_kwh: float
    system_name: str
    background_image_path: str | None = None
    logo_image_path: str | None = None
    data_refresh_interval: int
    dashboard_refresh_interval: int
    solar_refresh_interval: int
    ess_refresh_interval: int
    power_flow_refresh_interval: int
    trend_refresh_interval: int
