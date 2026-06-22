<template>
    <GlassPanel
        class="ess-panel ess-panel--summary"
        :title="overview?.system.name || 'ESS 운영 요약'"
        :value="statusLabel(overview?.summary.systemStatus)"
    >
        <h3 class="ess-summary-title">ESS 운영 요약</h3>

        <div class="ess-summary-kpis">
            <article>
                <span>SOC</span>
                <strong>{{ formatNumber(overview?.summary.soc) }}%</strong>
            </article>
            <article>
                <span>SOH</span>
                <strong>{{ formatNumber(overview?.summary.soh) }}%</strong>
            </article>
            <article>
                <span>충전</span>
                <strong>{{ formatNumber(overview?.summary.chargePowerKw) }} kW</strong>
            </article>
            <article>
                <span>방전</span>
                <strong>{{ formatNumber(overview?.summary.dischargePowerKw) }} kW</strong>
            </article>
        </div>

        <KeyValueList :items="operationItems" style="min-height: 190px; margin-top: 12px" />

        <section class="ess-device-section">
            <h3>장비 상태</h3>
            <article v-for="device in deviceItems" :key="device.label" class="ess-device-card">
                <div>
                    <span>{{ device.label }}</span>
                    <strong>{{ device.name }}</strong>
                </div>
                <em :class="statusClass(device.status)">{{ statusLabel(device.status) }}</em>
            </article>
        </section>
    </GlassPanel>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { GlassPanel, KeyValueList } from '@/shared/components'
import type { EssOverview } from '../service/ess.types'

const props = defineProps<{
    overview: EssOverview | null
}>()

const formatNumber = (value?: number) => {
    return Number(value ?? 0).toLocaleString(undefined, { maximumFractionDigits: 1 })
}

const modeLabel = (mode?: string) => {
    if (mode === 'CHARGING') {
        return '충전'
    }
    if (mode === 'DISCHARGING') {
        return '방전'
    }
    return '대기'
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

const operationItems = computed(() => [
    { label: '운전 모드', value: modeLabel(props.overview?.summary.mode) },
    { label: '전압', value: `${formatNumber(props.overview?.summary.batteryVoltageV)} V` },
    { label: '전류', value: `${formatNumber(props.overview?.summary.batteryCurrentA)} A` },
    { label: '배터리 온도', value: `${formatNumber(props.overview?.summary.batteryTemperatureC)}°C` },
    { label: '금일 충전량', value: `${formatNumber(props.overview?.summary.todayChargeKwh)} kWh` },
    { label: '금일 방전량', value: `${formatNumber(props.overview?.summary.todayDischargeKwh)} kWh` },
])

const deviceItems = computed(() => [
    { label: 'PCS', name: props.overview?.devices.pcs.name || '-', status: props.overview?.devices.pcs.status },
    { label: 'BMS', name: props.overview?.devices.bms.name || '-', status: props.overview?.devices.bms.status },
    {
        label: 'Battery',
        name: props.overview?.devices.battery.name || '-',
        status: props.overview?.devices.battery.status,
    },
])
</script>

<style scoped lang="scss">
.ess-panel--summary {
    flex: 1;
}

.ess-summary-title {
    margin: 0 0 12px;
    color: var(--text-color--secondary);
    font-size: 13px;
    font-weight: 700;
}

.ess-summary-kpis {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 10px;
}

.ess-summary-kpis article {
    flex: 1 1 calc(50% - 4px);
    min-width: 130px;
    padding: 8px 10px;
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.05);
}

.ess-summary-kpis span {
    display: block;
    margin-bottom: 4px;
    color: var(--text-color--secondary);
    font-size: 12px;
}

.ess-summary-kpis strong {
    color: var(--secondary-color);
    font-size: 17px;
}

.ess-panel--summary :deep(.key-value-list) {
    gap: 9px;
}

.ess-panel--summary :deep(.key-value-list div) {
    padding-bottom: 9px;
}

.ess-panel--summary :deep(.key-value-list dt),
.ess-panel--summary :deep(.key-value-list dd) {
    font-size: 13px;
}

.ess-device-section {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-top: 14px;
    padding-top: 12px;
}

.ess-device-section h3 {
    margin: 0;
    font-size: 14px;
}

.ess-device-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    min-height: 50px;
    padding: 9px 11px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.05);
}

.ess-device-card div {
    display: flex;
    flex-direction: column;
    gap: 4px;
    min-width: 0;
}

.ess-device-card span {
    color: var(--text-color--secondary);
    font-size: 12px;
}

.ess-device-card strong {
    overflow: hidden;
    font-size: 14px;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.ess-device-card em {
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
    .ess-panel--summary {
        flex: 0 0 auto;
        width: 100%;
    }
}
</style>
