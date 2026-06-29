import type { APIResponse } from '@/http/type'

export type MaintenanceStatus = 'SCHEDULED' | 'IN_PROGRESS' | 'COMPLETED' | 'HOLD' | 'CANCELED'

export type MaintenanceItem = {
    id: number
    device_id: number | null
    alarm_id: number | null
    maintenance_type: string
    title: string
    description: string | null
    action_taken: string | null
    status: MaintenanceStatus | string
    maintenance_date: string | null
    next_maintenance_date: string | null
    manager_name: string | null
    cause: string | null
    before_status: string | null
    after_status: string | null
    contractor_name: string | null
    cost: number | null
    memo: string | null
    device_name: string | null
    device_type: string | null
}

export type MaintenanceSaveParams = {
    device_id: number | null
    alarm_id?: number | null
    maintenance_type: string
    title: string
    description: string | null
    cause: string | null
    action_taken: string | null
    before_status: string | null
    after_status: string | null
    status: MaintenanceStatus | string
    maintenance_date: string | null
    next_maintenance_date: string | null
    manager_name: string | null
    contractor_name: string | null
    cost: number | null
    memo: string | null
}

export type MaintenanceSearchParams = {
    keyword?: string
    deviceId?: number
    maintenanceType?: string
    status?: string
    dateFrom?: string
    dateTo?: string
}

export type MaintenanceDeviceOption = {
    id: number
    name: string
    device_type: string
}

export type MaintenanceListResponse = APIResponse<{
    list: MaintenanceItem[]
    totalCount: number
}>

export type MaintenanceDetailResponse = APIResponse<MaintenanceItem>

export type MaintenanceDeviceListResponse = APIResponse<{
    list: MaintenanceDeviceOption[]
    totalCount: number
}>
