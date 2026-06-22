from ...shared.schemas import OrmModel


class DailyReportOut(OrmModel):
    id: int
    report_date: str
    generation_kwh: float
    ess_charge_kwh: float
    ess_discharge_kwh: float
    grid_export_kwh: float
    grid_import_kwh: float
    alarm_count: int
    maintenance_count: int


class ReportSummaryOut(OrmModel):
    date_from: str
    date_to: str
    day_count: int
    generation_kwh: float
    ess_charge_kwh: float
    ess_discharge_kwh: float
    grid_export_kwh: float
    grid_import_kwh: float
    alarm_count: int
    maintenance_count: int


class ReportStatisticsPointOut(OrmModel):
    date: str
    generation_kwh: float
    temperature_c: float
    ess_charge_kwh: float
    ess_discharge_kwh: float
    ess_soc: float
    grid_export_kwh: float
    grid_import_kwh: float
    load_total_kwh: float
    load_solar_kwh: float
    load_grid_kwh: float
    load_ess_kwh: float
    self_reliance_rate: float
    alarm_count: int


class AlarmSeverityDistributionOut(OrmModel):
    severity: str
    count: int


class AlarmDeviceDistributionOut(OrmModel):
    device_name: str
    count: int


class ReportStatisticsOut(OrmModel):
    summary: ReportSummaryOut
    series: list[ReportStatisticsPointOut]
    alarm_severity_distribution: list[AlarmSeverityDistributionOut]
    alarm_by_device: list[AlarmDeviceDistributionOut]
