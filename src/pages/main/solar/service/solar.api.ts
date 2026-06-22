import { fetchApi } from '@/http'
import type { SolarOverviewResponse } from './solar.types'

export default {
    async getOverview(): Promise<SolarOverviewResponse> {
        return await fetchApi().get('/api/solar/overview')
    },
}
