<template>
    <GlassPanel class="ess-system-panel" title="ESS 목록" :value="`${summary?.total ?? 0}대`">
        <div class="ess-system-panel__summary">
            <span
                >총 용량 <strong>{{ formatNumber(summary?.capacityKwh) }} kWh</strong></span
            >
        </div>

        <div class="ess-system-list">
            <button
                v-for="item in systems"
                :key="item.id"
                type="button"
                class="ess-system-card"
                :class="{ 'is-selected': item.id === selectedSystemId }"
                @click="$emit('select', item.id)"
            >
                <div class="ess-system-card__top">
                    <strong>{{ item.name }}</strong>
                    <span :class="statusClass(item.status)">{{ statusLabel(item.status) }}</span>
                </div>
                <div class="ess-system-card__body">
                    <div class="ess-system-card__battery">
                        <EssBattery
                            :soc="item.soc"
                            :mode="item.mode"
                            compact
                            icon-position="left"
                            battery-position="right"
                        />
                        <span>현재 전력 / 정격 용량</span>
                    </div>
                    <div class="ess-system-card__soc">
                        <strong>{{ formatNumber(item.soc) }}%</strong>
                        <span>{{ formatPower(item.currentPowerKw) }} / {{ formatNumber(item.capacityKwh) }} kWh</span>
                    </div>
                </div>
            </button>
        </div>
    </GlassPanel>
</template>

<script setup lang="ts">
import { GlassPanel } from '@/shared/components'
import EssBattery from '@/shared/components/custom/EssBattery.vue'
import type { EssSystemItem, EssSystemSummary } from '../service/ess.types'

defineProps<{
    systems: EssSystemItem[]
    summary: EssSystemSummary | null
    selectedSystemId: number | null
}>()

defineEmits<{
    select: [systemId: number]
}>()

const formatNumber = (value?: number) => {
    return Number(value ?? 0).toLocaleString(undefined, { maximumFractionDigits: 1 })
}

const formatPower = (value?: number) => {
    return `${formatNumber(value)} kW`
}

const statusLabel = (status?: string) => {
    if (status === 'NORMAL') {
        return '정상'
    }
    if (status === 'WARNING') {
        return '주의'
    }
    if (status === 'FAULT') {
        return '장애'
    }
    return status || '-'
}

const statusClass = (status?: string) => {
    return {
        'is-normal': status === 'NORMAL',
        'is-warning': status === 'WARNING' || status === 'UNKNOWN',
        'is-fault': status === 'FAULT',
    }
}
</script>

<style scoped lang="scss">
.ess-system-panel {
    flex: 1;
}

.ess-system-panel__summary {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 14px;
    color: var(--text-color--secondary);
    font-size: 13px;
}

.ess-system-panel__summary strong {
    color: var(--secondary-color);
}

.ess-system-list {
    display: flex;
    flex: 1 1 auto;
    flex-direction: column;
    gap: 10px;
    min-height: 0;
    overflow: auto;
    padding-right: 4px;
}

.ess-system-card {
    display: flex;
    flex-direction: column;
    gap: 12px;
    width: 100%;
    min-height: 120px;
    padding: 14px;
    color: var(--text-color--primary);
    text-align: left;
    cursor: pointer;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.05);
}

.ess-system-card:hover,
.ess-system-card.is-selected {
    border-color: rgba(21, 224, 183, 0.72);
    background: linear-gradient(135deg, rgba(21, 224, 183, 0.14), rgba(231, 109, 255, 0.1)), rgba(255, 255, 255, 0.06);
}

.ess-system-card__top,
.ess-system-card__body {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
}

.ess-system-card__body {
    align-items: flex-end;
}

.ess-system-card__battery {
    display: flex;
    flex-direction: column;
    gap: 9px;
    min-width: 0;
}

.ess-system-card__soc {
    display: flex;
    flex: 0 0 auto;
    flex-direction: column;
    align-items: flex-end;
    gap: 12px;
    min-width: 126px;
    text-align: right;
}

.ess-system-card__soc strong {
    color: var(--secondary-color);
    font-size: 30px;
    line-height: 32px;
}

.ess-system-card span {
    color: var(--text-color--secondary);
    font-size: 12px;
}

.ess-system-card span strong {
    color: var(--secondary-color);
}

.ess-system-card__top strong {
    font-size: 15px;
}

.ess-system-card__top > span {
    flex: 0 0 auto;
    min-width: 42px;
    padding: 3px 8px;
    border-radius: 999px;
    font-size: 12px;
    font-style: normal;
    font-weight: 700;
    text-align: center;
}

.is-normal {
    color: var(--secondary-color) !important;
    border: 1px solid rgba(21, 224, 183, 0.45);
    background: rgba(21, 224, 183, 0.1);
}

.is-warning {
    color: #f4c261 !important;
    border: 1px solid rgba(244, 194, 97, 0.42);
    background: rgba(244, 194, 97, 0.1);
}

.is-fault {
    color: #ff7a8a !important;
    border: 1px solid rgba(255, 122, 138, 0.42);
    background: rgba(255, 122, 138, 0.1);
}

@media (max-width: 1180px), (orientation: portrait) {
    .ess-system-panel {
        flex: 0 0 auto;
        width: 100%;
    }

    .ess-system-list {
        max-height: 280px;
    }
}
</style>
