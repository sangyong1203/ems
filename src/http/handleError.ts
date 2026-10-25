import { isNil } from 'lodash'
import { Notification } from '@/composables/useFeedback'
import { refreshAccessToken } from './authToken'
import type { RequestConfig } from './index'

export const getErrorMessage = (code: string) => {
    const msg = [
        { code: '404', message: 'The requested page or resource was not found.' },
        { code: '403', message: 'Access denied.' },
        { code: '500', message: 'System error. Please contact the administrator.' },
        { code: 'NO_MAP_IMAGE', message: 'No map image available.' },
        {
            code: 'UNEXPECTED_ERROR',
            message: 'An unexpected error has occurred. Please contact the administrator if the problem persists.',
        },
        { code: 'SESSION_EXPIRED', message: 'Session expired due to inactivity. Please log in again.' },
    ]
    const res = msg.find(item => item.code === code)
    return res?.message ?? ''
}

export const handleApiError = (props: {
    res: any
    config: RequestConfig
    resolve: (value: any) => void
    reject: (reason?: any) => void
}) => {
    const { res, config, resolve, reject } = props
    if (isNil(res)) {
        reject(res)
        return
    }

    if (res.status === 401) {
        void refreshAccessToken({ config, resolve, reject })
        return
    }

    if (res.status === 403) {
        Notification.error(getErrorMessage('403'))
        reject(res)
        return
    }

    if (res.status === 404) {
        Notification.error(getErrorMessage('404'))
        reject(res)
        return
    }

    if (res.status === 500) {
        Notification.error(getErrorMessage('500'))
        reject(res)
        return
    }

    Notification.error(res.data?.resultMessage || res.data?.detail || getErrorMessage('UNEXPECTED_ERROR'))
    reject(res.data)
}
