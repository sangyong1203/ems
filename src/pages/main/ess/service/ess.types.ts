import type { APIResponse } from '@/http/type'

// EssTelemetryPoint ESS 계측 데이터 시계열 포인트
export type EssTelemetryPoint = {
    id: number // 계측 데이터 ID
    device_id: number | null // 장치 ID
    metric_key: string // 계측 지표 키
    metric_value: number // 계측값
    unit: string | null // 단위
    measured_at: string // 계측 일시
}

// EssDevice ESS 세부 장치 정보
export type EssDevice = {
    id: number | null // 장치 ID
    name: string // 장치명
    status: string // 장치 상태
    manufacturer: string | null // 제조사
    modelName: string | null // 모델명
    capacity: number | null // 정격 용량
    capacityUnit: string | null // 용량 단위
}

// EssSystemItem ESS 시스템 목록 항목
export type EssSystemItem = {
    id: number // ESS 시스템 ID
    name: string // 시스템명
    code: string // 시스템 코드
    status: string // 운영 상태 (NORMAL, WARNING, FAULT)
    mode: string // 운전 모드 (CHARGING, DISCHARGING, STANDBY)
    soc: number // 충전율 (%)
    soh: number // 배터리 건강상태 (%)
    capacityKwh: number // 배터리 용량 (kWh)
    currentPowerKw: number // 현재 출력 (kW)
    isActive: boolean // 활성화 여부
    installLocation: string | null // 설치 위치
}

// EssSystemSummary ESS 시스템 전체 현황 요약
export type EssSystemSummary = {
    total: number // 전체 ESS 수
    normal: number // 정상 가동 수
    warning: number // 주의 수
    fault: number // 장애 수
    capacityKwh: number // 총 설비 용량 (kWh)
    averageSoc: number // 평균 SOC (%)
    currentPowerKw: number // 총 출력 전력 (kW)
}

// EssBatteryRack 배터리 랙 계측 정보
export type EssBatteryRack = {
    id: number // 배터리 랙 ID
    rackNo: number // 랙 번호
    name: string // 랙 명칭
    status: string // 상태 (NORMAL, WARNING, FAULT)
    isActive: boolean // 사용 여부
    capacityKwh: number // 랙 용량 (kWh)
    soc: number // 랙 SOC (%)
    soh: number // 랙 SOH (%)
    voltageV: number // 전압 (V)
    currentA: number // 전류 (A)
    averageTemperatureC: number // 평균 온도 (°C)
    maxTemperatureC: number // 최고 온도 (°C)
    updatedAt: string | null // 갱신 일시
}

// EssRackTemperatureHistory 랙별 온도 시계열
export type EssRackTemperatureHistory = {
    rackId: number // 랙 ID
    rackNo: number // 랙 번호
    rackName: string // 랙 명칭
    data: EssTelemetryPoint[] // 온도 계측 데이터 목록
}

// EssOverview ESS 상세 모니터링 종합 정보
export type EssOverview = {
    refreshInterval: number // 자동 갱신 주기 (ms)
    project: {
        projectName: string // 프로젝트명
        siteName: string // 사이트명
        systemName: string // 시스템명
        essCapacityKwh: number // ESS 총 용량 (kWh)
    }
    system: {
        id: number // 시스템 ID
        name: string // 시스템명
        code: string // 시스템 코드
        status: string // 운영 상태
        capacityKwh: number // 시스템 용량 (kWh)
        isActive: boolean // 활성화 여부
        installLocation: string | null // 설치 위치
        memo: string | null // 비고
    }
    updatedAt: string | null // 데이터 갱신 일시
    summary: {
        soc: number // 배터리 충전율 (%)
        soh: number // 배터리 건강상태 (%)
        mode: string // 운전 모드
        chargePowerKw: number // 충전 전력 (kW)
        dischargePowerKw: number // 방전 전력 (kW)
        batteryVoltageV: number // 배터리 전압 (V)
        batteryCurrentA: number // 배터리 전류 (A)
        batteryTemperatureC: number // 배터리 온도 (°C)
        todayChargeKwh: number // 금일 누적 충전량 (kWh)
        todayDischargeKwh: number // 금일 누적 방전량 (kWh)
        totalThroughputKwh: number // 총 방전량 (kWh)
        netEnergyKwh: number // 순 에너지량 (kWh)
        pcsStatus: string // PCS 상태
        bmsStatus: string // BMS 상태
        batteryStatus: string // 배터리 상태
        systemStatus: string // 시스템 종합 상태
    }
    limits: {
        socMin: number // SOC 하한치 (%)
        socMax: number // SOC 상한치 (%)
        voltageMinV: number // 전압 하한치 (V)
        voltageMaxV: number // 전압 상한치 (V)
        temperatureWarningC: number // 온도 주의 한계 (°C)
        temperatureFaultC: number // 온도 장애 한계 (°C)
    }
    history: {
        charge: EssTelemetryPoint[] // 충전 전력 시계열
        discharge: EssTelemetryPoint[] // 방전 전력 시계열
        soc: EssTelemetryPoint[] // SOC 시계열
        voltage: EssTelemetryPoint[] // 전압 시계열
        temperature: EssTelemetryPoint[] // 온도 시계열
        rackTemperatures: EssRackTemperatureHistory[] // 랙별 온도 시계열
    }
    batteryRacks: EssBatteryRack[] // 랙 목록
    devices: {
        pcs: EssDevice // PCS 장치 정보
        bms: EssDevice // BMS 장치 정보
        battery: EssDevice // 배터리 뱅크 정보
    }
}

// EssSystemListResponse ESS 시스템 목록 응답
export type EssSystemListResponse = APIResponse<{
    list: EssSystemItem[] // 시스템 목록
    totalCount: number // 총 시스템 수
    summary: EssSystemSummary // 시스템 전체 요약
}>

// EssOverviewResponse ESS 상세 개요 응답
export type EssOverviewResponse = APIResponse<EssOverview>
