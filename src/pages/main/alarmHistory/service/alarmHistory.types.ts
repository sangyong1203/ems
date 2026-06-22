import type { APIResponse } from '@/http/type'

export type AlarmSeverity = 'INFO' | 'WARNING' | 'CRITICAL'
export type AlarmStatus = 'OPEN' | 'ACKED' | 'RESOLVED'
export type AlarmActionStatus = 'OPEN' | 'ACKED' | 'SCHEDULED' | 'IN_PROGRESS' | 'COMPLETED' | 'HOLD' | 'CANCELED'

export type AlarmItem = {
    id: number
    device_id: number | null
    severity: AlarmSeverity | string
    alarm_type: string
    message: string
    status: AlarmStatus | string
    occurred_at: string
    acknowledged_at: string | null
    resolved_at: string | null
    device_name: string | null
    device_type: string | null
    maintenance_id: number | null
    maintenance_status: string | null
    maintenance_title: string | null
    maintenance_date: string | null
}

export type AlarmSearchParams = {
    keyword?: string
    deviceId?: number | null
    severity?: string
    alarmType?: string
    status?: string
    dateFrom?: string
    dateTo?: string
}

export type AlarmDeviceOption = {
    id: number
    name: string
    device_type: string
}

export type AlarmListResponse = APIResponse<{
    list: AlarmItem[]
    totalCount: number
}>

export type AlarmDetailResponse = APIResponse<AlarmItem>

export type AlarmDeviceListResponse = APIResponse<{
    list: AlarmDeviceOption[]
    totalCount: number
}>
