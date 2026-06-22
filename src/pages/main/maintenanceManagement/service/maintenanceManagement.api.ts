import { fetchApi } from '@/http'
import type { PayloadModel } from '@/http/type'
import type {
    MaintenanceDetailResponse,
    MaintenanceDeviceListResponse,
    MaintenanceListResponse,
    MaintenanceSaveParams,
    MaintenanceSearchParams,
} from './maintenanceManagement.types'

export default {
    async getList(params: MaintenanceSearchParams = {}): Promise<MaintenanceListResponse> {
        const payload: PayloadModel = { query: params }
        return await fetchApi().get('/api/maintenance', { payload })
    },

    async getDevices(): Promise<MaintenanceDeviceListResponse> {
        return await fetchApi().get('/api/devices')
    },

    async createMaintenance(params: MaintenanceSaveParams): Promise<MaintenanceDetailResponse> {
        const payload: PayloadModel = { body: params }
        return await fetchApi().post('/api/maintenance', { payload })
    },

    async updateMaintenance(id: number, params: MaintenanceSaveParams): Promise<MaintenanceDetailResponse> {
        const payload: PayloadModel = { body: params }
        return await fetchApi().put(`/api/maintenance/${id}`, { payload })
    },

    async deleteMaintenance(id: number): Promise<void> {
        await fetchApi().delete(`/api/maintenance/${id}`)
    },
}
