import axios from 'axios'
import { useAuthStore } from '@/stores/auth.store'
import type { RequestConfig } from './index'
import type { SessionTokens } from '@/pages/login/service/login.types'

let refreshPromise: Promise<SessionTokens> | null = null // 동시 401 요청이 공유하는 재발급 작업

// 동시에 만료된 요청은 한 번만 재발급하고 교체된 토큰을 공유합니다.
const reissueTokens = (): Promise<SessionTokens> => {
    if (refreshPromise) return refreshPromise

    const authStore = useAuthStore()
    const refreshToken = authStore.authState.tokens.refreshToken
    if (!refreshToken) return Promise.reject(new Error('No refresh token available.'))

    refreshPromise = axios
        .post('/api/auth/reissue', { refreshToken })
        .then(res => {
            const tokens = res.data?.data as SessionTokens | undefined
            if (res.data?.result !== 'SUCCESS' || !tokens?.accessToken || !tokens.refreshToken) {
                throw new Error('Invalid token reissue response.')
            }
            if (authStore.authState.tokens.refreshToken !== refreshToken) {
                throw new Error('Authentication session changed.')
            }
            authStore.setTokens(tokens)
            return tokens
        })
        .finally(() => {
            refreshPromise = null
        })
    return refreshPromise
}

// 토큰 갱신 후 원래 요청을 한 번만 재시도하고 실패도 호출자에게 전달합니다.
export const refreshAccessToken = async (props: {
    config: RequestConfig
    resolve: (value: any) => void
    reject: (reason?: any) => void
}) => {
    const { config, resolve, reject } = props
    const authStore = useAuthStore()
    const originalSessionId = authStore.authState.sessionId
    const originalRefreshToken = authStore.authState.tokens.refreshToken
    let retryAccessToken: string | null = null // 재시도에 사용한 토큰; 새 로그인 세션을 지우지 않도록 비교

    try {
        if (config.authSessionId !== originalSessionId) {
            throw new Error('Authentication session changed.')
        }
        const sentAuthorization = config.headers?.Authorization
        const currentAccessToken = authStore.authState.tokens.accessToken
        const tokens = currentAccessToken && sentAuthorization !== `Bearer ${currentAccessToken}`
            ? authStore.authState.tokens
            : await reissueTokens()
        if (authStore.authState.sessionId !== originalSessionId) {
            throw new Error('Authentication session changed.')
        }
        retryAccessToken = tokens.accessToken
        const response = await axios.request({
            ...config,
            headers: { ...config.headers, Authorization: `Bearer ${tokens.accessToken}` },
        })
        resolve(response.data)
    } catch (error) {
        const isUnauthorized = axios.isAxiosError(error) && [401, 403].includes(error.response?.status ?? 0)
        const sameSession = retryAccessToken
            ? authStore.authState.tokens.accessToken === retryAccessToken
            : authStore.authState.tokens.refreshToken === originalRefreshToken
        if (config.authSessionId === originalSessionId && sameSession && (isUnauthorized || !originalRefreshToken)) {
            authStore.clearSession()
            window.location.replace('/login')
        }
        reject(error)
    }
}
