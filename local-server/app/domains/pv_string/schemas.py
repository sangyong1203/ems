from pydantic import BaseModel

from ...shared.schemas import OrmModel


class PvStringLinkOut(OrmModel):
    id: int
    inverter_device_id: int
    pv_string_id: int
    mppt_no: int | None
    channel_no: int | None
    pv_string_name: str | None = None
    inverter_name: str | None = None


class PvStringLinkSaveBody(BaseModel):
    pv_string_id: int
    mppt_no: int | None = None
    channel_no: int | None = None


class PvStringOut(OrmModel):
    id: int
    name: str
    panel_count: int | None
    panel_capacity_kw: float | None
    rated_capacity_kw: float | None
    install_location: str | None
    status: str
    is_active: bool
    memo: str | None
    inverter_device_id: int | None = None
    inverter_name: str | None = None
    mppt_no: int | None = None
    channel_no: int | None = None


class PvStringSaveBody(BaseModel):
    name: str
    panel_count: int | None = None
    panel_capacity_kw: float | None = None
    rated_capacity_kw: float | None = None
    install_location: str | None = None
    status: str = "NORMAL"
    is_active: bool = True
    memo: str | None = None
