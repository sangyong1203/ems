import { fetchApi } from '@/http'
import type { PayloadModel } from '@/http/type'
import type { PowerFlowLayoutSaveBody } from '@/features/powerFlow/service/powerFlow.types'
import type { PowerFlowEditorResponse, PowerFlowResponse } from './powerFlow.types'

export default {
    // getPowerFlow 실시간 전력 조류 데이터 조회
    async getPowerFlow(): Promise<PowerFlowResponse> {
        return await fetchApi().get('/api/power-flow/overview')
    },

    // getEditor 다이어그램 편집기 레이아웃 데이터 조회
    async getEditor(): Promise<PowerFlowEditorResponse> {
        return await fetchApi().get('/api/power-flow/editor')
    },

    // saveEditor 다이어그램 편집기 레이아웃 저장
    async saveEditor(body: PowerFlowLayoutSaveBody): Promise<PowerFlowEditorResponse> {
        const payload: PayloadModel = { body }
        return await fetchApi().put('/api/power-flow/editor', { payload })
    },
}
