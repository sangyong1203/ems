<template>
    <GlassPanel class="battery-rack-panel" title="배터리 랙 목록" :value="`${racks.length}대`">
        <div class="battery-rack-summary">
            <span class="battery-rack-summary__capacity">
                Rack당 용량 <strong>{{ formatNumber(rackCapacityKwh) }} kWh</strong>
            </span>
            <div class="battery-rack-summary__statuses">
                <span class="is-normal"
                    >정상 <strong>{{ statusCounts.normal }}</strong></span
                >
                <span class="is-warning"
                    >주의 <strong>{{ statusCounts.warning }}</strong></span
                >
                <span class="is-fault"
                    >장애 <strong>{{ statusCounts.fault }}</strong></span
                >
                <span v-if="statusCounts.inactive > 0" class="is-inactive">
                    비활성 <strong>{{ statusCounts.inactive }}</strong>
                </span>
            </div>
        </div>

        <div class="battery-rack-list scroll-y">
            <article v-for="rack in racks" :key="rack.id" class="battery-rack-card">
                <header class="battery-rack-card__header">
                    <strong>{{ rack.name }}</strong>
                    <StatusBadge :label="statusLabel(rack.status)" :variant="statusVariant(rack.status)" />
                </header>

                <div class="battery-rack-card__metrics">
                    <div class="battery-rack-card__metric is-emphasis">
                        <span>SOC</span>
                        <strong>{{ formatNumber(rack.soc) }}%</strong>
                    </div>
                    <div class="battery-rack-card__metric is-emphasis">
                        <span>SOH</span>
                        <strong>{{ formatNumber(rack.soh) }}%</strong>
                    </div>
                    <div class="battery-rack-card__metric">
                        <span>전압</span>
                        <strong>{{ formatNumber(rack.voltageV) }}V</strong>
                    </div>
                    <div class="battery-rack-card__metric">
                        <span>전류</span>
                        <strong>{{ formatSignedNumber(rack.currentA) }} A</strong>
                    </div>
                    <div class="battery-rack-card__metric">
                        <span>평균</span>
                        <strong>{{ formatNumber(rack.averageTemperatureC) }}°C</strong>
                    </div>
                    <div class="battery-rack-card__metric" :class="{ 'is-warning': rack.status === 'WARNING' }">
                        <span>최고</span>
                        <strong>{{ formatNumber(rack.maxTemperatureC) }}°C</strong>
                    </div>
                </div>
            </article>

            <p v-if="racks.length === 0" class="battery-rack-list__empty">등록된 배터리 랙이 없습니다.</p>
        </div>
    </GlassPanel>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { GlassPanel, StatusBadge } from '@/shared/components'
import type { EssBatteryRack } from '../service/ess.types'

const props = defineProps<{
    racks: EssBatteryRack[]
}>()

const rackCapacityKwh = computed(() => props.racks[0]?.capacityKwh ?? 0)

const statusCounts = computed(() => ({
    normal: props.racks.filter(rack => rack.status === 'NORMAL').length,
    warning: props.racks.filter(rack => rack.status === 'WARNING').length,
    fault: props.racks.filter(rack => rack.status === 'FAULT').length,
    inactive: props.racks.filter(rack => rack.status === 'INACTIVE').length,
}))

const formatNumber = (value?: number) => {
    return Number(value ?? 0).toLocaleString(undefined, { maximumFractionDigits: 1 })
}

const formatSignedNumber = (value?: number) => {
    const numberValue = Number(value ?? 0)
    return `${numberValue > 0 ? '+' : ''}${formatNumber(numberValue)}`
}

const statusLabel = (status?: string) => {
    const labels: Record<string, string> = {
        NORMAL: '정상',
        WARNING: '주의',
        FAULT: '장애',
        INACTIVE: '비활성',
    }
    return labels[status ?? ''] ?? status ?? '-'
}

const statusVariant = (status?: string): 'success' | 'warning' | 'danger' | 'muted' => {
    if (status === 'NORMAL') {
        return 'success'
    }
    if (status === 'WARNING') {
        return 'warning'
    }
    if (status === 'FAULT') {
        return 'danger'
    }
    return 'muted'
}
</script>

<style scoped lang="scss">
.battery-rack-panel {
    flex: 1;
}

.battery-rack-summary {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 12px;
    color: var(--text-color--secondary);
    font-size: 12px;
}

.battery-rack-summary__capacity {
    flex: 0 0 auto;
    white-space: nowrap;
}

.battery-rack-summary__capacity strong {
    margin-left: 4px;
    color: var(--secondary-color);
}

.battery-rack-summary__statuses {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    flex-wrap: wrap;
    gap: 8px;
}

.battery-rack-summary__statuses span {
    white-space: nowrap;
}

.battery-rack-summary__statuses strong {
    margin-left: 2px;
}

.battery-rack-summary__statuses .is-normal {
    color: var(--secondary-color);
}

.battery-rack-summary__statuses .is-warning {
    color: #f6bd60;
}

.battery-rack-summary__statuses .is-fault {
    color: #ff6b6b;
}

.battery-rack-summary__statuses .is-inactive {
    color: var(--text-color--secondary);
}

.battery-rack-list {
    display: flex;
    flex: 1 1 auto;
    flex-direction: column;
    gap: 10px;
    min-height: 0;
}

.battery-rack-card {
    display: flex;
    flex: 0 0 auto;
    flex-direction: column;
    gap: 10px;
    width: 100%;
    min-height: 88px;
    padding: 11px 12px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.05);
}

.battery-rack-card__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
}

.battery-rack-card__header strong {
    overflow: hidden;
    font-size: 15px;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.battery-rack-card__metrics {
    display: flex;
    flex-wrap: wrap;
    column-gap: 4px;
    row-gap: 6px;
}

.battery-rack-card__metric {
    display: flex;
    flex: 1 1 calc(33.333% - 10px);
    align-items: center;
    justify-content: space-between;
    gap: 4px;
    min-width: 70px;
    border-radius: 4px;
    padding: 2px 6px;
    background-color: #15161f;
}

.battery-rack-card__metric span {
    color: var(--text-color--secondary);
    font-size: 11px;
    white-space: nowrap;
}

.battery-rack-card__metric strong {
    font-size: 13px;
    white-space: nowrap;
}

.battery-rack-card__metric.is-emphasis strong {
    color: var(--secondary-color);
}

.battery-rack-card__metric.is-warning strong {
    color: #f6bd60;
}

.battery-rack-list__empty {
    margin: auto;
    color: var(--text-color--secondary);
    font-size: 13px;
    text-align: center;
}

@media (max-width: 1180px), (orientation: portrait) {
    .battery-rack-panel {
        flex: 0 0 auto;
        width: 100%;
    }

    .battery-rack-list {
        max-height: 420px;
    }
}
</style>
