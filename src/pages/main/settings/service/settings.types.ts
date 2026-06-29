import type { APIResponse } from '@/http/type'

export type DeviceCounts = {
    INVERTER: number
    PCS: number
    ESS_BATTERY: number
    BATTERY_RACK: number
    BMS: number
    AC_PANEL: number
    METER: number
}

export type EquipmentCapacities = {
    solarInstalledKw: number
    solarOperatingKw: number
    essInstalledKwh: number
    essOperatingKwh: number
}

export type ProjectConfig = {
    id: number
    project_name: string
    site_name: string
    location: string | null
    customer_name: string | null
    contractor_name: string | null
    solar_capacity_kw: number
    ess_capacity_kwh: number
    system_name: string
    background_image_path: string | null
    logo_image_path: string | null
    data_refresh_interval: number
    dashboard_refresh_interval: number
    solar_refresh_interval: number
    ess_refresh_interval: number
    power_flow_refresh_interval: number
    trend_refresh_interval: number
    device_counts: DeviceCounts
    active_device_counts: DeviceCounts
    equipment_capacities: EquipmentCapacities
}

export type ProjectConfigSavePayload = Omit<
    ProjectConfig,
    'id' | 'device_counts' | 'active_device_counts' | 'equipment_capacities'
>
export type ProjectConfigResponse = APIResponse<ProjectConfig>
export type SimulatorActionResponse = APIResponse<{
    generatedAt?: string
    dayCount?: number
    alarmCount?: number
    maintenanceCount?: number
    reset?: boolean
}>
