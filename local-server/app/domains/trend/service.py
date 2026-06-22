from sqlalchemy.orm import Session

from ..device.equipment_repository import get_equipment_summary
from ..project.repository import get_project_config
from ..telemetry.repository import history_by_metric, latest_map
from ..telemetry.service import history_points, telemetry_time, telemetry_value


def get_trend_overview(db: Session) -> dict:
    project = get_project_config(db)
    equipment = get_equipment_summary(db)
    latest = latest_map(db)
    grid_export = telemetry_value(latest, "grid_export_kw")
    grid_import = telemetry_value(latest, "grid_import_kw")

    return {
        "refreshInterval": project.trend_refresh_interval if project else 5000,
        "project": {
            "projectName": project.project_name if project else "",
            "siteName": project.site_name if project else "",
            "systemName": project.system_name if project else "Solar ESS EMS",
            "solarCapacityKw": equipment["capacities"]["solarOperatingKw"],
            "essCapacityKwh": equipment["capacities"]["essOperatingKwh"],
        },
        "updatedAt": telemetry_time(latest, "solar_power_kw"),
        "summary": {
            "solarPowerKw": telemetry_value(latest, "solar_power_kw"),
            "essSoc": telemetry_value(latest, "ess_soc"),
            "essChargeKw": telemetry_value(latest, "ess_charge_kw"),
            "essDischargeKw": telemetry_value(latest, "ess_discharge_kw"),
            "batteryTemperatureC": telemetry_value(latest, "battery_temperature_c"),
            "loadPowerKw": telemetry_value(latest, "load_power_kw"),
            "gridExportKw": grid_export,
            "gridImportKw": grid_import,
            "gridStatus": _grid_status(grid_export, grid_import),
        },
        "history": {
            "solar": history_points(history_by_metric(db, "solar_power_kw", 24)),
            "essSoc": history_points(history_by_metric(db, "ess_soc", 24)),
            "essCharge": history_points(history_by_metric(db, "ess_charge_kw", 24)),
            "essDischarge": history_points(history_by_metric(db, "ess_discharge_kw", 24)),
            "batteryTemperature": history_points(history_by_metric(db, "battery_temperature_c", 24)),
            "load": history_points(history_by_metric(db, "load_power_kw", 24)),
            "gridExport": history_points(history_by_metric(db, "grid_export_kw", 24)),
            "gridImport": history_points(history_by_metric(db, "grid_import_kw", 24)),
        },
    }


def _grid_status(grid_export: float, grid_import: float) -> str:
    if grid_export > 0:
        return "EXPORT"
    if grid_import > 0:
        return "IMPORT"
    return "BALANCED"
