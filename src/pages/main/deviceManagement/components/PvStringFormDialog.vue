<template>
    <BaseDialog
        :model-value="modelValue"
        :title="pvString ? '태양광 스트링 수정' : '태양광 스트링 등록'"
        width="720px"
        max-height="86vh"
        :button-types="['Cancel', 'Save']"
        @update:modelValue="emit('update:modelValue', $event)"
        @onCancel="closeDialog"
        @onSave="savePvString"
    >
        <el-form
            ref="formRef"
            class="pv-string-form"
            :model="form"
            :rules="rules"
            label-position="top"
            require-asterisk-position="right"
        >
            <section class="form-section">
                <h3>기본 정보</h3>
                <div class="form-line">
                    <el-form-item label="스트링명" prop="name">
                        <el-input v-model="form.name" placeholder="PV String #1" />
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
                <el-form-item label="설치 위치">
                    <el-input v-model="form.install_location" placeholder="설치 위치" />
                </el-form-item>
            </section>

            <section class="form-section">
                <h3>용량 정보</h3>
                <div class="form-line">
                    <el-form-item label="패널 수량">
                        <el-input-number v-model="form.panel_count" :min="0" style="width: 100%" />
                    </el-form-item>
                    <el-form-item label="패널 정격 용량(kW)">
                        <el-input-number v-model="form.panel_capacity_kw" :min="0" :precision="3" style="width: 100%" />
                    </el-form-item>
                    <el-form-item label="스트링 정격 용량(kW)">
                        <el-input-number v-model="form.rated_capacity_kw" :min="0" :precision="2" style="width: 100%" />
                    </el-form-item>
                </div>
                <el-form-item label="메모">
                    <el-input v-model="form.memo" type="textarea" :rows="3" placeholder="비고 또는 관리 메모" />
                </el-form-item>
            </section>
        </el-form>
    </BaseDialog>
</template>

<script setup lang="ts">
import { nextTick, reactive, ref, watch } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { BaseDialog } from '@/shared/components'
import type { PvStringItem, PvStringSaveParams } from '../service/deviceManagement.types'

const props = defineProps<{
    modelValue: boolean
    pvString: PvStringItem | null
}>()

const emit = defineEmits<{
    'update:modelValue': [value: boolean]
    save: [value: PvStringSaveParams]
}>()

const formRef = ref<FormInstance | null>(null)
const statusOptions = [
    { label: '정상', value: 'NORMAL' },
    { label: '주의', value: 'WARNING' },
    { label: '장애', value: 'FAULT' },
    { label: '점검', value: 'MAINTENANCE' },
]

const createDefaultForm = (): PvStringSaveParams => ({
    name: '',
    panel_count: null,
    panel_capacity_kw: null,
    rated_capacity_kw: null,
    install_location: null,
    status: 'NORMAL',
    is_active: true,
    memo: null,
})

const form = reactive<PvStringSaveParams>(createDefaultForm())
const rules: FormRules = {
    name: [{ required: true, message: '스트링명을 입력하세요.', trigger: 'blur' }],
    status: [{ required: true, message: '상태를 선택하세요.', trigger: 'change' }],
}

const normalizeText = (value: string | null) => value?.trim() || null

const syncForm = async () => {
    Object.assign(form, createDefaultForm())
    if (props.pvString) {
        Object.assign(form, {
            name: props.pvString.name,
            panel_count: props.pvString.panel_count,
            panel_capacity_kw: props.pvString.panel_capacity_kw,
            rated_capacity_kw: props.pvString.rated_capacity_kw,
            install_location: props.pvString.install_location,
            status: props.pvString.status,
            is_active: props.pvString.is_active,
            memo: props.pvString.memo,
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

const savePvString = async () => {
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
        install_location: normalizeText(form.install_location),
        memo: normalizeText(form.memo),
    })
}
</script>

<style scoped lang="scss">
.pv-string-form :deep(.el-form-item__label) {
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
