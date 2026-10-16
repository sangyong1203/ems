import { fetchApi } from '@/http'
import type { ProjectConfigResponse, ProjectConfigSavePayload, SimulatorActionResponse } from './settings.types'

export default {
    // 프로젝트 환경설정 조회
    async getProject(): Promise<ProjectConfigResponse> {
        return await fetchApi().get('/api/project')
    },
    // 프로젝트 환경설정 수정 저장
    async saveProject(body: ProjectConfigSavePayload): Promise<ProjectConfigResponse> {
        return await fetchApi().put('/api/project', { payload: { body } })
    },
    // 오늘 가상 텔레메트리 데이터 생성
    async generateToday(): Promise<SimulatorActionResponse> {
        return await fetchApi().post('/api/simulator/generate-today')
    },
    // 최근 7일 통계용 가상 데이터 생성
    async generateLast7Days(): Promise<SimulatorActionResponse> {
        return await fetchApi().post('/api/simulator/generate-last-7-days')
    },
    // 가상 알림 데이터 생성
    async generateAlarms(): Promise<SimulatorActionResponse> {
        return await fetchApi().post('/api/simulator/generate-alarms')
    },
    // 가상 정비 일정 데이터 생성
    async generateMaintenance(): Promise<SimulatorActionResponse> {
        return await fetchApi().post('/api/simulator/generate-maintenance')
    },
    // 가상 시뮬레이터 데이터 전체 초기화
    async resetSimulator(): Promise<SimulatorActionResponse> {
        return await fetchApi().post('/api/simulator/reset')
    },
}
