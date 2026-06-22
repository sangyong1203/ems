import type { APIResponse } from '@/http/type'
import type { PowerFlowEditorData } from '@/features/powerFlow/service/powerFlow.types'

export type PowerFlowData = {
    refreshInterval: number
    updatedAt: string
    policy: {
        essGridExportEnabled: boolean
    }
    nodes: {
        solar: { label: string; powerKw: number; status: string }
        ess: { label: string; chargeKw: number; dischargeKw: number; soc: number; status: string }
        load: { label: string; powerKw: number; status: string }
        grid: { label: string; exportKw: number; importKw: number; status: string }
    }
    flows: {
        solarToLoadKw: number
        solarToEssKw: number
        essToLoadKw: number
        solarToGridKw: number
        essToGridKw: number
        gridExportKw: number
        gridImportKw: number
    }
}

export type PowerFlowResponse = APIResponse<PowerFlowData>
export type PowerFlowEditorResponse = APIResponse<PowerFlowEditorData>
