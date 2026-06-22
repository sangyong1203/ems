from fastapi import HTTPException
from sqlalchemy.orm import Session

from .models import EssSystem
from .repository import first_ess_system, get_ess_system, list_ess_systems
from ..device.models import Device
from ..device.repository import first_device_by_type, get_device
from ..project.repository import get_project_config
from ..report.repository import latest_daily_report
from ..telemetry.models import TelemetryHistory, TelemetryLatest
from ..telemetry.repository import history_by_metric, history_by_metric_any_device, latest_metric, latest_metric_any_device
from ..telemetry.service import history_points, metric_time, metric_value


def get_ess_systems(db: Session) -> dict:
    systems = list_ess_systems(db)
    items = [_system_list_item(db, system) for system in systems]
    normal_count = len([item for item in items if item["status"] == "NORMAL"])
    warning_count = len([item for item in items if item["status"] == "WARNING"])
    fault_count = len([item for item in items if item["status"] == "FAULT"])

    return {
        "list": items,
        "totalCount": len(items),
        "summary": {
            "total": len(items),
            "normal": normal_count,
            "warning": warning_count,
            "fault": fault_count,
            "capacityKwh": round(sum(item["capacityKwh"] for item in items), 1),
            "averageSoc": _average([item["soc"] for item in items]),
            "currentPowerKw": round(sum(item["currentPowerKw"] for item in items), 1),
        },
    }


def get_ess_overview(db: Session) -> dict:
    system = first_ess_system(db)
    if system is None:
        raise HTTPException(status_code=404, detail="ESS system not found")
    return _build_ess_overview(db, system)


def get_ess_system_overview(db: Session, system_id: int) -> dict:
    system = get_ess_system(db, system_id)
    if system is None:
        raise HTTPException(status_code=404, detail="ESS system not found")
    return _build_ess_overview(db, system)


def _system_list_item(db: Session, system: EssSystem) -> dict:
    pcs = get_device(db, system.pcs_device_id) if system.pcs_device_id else None
    bms = get_device(db, system.bms_device_id) if system.bms_device_id else None
    battery = get_device(db, system.battery_device_id) if system.battery_device_id else None
    soc = _metric_value_with_fallback(db, "ess_soc", _metric_device_id(bms, battery))
    soh = _metric_value_with_fallback(db, "ess_soh", _metric_device_id(bms, battery))
    charge_kw = _metric_value_with_fallback(db, "ess_charge_kw", _metric_device_id(pcs))
    discharge_kw = _metric_value_with_fallback(db, "ess_discharge_kw", _metric_device_id(pcs))
    current_power = charge_kw or discharge_kw

    return {
        "id": system.id,
        "name": system.name,
        "code": system.code,
        "status": _system_status(system, pcs, bms, battery),
        "mode": _ess_mode(charge_kw, discharge_kw),
        "soc": soc,
        "soh": soh,
        "capacityKwh": round(float(system.capacity_kwh or 0), 1),
        "currentPowerKw": current_power,
        "isActive": system.is_active,
        "installLocation": system.install_location,
    }


def _build_ess_overview(db: Session, system: EssSystem) -> dict:
    project = get_project_config(db)
    daily_report = latest_daily_report(db)
    pcs = get_device(db, system.pcs_device_id) if system.pcs_device_id else first_device_by_type(db, "PCS")
    bms = get_device(db, system.bms_device_id) if system.bms_device_id else first_device_by_type(db, "BMS")
    battery = (
        get_device(db, system.battery_device_id) if system.battery_device_id else first_device_by_type(db, "ESS_BATTERY")
    )

    pcs_device_id = _metric_device_id(pcs)
    battery_metric_device_id = _metric_device_id(bms, battery)

    soc = _latest_metric_with_fallback(db, "ess_soc", battery_metric_device_id)
    soh = _latest_metric_with_fallback(db, "ess_soh", battery_metric_device_id)
    charge_power = _latest_metric_with_fallback(db, "ess_charge_kw", pcs_device_id)
    discharge_power = _latest_metric_with_fallback(db, "ess_discharge_kw", pcs_device_id)
    battery_voltage = _latest_metric_with_fallback(db, "battery_voltage_v", battery_metric_device_id)
    battery_current = _latest_metric_with_fallback(db, "battery_current_a", battery_metric_device_id)
    battery_temperature = _latest_metric_with_fallback(db, "battery_temperature_c", battery_metric_device_id)

    charge_kw = metric_value(charge_power)
    discharge_kw = metric_value(discharge_power)
    system_status = _system_status(system, pcs, bms, battery)
    today_charge = round(float(daily_report.ess_charge_kwh if daily_report else 0), 1)
    today_discharge = round(float(daily_report.ess_discharge_kwh if daily_report else 0), 1)

    return {
        "refreshInterval": project.ess_refresh_interval if project else 5000,
        "project": {
            "projectName": project.project_name if project else "",
            "siteName": project.site_name if project else "",
            "systemName": project.system_name if project else "Solar ESS EMS",
            "essCapacityKwh": round(float(system.capacity_kwh or 0), 1),
        },
        "system": {
            "id": system.id,
            "name": system.name,
            "code": system.code,
            "status": system_status,
            "capacityKwh": round(float(system.capacity_kwh or 0), 1),
            "isActive": system.is_active,
            "installLocation": system.install_location,
            "memo": system.memo,
        },
        "updatedAt": metric_time(soc),
        "summary": {
            "soc": metric_value(soc),
            "soh": metric_value(soh),
            "mode": _ess_mode(charge_kw, discharge_kw),
            "chargePowerKw": charge_kw,
            "dischargePowerKw": discharge_kw,
            "batteryVoltageV": metric_value(battery_voltage),
            "batteryCurrentA": metric_value(battery_current),
            "batteryTemperatureC": metric_value(battery_temperature),
            "todayChargeKwh": today_charge,
            "todayDischargeKwh": today_discharge,
            "totalThroughputKwh": round(today_charge + today_discharge, 1),
            "netEnergyKwh": round(today_charge - today_discharge, 1),
            "pcsStatus": pcs.status if pcs else "UNKNOWN",
            "bmsStatus": bms.status if bms else "UNKNOWN",
            "batteryStatus": battery.status if battery else "UNKNOWN",
            "systemStatus": system_status,
        },
        "limits": {
            "socMin": 20,
            "socMax": 90,
            "temperatureWarningC": 40,
            "temperatureFaultC": 50,
        },
        "history": {
            "charge": _history_points_with_fallback(db, "ess_charge_kw", 24, pcs_device_id),
            "discharge": _history_points_with_fallback(db, "ess_discharge_kw", 24, pcs_device_id),
            "soc": _history_points_with_fallback(db, "ess_soc", 24, battery_metric_device_id),
            "temperature": _history_points_with_fallback(db, "battery_temperature_c", 24, battery_metric_device_id),
        },
        "devices": {
            "pcs": _device_to_dict(pcs),
            "bms": _device_to_dict(bms),
            "battery": _device_to_dict(battery),
        },
    }


def _metric_device_id(*devices: Device | None) -> int | None:
    for device in devices:
        if device is not None:
            return device.id
    return None


def _latest_metric_with_fallback(db: Session, metric_key: str, device_id: int | None) -> TelemetryLatest | None:
    item = latest_metric(db, metric_key, device_id)
    if item is not None:
        return item
    item = latest_metric(db, metric_key)
    if item is not None:
        return item
    return latest_metric_any_device(db, metric_key)


def _metric_value_with_fallback(db: Session, metric_key: str, device_id: int | None) -> float:
    return metric_value(_latest_metric_with_fallback(db, metric_key, device_id))


def _history_points_with_fallback(db: Session, metric_key: str, limit: int, device_id: int | None) -> list[dict]:
    items = history_by_metric(db, metric_key, limit, device_id)
    if not items:
        items = history_by_metric(db, metric_key, limit)
    if not items:
        items = history_by_metric_any_device(db, metric_key, limit)
    return history_points(items)


def _ess_mode(charge_kw: float, discharge_kw: float) -> str:
    if charge_kw > 0:
        return "CHARGING"
    if discharge_kw > 0:
        return "DISCHARGING"
    return "STANDBY"


def _system_status(system: EssSystem, pcs: Device | None, bms: Device | None, battery: Device | None) -> str:
    statuses = [system.status, pcs.status if pcs else "UNKNOWN", bms.status if bms else "UNKNOWN", battery.status if battery else "UNKNOWN"]
    if "FAULT" in statuses:
        return "FAULT"
    if "WARNING" in statuses or "UNKNOWN" in statuses:
        return "WARNING"
    return "NORMAL"


def _average(values: list[float]) -> float:
    if not values:
        return 0
    return round(sum(values) / len(values), 1)


def _device_to_dict(device: Device | None) -> dict:
    if not device:
        return {
            "id": None,
            "name": "-",
            "status": "UNKNOWN",
            "manufacturer": None,
            "modelName": None,
            "capacity": None,
            "capacityUnit": None,
        }

    return {
        "id": device.id,
        "name": device.name,
        "status": device.status,
        "manufacturer": device.manufacturer,
        "modelName": device.model_name,
        "capacity": device.capacity,
        "capacityUnit": device.capacity_unit,
    }
