from sqlalchemy.orm import Session

from ..device.models import Device
from ..alarm.repository import count_open_alarms, recent_alarms
from ..device.equipment_repository import get_equipment_summary
from ..device.repository import list_all_devices
from ..ess.repository import list_ess_systems
from ..maintenance.repository import recent_maintenance
from ..power_flow.service import get_power_flow_overview
from ..project.repository import get_project_config
from ..report.repository import latest_daily_report
from ..telemetry.repository import latest_site_map, latest_system_metric
from ..telemetry.service import metric_value, telemetry_time, telemetry_value


def get_dashboard_summary(db: Session) -> dict:
    project = get_project_config(db)
    latest = latest_site_map(db)
    devices = list_all_devices(db)
    equipment = get_equipment_summary(db)
    daily_report = latest_daily_report(db)

    inverter_total = len([item for item in devices if item.device_type == "INVERTER" and item.is_active])
    inverter_normal = len(
        [item for item in devices if item.device_type == "INVERTER" and item.is_active and item.status == "NORMAL"]
    )
    inverter_fault = inverter_total - inverter_normal
    average_ess_soc = _average_ess_soc(db)

    ess_charge_kw = telemetry_value(latest, "ess_charge_kw")
    ess_discharge_kw = telemetry_value(latest, "ess_discharge_kw")
    if ess_charge_kw > 0:
        ess_mode = "CHARGING"
    elif ess_discharge_kw > 0:
        ess_mode = "DISCHARGING"
    else:
        ess_mode = "STANDBY"

    return {
        "refreshInterval": project.dashboard_refresh_interval if project else 5000,
        "project": {
            "projectName": project.project_name if project else "",
            "siteName": project.site_name if project else "",
            "solarCapacityKw": equipment["capacities"]["solarOperatingKw"],
            "essCapacityKwh": equipment["capacities"]["essOperatingKwh"],
            "systemName": project.system_name if project else "Solar ESS EMS",
        },
        "operationStatus": "NORMAL" if count_open_alarms(db) == 0 else "WARNING",
        "updatedAt": telemetry_time(latest, "solar_power_kw"),
        "solar": {
            "currentPowerKw": telemetry_value(latest, "solar_power_kw"),
            "todayGenerationKwh": daily_report.generation_kwh if daily_report else 0,
            "totalGenerationKwh": telemetry_value(latest, "solar_total_kwh"),
            "inverterTotal": inverter_total,
            "inverterNormal": inverter_normal,
            "inverterFault": inverter_fault,
        },
        "ess": {
            "soc": average_ess_soc,
            "soh": _average_ess_system_metric(db, "ess_soh"),
            "mode": ess_mode,
            "chargePowerKw": ess_charge_kw,
            "dischargePowerKw": ess_discharge_kw,
            "pcsStatus": _status_for_device(devices, "PCS"),
            "bmsStatus": _status_for_device(devices, "BMS"),
            "batteryTemperatureC": telemetry_value(latest, "battery_temperature_avg_c"),
        },
        "grid": {
            "loadPowerKw": telemetry_value(latest, "load_power_kw"),
            "exportPowerKw": telemetry_value(latest, "grid_export_kw"),
            "importPowerKw": telemetry_value(latest, "grid_import_kw"),
        },
        "alarms": {
            "openCount": count_open_alarms(db),
            "recent": [_alarm_to_dict(item) for item in recent_alarms(db, 3)],
        },
        "maintenance": {
            "recent": [_maintenance_to_dict(item) for item in recent_maintenance(db, 3)],
        },
    }


def get_power_flow(db: Session) -> dict:
    return get_power_flow_overview(db)


def get_recent_alarm_ids(db: Session) -> list[int]:
    return [item.id for item in recent_alarms(db)]


def get_recent_maintenance_ids(db: Session) -> list[int]:
    return [item.id for item in recent_maintenance(db)]


def _status_for_device(devices: list[Device], device_type: str) -> str:
    device = next((item for item in devices if item.device_type == device_type), None)
    return device.status if device else "UNKNOWN"


def _average_ess_soc(db: Session) -> float:
    return _average_ess_system_metric(db, "ess_soc")


def _average_ess_system_metric(db: Session, metric_key: str) -> float:
    systems = list_ess_systems(db)
    if not systems:
        return 0

    values: list[float] = []
    for system in systems:
        values.append(metric_value(latest_system_metric(db, system.id, metric_key)))

    return round(sum(values) / len(values), 1) if values else 0


def _alarm_to_dict(item) -> dict:
    return {
        "id": item.id,
        "severity": item.severity,
        "alarmType": item.alarm_type,
        "message": item.message,
        "status": item.status,
        "occurredAt": item.occurred_at.strftime("%Y-%m-%d %H:%M:%S"),
    }


def _maintenance_to_dict(item) -> dict:
    return {
        "id": item.id,
        "maintenanceType": item.maintenance_type,
        "title": item.title,
        "status": item.status,
        "maintenanceDate": item.maintenance_date,
        "nextMaintenanceDate": item.next_maintenance_date,
        "managerName": item.manager_name,
    }
