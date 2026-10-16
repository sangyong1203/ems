import type { APIResponse } from '@/http/type'

// 태양광 시계열 텔레메트리 데이터
export type SolarTelemetryPoint = {
    id: number // 데이터 포인트 ID
    device_id: number | null // 장비 ID
    metric_key: string // 메트릭 키
    metric_value: number // 측정값
    unit: string | null // 단위
    measured_at: string // 측정 일시 (ISO)
}

// 태양광 인버터 장비 정보
export type SolarInverter = {
    id: number // 인버터 ID
    name: string // 인버터 명칭
    status: string // 운전 상태 코드
    isActive: boolean // 활성화 여부
    capacityKw: number // 정격 용량 (kW)
    capacityUnit: string | null // 용량 단위
    currentPowerKw: number // 현재 발전 출력 (kW)
    capacityRatio: number // 정격 대비 출력 비율 (%)
    updatedAt: string | null // 최종 데이터 수신 일시
}

// 태양광 종합 운영 현황 데이터
export type SolarOverview = {
    refreshInterval: number // 권장 자동 갱신 주기 (ms)
    project: {
        projectName: string // 사업명
        siteName: string // 사이트명
        systemName: string // 시스템 명칭
        solarCapacityKw: number // 태양광 설비 용량 (kW)
        solarInstalledCapacityKw: number // 설치 용량 (kW)
        solarOperatingCapacityKw: number // 운전 용량 (kW)
    }
    updatedAt: string | null // 데이터 갱신 일시
    summary: {
        currentPowerKw: number // 현재 발전 출력 (kW)
        todayGenerationKwh: number // 금일 누적 발전량 (kWh)
        totalGenerationKwh: number // 전체 누적 발전량 (kWh)
        capacityRatio: number // 설비 용량 대비 출력율 (%)
        peakPowerKw: number // 금일 피크 발전 출력 (kW)
        averagePowerKw: number // 금일 평균 발전 출력 (kW)
        inverterTotal: number // 전체 인버터 대수
        inverterNormal: number // 정상 인버터 대수
        inverterWarning: number // 이상/주의 인버터 대수
    }
    history: SolarTelemetryPoint[] // 시간대별 발전 출력 이력
    inverters: SolarInverter[] // 인버터 목록
}

export type SolarOverviewResponse = APIResponse<SolarOverview>
