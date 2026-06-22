import { fetchApi } from '@/http'
import type { APIResponse, PayloadModel } from '@/http/type'
import type { TemplateItem } from './types'

export default {
    async uploadImage(formData: FormData): Promise<{ imageId: string }> {
        const payload: PayloadModel = { body: formData }
        const res = await fetchApi().post('/system/email/uploadImage', { payload })
        return res.data
    },

    async createTemplate(params: TemplateItem): Promise<APIResponse> {
        const payload: PayloadModel = { body: params }
        return await fetchApi().post('/system/email/create', { payload })
    },

    async editTemplate(params: TemplateItem, templateId: number): Promise<APIResponse> {
        const payload: PayloadModel = { body: params }
        return await fetchApi().put(`/system/email/templates/${templateId}`, { payload })
    },
}
