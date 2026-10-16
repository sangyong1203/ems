import { fetchApi } from '@/http'
import type { TrendOverviewResponse } from './trend.types'

export default {
    // getOverview 트렌드 모니터링 종합 데이터 조회
    async getOverview(): Promise<TrendOverviewResponse> {
        return await fetchApi().get('/api/trend/overview')
    },
}
