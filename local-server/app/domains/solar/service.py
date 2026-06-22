from typing import TypedDict

from sqlalchemy.orm import Session

from ..device.models import Device
from ..device.equipment_repository import get_equipment_summary
from ..device.repository import list_devices_by_type
from ..project.repository import get_project_config
from ..telemetry.repository import history_by_metric, latest_metric
from ..telemetry.service import history_points, metric_time, metric_value


class InverterItem(TypedDict):
    id: int
    name: str
    status: str
    isActive: bool
    capacityKw: float
    capacityUnit: str | None
    currentPowerKw: float
    capacityRatio: float
    updatedAt: str | None


def get_solar_overview(db: Session) -> dict:
    project = get_project_config(db)
    inverters = list_devices_by_type(db, "INVERTER", order_by_id=True)
    equipment = get_equipment_summary(db)

    current_power = latest_metric(db, "solar_power_kw")
    today_generation = latest_metric(db, "solar_today_kwh")
    total_generation = latest_metric(db, "solar_total_kwh")
    solar_installed_capacity_kw = equipment["capacities"]["solarInstalledKw"]
    solar_operating_capacity_kw = equipment["capacities"]["solarOperatingKw"]

    ordered_history = history_points(history_by_metric(db, "solar_power_kw", 24))
    history_values = [float(item["metric_value"]) for item in ordered_history]
    peak_power_kw = max(history_values, default=0)
    average_power_kw = sum(history_values) / len(history_values) if history_values else 0

    inverter_items = [_inverter_item(db, inverter) for inverter in inverters]
    active_inverter_items = [item for item in inverter_items if item["isActive"]]
    inverter_total = len(active_inverter_items)
    inverter_normal = len([item for item in active_inverter_items if item["status"] == "NORMAL"])

    current_power_kw = metric_value(current_power)

    return {
        "refreshInterval": project.solar_refresh_interval if project else 5000,
        "project": {
            "projectName": project.project_name if project else "",
            "siteName": project.site_name if project else "",
            "systemName": project.system_name if project else "Solar ESS EMS",
            "solarCapacityKw": solar_operating_capacity_kw,
            "solarInstalledCapacityKw": solar_installed_capacity_kw,
            "solarOperatingCapacityKw": solar_operating_capacity_kw,
        },
        "updatedAt": metric_time(current_power),
        "summary": {
            "currentPowerKw": current_power_kw,
            "todayGenerationKwh": metric_value(today_generation),
            "totalGenerationKwh": metric_value(total_generation),
            "capacityRatio": round((current_power_kw / solar_operating_capacity_kw) * 100, 1)
            if solar_operating_capacity_kw
            else 0,
            "peakPowerKw": round(peak_power_kw, 1),
            "averagePowerKw": round(average_power_kw, 1),
            "inverterTotal": inverter_total,
            "inverterNormal": inverter_normal,
            "inverterWarning": inverter_total - inverter_normal,
        },
        "history": ordered_history,
        "inverters": inverter_items,
    }


def _inverter_item(db: Session, inverter: Device) -> InverterItem:
    inverter_power = latest_metric(db, "inverter_power_kw", inverter.id)
    capacity_kw = float(inverter.capacity or 0)
    current_kw = metric_value(inverter_power)
    return {
        "id": inverter.id,
        "name": inverter.name,
        "status": inverter.status,
        "isActive": inverter.is_active,
        "capacityKw": capacity_kw,
        "capacityUnit": inverter.capacity_unit,
        "currentPowerKw": current_kw,
        "capacityRatio": round((current_kw / capacity_kw) * 100, 1) if capacity_kw else 0,
        "updatedAt": metric_time(inverter_power),
    }
