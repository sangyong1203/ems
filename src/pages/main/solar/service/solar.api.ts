import { fetchApi } from '@/http'
import type { SolarOverviewResponse } from './solar.types'

export default {
    // 태양광 종합 운영 현황(설비 정보, 당일 통계, 인버터 목록, 시계열 이력)을 조회합니다.
    async getOverview(): Promise<SolarOverviewResponse> {
        return await fetchApi().get('/api/solar/overview')
    },
}
