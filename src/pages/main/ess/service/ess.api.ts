import { fetchApi } from '@/http'
import type { EssOverviewResponse, EssSystemListResponse } from './ess.types'

export default {
    async getSystems(): Promise<EssSystemListResponse> {
        return await fetchApi().get('/api/ess/systems')
    },

    async getOverview(): Promise<EssOverviewResponse> {
        return await fetchApi().get('/api/ess/overview')
    },

    async getSystemOverview(systemId: number): Promise<EssOverviewResponse> {
        return await fetchApi().get(`/api/ess/systems/${systemId}/overview`)
    },
}
