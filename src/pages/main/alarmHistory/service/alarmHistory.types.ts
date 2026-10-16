import type { APIResponse } from '@/http/type'

export type AlarmSeverity = 'INFO' | 'WARNING' | 'CRITICAL' // 알림 심각도 등급
export type AlarmStatus = 'OPEN' | 'ACKED' | 'RESOLVED' // 알림 기본 조치 상태
export type AlarmActionStatus = 'OPEN' | 'ACKED' | 'SCHEDULED' | 'IN_PROGRESS' | 'COMPLETED' | 'HOLD' | 'CANCELED' // 정비 연계 포함 종합 조치 상태

// 알림 이력 항목
export type AlarmItem = {
    id: number // 알림 고유 ID
    device_id: number | null // 발생 대상 장비 ID
    severity: AlarmSeverity | string // 알림 등급
    alarm_type: string // 알림 유형명
    message: string // 알림 상세 메시지
    status: AlarmStatus | string // 알림 상태
    occurred_at: string // 발생 일시 (ISO)
    acknowledged_at: string | null // 확인 일시 (ISO)
    resolved_at: string | null // 해결 일시 (ISO)
    device_name: string | null // 장비명
    device_type: string | null // 장비 유형 코드
    maintenance_id: number | null // 연계된 정비 이력 ID
    maintenance_status: string | null // 연계 정비 진행 상태
    maintenance_title: string | null // 연계 정비 제목
    maintenance_date: string | null // 연계 정비 예정/완료일
}

// 알림 이력 검색 조건
export type AlarmSearchParams = {
    keyword?: string // 장비명·유형·메시지 검색어
    deviceId?: number // 대상 장비 ID
    severity?: string // 알림 등급
    alarmType?: string // 알림 유형명
    status?: string // 조치 상태 코드
    dateFrom?: string // 발생 기간 시작일 (YYYY-MM-DD)
    dateTo?: string // 발생 기간 종료일 (YYYY-MM-DD)
}

// 장비 필터 옵션
export type AlarmDeviceOption = {
    id: number // 장비 ID
    name: string // 장비명
    device_type: string // 장비 유형 코드
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
