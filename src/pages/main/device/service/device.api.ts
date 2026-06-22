import { fetchApi } from '@/http'
import type { PayloadModel } from '@/http/type'
import type {
    DeviceCommandParams,
    DeviceCommandResponse,
    DeviceDetailResponse,
    DeviceListResponse,
    DeviceSaveParams,
    DeviceSearchParams,
    DeviceSettingParams,
} from './device.types'

export default {
    async getList(params: DeviceSearchParams): Promise<DeviceListResponse> {
        const payload: PayloadModel = { query: params }
        return await fetchApi().get('/system/devices', { payload })
    },

    async getDetail(id: number): Promise<DeviceDetailResponse> {
        return await fetchApi().get(`/system/devices/${id}`)
    },

    async createDevice(params: DeviceSaveParams): Promise<DeviceDetailResponse> {
        const payload: PayloadModel = { body: params }
        return await fetchApi().post('/system/devices', { payload })
    },

    async updateDevice(id: number, params: DeviceSaveParams): Promise<DeviceDetailResponse> {
        const payload: PayloadModel = { body: params }
        return await fetchApi().put(`/system/devices/${id}`, { payload })
    },

    async deleteDevice(id: number): Promise<void> {
        await fetchApi().delete(`/system/devices/${id}`)
    },

    async updateSettings(id: number, params: DeviceSettingParams): Promise<DeviceDetailResponse> {
        const payload: PayloadModel = { body: params }
        return await fetchApi().put(`/system/devices/${id}/settings`, { payload })
    },

    async sendCommand(id: number, params: DeviceCommandParams): Promise<DeviceCommandResponse> {
        const payload: PayloadModel = { body: params }
        return await fetchApi().post(`/system/devices/${id}/commands`, { payload })
    },
}
