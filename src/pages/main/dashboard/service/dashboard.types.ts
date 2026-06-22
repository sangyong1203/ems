import type { APIResponse } from '@/http/type'

export type DashboardSummary = {
    refreshInterval: number
    project: {
        projectName: string
        siteName: string
        solarCapacityKw: number
        essCapacityKwh: number
        systemName: string
    }
    operationStatus: string
    updatedAt: string
    solar: {
        currentPowerKw: number
        todayGenerationKwh: number
        totalGenerationKwh: number
        inverterTotal: number
        inverterNormal: number
        inverterFault: number
    }
    ess: {
        soc: number
        soh: number
        mode: string
        chargePowerKw: number
        dischargePowerKw: number
        pcsStatus: string
        bmsStatus: string
        batteryTemperatureC: number
    }
    grid: {
        loadPowerKw: number
        exportPowerKw: number
        importPowerKw: number
    }
    alarms: {
        openCount: number
        recent: Array<{
            id: number
            severity: string
            alarmType: string
            message: string
            status: string
            occurredAt: string
        }>
    }
    maintenance: {
        recent: Array<{
            id: number
            maintenanceType: string
            title: string
            status: string
            maintenanceDate: string
            nextMaintenanceDate: string
            managerName: string
        }>
    }
}

export type DashboardSummaryResponse = APIResponse<DashboardSummary>

export type DashboardPowerFlow = {
    updatedAt: string
    policy: {
        essGridExportEnabled: boolean
    }
    nodes: {
        solar: { label: string; powerKw: number; status: string }
        ess: { label: string; chargeKw: number; dischargeKw: number; soc: number; status: string }
        load: { label: string; powerKw: number; status: string }
        grid: { label: string; exportKw: number; importKw: number; status: string }
    }
    flows: {
        solarToLoadKw: number
        solarToEssKw: number
        solarToGridKw: number
        essToLoadKw: number
        essToGridKw: number
        gridExportKw: number
        gridImportKw: number
    }
}

export type DashboardPowerFlowResponse = APIResponse<DashboardPowerFlow>

export type DashboardTelemetryPoint = {
    id: number
    device_id: number | null
    metric_key: string
    metric_value: number
    unit: string | null
    measured_at: string
}

export type DashboardTelemetryHistoryResponse = APIResponse<DashboardTelemetryPoint[]>
