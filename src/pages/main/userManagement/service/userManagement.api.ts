import { fetchApi } from '@/http'
import type { PayloadModel } from '@/http/type'
import type { RequestParams, UserDeleteResponse, UserListResponse, UserSaveParams, UserSaveResponse } from './userManagement.types'

export default {
    // getList 검색 조건 기반 사용자 목록 조회
    async getList(params: RequestParams): Promise<UserListResponse> {
        const payload: PayloadModel = { query: params }
        return await fetchApi().get('/api/users', { payload })
    },

    // createUser 신규 사용자 등록
    async createUser(params: UserSaveParams): Promise<UserSaveResponse> {
        const payload: PayloadModel = { body: params }
        return await fetchApi().post('/api/users', { payload })
    },

    // updateUser 기존 사용자 정보 수정
    async updateUser(id: number, params: UserSaveParams): Promise<UserSaveResponse> {
        const payload: PayloadModel = { body: params }
        return await fetchApi().put(`/api/users/${id}`, { payload })
    },

    // deleteUser 사용자 계정 삭제
    async deleteUser(id: number): Promise<UserDeleteResponse> {
        return await fetchApi().delete(`/api/users/${id}`)
    },
}
