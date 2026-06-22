import type { APIResponse } from '@/http/type'

export type SolarTelemetryPoint = {
    id: number
    device_id: number | null
    metric_key: string
    metric_value: number
    unit: string | null
    measured_at: string
}

export type SolarInverter = {
    id: number
    name: string
    status: string
    isActive: boolean
    capacityKw: number
    capacityUnit: string | null
    currentPowerKw: number
    capacityRatio: number
    updatedAt: string | null
}

export type SolarOverview = {
    refreshInterval: number
    project: {
        projectName: string
        siteName: string
        systemName: string
        solarCapacityKw: number
        solarInstalledCapacityKw: number
        solarOperatingCapacityKw: number
    }
    updatedAt: string | null
    summary: {
        currentPowerKw: number
        todayGenerationKwh: number
        totalGenerationKwh: number
        capacityRatio: number
        peakPowerKw: number
        averagePowerKw: number
        inverterTotal: number
        inverterNormal: number
        inverterWarning: number
    }
    history: SolarTelemetryPoint[]
    inverters: SolarInverter[]
}

export type SolarOverviewResponse = APIResponse<SolarOverview>
