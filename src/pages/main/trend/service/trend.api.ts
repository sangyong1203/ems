import { fetchApi } from '@/http'
import type { TrendOverviewResponse } from './trend.types'

export default {
    async getOverview(): Promise<TrendOverviewResponse> {
        return await fetchApi().get('/api/trend/overview')
    },
}
