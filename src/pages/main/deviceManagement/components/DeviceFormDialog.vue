<template>
    <BaseDialog
        :model-value="modelValue"
        :title="device ? '장비 수정' : '장비 등록'"
        width="880px"
        max-height="90vh"
        :button-types="['Cancel', 'Save']"
        @update:modelValue="emit('update:modelValue', $event)"
        @onCancel="closeDialog"
        @onSave="saveDevice"
    >
        <el-form
            ref="formRef"
            class="device-management-form"
            :model="form"
            :rules="rules"
            label-position="top"
            require-asterisk-position="right"
        >
            <section class="form-section">
                <h3>기본 정보</h3>
                <div class="form-line">
                    <el-form-item label="장비 유형" prop="device_type">
                        <el-select v-model="form.device_type" placeholder="장비 유형" style="width: 100%">
                            <el-option
                                v-for="item in deviceTypeOptions"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                            />
                        </el-select>
                    </el-form-item>
                    <el-form-item label="상태" prop="status">
                        <el-select v-model="form.status" placeholder="상태" style="width: 100%">
                            <el-option
                                v-for="item in statusOptions"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                            />
                        </el-select>
                    </el-form-item>
                    <el-form-item label="운영 활성화">
                        <el-switch v-model="form.is_active" />
                    </el-form-item>
                </div>
                <el-form-item label="장비명" prop="name">
                    <el-input v-model="form.name" placeholder="장비명을 입력하세요" />
                </el-form-item>
                <div class="form-line">
                    <el-form-item label="제조사">
                        <el-input v-model="form.manufacturer" placeholder="제조사" />
                    </el-form-item>
                    <el-form-item label="모델명">
                        <el-input v-model="form.model_name" placeholder="모델명" />
                    </el-form-item>
                </div>
                <div class="form-line">
                    <el-form-item label="시리얼 번호">
                        <el-input v-model="form.serial_number" placeholder="Serial No." />
                    </el-form-item>
                    <el-form-item label="설치 위치">
                        <el-input v-model="form.install_location" placeholder="설치 위치" />
                    </el-form-item>
                </div>
                <div class="form-line">
                    <el-form-item :label="capacityLabel">
                        <el-input-number v-model="form.capacity" :min="0" :precision="1" style="width: 100%" />
                    </el-form-item>
                    <el-form-item :label="capacityUnitLabel">
                        <el-input v-model="form.capacity_unit" :placeholder="capacityUnitPlaceholder" />
                    </el-form-item>
                </div>
            </section>

            <section class="form-section">
                <h3>통신 정보</h3>
                <div class="form-line">
                    <el-form-item label="통신 방식">
                        <el-input v-model="form.communication_type" placeholder="Modbus TCP" />
                    </el-form-item>
                    <el-form-item label="Protocol">
                        <el-input v-model="form.protocol" placeholder="Modbus" />
                    </el-form-item>
                </div>
                <div class="form-line">
                    <el-form-item label="IP 주소">
                        <el-input v-model="form.ip_address" placeholder="예: 192.168.0.10" />
                    </el-form-item>
                    <el-form-item label="Port">
                        <el-input v-model="form.port" placeholder="예: 502" />
                    </el-form-item>
                    <el-form-item label="Slave ID">
                        <el-input v-model="form.slave_id" placeholder="예: 1" />
                    </el-form-item>
                </div>
            </section>

            <section class="form-section">
                <h3>보증/관리 정보</h3>
                <div class="form-line">
                    <el-form-item label="설치일">
                        <el-date-picker
                            v-model="form.install_date"
                            value-format="YYYY-MM-DD"
                            type="date"
                            style="width: 100%"
                        />
                    </el-form-item>
                    <el-form-item label="보증 시작일">
                        <el-date-picker
                            v-model="form.warranty_start_date"
                            value-format="YYYY-MM-DD"
                            type="date"
                            style="width: 100%"
                        />
                    </el-form-item>
                    <el-form-item label="보증 종료일">
                        <el-date-picker
                            v-model="form.warranty_end_date"
                            value-format="YYYY-MM-DD"
                            type="date"
                            style="width: 100%"
                        />
                    </el-form-item>
                </div>
                <div class="form-line">
                    <el-form-item label="업체명">
                        <el-input v-model="form.vendor_name" placeholder="유지보수 업체" />
                    </el-form-item>
                    <el-form-item label="연락처">
                        <el-input v-model="form.vendor_contact" placeholder="연락처" />
                    </el-form-item>
                </div>
                <el-form-item label="메모">
                    <el-input v-model="form.memo" type="textarea" :rows="3" placeholder="비고 또는 관리 메모" />
                </el-form-item>
            </section>

            <section v-if="form.device_type === 'INVERTER'" class="form-section">
                <h3>태양광 스트링 연결</h3>
                <div class="pv-string-link-editor">
                    <div class="pv-string-link-editor__controls">
                        <el-select v-model="selectedPvStringId" placeholder="미연결 스트링 선택" filterable>
                            <el-option
                                v-for="item in availablePvStrings"
                                :key="item.id"
                                :label="item.name"
                                :value="item.id"
                            />
                        </el-select>
                        <el-button type="primary" :disabled="!selectedPvStringId" @click="addPvStringLink">
                            추가
                        </el-button>
                    </div>

                    <div v-if="form.pv_string_links.length" class="pv-string-link-list">
                        <article v-for="link in form.pv_string_links" :key="link.pv_string_id">
                            <strong>{{ pvStringName(link.pv_string_id) }}</strong>
                            <el-input-number v-model="link.mppt_no" :min="1" controls-position="right" />
                            <el-input-number v-model="link.channel_no" :min="1" controls-position="right" />
                            <button type="button" @click="removePvStringLink(link.pv_string_id)">삭제</button>
                        </article>
                    </div>
                    <p v-else class="pv-string-link-editor__empty">연결된 태양광 스트링이 없습니다.</p>
                </div>
            </section>
        </el-form>
    </BaseDialog>
</template>

<script setup lang="ts">
import { computed, nextTick, reactive, ref, watch } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { BaseDialog } from '@/shared/components'
import type { DeviceItem, DeviceSaveParams, PvStringItem } from '../service/deviceManagement.types'

const props = defineProps<{
    modelValue: boolean
    device: DeviceItem | null
    pvStrings: PvStringItem[]
}>()

const emit = defineEmits<{
    'update:modelValue': [value: boolean]
    save: [value: DeviceSaveParams]
}>()

const formRef = ref<FormInstance | null>(null)
const selectedPvStringId = ref<number | null>(null)

const deviceTypeOptions = [
    { label: '인버터', value: 'INVERTER' },
    { label: 'PCS', value: 'PCS' },
    { label: '배터리 뱅크', value: 'ESS_BATTERY' },
    { label: '배터리 랙', value: 'BATTERY_RACK' },
    { label: 'BMS', value: 'BMS' },
    { label: 'AC 배전반', value: 'AC_PANEL' },
    { label: '계통 계량기', value: 'GRID_METER' },
    { label: '부하 계량기', value: 'LOAD_METER' },
    { label: '기상 센서', value: 'WEATHER_SENSOR' },
    { label: '일반 센서', value: 'SENSOR' },
    { label: '기타', value: 'ETC' },
]

const statusOptions = [
    { label: '정상', value: 'NORMAL' },
    { label: '주의', value: 'WARNING' },
    { label: '장애', value: 'FAULT' },
    { label: '점검', value: 'MAINTENANCE' },
]

const createDefaultForm = (): DeviceSaveParams => ({
    device_type: 'INVERTER',
    name: '',
    manufacturer: null,
    model_name: null,
    serial_number: null,
    capacity: null,
    capacity_unit: 'kW',
    install_location: null,
    install_date: null,
    communication_type: 'Modbus TCP',
    ip_address: null,
    port: 502,
    slave_id: null,
    protocol: 'Modbus',
    status: 'NORMAL',
    is_active: true,
    warranty_start_date: null,
    warranty_end_date: null,
    vendor_name: null,
    vendor_contact: null,
    memo: null,
    pv_string_links: [],
})

const form = reactive<DeviceSaveParams>(createDefaultForm())

const isSensorType = computed(() => ['WEATHER_SENSOR', 'SENSOR'].includes(form.device_type))
const capacityLabel = computed(() => (isSensorType.value ? '측정 범위' : '정격 용량'))
const capacityUnitLabel = computed(() => (isSensorType.value ? '측정 단위' : '용량 단위'))
const capacityUnitPlaceholder = computed(() => (isSensorType.value ? '°C, W/m², V' : 'kW, kWh'))
const linkedPvStringIds = computed(() => form.pv_string_links.map(item => item.pv_string_id))
const availablePvStrings = computed(() =>
    props.pvStrings.filter(item => !linkedPvStringIds.value.includes(item.id) && !item.inverter_device_id),
)

const rules: FormRules = {
    device_type: [{ required: true, message: '장비 유형을 선택하세요.', trigger: 'change' }],
    name: [{ required: true, message: '장비명을 입력하세요.', trigger: 'blur' }],
    status: [{ required: true, message: '상태를 선택하세요.', trigger: 'change' }],
}

const normalizeText = (value: string | null) => {
    return value?.trim() || null
}

const normalizeNumber = (value: number | string | null) => {
    if (value === null || value === '') {
        return null
    }
    return Number(value)
}

const resetForm = () => {
    Object.assign(form, createDefaultForm())
}

const syncForm = async () => {
    resetForm()
    if (props.device) {
        Object.assign(form, {
            device_type: props.device.device_type,
            name: props.device.name,
            manufacturer: props.device.manufacturer,
            model_name: props.device.model_name,
            serial_number: props.device.serial_number,
            capacity: props.device.capacity,
            capacity_unit: props.device.capacity_unit,
            install_location: props.device.install_location,
            install_date: props.device.install_date,
            communication_type: props.device.communication_type,
            ip_address: props.device.ip_address,
            port: props.device.port,
            slave_id: props.device.slave_id,
            protocol: props.device.protocol,
            status: props.device.status,
            is_active: props.device.is_active,
            warranty_start_date: props.device.warranty_start_date,
            warranty_end_date: props.device.warranty_end_date,
            vendor_name: props.device.vendor_name,
            vendor_contact: props.device.vendor_contact,
            memo: props.device.memo,
            pv_string_links: props.device.pv_string_links.map(link => ({ ...link })),
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

const pvStringName = (pvStringId: number) => {
    const pvString = props.pvStrings.find(item => item.id === pvStringId)
    const link = form.pv_string_links.find(item => item.pv_string_id === pvStringId)
    return pvString?.name || link?.pv_string_name || `PV String #${pvStringId}`
}

const addPvStringLink = () => {
    if (!selectedPvStringId.value || linkedPvStringIds.value.includes(selectedPvStringId.value)) {
        return
    }
    form.pv_string_links.push({
        pv_string_id: selectedPvStringId.value,
        mppt_no: null,
        channel_no: null,
    })
    selectedPvStringId.value = null
}

const removePvStringLink = (pvStringId: number) => {
    form.pv_string_links = form.pv_string_links.filter(item => item.pv_string_id !== pvStringId)
}

const saveDevice = async () => {
    if (!formRef.value) {
        return
    }
    const isValid = await formRef.value.validate().catch(() => false)
    if (!isValid) {
        return
    }
    emit('save', {
        ...form,
        name: form.name.trim(),
        manufacturer: normalizeText(form.manufacturer),
        model_name: normalizeText(form.model_name),
        serial_number: normalizeText(form.serial_number),
        capacity_unit: normalizeText(form.capacity_unit),
        install_location: normalizeText(form.install_location),
        communication_type: normalizeText(form.communication_type),
        ip_address: normalizeText(form.ip_address),
        port: normalizeNumber(form.port),
        slave_id: normalizeNumber(form.slave_id),
        protocol: normalizeText(form.protocol),
        vendor_name: normalizeText(form.vendor_name),
        vendor_contact: normalizeText(form.vendor_contact),
        memo: normalizeText(form.memo),
        pv_string_links: form.device_type === 'INVERTER' ? form.pv_string_links : [],
    })
}
</script>

<style scoped lang="scss">
.device-management-form :deep(.el-form-item__label) {
    color: var(--text-color--secondary);
    font-size: 14px;
}

.form-section {
    padding: 18px 0 4px;
    border-bottom: 1px solid var(--border-color);
}

.form-section:first-child {
    padding-top: 0;
}

.form-section:last-child {
    border-bottom: 0;
}

.form-section h3 {
    margin: 0 0 16px;
    color: var(--text-color--primary);
    font-size: 15px;
}

.form-line {
    display: flex;
    align-items: flex-start;
    gap: 18px;
}

.form-line :deep(.el-form-item) {
    flex: 1 1 0;
    min-width: 0;
}

.pv-string-link-editor {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.pv-string-link-editor__controls {
    display: flex;
    gap: 10px;
}

.pv-string-link-editor__controls .el-select {
    flex: 1;
}

.pv-string-link-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.pv-string-link-list article {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    border: 1px solid rgba(21, 224, 183, 0.22);
    border-radius: 6px;
    background: rgba(21, 224, 183, 0.06);
}

.pv-string-link-list strong {
    flex: 1;
    font-size: 13px;
}

.pv-string-link-list :deep(.el-input-number) {
    width: 112px;
}

.pv-string-link-list button {
    border: 0;
    color: #ff6b78;
    cursor: pointer;
    background: transparent;
}

.pv-string-link-editor__empty {
    margin: 0;
    color: var(--text-color--secondary);
    font-size: 13px;
}
</style>
