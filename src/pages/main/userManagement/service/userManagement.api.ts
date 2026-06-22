import { fetchApi } from '@/http'
import type { PayloadModel } from '@/http/type'
import type { RequestParams, UserDeleteResponse, UserListResponse, UserSaveParams, UserSaveResponse } from './userManagement.types'

export default {
    async getList(params: RequestParams): Promise<UserListResponse> {
        const payload: PayloadModel = { query: params }
        return await fetchApi().get('/api/users', { payload })
    },

    async createUser(params: UserSaveParams): Promise<UserSaveResponse> {
        const payload: PayloadModel = { body: params }
        return await fetchApi().post('/api/users', { payload })
    },

    async updateUser(id: number, params: UserSaveParams): Promise<UserSaveResponse> {
        const payload: PayloadModel = { body: params }
        return await fetchApi().put(`/api/users/${id}`, { payload })
    },

    async deleteUser(id: number): Promise<UserDeleteResponse> {
        return await fetchApi().delete(`/api/users/${id}`)
    },
}
