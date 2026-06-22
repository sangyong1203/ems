import type { APIResponse } from '@/http/type'

export type DeviceStatus = 'Online' | 'Offline' | 'Error' | 'Maintenance'

export type DetectionTarget =
    | 'Person'
    | 'Vehicle'
    | 'Face'
    | 'SafetyHelmet'
    | 'Fire'
    | 'Smoke'
    | 'Intrusion'

export type DeviceCommand = 'RESTART' | 'START_STREAM' | 'STOP_STREAM' | 'SYNC_SETTINGS' | 'TEST_CONNECTION'

export type DeviceItem = {
    id: number
    name: string
    ipAddress: string
    rtspUrl: string
    location: string
    manufacturer: string
    model: string
    resolutionWidth: number
    resolutionHeight: number
    fps: number
    lensType: string
    firmwareVersion: string
    status: DeviceStatus
    activeFlag: 'Y' | 'N'
    objectDetectionEnabled: boolean
    aiAnalysisEnabled: boolean
    detectionTargets: DetectionTarget[]
    sensitivity: number
    confidenceThreshold: number
    detectionInterval: number
    analysisModel: string
    analysisInterval: number
    streamEnabled: boolean
    lastSeenAt: string
    createdAt: string
    updatedAt: string
}

export type DeviceSearchParams = {
    keyword: string
    status: DeviceStatus | ''
    model: string
    detectionEnabled: '' | 'Y' | 'N'
    aiAnalysisEnabled: '' | 'Y' | 'N'
    pageNumber: number
    pageSize: number
}

export type DeviceSaveParams = Pick<
    DeviceItem,
    | 'name'
    | 'ipAddress'
    | 'rtspUrl'
    | 'location'
    | 'manufacturer'
    | 'model'
    | 'resolutionWidth'
    | 'resolutionHeight'
    | 'fps'
    | 'lensType'
    | 'firmwareVersion'
    | 'status'
    | 'activeFlag'
    | 'objectDetectionEnabled'
    | 'aiAnalysisEnabled'
    | 'detectionTargets'
>

export type DeviceSettingParams = Pick<
    DeviceItem,
    | 'streamEnabled'
    | 'rtspUrl'
    | 'resolutionWidth'
    | 'resolutionHeight'
    | 'fps'
    | 'objectDetectionEnabled'
    | 'sensitivity'
    | 'confidenceThreshold'
    | 'detectionInterval'
    | 'aiAnalysisEnabled'
    | 'analysisModel'
    | 'analysisInterval'
    | 'detectionTargets'
>

export type DeviceCommandParams = {
    command: DeviceCommand
}

export type DeviceListResponse = APIResponse<{
    list: DeviceItem[]
    totalCount: number
}>

export type DeviceDetailResponse = APIResponse<DeviceItem>

export type DeviceCommandResponse = APIResponse<{
    command: DeviceCommand
    accepted: boolean
    executedAt: string
}>
