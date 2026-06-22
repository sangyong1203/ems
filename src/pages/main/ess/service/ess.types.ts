import type { APIResponse } from '@/http/type'

export type EssTelemetryPoint = {
    id: number
    device_id: number | null
    metric_key: string
    metric_value: number
    unit: string | null
    measured_at: string
}

export type EssDevice = {
    id: number | null
    name: string
    status: string
    manufacturer: string | null
    modelName: string | null
    capacity: number | null
    capacityUnit: string | null
}

export type EssSystemItem = {
    id: number
    name: string
    code: string
    status: string
    mode: string
    soc: number
    soh: number
    capacityKwh: number
    currentPowerKw: number
    isActive: boolean
    installLocation: string | null
}

export type EssSystemSummary = {
    total: number
    normal: number
    warning: number
    fault: number
    capacityKwh: number
    averageSoc: number
    currentPowerKw: number
}

export type EssOverview = {
    refreshInterval: number
    project: {
        projectName: string
        siteName: string
        systemName: string
        essCapacityKwh: number
    }
    system: {
        id: number
        name: string
        code: string
        status: string
        capacityKwh: number
        isActive: boolean
        installLocation: string | null
        memo: string | null
    }
    updatedAt: string | null
    summary: {
        soc: number
        soh: number
        mode: string
        chargePowerKw: number
        dischargePowerKw: number
        batteryVoltageV: number
        batteryCurrentA: number
        batteryTemperatureC: number
        todayChargeKwh: number
        todayDischargeKwh: number
        totalThroughputKwh: number
        netEnergyKwh: number
        pcsStatus: string
        bmsStatus: string
        batteryStatus: string
        systemStatus: string
    }
    limits: {
        socMin: number
        socMax: number
        temperatureWarningC: number
        temperatureFaultC: number
    }
    history: {
        charge: EssTelemetryPoint[]
        discharge: EssTelemetryPoint[]
        soc: EssTelemetryPoint[]
        temperature: EssTelemetryPoint[]
    }
    devices: {
        pcs: EssDevice
        bms: EssDevice
        battery: EssDevice
    }
}

export type EssSystemListResponse = APIResponse<{
    list: EssSystemItem[]
    totalCount: number
    summary: EssSystemSummary
}>

export type EssOverviewResponse = APIResponse<EssOverview>
