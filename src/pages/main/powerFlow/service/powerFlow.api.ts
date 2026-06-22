import { fetchApi } from '@/http'
import type { PayloadModel } from '@/http/type'
import type { PowerFlowLayoutSaveBody } from '@/features/powerFlow/service/powerFlow.types'
import type { PowerFlowEditorResponse, PowerFlowResponse } from './powerFlow.types'

export default {
    async getPowerFlow(): Promise<PowerFlowResponse> {
        return await fetchApi().get('/api/power-flow/overview')
    },
    async getEditor(): Promise<PowerFlowEditorResponse> {
        return await fetchApi().get('/api/power-flow/editor')
    },
    async saveEditor(body: PowerFlowLayoutSaveBody): Promise<PowerFlowEditorResponse> {
        const payload: PayloadModel = { body }
        return await fetchApi().put('/api/power-flow/editor', { payload })
    },
}
