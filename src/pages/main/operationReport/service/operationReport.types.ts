import type { APIResponse } from '@/http/type'

// DailyReport 일간 운영 보고서 레코드
export type DailyReport = {
    id: number // 보고서 ID
    report_date: string // 보고 일자 (YYYY-MM-DD)
    generation_kwh: number // 발전량 (kWh)
    ess_charge_kwh: number // ESS 충전량 (kWh)
    ess_discharge_kwh: number // ESS 방전량 (kWh)
    grid_export_kwh: number // 계통 송전량 (kWh)
    grid_import_kwh: number // 계통 수전량 (kWh)
    alarm_count: number // 알람 발생 건수
    maintenance_count: number // 정비 건수
}

// DailyReportResponse 일간 운영 보고서 응답
export type DailyReportResponse = APIResponse<DailyReport | null>

// ReportSummary 기간 운영 보고서 종합 요약
export type ReportSummary = {
    date_from: string // 조회 시작일 (YYYY-MM-DD)
    date_to: string // 조회 종료일 (YYYY-MM-DD)
    day_count: number // 집계 일수
    generation_kwh: number // 총 발전량 (kWh)
    ess_charge_kwh: number // 총 충전량 (kWh)
    ess_discharge_kwh: number // 총 방전량 (kWh)
    grid_export_kwh: number // 총 송전량 (kWh)
    grid_import_kwh: number // 총 수전량 (kWh)
    alarm_count: number // 총 알람 발생 건수
    maintenance_count: number // 총 정비 건수
}

// ReportSummaryResponse 기간 운영 보고서 요약 응답
export type ReportSummaryResponse = APIResponse<ReportSummary | null>

// ReportStatisticsPoint 일별 운영 통계 시계열 포인트
export type ReportStatisticsPoint = {
    date: string // 일자 (YYYY-MM-DD)
    generation_kwh: number // 발전량 (kWh)
    temperature_c: number // 평균 기온 (°C)
    ess_charge_kwh: number // 충전량 (kWh)
    ess_discharge_kwh: number // 방전량 (kWh)
    ess_soc: number // 평균 SOC (%)
    grid_export_kwh: number // 송전량 (kWh)
    grid_import_kwh: number // 수전량 (kWh)
    load_total_kwh: number // 총 부하 소비량 (kWh)
    load_solar_kwh: number // 태양광 직접 소비량 (kWh)
    load_grid_kwh: number // 계통 수전 소비량 (kWh)
    load_ess_kwh: number // ESS 방전 소비량 (kWh)
    self_reliance_rate: number // 에너지 자립률 (%)
    alarm_count: number // 알람 수
}

// AlarmSeverityDistribution 알람 심각도별 발생 분포
export type AlarmSeverityDistribution = {
    severity: string // 심각도 (CRITICAL, WARNING, INFO)
    count: number // 발생 건수
}

// AlarmDeviceDistribution 장치별 알람 발생 분포
export type AlarmDeviceDistribution = {
    device_name: string // 장치명
    count: number // 발생 건수
}

// ReportStatistics 운영 보고서 종합 통계
export type ReportStatistics = {
    summary: ReportSummary // 기간 요약
    series: ReportStatisticsPoint[] // 일별 통계 시계열
    alarm_severity_distribution: AlarmSeverityDistribution[] // 심각도별 분포
    alarm_by_device: AlarmDeviceDistribution[] // 장치별 분포
}

// ReportStatisticsResponse 운영 보고서 종합 통계 응답
export type ReportStatisticsResponse = APIResponse<ReportStatistics | null>
