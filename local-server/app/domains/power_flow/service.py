from sqlalchemy.orm import Session

from ..project.repository import get_project_config
from ..telemetry.repository import latest_site_map
from ..telemetry.service import telemetry_time, telemetry_value


def get_power_flow_overview(db: Session) -> dict:
    project = get_project_config(db)
    latest = latest_site_map(db)
    power_flow = calculate_power_flow(
        solar_power=telemetry_value(latest, "solar_power_kw"),
        load_power=telemetry_value(latest, "load_power_kw"),
        ess_charge=telemetry_value(latest, "ess_charge_kw"),
        ess_discharge=telemetry_value(latest, "ess_discharge_kw"),
        ess_soc=telemetry_value(latest, "ess_soc_avg"),
        ess_soh=telemetry_value(latest, "ess_soh_avg"),
        battery_temperature=telemetry_value(latest, "battery_temperature_avg_c"),
        ess_grid_export_enabled=False,
    )

    return {
        "refreshInterval": project.power_flow_refresh_interval if project else 5000,
        "updatedAt": telemetry_time(latest, "solar_power_kw"),
        **power_flow,
    }


def calculate_power_flow(
    solar_power: float,
    load_power: float,
    ess_charge: float,
    ess_discharge: float,
    ess_soc: float,
    ess_soh: float,
    battery_temperature: float,
    ess_grid_export_enabled: bool,
) -> dict:
    solar_to_load = min(solar_power, load_power)
    remaining_solar = max(solar_power - solar_to_load, 0)

    solar_to_ess = min(ess_charge, remaining_solar)
    remaining_solar = max(remaining_solar - solar_to_ess, 0)

    solar_to_grid = remaining_solar
    remaining_load = max(load_power - solar_to_load, 0)

    ess_to_load = min(ess_discharge, remaining_load)
    remaining_ess_discharge = max(ess_discharge - ess_to_load, 0)
    ess_to_grid = remaining_ess_discharge if ess_grid_export_enabled else 0
    grid_import = max(remaining_load - ess_to_load, 0)
    grid_export = solar_to_grid + ess_to_grid

    return {
        "policy": {
            "essGridExportEnabled": ess_grid_export_enabled,
        },
        "nodes": {
            "solar": {"label": "태양광", "powerKw": solar_power, "status": "GENERATING" if solar_power > 0 else "IDLE"},
            "ess": {
                "label": "ESS",
                "chargeKw": solar_to_ess,
                "dischargeKw": ess_to_load + ess_to_grid,
                "soc": ess_soc,
                "soh": ess_soh,
                "temperatureC": battery_temperature,
                "status": _ess_status(solar_to_ess, ess_discharge),
            },
            "load": {"label": "부하", "powerKw": load_power, "status": "CONSUMING"},
            "grid": {
                "label": "계통",
                "exportKw": grid_export,
                "importKw": grid_import,
                "status": _grid_status(grid_export, grid_import),
            },
        },
        "flows": {
            "solarToLoadKw": solar_to_load,
            "solarToEssKw": solar_to_ess,
            "solarToGridKw": solar_to_grid,
            "essToLoadKw": ess_to_load,
            "essToGridKw": ess_to_grid,
            "gridExportKw": grid_export,
            "gridImportKw": grid_import,
        },
    }


def _ess_status(solar_to_ess: float, ess_discharge: float) -> str:
    if solar_to_ess > 0:
        return "CHARGING"
    if ess_discharge > 0:
        return "DISCHARGING"
    return "STANDBY"


def _grid_status(grid_export: float, grid_import: float) -> str:
    if grid_export > 0:
        return "EXPORT"
    if grid_import > 0:
        return "IMPORT"
    return "BALANCED"
