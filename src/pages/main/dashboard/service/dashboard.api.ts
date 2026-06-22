import { fetchApi } from '@/http'
import type { PayloadModel } from '@/http/type'
import type { PowerFlowEditorResponse } from '@/pages/main/powerFlow/service/powerFlow.types'
import type { DashboardPowerFlowResponse, DashboardSummaryResponse, DashboardTelemetryHistoryResponse } from './dashboard.types'

export default {
    async getSummary(): Promise<DashboardSummaryResponse> {
        return await fetchApi().get('/api/dashboard/summary')
    },
    async getPowerFlow(): Promise<DashboardPowerFlowResponse> {
        return await fetchApi().get('/api/dashboard/power-flow')
    },
    async getPowerFlowEditor(): Promise<PowerFlowEditorResponse> {
        return await fetchApi().get('/api/power-flow/editor')
    },
    async getTelemetryHistory(metricKey: string): Promise<DashboardTelemetryHistoryResponse> {
        const payload: PayloadModel = {
            query: {
                metricKey,
                limit: 24,
            },
        }
        return await fetchApi().get('/api/telemetry/history', { payload })
    },
}
