<template>
    <div class="alarm-row-actions">
        <button
            class="alarm-row-actions__button"
            type="button"
            :disabled="alarm.status !== 'OPEN'"
            title="확인"
            @click.stop="emit('ack')"
        >
            확인
        </button>
        <button
            class="alarm-row-actions__button is-maintenance"
            type="button"
            :disabled="Boolean(alarm.maintenance_id)"
            title="정비등록"
            @click.stop="emit('maintenance')"
        >
            정비등록
        </button>
    </div>
</template>

<script setup lang="ts">
import type { AlarmItem } from '../service/alarmHistory.types'

defineProps<{
    alarm: AlarmItem
}>()

const emit = defineEmits<{
    ack: []
    maintenance: []
}>()
</script>

<style scoped lang="scss">
.alarm-row-actions {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    width: 100%;
    min-height: 48px;
}

.alarm-row-actions__button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    height: 28px;
    padding: 0 10px;
    border: 0;
    border-radius: 999px;
    background: rgba(21, 224, 183, 0.1);
    color: var(--secondary-color);
    font-size: 12px;
    font-weight: 800;
    cursor: pointer;
}

.alarm-row-actions__button.is-maintenance {
    min-width: 58px;
    background: rgba(231, 109, 255, 0.12);
    color: var(--primary-color);
}

.alarm-row-actions__button:hover {
    background: rgba(21, 224, 183, 0.2);
}

.alarm-row-actions__button.is-maintenance:hover {
    background: rgba(231, 109, 255, 0.22);
}

.alarm-row-actions__button:disabled {
    background: rgba(255, 255, 255, 0.05);
    color: rgba(255, 255, 255, 0.24);
    cursor: default;
}

.alarm-row-actions__button:disabled:hover {
    background: rgba(255, 255, 255, 0.05);
}
</style>
