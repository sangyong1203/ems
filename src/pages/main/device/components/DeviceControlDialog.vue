<template>
    <BaseDialog
        :model-value="modelValue"
        title="Camera Control"
        width="720px"
        max-height="90vh"
        :button-types="['Cancel', 'Save']"
        @update:modelValue="emit('update:modelValue', $event)"
        @onCancel="closeDialog"
        @onSave="saveSettings"
    >
        <div v-if="device" class="control-dialog">
            <div class="camera-summary">
                <div>
                    <p class="camera-summary__name">{{ device.name }}</p>
                    <p class="camera-summary__meta">{{ device.ipAddress }} · {{ device.location }}</p>
                </div>
                <CommonTag :label="device.status" :variant="device.status" />
            </div>

            <el-form class="control-form" :model="form" label-width="170px" label-position="left">
                <div class="form-section">
                    <p class="form-section__title">Stream</p>
                    <el-form-item label="Stream Enabled">
                        <el-switch v-model="form.streamEnabled" />
                    </el-form-item>
                    <el-form-item label="RTSP URL">
                        <el-input v-model="form.rtspUrl" />
                    </el-form-item>
                    <el-row class="control-field-grid" :gutter="16">
                        <el-col :span="8">
                            <el-form-item label="Width">
                                <el-input-number
                                    v-model="form.resolutionWidth"
                                    :min="320"
                                    :max="7680"
                                    style="width: 100%"
                                />
                            </el-form-item>
                        </el-col>
                        <el-col :span="8">
                            <el-form-item label="Height">
                                <el-input-number
                                    v-model="form.resolutionHeight"
                                    :min="240"
                                    :max="4320"
                                    style="width: 100%"
                                />
                            </el-form-item>
                        </el-col>
                        <el-col :span="8">
                            <el-form-item label="FPS">
                                <el-input-number v-model="form.fps" :min="1" :max="120" style="width: 100%" />
                            </el-form-item>
                        </el-col>
                    </el-row>
                </div>

                <div class="form-section">
                    <p class="form-section__title">Detection</p>
                    <el-form-item label="Object Detection">
                        <el-switch v-model="form.objectDetectionEnabled" />
                    </el-form-item>
                    <el-form-item label="Sensitivity">
                        <el-slider v-model="form.sensitivity" :min="1" :max="100" />
                    </el-form-item>
                    <el-form-item label="Confidence Threshold">
                        <el-slider v-model="form.confidenceThreshold" :min="1" :max="100" />
                    </el-form-item>
                    <el-form-item label="Detection Interval">
                        <el-input-number v-model="form.detectionInterval" :min="1" :max="60" />
                    </el-form-item>
                    <el-form-item label="Targets">
                        <el-checkbox-group v-model="form.detectionTargets">
                            <el-checkbox v-for="item in targetOptions" :key="item.value" :label="item.value">
                                {{ item.label }}
                            </el-checkbox>
                        </el-checkbox-group>
                    </el-form-item>
                </div>

                <div class="form-section">
                    <p class="form-section__title">AI Analysis</p>
                    <el-form-item label="AI Analysis">
                        <el-switch v-model="form.aiAnalysisEnabled" />
                    </el-form-item>
                    <el-form-item label="Analysis Model">
                        <el-select v-model="form.analysisModel" style="width: 100%">
                            <el-option label="Vision Object Analyzer" value="Vision Object Analyzer" />
                            <el-option label="Safety Monitoring Model" value="Safety Monitoring Model" />
                            <el-option label="Traffic Insight Model" value="Traffic Insight Model" />
                        </el-select>
                    </el-form-item>
                    <el-form-item label="Analysis Interval">
                        <el-input-number v-model="form.analysisInterval" :min="1" :max="300" />
                    </el-form-item>
                </div>
            </el-form>

            <div class="command-panel">
                <el-button plain @click="sendCommand('TEST_CONNECTION')">Test Connection</el-button>
                <el-button plain @click="sendCommand('SYNC_SETTINGS')">Sync Settings</el-button>
                <el-button plain @click="sendCommand('START_STREAM')">Start Stream</el-button>
                <el-button plain @click="sendCommand('STOP_STREAM')">Stop Stream</el-button>
                <el-button type="primary" @click="sendCommand('RESTART')">Restart</el-button>
            </div>
        </div>
    </BaseDialog>
</template>

<script lang="ts" setup>
import { reactive, watch } from 'vue'
import { BaseDialog, CommonTag } from '@/shared/components'
import type { DetectionTarget, DeviceCommand, DeviceItem, DeviceSettingParams } from '../service/device.types'

const props = defineProps<{
    modelValue: boolean
    device: DeviceItem | null
}>()

const emit = defineEmits<{
    'update:modelValue': [value: boolean]
    save: [value: DeviceSettingParams]
    command: [value: DeviceCommand]
}>()

const targetOptions: Array<{ label: string; value: DetectionTarget }> = [
    { label: 'Person', value: 'Person' },
    { label: 'Vehicle', value: 'Vehicle' },
    { label: 'Face', value: 'Face' },
    { label: 'Safety Helmet', value: 'SafetyHelmet' },
    { label: 'Fire', value: 'Fire' },
    { label: 'Smoke', value: 'Smoke' },
    { label: 'Intrusion', value: 'Intrusion' },
]

const form = reactive<DeviceSettingParams>({
    streamEnabled: false,
    rtspUrl: '',
    resolutionWidth: 1920,
    resolutionHeight: 1080,
    fps: 30,
    objectDetectionEnabled: true,
    sensitivity: 70,
    confidenceThreshold: 80,
    detectionInterval: 5,
    aiAnalysisEnabled: true,
    analysisModel: 'Vision Object Analyzer',
    analysisInterval: 10,
    detectionTargets: [],
})

const syncForm = () => {
    if (!props.device) return
    Object.assign(form, {
        streamEnabled: props.device.streamEnabled,
        rtspUrl: props.device.rtspUrl,
        resolutionWidth: props.device.resolutionWidth,
        resolutionHeight: props.device.resolutionHeight,
        fps: props.device.fps,
        objectDetectionEnabled: props.device.objectDetectionEnabled,
        sensitivity: props.device.sensitivity,
        confidenceThreshold: props.device.confidenceThreshold,
        detectionInterval: props.device.detectionInterval,
        aiAnalysisEnabled: props.device.aiAnalysisEnabled,
        analysisModel: props.device.analysisModel,
        analysisInterval: props.device.analysisInterval,
        detectionTargets: [...props.device.detectionTargets],
    })
}

watch(
    () => props.modelValue,
    value => {
        if (value) {
            syncForm()
        }
    },
)

const closeDialog = () => {
    emit('update:modelValue', false)
}

const saveSettings = () => {
    emit('save', { ...form, detectionTargets: [...form.detectionTargets] })
}

const sendCommand = (command: DeviceCommand) => {
    emit('command', command)
}
</script>

<style lang="scss" scoped>
.control-dialog {
    max-height: 66vh;
    padding-right: 8px;
    overflow: auto;
}

.camera-summary {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 16px;
    margin-bottom: 16px;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    background: var(--surface-control-color);
}

.camera-summary__name {
    margin: 0;
    font-size: 17px;
    font-weight: 700;
    color: var(--text-color--primary);
}

.camera-summary__meta {
    margin: 6px 0 0;
    color: var(--text-color--secondary);
}

.form-section {
    padding: 16px 0;
    border-bottom: 1px solid var(--border-color);
}

.form-section__title {
    margin: 0 0 14px;
    font-size: 15px;
    font-weight: 700;
    color: var(--text-color--primary);
}

.command-panel {
    display: flex;
    flex-wrap: wrap;
    padding-top: 16px;
}

.control-field-grid :deep(.el-form-item) {
    display: block;
}

.control-field-grid :deep(.el-form-item__label) {
    width: auto !important;
    height: auto;
    margin-bottom: 6px;
    justify-content: flex-start;
    line-height: 20px;
}

.control-field-grid :deep(.el-form-item__content) {
    margin-left: 0 !important;
}
</style>
