from pydantic import BaseModel, ConfigDict, Field

from ...shared.schemas import OrmModel
from ..pv_string.schemas import PvStringLinkOut, PvStringLinkSaveBody


class DeviceOut(OrmModel):
    id: int
    device_type: str
    name: str
    manufacturer: str | None
    model_name: str | None
    serial_number: str | None
    capacity: float | None
    capacity_unit: str | None
    install_location: str | None
    install_date: str | None
    communication_type: str | None
    ip_address: str | None
    port: int | None
    slave_id: int | None
    protocol: str | None
    status: str
    is_active: bool
    warranty_start_date: str | None
    warranty_end_date: str | None
    vendor_name: str | None
    vendor_contact: str | None
    memo: str | None
    image_path: str | None
    pv_string_links: list[PvStringLinkOut] = Field(default_factory=list)


class DeviceSaveBody(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    device_type: str
    name: str
    manufacturer: str | None = None
    model_name: str | None = None
    serial_number: str | None = None
    capacity: float | None = None
    capacity_unit: str | None = None
    install_location: str | None = None
    install_date: str | None = None
    communication_type: str | None = None
    ip_address: str | None = None
    port: int | None = None
    slave_id: int | None = None
    protocol: str | None = None
    status: str = "NORMAL"
    is_active: bool = True
    warranty_start_date: str | None = None
    warranty_end_date: str | None = None
    vendor_name: str | None = None
    vendor_contact: str | None = None
    memo: str | None = None
    image_path: str | None = None
    pv_string_links: list[PvStringLinkSaveBody] = Field(default_factory=list)
