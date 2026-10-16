import { fetchApi } from '@/http'
import type { PayloadModel } from '@/http/type'
import type { SearchParams, TemplateDetailResponse, TemplateItem, TemplateListResponse, TemplateTypesResponse } from './notificationManagement.types'

export default {
    // getList 검색 조건 기반 알림 템플릿 목록 조회
    async getList(params: SearchParams): Promise<TemplateListResponse> {
        const payload: PayloadModel = { query: params }
        return await fetchApi().get('/system/email/templatesList', { payload })
    },

    // getTemplate 특정 알림 템플릿 상세 정보 조회
    async getTemplate(templateId: number): Promise<TemplateDetailResponse> {
        return await fetchApi().get(`/system/email/templates/${templateId}`)
    },

    // editTemplate 알림 템플릿 정보 수정
    async editTemplate(params: TemplateItem, templateId: number): Promise<TemplateDetailResponse> {
        const payload: PayloadModel = { body: params }
        return await fetchApi().put(`/system/email/templates/${templateId}`, { payload })
    },

    // getTemplateTypes 사용 가능한 알림 템플릿 분류 유형 목록 조회
    async getTemplateTypes(): Promise<TemplateTypesResponse> {
        return await fetchApi().get('/system/email/templates/types')
    },
}
