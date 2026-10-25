import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import type { PersistedStateOptions } from 'pinia-plugin-persistedstate'

export type RoleLevel = 'PLATFORM_ADMIN' // 현재 앱은 관리자만 사용

export type AuthUser = {
    loginId: string
    name: string
    userLevel: RoleLevel
    email: string
    landingPage: string
}

export type AuthTokens = {
    accessToken: string
    refreshToken: string
}

export type AuthState = {
    sessionId: string // 프론트 로그인 구분값; 서버 인증에는 사용하지 않음
    user: AuthUser | null
    tokens: AuthTokens
}

const createEmptyTokens = (): AuthTokens => ({
    accessToken: '',
    refreshToken: '',
})

const createInitialAuthState = (): AuthState => ({
    sessionId: `${Date.now()}-${Math.random()}`,
    user: null,
    tokens: createEmptyTokens(),
})

export const useAuthStore = defineStore(
    'auth',
    () => {
        const authState = ref<AuthState>(createInitialAuthState())

        const isAuthenticated = computed(() => Boolean(authState.value.user?.loginId && authState.value.tokens.accessToken))

        const setUser = (user: AuthUser | null) => {
            authState.value.user = user
        }

        const setTokens = (tokens: Partial<AuthTokens>) => {
            authState.value.tokens = {
                ...authState.value.tokens,
                ...tokens,
            }
        }

        const setSession = (session: { user: AuthUser; tokens: Partial<AuthTokens> }) => {
            authState.value = {
                sessionId: authState.value.sessionId,
                user: session.user,
                tokens: {
                    ...createEmptyTokens(),
                    ...session.tokens,
                },
            }
        }

        const clearSession = () => {
            authState.value = createInitialAuthState()
        }

        return {
            authState,
            isAuthenticated,
            setUser,
            setTokens,
            setSession,
            clearSession,
        }
    },
    {
        persist: {
            enabled: true,
            storage: window.sessionStorage,
            key: 'Auth',
        } as PersistedStateOptions,
    },
)
