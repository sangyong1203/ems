import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import type { PersistedStateOptions } from 'pinia-plugin-persistedstate'

export type RoleLevel = 'PLATFORM_ADMIN' | 'USER'

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
    verificationToken: string
}

export type AuthState = {
    user: AuthUser | null
    tokens: AuthTokens
}

const createEmptyTokens = (): AuthTokens => ({
    accessToken: '',
    refreshToken: '',
    verificationToken: '',
})

const createInitialAuthState = (): AuthState => ({
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
