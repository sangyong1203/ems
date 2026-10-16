import type { APIResponse } from '@/http/type'
import type { PowerFlowEditorData } from '@/features/powerFlow/service/powerFlow.types'

// PowerFlowData 실시간 전력 조류 데이터
export type PowerFlowData = {
    refreshInterval: number // 자동 갱신 주기 (ms)
    updatedAt: string // 데이터 갱신 일시
    policy: {
        essGridExportEnabled: boolean // ESS 계통 방전 허용 여부
    }
    nodes: {
        solar: { label: string; powerKw: number; status: string } // 태양광 노드 현황
        ess: {
            label: string // ESS 라벨
            chargeKw: number // 충전 전력 (kW)
            dischargeKw: number // 방전 전력 (kW)
            soc: number // 충전율 (%)
            soh: number // 건강상태 (%)
            temperatureC: number // 온도 (°C)
            status: string // 운영 상태
        }
        load: { label: string; powerKw: number; status: string } // 부하 노드 현황
        grid: { label: string; exportKw: number; importKw: number; status: string } // 계통 노드 현황
    }
    flows: {
        solarToLoadKw: number // PV → 부하 전력 (kW)
        solarToEssKw: number // PV → ESS 전력 (kW)
        essToLoadKw: number // ESS → 부하 전력 (kW)
        solarToGridKw: number // PV → 계통 전력 (kW)
        essToGridKw: number // ESS → 계통 전력 (kW)
        gridExportKw: number // 총 송전 전력 (kW)
        gridImportKw: number // 총 수전 전력 (kW)
    }
}

// PowerFlowResponse 전력 조류 응답
export type PowerFlowResponse = APIResponse<PowerFlowData>

// PowerFlowEditorResponse 전력 조류 편집기 레이아웃 응답
export type PowerFlowEditorResponse = APIResponse<PowerFlowEditorData>
