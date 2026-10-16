import type { APIResponse } from '@/http/type'

// 장비 유형별 수량
export type DeviceCounts = {
    INVERTER: number // 인버터 수량
    PCS: number // PCS 수량
    ESS_BATTERY: number // 배터리 수량
    BATTERY_RACK: number // 배터리 랙 수량
    BMS: number // BMS 수량
    AC_PANEL: number // 수배전반 수량
    METER: number // 계량기 수량
}

// 설비 설치/운영 용량 요약
export type EquipmentCapacities = {
    solarInstalledKw: number // 태양광 설치 용량 (kW)
    solarOperatingKw: number // 태양광 가동 용량 (kW)
    essInstalledKwh: number // ESS 설치 용량 (kWh)
    essOperatingKwh: number // ESS 가동 용량 (kWh)
}

// 프로젝트 환경설정 상세
export type ProjectConfig = {
    id: number // 설정 ID
    project_name: string // 프로젝트명
    site_name: string // 사업장/현장명
    location: string | null // 설치 위치
    customer_name: string | null // 고객사명
    contractor_name: string | null // 시공사명
    solar_capacity_kw: number // 태양광 설비 용량 (kW)
    ess_capacity_kwh: number // ESS 설비 용량 (kWh)
    system_name: string // 시스템명
    background_image_path: string | null // 배경 이미지 경로
    logo_image_path: string | null // 로고 이미지 경로
    data_refresh_interval: number // 기본 데이터 갱신 주기 (ms)
    dashboard_refresh_interval: number // 대시보드 갱신 주기 (ms)
    solar_refresh_interval: number // 태양광 화면 갱신 주기 (ms)
    ess_refresh_interval: number // ESS 화면 갱신 주기 (ms)
    power_flow_refresh_interval: number // 전력 흐름 화면 갱신 주기 (ms)
    trend_refresh_interval: number // 트렌드 화면 갱신 주기 (ms)
    device_counts: DeviceCounts // 전체 등록 장비 수량
    active_device_counts: DeviceCounts // 정상 가동 중인 장비 수량
    equipment_capacities: EquipmentCapacities // 설비 가동 용량 요약
}

// 프로젝트 환경설정 저장 페이로드
export type ProjectConfigSavePayload = Omit<
    ProjectConfig,
    'id' | 'device_counts' | 'active_device_counts' | 'equipment_capacities'
>
export type ProjectConfigResponse = APIResponse<ProjectConfig> // 프로젝트 환경설정 응답 타입
export type SimulatorActionResponse = APIResponse<{ // 시뮬레이터 실행 결과 응답 타입
    generatedAt?: string // 생성 시각
    dayCount?: number // 생성 일수
    alarmCount?: number // 생성 알림 수
    maintenanceCount?: number // 생성 정비 건수
    reset?: boolean // 초기화 완료 여부
}>
