from sqlalchemy.orm import Session

from ..device.equipment_repository import get_equipment_summary
from ..ess.repository import first_ess_system
from ..project.repository import get_project_config
from ..telemetry.repository import (
    latest_site_map,
    latest_system_metric,
    site_history_by_metric,
    system_history_by_metric,
)
from ..telemetry.service import history_points, metric_time, metric_value, telemetry_value


# 사업장 계측과 첫 ESS 시스템의 최신값·최근 이력 24개를 트렌드 응답으로 구성합니다.
def get_trend_overview(db: Session) -> dict:
    project = get_project_config(db)
    equipment = get_equipment_summary(db)
    latest_site = latest_site_map(db)
    ess_system = first_ess_system(db)
    system_id = ess_system.id if ess_system else None

    # 첫 ESS가 있을 때만 시스템별 최신 계측값을 조회합니다.
    def system_latest(metric_key: str):
        return latest_system_metric(db, system_id, metric_key) if system_id is not None else None

    # 첫 ESS의 최근 지표 이력 24개를 조회하며 시스템이 없으면 빈 목록을 반환합니다.
    def system_history(metric_key: str):
        return system_history_by_metric(db, system_id, metric_key, 24) if system_id is not None else []

    ess_soc = system_latest("ess_soc")
    ess_charge = system_latest("ess_charge_kw")
    ess_discharge = system_latest("ess_discharge_kw")
    battery_temperature = system_latest("battery_temperature_c")
    grid_export = telemetry_value(latest_site, "grid_export_kw")
    grid_import = telemetry_value(latest_site, "grid_import_kw")

    return {
        "refreshInterval": project.trend_refresh_interval if project else 5000,
        "project": {
            "projectName": project.project_name if project else "",
            "siteName": project.site_name if project else "",
            "systemName": project.system_name if project else "Solar ESS EMS",
            "solarCapacityKw": equipment["capacities"]["solarOperatingKw"],
            "essCapacityKwh": equipment["capacities"]["essOperatingKwh"],
        },
        "updatedAt": metric_time(latest_site.get("solar_power_kw")),
        "summary": {
            "solarPowerKw": telemetry_value(latest_site, "solar_power_kw"),
            "essSoc": metric_value(ess_soc),
            "essChargeKw": metric_value(ess_charge),
            "essDischargeKw": metric_value(ess_discharge),
            "batteryTemperatureC": metric_value(battery_temperature),
            "loadPowerKw": telemetry_value(latest_site, "load_power_kw"),
            "gridExportKw": grid_export,
            "gridImportKw": grid_import,
            "gridStatus": _grid_status(grid_export, grid_import),
        },
        "history": {
            "solar": history_points(site_history_by_metric(db, "solar_power_kw", 24)),
            "essSoc": history_points(system_history("ess_soc")),
            "essCharge": history_points(system_history("ess_charge_kw")),
            "essDischarge": history_points(system_history("ess_discharge_kw")),
            "batteryTemperature": history_points(system_history("battery_temperature_c")),
            "load": history_points(site_history_by_metric(db, "load_power_kw", 24)),
            "gridExport": history_points(site_history_by_metric(db, "grid_export_kw", 24)),
            "gridImport": history_points(site_history_by_metric(db, "grid_import_kw", 24)),
        },
    }


# 송전을 우선 판정하고 수전·균형 순으로 계통 상태를 반환합니다.
def _grid_status(grid_export: float, grid_import: float) -> str:
    if grid_export > 0:
        return "EXPORT"
    if grid_import > 0:
        return "IMPORT"
    return "BALANCED"
