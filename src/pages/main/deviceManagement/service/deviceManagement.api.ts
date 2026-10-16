import { fetchApi } from '@/http'
import type { PayloadModel } from '@/http/type'
import type {
    DeviceDetailResponse,
    DeviceListResponse,
    DeviceSaveParams,
    PvStringDetailResponse,
    PvStringListResponse,
    PvStringSaveParams,
} from './deviceManagement.types'

export default {
    // getList 검색 조건 기반 장비 목록 조회
    async getList(params: { keyword?: string; deviceType?: string; status?: string } = {}): Promise<DeviceListResponse> {
        const payload: PayloadModel = { query: params }
        return await fetchApi().get('/api/devices', { payload })
    },

    // getDetail 특정 장비 상세 정보 조회
    async getDetail(id: number): Promise<DeviceDetailResponse> {
        return await fetchApi().get(`/api/devices/${id}`)
    },

    // createDevice 신규 장비 등록
    async createDevice(params: DeviceSaveParams): Promise<DeviceDetailResponse> {
        const payload: PayloadModel = { body: params }
        return await fetchApi().post('/api/devices', { payload })
    },

    // updateDevice 기존 장비 정보 수정
    async updateDevice(id: number, params: DeviceSaveParams): Promise<DeviceDetailResponse> {
        const payload: PayloadModel = { body: params }
        return await fetchApi().put(`/api/devices/${id}`, { payload })
    },

    // deleteDevice 장비 삭제
    async deleteDevice(id: number): Promise<void> {
        await fetchApi().delete(`/api/devices/${id}`)
    },

    // getPvStrings 검색 조건 기반 PV 스트링 목록 조회
    async getPvStrings(params: { keyword?: string; status?: string; connection?: string } = {}): Promise<PvStringListResponse> {
        const payload: PayloadModel = { query: params }
        return await fetchApi().get('/api/pv-strings', { payload })
    },

    // createPvString 신규 PV 스트링 등록
    async createPvString(params: PvStringSaveParams): Promise<PvStringDetailResponse> {
        const payload: PayloadModel = { body: params }
        return await fetchApi().post('/api/pv-strings', { payload })
    },

    // updatePvString 기존 PV 스트링 정보 수정
    async updatePvString(id: number, params: PvStringSaveParams): Promise<PvStringDetailResponse> {
        const payload: PayloadModel = { body: params }
        return await fetchApi().put(`/api/pv-strings/${id}`, { payload })
    },

    // deletePvString PV 스트링 삭제
    async deletePvString(id: number): Promise<void> {
        await fetchApi().delete(`/api/pv-strings/${id}`)
    },
}
