import type { APIResponse } from '@/http/type'

export type DeviceStatus = 'NORMAL' | 'WARNING' | 'FAULT' | 'MAINTENANCE' | 'UNKNOWN'
export type DeviceType =
    | 'INVERTER'
    | 'PCS'
    | 'ESS_BATTERY'
    | 'BATTERY_RACK'
    | 'BMS'
    | 'AC_PANEL'
    | 'GRID_METER'
    | 'LOAD_METER'
    | 'WEATHER_SENSOR'
    | 'SENSOR'
    | 'ETC'

export type DeviceItem = {
    id: number
    device_type: string
    name: string
    manufacturer: string | null
    model_name: string | null
    serial_number: string | null
    capacity: number | null
    capacity_unit: string | null
    install_location: string | null
    install_date: string | null
    communication_type: string | null
    ip_address: string | null
    port: number | null
    slave_id: number | null
    protocol: string | null
    status: string
    is_active: boolean
    warranty_start_date: string | null
    warranty_end_date: string | null
    vendor_name: string | null
    vendor_contact: string | null
    memo: string | null
    pv_string_links: PvStringLinkItem[]
}

export type DeviceSaveParams = Omit<DeviceItem, 'id'>

export type PvStringLinkItem = {
    id?: number
    inverter_device_id?: number
    pv_string_id: number
    pv_string_name?: string | null
    inverter_name?: string | null
    mppt_no: number | null
    channel_no: number | null
}

export type PvStringItem = {
    id: number
    name: string
    panel_count: number | null
    panel_capacity_kw: number | null
    rated_capacity_kw: number | null
    install_location: string | null
    status: string
    is_active: boolean
    memo: string | null
    inverter_device_id: number | null
    inverter_name: string | null
    mppt_no: number | null
    channel_no: number | null
}

export type PvStringSaveParams = Omit<
    PvStringItem,
    'id' | 'inverter_device_id' | 'inverter_name' | 'mppt_no' | 'channel_no'
>

export type DeviceListResponse = APIResponse<{
    list: DeviceItem[]
    totalCount: number
}>

export type DeviceDetailResponse = APIResponse<DeviceItem>

export type PvStringListResponse = APIResponse<{
    list: PvStringItem[]
    totalCount: number
}>

export type PvStringDetailResponse = APIResponse<PvStringItem>
