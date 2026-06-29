from fastapi import HTTPException
from sqlalchemy.orm import Session

from .models import EssSystem
from .repository import first_ess_system, get_ess_system, list_battery_racks, list_ess_systems
from ..device.models import Device
from ..device.repository import get_device
from ..project.repository import get_project_config
from ..report.repository import latest_ess_daily_report
from ..telemetry.repository import history_by_metric, latest_metric, latest_system_metric, system_history_by_metric
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
    soc = metric_value(latest_system_metric(db, system.id, "ess_soc"))
    soh = metric_value(latest_system_metric(db, system.id, "ess_soh"))
    charge_kw = metric_value(latest_system_metric(db, system.id, "ess_charge_kw"))
    discharge_kw = metric_value(latest_system_metric(db, system.id, "ess_discharge_kw"))
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
    daily_report = latest_ess_daily_report(db, system.id)
    pcs = get_device(db, system.pcs_device_id) if system.pcs_device_id else None
    bms = get_device(db, system.bms_device_id) if system.bms_device_id else None
    battery = get_device(db, system.battery_device_id) if system.battery_device_id else None

    soc = latest_system_metric(db, system.id, "ess_soc")
    soh = latest_system_metric(db, system.id, "ess_soh")
    charge_power = latest_system_metric(db, system.id, "ess_charge_kw")
    discharge_power = latest_system_metric(db, system.id, "ess_discharge_kw")
    battery_voltage = latest_system_metric(db, system.id, "battery_voltage_v")
    battery_current = latest_system_metric(db, system.id, "battery_current_a")
    battery_temperature = latest_system_metric(db, system.id, "battery_temperature_c")

    charge_kw = metric_value(charge_power)
    discharge_kw = metric_value(discharge_power)
    system_status = _system_status(system, pcs, bms, battery)
    today_charge = round(float(daily_report.ess_charge_kwh if daily_report else 0), 1)
    today_discharge = round(float(daily_report.ess_discharge_kwh if daily_report else 0), 1)
    total_throughput = round(float(daily_report.total_throughput_kwh if daily_report else 0), 1)
    net_energy = round(float(daily_report.net_energy_kwh if daily_report else 0), 1)

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
            "totalThroughputKwh": total_throughput,
            "netEnergyKwh": net_energy,
            "pcsStatus": pcs.status if pcs else "UNKNOWN",
            "bmsStatus": bms.status if bms else "UNKNOWN",
            "batteryStatus": battery.status if battery else "UNKNOWN",
            "systemStatus": system_status,
        },
        "limits": {
            "socMin": 20,
            "socMax": 90,
            "voltageMinV": 760,
            "voltageMaxV": 880,
            "temperatureWarningC": 40,
            "temperatureFaultC": 50,
        },
        "history": {
            "charge": history_points(system_history_by_metric(db, system.id, "ess_charge_kw", 24)),
            "discharge": history_points(system_history_by_metric(db, system.id, "ess_discharge_kw", 24)),
            "soc": history_points(system_history_by_metric(db, system.id, "ess_soc", 24)),
            "voltage": history_points(system_history_by_metric(db, system.id, "battery_voltage_v", 24)),
            "temperature": history_points(system_history_by_metric(db, system.id, "battery_temperature_c", 24)),
            "rackTemperatures": _battery_rack_temperature_history(db, system),
        },
        "batteryRacks": _battery_rack_items(db, system),
        "devices": {
            "pcs": _device_to_dict(pcs),
            "bms": _device_to_dict(bms),
            "battery": _device_to_dict(battery),
        },
    }


def _battery_rack_temperature_history(db: Session, system: EssSystem) -> list[dict]:
    return [
        {
            "rackId": rack.id,
            "rackNo": link.rack_no,
            "rackName": rack.name,
            "data": history_points(history_by_metric(db, "battery_rack_avg_temperature_c", 24, rack.id)),
        }
        for link, rack in list_battery_racks(db, system.id)
    ]


def _battery_rack_items(db: Session, system: EssSystem) -> list[dict]:
    items: list[dict] = []
    for link, rack in list_battery_racks(db, system.id):
        metrics = {
            "soc": latest_metric(db, "battery_rack_soc", rack.id),
            "soh": latest_metric(db, "battery_rack_soh", rack.id),
            "voltage": latest_metric(db, "battery_rack_voltage_v", rack.id),
            "current": latest_metric(db, "battery_rack_current_a", rack.id),
            "averageTemperature": latest_metric(db, "battery_rack_avg_temperature_c", rack.id),
            "maxTemperature": latest_metric(db, "battery_rack_max_temperature_c", rack.id),
        }
        latest_items = [item for item in metrics.values() if item is not None]
        latest_item = max(latest_items, key=lambda item: item.measured_at) if latest_items else None
        max_temperature = metric_value(metrics["maxTemperature"])

        items.append(
            {
                "id": rack.id,
                "rackNo": link.rack_no,
                "name": rack.name,
                "status": _battery_rack_status(rack, max_temperature),
                "isActive": rack.is_active,
                "capacityKwh": round(float(rack.capacity or 0), 1),
                "soc": metric_value(metrics["soc"]),
                "soh": metric_value(metrics["soh"]),
                "voltageV": metric_value(metrics["voltage"]),
                "currentA": metric_value(metrics["current"]),
                "averageTemperatureC": metric_value(metrics["averageTemperature"]),
                "maxTemperatureC": max_temperature,
                "updatedAt": metric_time(latest_item),
            }
        )
    return items


def _battery_rack_status(rack: Device, max_temperature: float) -> str:
    if not rack.is_active:
        return "INACTIVE"
    if rack.status == "FAULT" or max_temperature >= 50:
        return "FAULT"
    if rack.status in {"WARNING", "UNKNOWN"} or max_temperature >= 40:
        return "WARNING"
    return "NORMAL"


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
