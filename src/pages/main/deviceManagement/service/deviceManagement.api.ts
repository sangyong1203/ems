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
    async getList(params: { keyword?: string; deviceType?: string; status?: string } = {}): Promise<DeviceListResponse> {
        const payload: PayloadModel = { query: params }
        return await fetchApi().get('/api/devices', { payload })
    },

    async getDetail(id: number): Promise<DeviceDetailResponse> {
        return await fetchApi().get(`/api/devices/${id}`)
    },

    async createDevice(params: DeviceSaveParams): Promise<DeviceDetailResponse> {
        const payload: PayloadModel = { body: params }
        return await fetchApi().post('/api/devices', { payload })
    },

    async updateDevice(id: number, params: DeviceSaveParams): Promise<DeviceDetailResponse> {
        const payload: PayloadModel = { body: params }
        return await fetchApi().put(`/api/devices/${id}`, { payload })
    },

    async deleteDevice(id: number): Promise<void> {
        await fetchApi().delete(`/api/devices/${id}`)
    },

    async getPvStrings(params: { keyword?: string; status?: string; connection?: string } = {}): Promise<PvStringListResponse> {
        const payload: PayloadModel = { query: params }
        return await fetchApi().get('/api/pv-strings', { payload })
    },

    async createPvString(params: PvStringSaveParams): Promise<PvStringDetailResponse> {
        const payload: PayloadModel = { body: params }
        return await fetchApi().post('/api/pv-strings', { payload })
    },

    async updatePvString(id: number, params: PvStringSaveParams): Promise<PvStringDetailResponse> {
        const payload: PayloadModel = { body: params }
        return await fetchApi().put(`/api/pv-strings/${id}`, { payload })
    },

    async deletePvString(id: number): Promise<void> {
        await fetchApi().delete(`/api/pv-strings/${id}`)
    },
}
