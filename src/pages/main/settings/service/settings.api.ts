import { fetchApi } from '@/http'
import type { ProjectConfigResponse, ProjectConfigSavePayload, SimulatorActionResponse } from './settings.types'

export default {
    async getProject(): Promise<ProjectConfigResponse> {
        return await fetchApi().get('/api/project')
    },
    async saveProject(body: ProjectConfigSavePayload): Promise<ProjectConfigResponse> {
        return await fetchApi().put('/api/project', { payload: { body } })
    },
    async generateToday(): Promise<SimulatorActionResponse> {
        return await fetchApi().post('/api/simulator/generate-today')
    },
    async generateLast7Days(): Promise<SimulatorActionResponse> {
        return await fetchApi().post('/api/simulator/generate-last-7-days')
    },
    async generateAlarms(): Promise<SimulatorActionResponse> {
        return await fetchApi().post('/api/simulator/generate-alarms')
    },
    async generateMaintenance(): Promise<SimulatorActionResponse> {
        return await fetchApi().post('/api/simulator/generate-maintenance')
    },
    async resetSimulator(): Promise<SimulatorActionResponse> {
        return await fetchApi().post('/api/simulator/reset')
    },
}
