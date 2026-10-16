import type { APIResponse } from '@/http/type'

// DeviceStatus 장비 운영 상태
export type DeviceStatus = 'NORMAL' | 'WARNING' | 'FAULT' | 'MAINTENANCE' | 'UNKNOWN'

// DeviceType 장비 유형
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

// DeviceItem 등록 장비 상세 정보
export type DeviceItem = {
    id: number // 장비 ID
    device_type: string // 장비 유형
    name: string // 장비명
    manufacturer: string | null // 제조사
    model_name: string | null // 모델명
    serial_number: string | null // 시리얼 번호
    capacity: number | null // 정격 용량
    capacity_unit: string | null // 용량 단위
    install_location: string | null // 설치 위치
    install_date: string | null // 설치일 (YYYY-MM-DD)
    communication_type: string | null // 통신 방식
    ip_address: string | null // IP 주소
    port: number | null // 포트 번호
    slave_id: number | null // Slave ID
    protocol: string | null // 통신 프로토콜
    status: string // 운영 상태
    is_active: boolean // 운영 활성화 여부
    warranty_start_date: string | null // 보증 시작일
    warranty_end_date: string | null // 보증 만료일
    vendor_name: string | null // 관리 업체명
    vendor_contact: string | null // 업체 연락처
    memo: string | null // 비고
    pv_string_links: PvStringLinkItem[] // 연결된 PV 스트링 목록
}

// DeviceSaveParams 장비 등록/수정 파라미터
export type DeviceSaveParams = Omit<DeviceItem, 'id'>

// PvStringLinkItem 인버터-스트링 연결 정보
export type PvStringLinkItem = {
    id?: number // 연결 ID
    inverter_device_id?: number // 인버터 장비 ID
    pv_string_id: number // PV 스트링 ID
    pv_string_name?: string | null // PV 스트링명
    inverter_name?: string | null // 인버터명
    mppt_no: number | null // MPPT 번호
    channel_no: number | null // 채널 번호
}

// PvStringItem PV 스트링 상세 정보
export type PvStringItem = {
    id: number // 스트링 ID
    name: string // 스트링명
    panel_count: number | null // 패널 수량
    panel_capacity_kw: number | null // 패널 정격 (kW)
    rated_capacity_kw: number | null // 스트링 총 정격 용량 (kW)
    install_location: string | null // 설치 위치
    status: string // 상태
    is_active: boolean // 활성화 여부
    memo: string | null // 비고
    inverter_device_id: number | null // 연결 인버터 ID
    inverter_name: string | null // 연결 인버터명
    mppt_no: number | null // 연결 MPPT 번호
    channel_no: number | null // 연결 채널 번호
}

// PvStringSaveParams PV 스트링 등록/수정 파라미터
export type PvStringSaveParams = Omit<
    PvStringItem,
    'id' | 'inverter_device_id' | 'inverter_name' | 'mppt_no' | 'channel_no'
>

// DeviceListResponse 장비 목록 응답
export type DeviceListResponse = APIResponse<{
    list: DeviceItem[] // 장비 목록
    totalCount: number // 총 건수
}>

// DeviceDetailResponse 장비 상세 응답
export type DeviceDetailResponse = APIResponse<DeviceItem>

// PvStringListResponse PV 스트링 목록 응답
export type PvStringListResponse = APIResponse<{
    list: PvStringItem[] // 스트링 목록
    totalCount: number // 총 건수
}>

// PvStringDetailResponse PV 스트링 상세 응답
export type PvStringDetailResponse = APIResponse<PvStringItem>
