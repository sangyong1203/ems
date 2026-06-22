<template>
    <BaseDialog
        :model-value="modelValue"
        :title="maintenance ? '정비 수정' : '정비 등록'"
        width="860px"
        max-height="90vh"
        :button-types="['Cancel', 'Save']"
        @update:modelValue="emit('update:modelValue', $event)"
        @onCancel="closeDialog"
        @onSave="saveMaintenance"
    >
        <el-form
            ref="formRef"
            class="maintenance-form"
            :model="form"
            :rules="rules"
            label-position="top"
            require-asterisk-position="right"
        >
            <section class="form-section">
                <h3>기본 정보</h3>
                <div class="form-line">
                    <el-form-item label="대상 장비" prop="device_id">
                        <el-select v-model="form.device_id" placeholder="대상 장비" style="width: 100%">
                            <el-option
                                v-for="device in deviceOptions"
                                :key="device.id"
                                :label="device.name"
                                :value="device.id"
                            />
                        </el-select>
                    </el-form-item>
                    <el-form-item label="정비 유형" prop="maintenance_type">
                        <el-select v-model="form.maintenance_type" placeholder="정비 유형" style="width: 100%">
                            <el-option
                                v-for="item in maintenanceTypeOptions"
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
                </div>

                <el-form-item label="정비 제목" prop="title">
                    <el-input v-model="form.title" placeholder="정비 제목을 입력하세요" />
                </el-form-item>

                <div class="form-line">
                    <el-form-item label="정비일">
                        <el-date-picker
                            v-model="form.maintenance_date"
                            value-format="YYYY-MM-DD"
                            type="date"
                            style="width: 100%"
                        />
                    </el-form-item>
                    <el-form-item label="다음 점검 예정일">
                        <el-date-picker
                            v-model="form.next_maintenance_date"
                            value-format="YYYY-MM-DD"
                            type="date"
                            style="width: 100%"
                        />
                    </el-form-item>
                    <el-form-item label="담당자">
                        <el-input v-model="form.manager_name" placeholder="담당자" />
                    </el-form-item>
                </div>
            </section>

            <section class="form-section">
                <h3>정비 내용</h3>
                <el-form-item label="내용">
                    <el-input v-model="form.description" type="textarea" :rows="4" placeholder="점검 또는 장애 내용" />
                </el-form-item>
                <el-form-item label="조치 내용">
                    <el-input v-model="form.action_taken" type="textarea" :rows="4" placeholder="조치 내역" />
                </el-form-item>
                <el-form-item label="비고">
                    <el-input v-model="form.memo" type="textarea" :rows="3" placeholder="비고" />
                </el-form-item>
            </section>
        </el-form>
    </BaseDialog>
</template>

<script setup lang="ts">
import { nextTick, reactive, ref, watch } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { BaseDialog } from '@/shared/components'
import type {
    MaintenanceDeviceOption,
    MaintenanceItem,
    MaintenanceSaveParams,
} from '../service/maintenanceManagement.types'

const props = defineProps<{
    modelValue: boolean
    maintenance: MaintenanceItem | null
    deviceOptions: MaintenanceDeviceOption[]
    maintenanceTypeOptions: { label: string; value: string }[]
    statusOptions: { label: string; value: string }[]
}>()

const emit = defineEmits<{
    'update:modelValue': [value: boolean]
    save: [value: MaintenanceSaveParams]
}>()

const formRef = ref<FormInstance | null>(null)

const createDefaultForm = (): MaintenanceSaveParams => ({
    device_id: null,
    alarm_id: null,
    maintenance_type: '정기점검',
    title: '',
    description: null,
    action_taken: null,
    status: 'SCHEDULED',
    maintenance_date: null,
    next_maintenance_date: null,
    manager_name: null,
    memo: null,
})

const form = reactive<MaintenanceSaveParams>(createDefaultForm())

const rules: FormRules = {
    device_id: [{ required: true, message: '대상 장비를 선택하세요.', trigger: 'change' }],
    maintenance_type: [{ required: true, message: '정비 유형을 선택하세요.', trigger: 'change' }],
    title: [{ required: true, message: '정비 제목을 입력하세요.', trigger: 'blur' }],
    status: [{ required: true, message: '상태를 선택하세요.', trigger: 'change' }],
}

const normalizeText = (value: string | null | undefined) => value?.trim() || null

const resetForm = () => {
    Object.assign(form, createDefaultForm())
}

const syncForm = async () => {
    resetForm()
    if (props.maintenance) {
        Object.assign(form, {
            device_id: props.maintenance.device_id,
            alarm_id: props.maintenance.alarm_id,
            maintenance_type: props.maintenance.maintenance_type,
            title: props.maintenance.title,
            description: props.maintenance.description,
            action_taken: props.maintenance.action_taken,
            status: props.maintenance.status,
            maintenance_date: props.maintenance.maintenance_date,
            next_maintenance_date: props.maintenance.next_maintenance_date,
            manager_name: props.maintenance.manager_name,
            memo: props.maintenance.memo,
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

const saveMaintenance = async () => {
    if (!formRef.value) {
        return
    }
    const isValid = await formRef.value.validate().catch(() => false)
    if (!isValid) {
        return
    }
    emit('save', {
        ...form,
        title: form.title.trim(),
        description: normalizeText(form.description),
        action_taken: normalizeText(form.action_taken),
        manager_name: normalizeText(form.manager_name),
        memo: normalizeText(form.memo),
    })
}
</script>

<style scoped lang="scss">
.maintenance-form :deep(.el-form-item__label) {
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
</style>
