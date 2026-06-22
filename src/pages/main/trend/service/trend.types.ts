import type { APIResponse } from '@/http/type'

export type TrendTelemetryPoint = {
    id: number
    device_id: number | null
    metric_key: string
    metric_value: number
    unit: string | null
    measured_at: string
}

export type TrendOverview = {
    refreshInterval: number
    project: {
        projectName: string
        siteName: string
        systemName: string
        solarCapacityKw: number
        essCapacityKwh: number
    }
    updatedAt: string | null
    summary: {
        solarPowerKw: number
        essSoc: number
        essChargeKw: number
        essDischargeKw: number
        batteryTemperatureC: number
        loadPowerKw: number
        gridExportKw: number
        gridImportKw: number
        gridStatus: string
    }
    history: {
        solar: TrendTelemetryPoint[]
        essSoc: TrendTelemetryPoint[]
        essCharge: TrendTelemetryPoint[]
        essDischarge: TrendTelemetryPoint[]
        batteryTemperature: TrendTelemetryPoint[]
        load: TrendTelemetryPoint[]
        gridExport: TrendTelemetryPoint[]
        gridImport: TrendTelemetryPoint[]
    }
}

export type TrendOverviewResponse = APIResponse<TrendOverview>
