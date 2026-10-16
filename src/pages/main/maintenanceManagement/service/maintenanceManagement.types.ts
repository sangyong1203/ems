import type { APIResponse } from '@/http/type'

// MaintenanceStatus 정비 진행 상태
export type MaintenanceStatus = 'SCHEDULED' | 'IN_PROGRESS' | 'COMPLETED' | 'HOLD' | 'CANCELED'

// MaintenanceItem 정비 이력 레코드
export type MaintenanceItem = {
    id: number // 정비 ID
    device_id: number | null // 대상 장비 ID
    alarm_id: number | null // 연동 알람 ID
    maintenance_type: string // 정비 유형 (정기점검, 장애점검 등)
    title: string // 정비 제목
    description: string | null // 정비 내용
    action_taken: string | null // 조치 내용
    status: MaintenanceStatus | string // 정비 상태
    maintenance_date: string | null // 점검 일자
    next_maintenance_date: string | null // 다음 점검 예정일
    manager_name: string | null // 담당자명
    cause: string | null // 원인 분석
    before_status: string | null // 조치 전 상태
    after_status: string | null // 조치 후 상태
    contractor_name: string | null // 수행 업체명
    cost: number | null // 소요 비용
    memo: string | null // 비고
    device_name: string | null // 대상 장비명
    device_type: string | null // 장비 유형
}

// MaintenanceSaveParams 정비 등록/수정 파라미터
export type MaintenanceSaveParams = {
    device_id: number | null // 대상 장비 ID
    alarm_id?: number | null // 연동 알람 ID
    maintenance_type: string // 정비 유형
    title: string // 정비 제목
    description: string | null // 정비 내용
    cause: string | null // 원인 분석
    action_taken: string | null // 조치 내용
    before_status: string | null // 조치 전 상태
    after_status: string | null // 조치 후 상태
    status: MaintenanceStatus | string // 정비 상태
    maintenance_date: string | null // 점검 일자
    next_maintenance_date: string | null // 다음 점검 예정일
    manager_name: string | null // 담당자명
    contractor_name: string | null // 수행 업체명
    cost: number | null // 소요 비용
    memo: string | null // 비고
}

// MaintenanceSearchParams 정비 이력 검색 파라미터
export type MaintenanceSearchParams = {
    keyword?: string // 검색 키워드 (제목/내용)
    deviceId?: number // 대상 장비 ID 필터
    maintenanceType?: string // 정비 유형 필터
    status?: string // 정비 상태 필터
    dateFrom?: string // 점검 시작일 필터
    dateTo?: string // 점검 종료일 필터
}

// MaintenanceDeviceOption 정비 대상 장비 옵션
export type MaintenanceDeviceOption = {
    id: number // 장비 ID
    name: string // 장비명
    device_type: string // 장비 유형
}

// MaintenanceListResponse 정비 이력 목록 응답
export type MaintenanceListResponse = APIResponse<{
    list: MaintenanceItem[] // 정비 목록
    totalCount: number // 총 건수
}>

// MaintenanceDetailResponse 정비 이력 상세 응답
export type MaintenanceDetailResponse = APIResponse<MaintenanceItem>

// MaintenanceDeviceListResponse 정비 대상 장비 목록 응답
export type MaintenanceDeviceListResponse = APIResponse<{
    list: MaintenanceDeviceOption[] // 장비 목록
    totalCount: number // 총 건수
}>
