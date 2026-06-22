import { fetchApi } from '@/http'
import type { PayloadModel } from '@/http/type'
import type {
    AlarmDetailResponse,
    AlarmDeviceListResponse,
    AlarmListResponse,
    AlarmSearchParams,
} from './alarmHistory.types'

export default {
    async getList(params: AlarmSearchParams = {}): Promise<AlarmListResponse> {
        const payload: PayloadModel = { query: params }
        return await fetchApi().get('/api/alarms', { payload })
    },

    async getDevices(): Promise<AlarmDeviceListResponse> {
        return await fetchApi().get('/api/devices')
    },

    async acknowledge(id: number): Promise<AlarmDetailResponse> {
        return await fetchApi().put(`/api/alarms/${id}/ack`)
    },

    async resolve(id: number): Promise<AlarmDetailResponse> {
        return await fetchApi().put(`/api/alarms/${id}/resolve`)
    },

    async createMaintenance(id: number): Promise<void> {
        await fetchApi().post(`/api/alarms/${id}/maintenance`)
    },
}
