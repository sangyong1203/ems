import { fetchApi } from '@/http'
import type { EssOverviewResponse, EssSystemListResponse } from './ess.types'

export default {
    // getSystems ESS 장치 목록 및 요약 조회
    async getSystems(): Promise<EssSystemListResponse> {
        return await fetchApi().get('/api/ess/systems')
    },

    // getOverview ESS 기본 개요 정보 조회
    async getOverview(): Promise<EssOverviewResponse> {
        return await fetchApi().get('/api/ess/overview')
    },

    // getSystemOverview 특정 ESS 장치의 상세 현황 및 계측 데이터 조회
    async getSystemOverview(systemId: number): Promise<EssOverviewResponse> {
        return await fetchApi().get(`/api/ess/systems/${systemId}/overview`)
    },
}
