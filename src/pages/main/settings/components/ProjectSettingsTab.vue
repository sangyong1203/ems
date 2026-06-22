<template>
    <el-form class="settings-form" label-position="top">
        <div class="settings-form__row">
            <el-form-item label="프로젝트명">
                <el-input v-model="form.project_name" />
            </el-form-item>
            <el-form-item label="현장명">
                <el-input v-model="form.site_name" />
            </el-form-item>
        </div>
        <div class="settings-form__row">
            <el-form-item label="고객사">
                <el-input v-model="form.customer_name" />
            </el-form-item>
            <el-form-item label="시공사">
                <el-input v-model="form.contractor_name" />
            </el-form-item>
        </div>
        <el-form-item label="설치 위치">
            <el-input v-model="form.location" />
        </el-form-item>
        <el-form-item label="시스템명">
            <el-input v-model="form.system_name" />
        </el-form-item>
    </el-form>
    <div class="settings-footer">
        <el-button type="primary" :loading="saving" @click="$emit('save')">저장</el-button>
    </div>
</template>

<script setup lang="ts">
import { toRefs } from 'vue'
import type { ProjectConfigSavePayload } from '../service/settings.types'

const props = defineProps<{
    form: ProjectConfigSavePayload
    saving: boolean
}>()
const { form, saving } = toRefs(props)
defineEmits<{
    save: []
}>()
</script>

<style scoped lang="scss">
.settings-form {
    max-width: 980px;
}

.settings-form__row {
    display: flex;
    gap: 18px;
}

.settings-form__row > * {
    flex: 1;
    min-width: 0;
}

.settings-form :deep(.el-form-item) {
    margin-bottom: 20px;
}

.settings-form :deep(.el-form-item__label) {
    color: var(--text-color--secondary);
}

.settings-form :deep(.el-input__wrapper) {
    background: var(--common-control-bg-color);
    box-shadow: 0 0 0 1px var(--common-control-border-color) inset;
}

.settings-footer {
    display: flex;
    justify-content: flex-end;
    max-width: 980px;
    padding-top: 14px;
}

@media (max-width: 760px) {
    .settings-form__row {
        flex-direction: column;
        gap: 0;
    }
}
</style>
