import { fetchApi } from '@/http'
import type { APIResponse, PayloadModel } from '@/http/type'
import type { TemplateItem } from './types'

export default {
    // uploadImage 템플릿 삽입용 이미지 파일 업로드
    async uploadImage(formData: FormData): Promise<{ imageId: string }> {
        const payload: PayloadModel = { body: formData }
        const res = await fetchApi().post('/system/email/uploadImage', { payload })
        return res.data
    },

    // createTemplate 신규 알림 템플릿 생성
    async createTemplate(params: TemplateItem): Promise<APIResponse> {
        const payload: PayloadModel = { body: params }
        return await fetchApi().post('/system/email/create', { payload })
    },

    // editTemplate 기존 알림 템플릿 수정
    async editTemplate(params: TemplateItem, templateId: number): Promise<APIResponse> {
        const payload: PayloadModel = { body: params }
        return await fetchApi().put(`/system/email/templates/${templateId}`, { payload })
    },
}
