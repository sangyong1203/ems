import { fetchApi } from '@/http'
import type { APIResponse } from '@/http/type'
import type { ChangePasswordParams, SigninParams, SigninResponse, UserInfoResponse } from './login.types'

export default {
    // 로그인은 만료된 기존 세션의 재발급을 시도하지 않습니다.
    async signin(params: SigninParams): Promise<SigninResponse> {
        return await fetchApi().post('/api/auth/login', { payload: { body: params }, auth: false })
    },

    // 현재 비밀번호 확인 후 변경하며 서버가 해당 사용자의 모든 세션을 폐기합니다.
    async changePassword(params: ChangePasswordParams): Promise<APIResponse<{ changed: boolean }>> {
        return await fetchApi().post('/api/auth/password/change', { payload: { body: params } })
    },

    // 갱신 토큰으로 서버 세션을 폐기하며 만료된 액세스 토큰을 재발급하지 않습니다.
    async logout(refreshToken: string): Promise<APIResponse<{ loggedOut: boolean }>> {
        return await fetchApi().post('/api/auth/logout', { payload: { body: { refreshToken } }, auth: false })
    },

    // 서버가 인증한 현재 관리자 정보를 조회합니다.
    async getUserInfo(): Promise<UserInfoResponse> {
        return await fetchApi().get('/api/auth/me')
    },
}
