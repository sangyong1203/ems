import type { APIResponse } from '@/http/type'

// 대시보드 종합 운영 요약 지표
export type DashboardSummary = {
    refreshInterval: number // 권장 자동 갱신 주기 (ms)
    project: {
        projectName: string // 사업명
        siteName: string // 사이트/발전소명
        solarCapacityKw: number // 태양광 설비 용량 (kW)
        essCapacityKwh: number // ESS 배터리 용량 (kWh)
        systemName: string // 시스템 명칭
    }
    operationStatus: string // 종합 운영 상태 코드
    updatedAt: string // 데이터 갱신 일시 (ISO)
    solar: {
        currentPowerKw: number // 현재 태양광 발전 출력 (kW)
        todayGenerationKwh: number // 금일 누적 발전량 (kWh)
        totalGenerationKwh: number // 전체 누적 발전량 (kWh)
        inverterTotal: number // 전체 인버터 대수
        inverterNormal: number // 정상 인버터 대수
        inverterFault: number // 장애 인버터 대수
    }
    ess: {
        soc: number // 충전율 (SOC %)
        soh: number // 건강상태 (SOH %)
        mode: string // 운전 모드 코드
        chargePowerKw: number // 충전 전력 (kW)
        dischargePowerKw: number // 방전 전력 (kW)
        pcsStatus: string // PCS 상태 코드
        bmsStatus: string // BMS 상태 코드
        batteryTemperatureC: number // 배터리 대표 온도 (°C)
    }
    grid: {
        loadPowerKw: number // 부하 소비 전력 (kW)
        exportPowerKw: number // 계통 송전(역송) 전력 (kW)
        importPowerKw: number // 계통 수전 전력 (kW)
    }
    alarms: {
        openCount: number // 미처리 알림 건수
        recent: Array<{
            id: number // 알림 ID
            severity: string // 심각도
            alarmType: string // 알림 유형
            message: string // 메시지
            status: string // 조치 상태
            occurredAt: string // 발생 일시
        }>
    }
    maintenance: {
        recent: Array<{
            id: number // 정비 ID
            maintenanceType: string // 정비 유형
            title: string // 정비 제목
            status: string // 진행 상태
            maintenanceDate: string // 정비일
            nextMaintenanceDate: string // 차기 정비일
            managerName: string // 담당자명
        }>
    }
}

export type DashboardSummaryResponse = APIResponse<DashboardSummary>

// 실시간 전력 흐름 및 계통 연계 데이터
export type DashboardPowerFlow = {
    updatedAt: string // 갱신 일시
    policy: {
        essGridExportEnabled: boolean // ESS 계통 방전 허용 여부
    }
    nodes: {
        solar: { label: string; powerKw: number; status: string }
        ess: { label: string; chargeKw: number; dischargeKw: number; soc: number; status: string }
        load: { label: string; powerKw: number; status: string }
        grid: { label: string; exportKw: number; importKw: number; status: string }
    }
    flows: {
        solarToLoadKw: number // 태양광 -> 부하 흐름 (kW)
        solarToEssKw: number // 태양광 -> ESS 충전 흐름 (kW)
        solarToGridKw: number // 태양광 -> 계통 송전 흐름 (kW)
        essToLoadKw: number // ESS 방전 -> 부하 흐름 (kW)
        essToGridKw: number // ESS 방전 -> 계통 송전 흐름 (kW)
        gridExportKw: number // 총 송전 전력 (kW)
        gridImportKw: number // 총 수전 전력 (kW)
    }
}

export type DashboardPowerFlowResponse = APIResponse<DashboardPowerFlow>

// 시계열 텔레메트리 측정 포인트
export type DashboardTelemetryPoint = {
    id: number // 데이터 포인트 ID
    device_id: number | null // 장비 ID
    metric_key: string // 메트릭 식별 키
    metric_value: number // 측정값
    unit: string | null // 단위
    measured_at: string // 측정 일시 (ISO)
}

export type DashboardTelemetryHistoryResponse = APIResponse<DashboardTelemetryPoint[]>
