import { fetchApi } from '@/http'
import type { PayloadModel } from '@/http/type'
import type { PowerFlowEditorResponse } from '@/pages/main/powerFlow/service/powerFlow.types'
import type { DashboardPowerFlowResponse, DashboardSummaryResponse, DashboardTelemetryHistoryResponse } from './dashboard.types'

export default {
    // 대시보드 메인 종합 요약 지표를 조회합니다.
    async getSummary(): Promise<DashboardSummaryResponse> {
        return await fetchApi().get('/api/dashboard/summary')
    },

    // 실시간 전력 흐름(PV, ESS, 계통, 부하) 데이터를 조회합니다.
    async getPowerFlow(): Promise<DashboardPowerFlowResponse> {
        return await fetchApi().get('/api/dashboard/power-flow')
    },

    // 전력 흐름도 캔버스 다이어그램 레이아웃 및 장비 목록을 조회합니다.
    async getPowerFlowEditor(): Promise<PowerFlowEditorResponse> {
        return await fetchApi().get('/api/power-flow/editor')
    },

    // 지정 메트릭 키의 최근 24개 시계열 텔레메트리 이력을 조회합니다.
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
