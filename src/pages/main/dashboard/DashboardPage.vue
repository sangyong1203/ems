<template>
    <section class="dashboard-page">
        <div class="dashboard-content">
            <div class="dashboard-main">
                <div class="dashboard-power-flow-row">
                    <!-- <GlassPanel
                        class="dashboard-panel--power-flow-devices"
                        title="장비 목록"
                        :value="powerFlowDeviceCountText"
                    >
                        <PowerFlowPalette
                            v-if="powerFlowEditorData"
                            class="dashboard-power-flow-palette"
                            :devices="powerFlowEditorData.devices"
                            :placed-device-ids="dashboardPalettePlacedDeviceIds"
                            :editable="false"
                        />
                    </GlassPanel> -->
                    <GlassPanel
                        class="dashboard-panel--power-flow"
                        title="전력 흐름"
                        subtitle="PV / ESS / 부하 / 계통 실시간 흐름"
                        subtitle-position="right"
                        :value="updatedAtText"
                    >
                        <PowerFlowPalette
                            v-if="powerFlowEditorData"
                            class="dashboard-power-flow-palette"
                            :devices="powerFlowEditorData.devices"
                            :placed-device-ids="dashboardPalettePlacedDeviceIds"
                            :editable="false"
                        />
                        <!-- <DashboardPowerFlowMap :data="powerFlow" /> -->
                        <PowerFlowCanvas
                            v-if="powerFlowLayout && powerFlowEditorData"
                            :model-value="powerFlowLayout"
                            :devices="powerFlowEditorData.devices"
                            :telemetry="powerFlowEditorData.telemetry"
                            :device-telemetry="powerFlowEditorData.device_telemetry"
                            :editable="false"
                            :show-palette="false"
                        />
                    </GlassPanel>
                </div>

                <div class="dashboard-chart-row">
                    <GlassPanel
                        class="dashboard-panel--chart"
                        title="태양광 발전 출력"
                        subtitle="오늘 시간대별 발전 추이"
                        :value="`${formatNumber(summary?.solar.currentPowerKw)} kW`"
                    >
                        <TrendAreaChart
                            :data="solarHistory"
                            :capacity="summary?.project.solarCapacityKw ?? 0"
                            name="태양광 발전 출력"
                            unit="kW"
                        />
                    </GlassPanel>

                    <GlassPanel
                        class="dashboard-panel--grid-chart"
                        title="계통 송전/수전 전력"
                        subtitle="시간대별 계통 전력 추이"
                        :value="gridPowerText"
                    >
                        <DashboardPowerChart
                            :first-points="gridExportHistory"
                            :second-points="gridImportHistory"
                            first-name="송전"
                            second-name="수전"
                            unit="kW"
                        />
                    </GlassPanel>

                    <GlassPanel
                        class="dashboard-panel--ess-chart"
                        title="ESS 충전/방전 전력"
                        :value="`충전 ${formatNumber(summary?.ess.chargePowerKw)} kW / 방전 ${formatNumber(
                            summary?.ess.dischargePowerKw,
                        )} kW`"
                    >
                        <EssPowerChart
                            :charge-data="essChargeHistory"
                            :discharge-data="essDischargeHistory"
                            :soc-data="essSocHistory"
                            :left-split-number="2"
                            :right-split-number="4"
                            unit="kW"
                        />
                    </GlassPanel>
                </div>
            </div>

            <DashboardKpiSummary
                class="dashboard-panel--kpi"
                :items="kpiItems"
                :ess-soc="summary?.ess.soc ?? 0"
                :ess-mode="essModeLabel"
                :ess-status-label="essStatus.label"
                :ess-status-tone="essStatus.tone"
                :ess-items="essStatusItems"
                :inverter-normal="summary?.solar.inverterNormal ?? 0"
                :inverter-warning="summary?.solar.inverterFault ?? 0"
                :inverter-total="summary?.solar.inverterTotal ?? 0"
            />
        </div>
    </section>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { EssPowerChart, GlassPanel, TrendAreaChart } from '@/shared/components'
import PowerFlowCanvas from '@/features/powerFlow/components/PowerFlowCanvas.vue'
import PowerFlowPalette from '@/features/powerFlow/components/PowerFlowPalette.vue'
import type { PowerFlowEditorData, PowerFlowLayout } from '@/features/powerFlow/service/powerFlow.types'
import { isSuccessResponse } from '@/shared/utils'
import DashboardPowerChart from './components/DashboardPowerChart.vue'
import DashboardKpiSummary from './components/DashboardKpiSummary.vue'
// import DashboardPowerFlowMap from './components/DashboardPowerFlowMap.vue'
import dashboardApi from './service/dashboard.api'
import type { DashboardPowerFlow, DashboardSummary, DashboardTelemetryPoint } from './service/dashboard.types'

const DEFAULT_REFRESH_INTERVAL = 10000
const dashboardPalettePlacedDeviceIds: number[] = []

const summary = ref<DashboardSummary | null>(null)
const powerFlow = ref<DashboardPowerFlow | null>(null)
const powerFlowEditorData = ref<PowerFlowEditorData | null>(null)
const powerFlowLayout = ref<PowerFlowLayout | null>(null)
const solarHistory = ref<DashboardTelemetryPoint[]>([])
const essChargeHistory = ref<DashboardTelemetryPoint[]>([])
const essDischargeHistory = ref<DashboardTelemetryPoint[]>([])
const essSocHistory = ref<DashboardTelemetryPoint[]>([])
const gridExportHistory = ref<DashboardTelemetryPoint[]>([])
const gridImportHistory = ref<DashboardTelemetryPoint[]>([])
let pollingTimer: number | undefined

const formatNumber = (value?: number) => {
    return Number(value ?? 0).toLocaleString(undefined, { maximumFractionDigits: 1 })
}

const essModeLabel = computed(() => {
    if (!summary.value) {
        return '대기'
    }
    if (summary.value.ess.chargePowerKw > 0) {
        return '충전'
    }
    if (summary.value.ess.dischargePowerKw > 0) {
        return '방전'
    }
    return '대기'
})

const essStatus = computed<{ label: string; tone: 'normal' | 'warning' | 'fault' | 'unknown' }>(() => {
    const statuses = [summary.value?.ess.pcsStatus, summary.value?.ess.bmsStatus].filter(Boolean)
    if (!statuses.length) {
        return { label: '확인 필요', tone: 'unknown' }
    }
    if (statuses.some(status => ['FAULT', 'ERROR', 'FAIL'].includes(status ?? ''))) {
        return { label: '장애', tone: 'fault' }
    }
    if (statuses.some(status => ['WARNING', 'WARN', 'CAUTION'].includes(status ?? ''))) {
        return { label: '주의', tone: 'warning' }
    }
    if (statuses.every(status => status === 'NORMAL')) {
        return { label: '정상', tone: 'normal' }
    }
    return { label: '확인 필요', tone: 'unknown' }
})

const gridPowerText = computed(() => {
    if (!summary.value) {
        return '0 kW'
    }
    if (summary.value.grid.exportPowerKw > 0) {
        return `${formatNumber(summary.value.grid.exportPowerKw)} kW 송전`
    }
    if (summary.value.grid.importPowerKw > 0) {
        return `${formatNumber(summary.value.grid.importPowerKw)} kW 수전`
    }
    return '0 kW'
})

const gridPowerValue = computed(() => {
    if (!summary.value) {
        return '0'
    }
    return formatNumber(summary.value.grid.exportPowerKw || summary.value.grid.importPowerKw)
})

const gridPowerStatus = computed(() => {
    if (!summary.value) {
        return '대기'
    }
    if (summary.value.grid.exportPowerKw > 0) {
        return '계통 송전'
    }
    if (summary.value.grid.importPowerKw > 0) {
        return '계통 수전'
    }
    return '계통 대기'
})

const updatedAtText = computed(() => {
    if (!powerFlow.value?.updatedAt) {
        return 'Updated -'
    }
    return `Updated ${powerFlow.value.updatedAt.replace('T', ' ').slice(0, 19)}`
})

const powerFlowDeviceCountText = computed(() => `${powerFlowEditorData.value?.devices.length ?? 0}대`)

const kpiItems = computed(() => [
    {
        label: '현재 발전 출력',
        value: formatNumber(summary.value?.solar.currentPowerKw),
        unit: 'kW',
        hint: `${formatNumber(summary.value?.project.solarCapacityKw)} kW 설비`,
        variant: 'is-solar',
    },
    {
        label: '금일 발전량',
        value: formatNumber(summary.value?.solar.todayGenerationKwh),
        unit: 'kWh',
        hint: '오늘 누적',
        variant: 'is-energy',
    },
    {
        label: '부하 전력',
        value: formatNumber(summary.value?.grid.loadPowerKw),
        unit: 'kW',
        hint: '현재 사용량',
        variant: 'is-load',
    },
    {
        label: '계통 전력',
        value: gridPowerValue.value,
        unit: 'kW',
        hint: gridPowerStatus.value,
        variant: 'is-grid',
    },
    {
        label: '미처리 알림',
        value: String(summary.value?.alarms.openCount ?? 0),
        unit: '건',
        hint: summary.value?.operationStatus === 'NORMAL' ? '정상' : '확인 필요',
        variant: 'is-alarm',
    },
])

const essStatusItems = computed(() => [
    { label: 'SOH', value: `${formatNumber(summary.value?.ess.soh)}%` },
    { label: 'PCS', value: summary.value?.ess.pcsStatus || '-' },
    { label: 'BMS', value: summary.value?.ess.bmsStatus || '-' },
    { label: '배터리 온도', value: `${formatNumber(summary.value?.ess.batteryTemperatureC)}°C` },
])

const getDashboardData = async () => {
    const [
        summaryRes,
        powerFlowRes,
        powerFlowEditorRes,
        solarHistoryRes,
        essChargeHistoryRes,
        essDischargeHistoryRes,
        essSocHistoryRes,
        gridExportHistoryRes,
        gridImportHistoryRes,
    ] = await Promise.all([
        dashboardApi.getSummary(),
        dashboardApi.getPowerFlow(),
        dashboardApi.getPowerFlowEditor(),
        dashboardApi.getTelemetryHistory('solar_power_kw'),
        dashboardApi.getTelemetryHistory('ess_charge_kw'),
        dashboardApi.getTelemetryHistory('ess_discharge_kw'),
        dashboardApi.getTelemetryHistory('ess_soc'),
        dashboardApi.getTelemetryHistory('grid_export_kw'),
        dashboardApi.getTelemetryHistory('grid_import_kw'),
    ])

    if (isSuccessResponse(summaryRes.result)) {
        summary.value = summaryRes.data
    }

    if (isSuccessResponse(powerFlowRes.result)) {
        powerFlow.value = powerFlowRes.data
    }

    if (isSuccessResponse(powerFlowEditorRes.result)) {
        powerFlowEditorData.value = powerFlowEditorRes.data
        powerFlowLayout.value = JSON.parse(JSON.stringify(powerFlowEditorRes.data.layout))
    }

    if (isSuccessResponse(solarHistoryRes.result)) {
        solarHistory.value = solarHistoryRes.data
    }

    if (isSuccessResponse(essChargeHistoryRes.result)) {
        essChargeHistory.value = essChargeHistoryRes.data
    }

    if (isSuccessResponse(essDischargeHistoryRes.result)) {
        essDischargeHistory.value = essDischargeHistoryRes.data
    }

    if (isSuccessResponse(essSocHistoryRes.result)) {
        essSocHistory.value = essSocHistoryRes.data
    }

    if (isSuccessResponse(gridExportHistoryRes.result)) {
        gridExportHistory.value = gridExportHistoryRes.data
    }

    if (isSuccessResponse(gridImportHistoryRes.result)) {
        gridImportHistory.value = gridImportHistoryRes.data
    }
}

const startPolling = (interval: number) => {
    pollingTimer = window.setInterval(() => {
        getDashboardData()
    }, interval)
}

onMounted(async () => {
    await getDashboardData()
    startPolling(summary.value?.refreshInterval ?? DEFAULT_REFRESH_INTERVAL)
})

onBeforeUnmount(() => {
    if (pollingTimer) {
        window.clearInterval(pollingTimer)
    }
})
</script>

<style scoped lang="scss">
.dashboard-page {
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 14px;
    width: 100%;
    height: 100%;
    min-height: 0;
    min-width: 1180px;
    padding: 10px 12px 14px;
    overflow: hidden;
    color: var(--text-color--primary);
}

.dashboard-content {
    z-index: 1;
    flex: 1 1 auto;
    display: grid;
    grid-template-columns: minmax(0, 1fr) 320px;
    gap: 14px;
    min-height: 0;
}

.dashboard-main {
    display: flex;
    flex-direction: column;
    gap: 14px;
    min-width: 0;
    min-height: 0;
}

.dashboard-power-flow-row {
    flex: 1.25 1 0;
    display: flex;
    gap: 14px;
    min-width: 0;
    min-height: 0;
    :deep(.glass-panel__body) {
        flex-direction: row;
    }
}

.dashboard-panel--power-flow-devices {
    flex: 0 0 240px;
    min-width: 0;
}

.dashboard-panel--power-flow {
    flex: 1 1 0;
    min-width: 0;
    min-height: 0;
    :deep(.glass-panel__body) {
        gap: 8px;
    }
}

.dashboard-power-flow-palette {
    width: 220px;
    padding: 0 2px 12px 4px;
    border-right: none;

    // :deep(.power-flow-palette__header) {
    //     display: none;
    // }
    // :deep(.power-flow-palette__list) {
    //     padding: 0 2px 2px 0;
    // }
    // :deep(.power-flow-palette__item) {
    //     cursor: default;
    // }
}

.dashboard-chart-row {
    display: flex;
    gap: 14px;
    height: 31%;
}

.dashboard-panel--chart,
.dashboard-panel--ess-chart,
.dashboard-panel--grid-chart {
    flex: 1 1 0;
    min-width: 0;
}

.dashboard-panel--kpi {
    min-width: 0;
}
.dashboard-panel--kpi :deep(.glass-panel__body) {
    justify-content: space-around !important;
}

@media (max-width: 1180px), (orientation: portrait) {
    .dashboard-page {
        min-width: 0;
        overflow: auto;
        margin-bottom: 40px;
    }

    .dashboard-content {
        display: flex;
        flex-direction: column;
        min-height: auto;
    }

    .dashboard-main {
        flex: 0 0 auto;
    }

    .dashboard-power-flow-row {
        flex: 0 0 auto;
        min-height: 430px;
    }

    .dashboard-chart-row {
        flex: 0 0 auto;
        flex-wrap: wrap;
        height: auto;
    }

    .dashboard-panel--chart,
    .dashboard-panel--ess-chart,
    .dashboard-panel--grid-chart {
        flex: 1 1 calc(50% - 7px);
        min-height: 300px;
    }

    .dashboard-panel--kpi :deep(.glass-panel__body) {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        gap: 48px;
        section {
            flex: 1;
        }
    }
}

@media (max-width: 760px), (orientation: portrait) and (max-width: 900px) {
    .dashboard-power-flow-row {
        min-height: 380px;
    }

    .dashboard-chart-row {
        flex-direction: column;
    }

    .dashboard-panel--chart,
    .dashboard-panel--ess-chart,
    .dashboard-panel--grid-chart {
        flex-basis: auto;
        min-height: 280px;
    }
}
</style>
