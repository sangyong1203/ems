<template>
    <div class="settings-form">
        <p class="settings-form__description">대시보드 및 모니터링 화면의 데이터 자동 갱신 간격을 설정합니다.</p>
        <ContentBlock>
            <div class="monitoring-setting-list">
                <DropdownList
                    v-for="item in monitoringSettings"
                    :key="item.key"
                    v-model="form[item.key]"
                    class="settings-refresh-select"
                    :label="item.label"
                    label-position="left"
                    label-width="120px"
                    selection-width="100px"
                    option-label="label"
                    option-value="value"
                    :clearable="false"
                    :list="refreshIntervalOptions"
                />
            </div>
        </ContentBlock>
        <div class="settings-footer">
            <el-button type="primary" :loading="saving" @click="$emit('save')">저장</el-button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { DropdownList } from '@/shared/components'
import type { ProjectConfigSavePayload } from '../service/settings.types'
import { toRefs } from 'vue'

type RefreshIntervalKey =
    | 'dashboard_refresh_interval'
    | 'solar_refresh_interval'
    | 'ess_refresh_interval'
    | 'power_flow_refresh_interval'
    | 'trend_refresh_interval'

const props = defineProps<{
    form: ProjectConfigSavePayload
    saving: boolean
}>()
const { form, saving } = toRefs(props)

defineEmits<{
    save: []
}>()

const refreshIntervalOptions = [
    { label: '3초', value: 3000 },
    { label: '5초', value: 5000 },
    { label: '10초', value: 10000 },
    { label: '30초', value: 30000 },
    { label: '1분', value: 60000 },
    { label: '5분', value: 300000 },
    { label: '10분', value: 600000 },
]

const monitoringSettings: Array<{ key: RefreshIntervalKey; label: string }> = [
    { key: 'dashboard_refresh_interval', label: '대시보드 갱신 주기' },
    { key: 'solar_refresh_interval', label: '태양광 갱신 주기' },
    { key: 'ess_refresh_interval', label: 'ESS 갱신 주기' },
    { key: 'power_flow_refresh_interval', label: '전력 흐름 갱신 주기' },
    { key: 'trend_refresh_interval', label: '트렌드 갱신 주기' },
]
</script>

<style scoped lang="scss">
.settings-form {
    max-width: 980px;
}

.settings-form__description {
    margin: 0 0 18px;
    color: var(--text-color--secondary);
    font-size: 13px;
}

.monitoring-setting-list {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 18px;
}

.settings-footer {
    display: flex;
    justify-content: flex-end;
    max-width: 980px;
    padding-top: 14px;
}
</style>
