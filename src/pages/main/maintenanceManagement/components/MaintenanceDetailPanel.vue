<template>
    <GlassPanel class="maintenance-detail-panel" title="정비 상세" :value="statusLabel">
        <template v-if="maintenance">
            <div class="maintenance-detail-panel__summary">
                <span class="maintenance-detail-panel__type">{{ maintenance.maintenance_type }}</span>
                <h3>{{ maintenance.title }}</h3>
                <p>{{ maintenance.device_name || '대상 장비 미지정' }}</p>
            </div>

            <KeyValueList :items="basicItems" />

            <section class="maintenance-detail-panel__section">
                <h4>정비 내용</h4>
                <p>{{ maintenance.description || '-' }}</p>
            </section>

            <section class="maintenance-detail-panel__section">
                <h4>조치 내용</h4>
                <p>{{ maintenance.action_taken || '-' }}</p>
            </section>

            <section class="maintenance-detail-panel__section">
                <h4>비고</h4>
                <p>{{ maintenance.memo || '-' }}</p>
            </section>
        </template>

        <div v-else class="maintenance-detail-panel__empty">정비 이력을 선택하세요.</div>
    </GlassPanel>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { GlassPanel, KeyValueList } from '@/shared/components'
import type { MaintenanceItem } from '../service/maintenanceManagement.types'

const props = defineProps<{
    maintenance: MaintenanceItem | null
}>()

const statusLabels: Record<string, string> = {
    SCHEDULED: '예정',
    IN_PROGRESS: '진행중',
    COMPLETED: '완료',
    HOLD: '보류',
    CANCELED: '취소',
}

const emptyText = (value: string | null | undefined) => value || '-'

const statusLabel = computed(() => {
    if (!props.maintenance) {
        return ''
    }
    return statusLabels[props.maintenance.status] || props.maintenance.status
})

const basicItems = computed(() => {
    if (!props.maintenance) {
        return []
    }
    return [
        { label: '정비일', value: emptyText(props.maintenance.maintenance_date) },
        { label: '다음 점검일', value: emptyText(props.maintenance.next_maintenance_date) },
        { label: '담당자', value: emptyText(props.maintenance.manager_name) },
        { label: '장비 유형', value: emptyText(props.maintenance.device_type) },
    ]
})
</script>

<style scoped lang="scss">
.maintenance-detail-panel {
    flex: 0 0 24.4%;
}

.maintenance-detail-panel__summary {
    padding-bottom: 16px;
    margin-bottom: 16px;
    border-bottom: 1px solid var(--border-color);
}

.maintenance-detail-panel__type {
    color: var(--text-color--secondary);
    font-size: 13px;
    font-weight: 700;
}

.maintenance-detail-panel__summary h3 {
    margin: 10px 0 6px;
    color: #ffffff;
    font-size: 26px;
    line-height: 32px;
}

.maintenance-detail-panel__summary p {
    margin: 0;
    color: var(--text-color--secondary);
    font-size: 14px;
}

.maintenance-detail-panel__section {
    padding-top: 16px;
}

.maintenance-detail-panel__section h4 {
    margin: 0 0 8px;
    color: var(--text-color--primary);
    font-size: 14px;
}

.maintenance-detail-panel__section p {
    min-height: 44px;
    margin: 0;
    color: var(--text-color--secondary);
    font-size: 14px;
    line-height: 22px;
}

.maintenance-detail-panel__empty {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 240px;
    color: var(--text-color--secondary);
}

@media (max-width: 1180px), (orientation: portrait) {
    .maintenance-detail-panel {
        flex: 0 0 auto;
        width: 100%;
        min-width: 0;
    }
}

@media (max-width: 760px), (orientation: portrait) and (max-width: 900px) {
    .maintenance-detail-panel__summary h3 {
        font-size: 22px;
        line-height: 28px;
    }

    .maintenance-detail-panel__section p {
        min-height: 0;
    }
}
</style>
