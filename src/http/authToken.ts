import axios from 'axios'
import { isEmpty } from 'lodash'
import { useAuthStore } from '@/stores/auth.store'
import type { RequestConfig } from './index'

export const refreshAccessToken = (props: { config: RequestConfig; resolve: (value: any) => void }) => {
    const { config, resolve } = props
    const authStore = useAuthStore()

    if (!authStore.authState.user?.loginId) return

    axios
        .post('/api/auth/reissue', { refreshToken: authStore.authState.tokens.refreshToken, isAdmin: 'Y' })
        .then(res => {
            const resData = res.data?.data
            if (resData.accessToken) {
                authStore.setTokens({
                    accessToken: resData.accessToken,
                    refreshToken: resData.refreshToken,
                })

                if (config.headers) {
                    config.headers.Authorization = `Bearer ${resData.accessToken}`
                }

                axios.request(config).then(retryRes => {
                    resolve(retryRes.data)
                })
            } else if (isEmpty(resData)) {
                window.location.replace('/login')
            }
        })
        .catch(err => {
            console.log('token refresh error', err)
        })
}
