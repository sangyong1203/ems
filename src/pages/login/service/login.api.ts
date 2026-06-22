import { fetchApi } from '@/http'
import type { APIResponse, PayloadModel } from '@/http/type'
import type {
    ChangePasswordParams,
    PasswordResetRequestParams,
    ResetPasswordParams,
    SigninParams,
    UserInfoResponse,
} from './login.types'

export default {
    async signin(params: SigninParams): Promise<APIResponse<any>> {
        const payload: PayloadModel = { body: params }
        return await fetchApi().post('/api/auth/login', { payload })
    },

    async changePassword(params: ChangePasswordParams): Promise<APIResponse<any>> {
        const payload: PayloadModel = { body: params }
        return await fetchApi().post('/api/auth/password/change', { payload })
    },

    async requestPasswordReset(params: PasswordResetRequestParams): Promise<APIResponse<any>> {
        const payload: PayloadModel = { body: params }
        return await fetchApi().post('/api/auth/password/reset', { payload })
    },

    async resetPassword(params: ResetPasswordParams): Promise<APIResponse<any>> {
        const payload: PayloadModel = { body: params }
        return await fetchApi().put('/api/auth/password/reset', { payload })
    },

    async getUserInfo(): Promise<UserInfoResponse> {
        return await fetchApi().get('/api/auth/me', {})
    },
}
