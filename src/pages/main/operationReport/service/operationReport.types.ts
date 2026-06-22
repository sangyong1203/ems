import type { APIResponse } from '@/http/type'

export type DailyReport = {
    id: number
    report_date: string
    generation_kwh: number
    ess_charge_kwh: number
    ess_discharge_kwh: number
    grid_export_kwh: number
    grid_import_kwh: number
    alarm_count: number
    maintenance_count: number
}

export type DailyReportResponse = APIResponse<DailyReport | null>

export type ReportSummary = {
    date_from: string
    date_to: string
    day_count: number
    generation_kwh: number
    ess_charge_kwh: number
    ess_discharge_kwh: number
    grid_export_kwh: number
    grid_import_kwh: number
    alarm_count: number
    maintenance_count: number
}

export type ReportSummaryResponse = APIResponse<ReportSummary | null>

export type ReportStatisticsPoint = {
    date: string
    generation_kwh: number
    temperature_c: number
    ess_charge_kwh: number
    ess_discharge_kwh: number
    ess_soc: number
    grid_export_kwh: number
    grid_import_kwh: number
    load_total_kwh: number
    load_solar_kwh: number
    load_grid_kwh: number
    load_ess_kwh: number
    self_reliance_rate: number
    alarm_count: number
}

export type AlarmSeverityDistribution = {
    severity: string
    count: number
}

export type AlarmDeviceDistribution = {
    device_name: string
    count: number
}

export type ReportStatistics = {
    summary: ReportSummary
    series: ReportStatisticsPoint[]
    alarm_severity_distribution: AlarmSeverityDistribution[]
    alarm_by_device: AlarmDeviceDistribution[]
}

export type ReportStatisticsResponse = APIResponse<ReportStatistics | null>
