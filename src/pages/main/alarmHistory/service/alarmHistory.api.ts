import { fetchApi } from '@/http'
import type { PayloadModel } from '@/http/type'
import type {
    AlarmDetailResponse,
    AlarmDeviceListResponse,
    AlarmListResponse,
    AlarmSearchParams,
} from './alarmHistory.types'

export default {
    // 검색 조건(장비·등급·상태·기간)에 맞는 알림 이력 목록을 조회합니다.
    async getList(params: AlarmSearchParams = {}): Promise<AlarmListResponse> {
        const payload: PayloadModel = { query: params }
        return await fetchApi().get('/api/alarms', { payload })
    },

    // 필터 드롭다운용 장비 마스터 목록을 조회합니다.
    async getDevices(): Promise<AlarmDeviceListResponse> {
        return await fetchApi().get('/api/devices')
    },

    // 지정한 알림을 확인(ACKED) 처리합니다.
    async acknowledge(id: number): Promise<AlarmDetailResponse> {
        return await fetchApi().put(`/api/alarms/${id}/ack`)
    },

    // 지정한 알림을 조치 완료(RESOLVED) 상태로 변경합니다.
    async resolve(id: number): Promise<AlarmDetailResponse> {
        return await fetchApi().put(`/api/alarms/${id}/resolve`)
    },

    // 알림에 대응하는 신규 정비 이력을 생성하고 연계합니다.
    async createMaintenance(id: number): Promise<void> {
        await fetchApi().post(`/api/alarms/${id}/maintenance`)
    },
}
