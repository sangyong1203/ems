import { fetchApi } from '@/http'
import type { PayloadModel } from '@/http/type'
import type { SearchParams, TemplateDetailResponse, TemplateItem, TemplateListResponse, TemplateTypesResponse } from './notificationManagement.types'

export default {
    async getList(params: SearchParams): Promise<TemplateListResponse> {
        const payload: PayloadModel = { query: params }
        return await fetchApi().get('/system/email/templatesList', { payload })
    },

    async getTemplate(templateId: number): Promise<TemplateDetailResponse> {
        return await fetchApi().get(`/system/email/templates/${templateId}`)
    },

    async editTemplate(params: TemplateItem, templateId: number): Promise<TemplateDetailResponse> {
        const payload: PayloadModel = { body: params }
        return await fetchApi().put(`/system/email/templates/${templateId}`, { payload })
    },

    async getTemplateTypes(): Promise<TemplateTypesResponse> {
        return await fetchApi().get('/system/email/templates/types')
    },
}
