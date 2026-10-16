import type { APIResponse } from '@/http/type'

// TrendTelemetryPoint 트렌드 계측 데이터 시계열 포인트
export type TrendTelemetryPoint = {
    id: number // 계측 데이터 ID
    device_id: number | null // 장치 ID
    metric_key: string // 계측 지표 키
    metric_value: number // 계측값
    unit: string | null // 단위
    measured_at: string // 계측 일시
}

// TrendOverview 트렌드 모니터링 종합 정보
export type TrendOverview = {
    refreshInterval: number // 자동 갱신 주기 (ms)
    project: {
        projectName: string // 프로젝트명
        siteName: string // 사이트명
        systemName: string // 시스템명
        solarCapacityKw: number // 태양광 설비 용량 (kW)
        essCapacityKwh: number // ESS 설비 용량 (kWh)
    }
    updatedAt: string | null // 데이터 갱신 일시
    summary: {
        solarPowerKw: number // 태양광 발전 전력 (kW)
        essSoc: number // ESS 충전율 (%)
        essChargeKw: number // ESS 충전 전력 (kW)
        essDischargeKw: number // ESS 방전 전력 (kW)
        batteryTemperatureC: number // 배터리 온도 (°C)
        loadPowerKw: number // 부하 소비 전력 (kW)
        gridExportKw: number // 계통 송전 전력 (kW)
        gridImportKw: number // 계통 수전 전력 (kW)
        gridStatus: string // 계통 연계 상태
    }
    history: {
        solar: TrendTelemetryPoint[] // 태양광 발전 시계열
        essSoc: TrendTelemetryPoint[] // ESS SOC 시계열
        essCharge: TrendTelemetryPoint[] // ESS 충전 전력 시계열
        essDischarge: TrendTelemetryPoint[] // ESS 방전 전력 시계열
        batteryTemperature: TrendTelemetryPoint[] // 배터리 온도 시계열
        load: TrendTelemetryPoint[] // 부하 소비 전력 시계열
        gridExport: TrendTelemetryPoint[] // 송전 전력 시계열
        gridImport: TrendTelemetryPoint[] // 수전 전력 시계열
    }
}

// TrendOverviewResponse 트렌드 모니터링 개요 응답
export type TrendOverviewResponse = APIResponse<TrendOverview>
