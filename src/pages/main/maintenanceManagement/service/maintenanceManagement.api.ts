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
    // getList 검색 조건 기반 정비 이력 목록 조회
    async getList(params: MaintenanceSearchParams = {}): Promise<MaintenanceListResponse> {
        const payload: PayloadModel = { query: params }
        return await fetchApi().get('/api/maintenance', { payload })
    },

    // getDevices 정비 대상 장비 목록 조회
    async getDevices(): Promise<MaintenanceDeviceListResponse> {
        return await fetchApi().get('/api/devices')
    },

    // createMaintenance 신규 정비 이력 등록
    async createMaintenance(params: MaintenanceSaveParams): Promise<MaintenanceDetailResponse> {
        const payload: PayloadModel = { body: params }
        return await fetchApi().post('/api/maintenance', { payload })
    },

    // updateMaintenance 기존 정비 이력 정보 수정
    async updateMaintenance(id: number, params: MaintenanceSaveParams): Promise<MaintenanceDetailResponse> {
        const payload: PayloadModel = { body: params }
        return await fetchApi().put(`/api/maintenance/${id}`, { payload })
    },

    // deleteMaintenance 정비 이력 삭제
    async deleteMaintenance(id: number): Promise<void> {
        await fetchApi().delete(`/api/maintenance/${id}`)
    },
}
