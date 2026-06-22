<template>
    <BaseDialog
        :model-value="modelValue"
        :title="device ? 'Edit Camera' : 'Add Camera'"
        width="720px"
        max-height="90vh"
        :button-types="['Cancel', 'Save']"
        @update:modelValue="emit('update:modelValue', $event)"
        @onCancel="closeDialog"
        @onSave="saveDevice"
    >
        <el-form
            ref="formRef"
            class="device-form"
            :model="form"
            :rules="rules"
            label-width="150px"
            label-position="left"
        >
            <div class="form-section">
                <p class="form-section__title">Basic</p>
                <el-form-item label="Camera Name" prop="name">
                    <el-input v-model="form.name" placeholder="Enter camera name" />
                </el-form-item>
                <el-form-item label="IP Address" prop="ipAddress">
                    <el-input v-model="form.ipAddress" placeholder="192.168.0.10" />
                </el-form-item>
                <el-form-item label="RTSP URL" prop="rtspUrl">
                    <el-input v-model="form.rtspUrl" placeholder="rtsp://camera.local/stream" />
                </el-form-item>
                <el-form-item label="Location" prop="location">
                    <el-input v-model="form.location" placeholder="Enter installation location" />
                </el-form-item>
                <el-form-item label="Status" prop="status">
                    <el-select v-model="form.status" placeholder="Select status" style="width: 100%">
                        <el-option
                            v-for="item in statusOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        />
                    </el-select>
                </el-form-item>
                <el-form-item label="In Use" prop="activeFlag">
                    <el-switch v-model="form.activeFlag" active-value="Y" inactive-value="N" />
                </el-form-item>
            </div>

            <div class="form-section">
                <p class="form-section__title">Spec</p>
                <el-row class="spec-field-grid" :gutter="16">
                    <el-col :span="12">
                        <el-form-item label="Manufacturer" prop="manufacturer">
                            <el-input v-model="form.manufacturer" placeholder="Manufacturer" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="Model" prop="model">
                            <el-input v-model="form.model" placeholder="Model" />
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row class="spec-field-grid" :gutter="16">
                    <el-col :span="8">
                        <el-form-item label="Width" prop="resolutionWidth">
                            <el-input-number
                                v-model="form.resolutionWidth"
                                :min="320"
                                :max="7680"
                                style="width: 100%"
                            />
                        </el-form-item>
                    </el-col>
                    <el-col :span="8">
                        <el-form-item label="Height" prop="resolutionHeight">
                            <el-input-number
                                v-model="form.resolutionHeight"
                                :min="240"
                                :max="4320"
                                style="width: 100%"
                            />
                        </el-form-item>
                    </el-col>
                    <el-col :span="8">
                        <el-form-item label="FPS" prop="fps">
                            <el-input-number v-model="form.fps" :min="1" :max="120" style="width: 100%" />
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row class="spec-field-grid" :gutter="16">
                    <el-col :span="12">
                        <el-form-item label="Lens Type" prop="lensType">
                            <el-input v-model="form.lensType" placeholder="Wide Angle" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="Firmware" prop="firmwareVersion">
                            <el-input v-model="form.firmwareVersion" placeholder="1.0.0" />
                        </el-form-item>
                    </el-col>
                </el-row>
            </div>

            <div class="form-section">
                <p class="form-section__title">AI Features</p>
                <el-row :gutter="16">
                    <el-col :span="12">
                        <el-form-item label="Object Detection">
                            <el-switch v-model="form.objectDetectionEnabled" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="AI Analysis">
                            <el-switch v-model="form.aiAnalysisEnabled" />
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-form-item label="Detection Targets" prop="detectionTargets">
                    <el-checkbox-group v-model="form.detectionTargets">
                        <el-checkbox v-for="item in targetOptions" :key="item.value" :label="item.value">
                            {{ item.label }}
                        </el-checkbox>
                    </el-checkbox-group>
                </el-form-item>
            </div>
        </el-form>
    </BaseDialog>
</template>

<script lang="ts" setup>
import { nextTick, reactive, ref, watch } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { BaseDialog } from '@/shared/components'
import type { DetectionTarget, DeviceItem, DeviceSaveParams, DeviceStatus } from '../service/device.types'

const props = defineProps<{
    modelValue: boolean
    device: DeviceItem | null
}>()

const emit = defineEmits<{
    'update:modelValue': [value: boolean]
    save: [value: DeviceSaveParams]
}>()

const formRef = ref<FormInstance | null>(null)

const statusOptions: Array<{ label: DeviceStatus; value: DeviceStatus }> = [
    { label: 'Online', value: 'Online' },
    { label: 'Offline', value: 'Offline' },
    { label: 'Error', value: 'Error' },
    { label: 'Maintenance', value: 'Maintenance' },
]

const targetOptions: Array<{ label: string; value: DetectionTarget }> = [
    { label: 'Person', value: 'Person' },
    { label: 'Vehicle', value: 'Vehicle' },
    { label: 'Face', value: 'Face' },
    { label: 'Safety Helmet', value: 'SafetyHelmet' },
    { label: 'Fire', value: 'Fire' },
    { label: 'Smoke', value: 'Smoke' },
    { label: 'Intrusion', value: 'Intrusion' },
]

const createDefaultForm = (): DeviceSaveParams => ({
    name: '',
    ipAddress: '',
    rtspUrl: '',
    location: '',
    manufacturer: '',
    model: '',
    resolutionWidth: 1920,
    resolutionHeight: 1080,
    fps: 30,
    lensType: '',
    firmwareVersion: '',
    status: 'Offline',
    activeFlag: 'Y',
    objectDetectionEnabled: true,
    aiAnalysisEnabled: true,
    detectionTargets: ['Person', 'Vehicle'],
})

const form = reactive<DeviceSaveParams>(createDefaultForm())

const rules: FormRules = {
    name: [{ required: true, message: 'Please enter a camera name.', trigger: 'blur' }],
    ipAddress: [{ required: true, message: 'Please enter an IP address.', trigger: 'blur' }],
    rtspUrl: [{ required: true, message: 'Please enter an RTSP URL.', trigger: 'blur' }],
    location: [{ required: true, message: 'Please enter a location.', trigger: 'blur' }],
    manufacturer: [{ required: true, message: 'Please enter a manufacturer.', trigger: 'blur' }],
    model: [{ required: true, message: 'Please enter a model.', trigger: 'blur' }],
    detectionTargets: [{ required: true, message: 'Please select at least one detection target.', trigger: 'change' }],
}

const resetForm = () => {
    Object.assign(form, createDefaultForm())
}

const syncForm = async () => {
    resetForm()
    if (props.device) {
        Object.assign(form, {
            name: props.device.name,
            ipAddress: props.device.ipAddress,
            rtspUrl: props.device.rtspUrl,
            location: props.device.location,
            manufacturer: props.device.manufacturer,
            model: props.device.model,
            resolutionWidth: props.device.resolutionWidth,
            resolutionHeight: props.device.resolutionHeight,
            fps: props.device.fps,
            lensType: props.device.lensType,
            firmwareVersion: props.device.firmwareVersion,
            status: props.device.status,
            activeFlag: props.device.activeFlag,
            objectDetectionEnabled: props.device.objectDetectionEnabled,
            aiAnalysisEnabled: props.device.aiAnalysisEnabled,
            detectionTargets: [...props.device.detectionTargets],
        })
    }
    await nextTick()
    formRef.value?.clearValidate()
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

const saveDevice = async () => {
    if (!formRef.value) return
    const isValid = await formRef.value.validate().catch(() => false)
    if (!isValid) return
    emit('save', { ...form, detectionTargets: [...form.detectionTargets] })
}
</script>

<style lang="scss" scoped>
.device-form {
    max-height: 66vh;
    padding-right: 8px;
    overflow: auto;
}

.form-section {
    padding: 16px 0;
    border-bottom: 1px solid var(--border-color);
}

.form-section:first-child {
    padding-top: 0;
}

.form-section:last-child {
    border-bottom: none;
}

.form-section__title {
    margin: 0 0 14px;
    font-size: 15px;
    font-weight: 700;
    color: var(--text-color--primary);
}

.spec-field-grid :deep(.el-form-item) {
    display: block;
}

.spec-field-grid :deep(.el-form-item__label) {
    width: auto !important;
    height: auto;
    margin-bottom: 6px;
    justify-content: flex-start;
    line-height: 20px;
}

.spec-field-grid :deep(.el-form-item__content) {
    margin-left: 0 !important;
}
</style>
