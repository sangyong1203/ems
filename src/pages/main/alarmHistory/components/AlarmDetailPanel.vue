<template>
    <GlassPanel class="alarm-detail-panel" title="알림 상세" :value="statusLabel">
        <template v-if="alarm">
            <div class="alarm-detail-panel__summary">
                <StatusBadge :label="severityLabel" :variant="severityVariant" min-width="56px" />
                <h3>{{ alarm.alarm_type }}</h3>
                <p>{{ alarm.message }}</p>
            </div>

            <KeyValueList :items="basicItems" />

            <div class="alarm-detail-panel__actions">
                <button type="button" :disabled="alarm.status !== 'OPEN'" @click="emit('ack')">확인</button>
                <button
                    type="button"
                    class="is-primary"
                    :disabled="Boolean(alarm.maintenance_id)"
                    @click="emit('maintenance')"
                >
                    정비등록
                </button>
            </div>
        </template>

        <div v-else class="alarm-detail-panel__empty">알림을 선택하세요.</div>
    </GlassPanel>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { GlassPanel, KeyValueList, StatusBadge } from '@/shared/components'
import type { AlarmActionStatus, AlarmItem } from '../service/alarmHistory.types'

const props = defineProps<{
    alarm: AlarmItem | null
}>()

const emit = defineEmits<{
    ack: []
    maintenance: []
}>()

const severityLabels: Record<string, string> = {
    INFO: '정보',
    WARNING: '주의',
    CRITICAL: '심각',
}

const actionStatusLabels: Record<string, string> = {
    OPEN: '미확인',
    ACKED: '확인됨',
    SCHEDULED: '정비등록',
    IN_PROGRESS: '조치중',
    COMPLETED: '조치완료',
    HOLD: '보류',
    CANCELED: '취소',
}

const deviceTypeLabels: Record<string, string> = {
    INVERTER: '인버터',
    PCS: 'PCS',
    ESS_BATTERY: 'ESS Battery',
    BMS: 'BMS',
    AC_PANEL: 'AC 배전반',
    METER: '계량기',
    SENSOR: '센서',
    ETC: '기타',
}

const emptyText = (value: string | null | undefined) => value || '-'
const formatDateTime = (value: string | null | undefined) => {
    return value ? value.replace('T', ' ').slice(0, 19) : '-'
}

const severityLabel = computed(() => (props.alarm ? severityLabels[props.alarm.severity] || props.alarm.severity : ''))
const severityVariant = computed(() => {
    if (props.alarm?.severity === 'CRITICAL') {
        return 'danger'
    }
    if (props.alarm?.severity === 'WARNING') {
        return 'warning'
    }
    return 'info'
})
const actionStatus = computed<AlarmActionStatus | ''>(() => {
    if (!props.alarm) {
        return ''
    }
    if (props.alarm.maintenance_status) {
        return props.alarm.maintenance_status as AlarmActionStatus
    }
    return props.alarm.status === 'OPEN' ? 'OPEN' : 'ACKED'
})
const statusLabel = computed(() =>
    actionStatus.value ? actionStatusLabels[actionStatus.value] || actionStatus.value : '',
)

const basicItems = computed(() => {
    if (!props.alarm) {
        return []
    }
    return [
        { label: '대상 장비', value: emptyText(props.alarm.device_name) },
        {
            label: '장비 유형',
            value: props.alarm.device_type ? deviceTypeLabels[props.alarm.device_type] || props.alarm.device_type : '-',
        },
        { label: '발생 시간', value: formatDateTime(props.alarm.occurred_at) },
        { label: '확인 시간', value: formatDateTime(props.alarm.acknowledged_at) },
        { label: '연결 정비', value: emptyText(props.alarm.maintenance_title) },
        {
            label: '정비 상태',
            value: props.alarm.maintenance_status
                ? actionStatusLabels[props.alarm.maintenance_status] || props.alarm.maintenance_status
                : '-',
        },
        { label: '정비일', value: emptyText(props.alarm.maintenance_date) },
    ]
})
</script>

<style scoped lang="scss">
.alarm-detail-panel {
    flex: 0 0 24.4%;
}

.alarm-detail-panel__summary {
    padding-bottom: 16px;
    margin-bottom: 16px;
    border-bottom: 1px solid var(--border-color);
}

.alarm-detail-panel__summary h3 {
    margin: 12px 0 8px;
    color: #ffffff;
    font-size: 26px;
    line-height: 32px;
}

.alarm-detail-panel__summary p {
    margin: 0;
    color: var(--text-color--secondary);
    font-size: 14px;
    line-height: 22px;
}

.alarm-detail-panel__actions {
    display: flex;
    gap: 8px;
    margin-top: 18px;
}

.alarm-detail-panel__actions button {
    flex: 1;
    height: 34px;
    border: 1px solid rgba(231, 109, 255, 0.42);
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.02);
    color: var(--text-color--primary);
    font-size: 13px;
    font-weight: 800;
    cursor: pointer;
}

.alarm-detail-panel__actions button.is-primary {
    border-color: rgba(21, 224, 183, 0.42);
    color: var(--secondary-color);
}

.alarm-detail-panel__actions button:disabled {
    color: rgba(255, 255, 255, 0.26);
    border-color: rgba(255, 255, 255, 0.08);
    cursor: default;
}

.alarm-detail-panel__empty {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 240px;
    color: var(--text-color--secondary);
}

@media (max-width: 1180px), (orientation: portrait) {
    .alarm-detail-panel {
        flex: 0 0 auto;
        width: 100%;
        min-width: 0;
        max-width: none;
    }
}

@media (max-width: 760px), (orientation: portrait) and (max-width: 900px) {
    .alarm-detail-panel__summary h3 {
        font-size: 22px;
        line-height: 28px;
    }

    .alarm-detail-panel__actions {
        flex-direction: column;
    }
}
</style>
