import type { AxiosRequestConfig, AxiosResponse, Method, ResponseType } from 'axios'
import axios from 'axios'
import { forEach, get, isArray, isBoolean, isEmpty, isNil, isNumber, isObject, keys, replace, set } from 'lodash'
import { useAppStore } from '@/stores/app.store'
import { useProgress } from '@/shared/composables/useProgressBar'
import { useAuthStore } from '@/stores/auth.store'
import { handleApiError } from './handleError'
import type { APIResponse, PathVariables, PayloadModel } from './type'

export type RequestConfig = AxiosRequestConfig

export type RequestOption = {
    headers?: any
    payload?: PayloadModel
    responseType?: ResponseType
    auth?: boolean
    progress?: boolean
    timeout?: number
}

const replaceUrl = (url: string, pathVariables?: PathVariables) => {
    let result = url
    if (isNil(pathVariables)) return result
    forEach(keys(pathVariables), key => {
        result = replace(result, `{${key}}`, get(pathVariables, key))
    })
    return result
}

const getDataCleansing = (obj: any, filedName: string) => {
    const data = get(obj, filedName)
    if (isEmpty(data)) return

    const result = {}
    forEach(keys(data), key => {
        const value = get(data, key)
        if (isBoolean(value) || isNumber(value)) {
            set(result, key, value)
            return
        }
        if (isNil(value)) return
        set(result, key, value)
    })
    if (isEmpty(result)) return
    return result
}

export const makeRequiredRequestConfig = (method: Method) => {
    return (props: { url: string; opt?: RequestOption }): RequestConfig => {
        const { url, opt } = props
        const { headers = {}, payload, responseType } = opt ?? {}

        const path = get(payload, 'pathVariables')
            ? get(payload, 'pathVariables', {})
            : getDataCleansing(payload, 'path')
        const data =
            isObject(payload?.body) || payload?.body instanceof FormData || isArray(payload?.body)
                ? payload?.body
                : getDataCleansing(payload, 'body')
        const params = get(payload, 'params') ? get(payload, 'params', {}) : getDataCleansing(payload, 'query')

        return {
            url: replaceUrl(url, path),
            withCredentials: true,
            method,
            headers: {
                Authorization: `Bearer ${useAuthStore().authState.tokens.accessToken}`,
                ...headers,
            },
            data,
            params,
            responseType,
        }
    }
}

export const request = (method: Method) => {
    return (url: string) => {
        return async (opt: RequestOption = {}) => {
            const progressStore = useProgress()
            const appStore = useAppStore()
            const config = makeRequiredRequestConfig(method)({ url, opt })

            appStore.setLoading(true)

            return new Promise<APIResponse>((resolve, reject) => {
                if (opt.progress) {
                    progressStore.startProgress()
                    config.onUploadProgress = (progressEvent: any) => {
                        progressStore.setPercentCompleted(progressEvent.loaded, progressEvent.total)
                    }
                }

                axios
                    .request(config)
                    .then((response: AxiosResponse) => {
                        resolve(response.data)
                    })
                    .catch(err => {
                        if (config.url === '/api/auth/login' || config.url === '/api/auth/password/reset') {
                            reject(err.response ?? err)
                        } else {
                            handleApiError({
                                res: err.response ?? err,
                                config,
                                resolve,
                                reject,
                            })
                        }
                    })
                    .finally(() => {
                        appStore.setLoading(false)
                        progressStore.endProgress()
                    })
            })
        }
    }
}

export const fetchApi = () => {
    return {
        get: async (url: string, opt: RequestOption = {}): Promise<APIResponse> => request('GET')(url)(opt),
        post: async (url: string, opt: RequestOption = {}): Promise<APIResponse> => request('POST')(url)(opt),
        put: async (url: string, opt: RequestOption = {}): Promise<APIResponse> => request('PUT')(url)(opt),
        delete: async (url: string, opt: RequestOption = {}): Promise<APIResponse> => request('DELETE')(url)(opt),
        getFile: async (url: string, opt?: RequestOption) => request('GET')(url)({ responseType: 'blob', ...opt }),
    }
}
