<template>
    <section class="trend-page">
        <MetricCardRow :items="kpiItems" />

        <div class="trend-content">
            <div class="trend-content__main">
                <GlassPanel
                    class="trend-panel trend-panel--primary"
                    title="태양광 발전 출력"
                    subtitle="시간대별 발전 전력 추이"
                    :value="`${formatNumber(overview?.summary.solarPowerKw)} kW`"
                >
                    <TrendAreaChart
                        :data="overview?.history.solar ?? []"
                        name="태양광 발전 출력"
                        unit="kW"
                        :capacity="overview?.project.solarCapacityKw ?? 0"
                        :line-width="2"
                        show-line-glow
                        :grid-top="34"
                        :grid-right="26"
                        :grid-left="48"
                    />
                </GlassPanel>

                <div class="trend-row">
                    <GlassPanel
                        class="trend-panel trend-panel--half"
                        title="ESS 충전/방전 전력"
                        subtitle="시간대별 PCS 전력 추이"
                        :value="`충전 ${formatNumber(overview?.summary.essChargeKw)} kW / 방전 ${formatNumber(
                            overview?.summary.essDischargeKw,
                        )} kW`"
                    >
                        <TrendDualAreaChart
                            first-name="충전"
                            second-name="방전"
                            :first-data="overview?.history.essCharge ?? []"
                            :second-data="overview?.history.essDischarge ?? []"
                            unit="kW"
                        />
                    </GlassPanel>

                    <GlassPanel
                        class="trend-panel trend-panel--half"
                        title="계통 송전/수전"
                        subtitle="시간대별 계통 전력 추이"
                        :value="gridPowerText"
                    >
                        <TrendDualAreaChart
                            first-name="송전"
                            second-name="수전"
                            :first-data="overview?.history.gridExport ?? []"
                            :second-data="overview?.history.gridImport ?? []"
                            unit="kW"
                        />
                    </GlassPanel>
                </div>
            </div>

            <div class="trend-content__side">
                <GlassPanel
                    class="trend-panel trend-panel--soc"
                    title="ESS SOC"
                    subtitle="배터리 충전율 추이"
                    :value="`${formatNumber(overview?.summary.essSoc)}%`"
                >
                    <TrendAreaChart
                        :data="overview?.history.essSoc ?? []"
                        name="ESS SOC"
                        unit="%"
                        y-axis-name=""
                        :show-peak="false"
                        :line-width="2"
                        show-line-glow
                        :grid-top="10"
                        :grid-right="16"
                        :grid-bottom="26"
                        :grid-left="38"
                        :y-split-number="3"
                    />
                </GlassPanel>

                <GlassPanel
                    class="trend-panel trend-panel--load"
                    title="부하 전력"
                    subtitle="시간대별 소비 전력 추이"
                    :value="`${formatNumber(overview?.summary.loadPowerKw)} kW`"
                >
                    <TrendAreaChart
                        :data="overview?.history.load ?? []"
                        name="부하 전력"
                        unit="kW"
                        y-axis-name=""
                        :show-peak="false"
                        :line-width="2"
                        :grid-top="10"
                        :grid-right="16"
                        :grid-bottom="26"
                        :grid-left="38"
                        :y-split-number="3"
                    />
                </GlassPanel>

                <GlassPanel
                    class="trend-panel trend-panel--temperature"
                    title="배터리 온도"
                    subtitle="BMS 측정값 추이"
                    :value="`${formatNumber(overview?.summary.batteryTemperatureC)}℃`"
                >
                    <TrendAreaChart
                        :data="overview?.history.batteryTemperature ?? []"
                        name="배터리 온도"
                        unit="℃"
                        y-axis-name=""
                        :show-peak="false"
                        :line-width="2"
                        :grid-top="10"
                        :grid-right="16"
                        :grid-bottom="26"
                        :grid-left="38"
                        :y-split-number="3"
                    />
                </GlassPanel>
            </div>
        </div>
    </section>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { GlassPanel, MetricCardRow, TrendAreaChart } from '@/shared/components'
import { isSuccessResponse } from '@/shared/utils'
import TrendDualAreaChart from './components/TrendDualAreaChart.vue'
import trendApi from './service/trend.api'
import type { TrendOverview } from './service/trend.types'

const DEFAULT_REFRESH_INTERVAL = 10000

const overview = ref<TrendOverview | null>(null)
let pollingTimer: number | undefined

const formatNumber = (value?: number) => {
    return Number(value ?? 0).toLocaleString(undefined, { maximumFractionDigits: 1 })
}

const statusLabel = (status?: string) => {
    if (status === 'EXPORT') {
        return '송전'
    }
    if (status === 'IMPORT') {
        return '수전'
    }
    if (status === 'BALANCED') {
        return '균형'
    }
    return status || '-'
}

const gridPowerText = computed(() => {
    if (!overview.value) {
        return '0 kW'
    }
    if (overview.value.summary.gridExportKw > 0) {
        return `${formatNumber(overview.value.summary.gridExportKw)} kW 송전`
    }
    if (overview.value.summary.gridImportKw > 0) {
        return `${formatNumber(overview.value.summary.gridImportKw)} kW 수전`
    }
    return '0 kW'
})

const essModeText = computed(() => {
    if ((overview.value?.summary.essChargeKw ?? 0) > 0) {
        return `충전 ${formatNumber(overview.value?.summary.essChargeKw)} kW`
    }
    if ((overview.value?.summary.essDischargeKw ?? 0) > 0) {
        return `방전 ${formatNumber(overview.value?.summary.essDischargeKw)} kW`
    }
    return '대기'
})

const kpiItems = computed(() => [
    {
        label: '태양광 발전',
        value: formatNumber(overview.value?.summary.solarPowerKw),
        unit: 'kW',
        hint: `${formatNumber(overview.value?.project.solarCapacityKw)} kW 설비`,
        variant: 'is-solar',
    },
    {
        label: 'ESS SOC',
        value: formatNumber(overview.value?.summary.essSoc),
        unit: '%',
        hint: essModeText.value,
        variant: 'is-ess',
    },
    {
        label: '부하 전력',
        value: formatNumber(overview.value?.summary.loadPowerKw),
        unit: 'kW',
        hint: '현재 사용',
        variant: 'is-load',
    },
    {
        label: '계통 상태',
        value: statusLabel(overview.value?.summary.gridStatus),
        unit: '',
        hint: gridPowerText.value,
        variant: 'is-grid',
    },
    {
        label: '배터리 온도',
        value: formatNumber(overview.value?.summary.batteryTemperatureC),
        unit: '℃',
        hint: 'BMS 측정값',
        variant: 'is-temperature',
    },
])

const getTrendOverview = async () => {
    const res = await trendApi.getOverview()
    if (isSuccessResponse(res.result)) {
        overview.value = res.data
    }
}

const startPolling = (interval: number) => {
    pollingTimer = window.setInterval(() => {
        getTrendOverview()
    }, interval)
}

onMounted(async () => {
    await getTrendOverview()
    startPolling(overview.value?.refreshInterval ?? DEFAULT_REFRESH_INTERVAL)
})

onBeforeUnmount(() => {
    if (pollingTimer) {
        window.clearInterval(pollingTimer)
    }
})
</script>

<style scoped lang="scss">
.trend-page {
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 14px;
    width: 100%;
    height: 100%;
    min-width: 1180px;
    min-height: 0;
    padding: 10px 12px 14px;
    overflow: hidden;
    color: var(--text-color--primary);
}

.trend-content {
    flex: 1 1 auto;
    display: flex;
    gap: 14px;
    height: calc(100vh - 192px);
    min-height: 0;
    overflow: hidden;
}

.trend-content__main {
    flex: 0 0 calc(68% - 7px);
    display: flex;
    flex-direction: column;
    gap: 14px;
    min-width: 0;
    min-height: 0;
}

.trend-content__side {
    flex: 0 0 calc(32% - 7px);
    display: flex;
    flex-direction: column;
    gap: 14px;
    min-width: 0;
    min-height: 0;
}

.trend-row {
    flex: 0 0 41%;
    display: flex;
    gap: 14px;
    min-height: 0;
}

.trend-panel {
    min-height: 0;
}

.trend-panel :deep(.trend-area-chart),
.trend-panel :deep(.trend-dual-area-chart) {
    min-height: 180px;
}

.trend-panel--primary {
    flex: 1 1 59%;
}

.trend-panel--half {
    flex: 1 1 0;
    min-width: 0;
}

.trend-panel--soc,
.trend-panel--load,
.trend-panel--temperature {
    flex: 1 1 0;
    min-height: 0;
}

.trend-panel--soc :deep(.trend-area-chart),
.trend-panel--load :deep(.trend-area-chart),
.trend-panel--temperature :deep(.trend-area-chart) {
    min-height: 130px;
}

@media (max-width: 1180px), (orientation: portrait) {
    .trend-page {
        min-width: 0;
        overflow: auto;
    }

    .trend-content {
        flex: 0 0 auto;
        flex-direction: column;
        height: auto;
        overflow: visible;
    }

    .trend-content__main,
    .trend-content__side {
        flex: 0 0 auto;
        width: 100%;
    }

    .trend-panel--primary {
        flex: 0 0 auto;
        min-height: 430px;
    }

    .trend-row {
        flex: 0 0 auto;
        flex-wrap: wrap;
        min-height: auto;
    }

    .trend-panel--half {
        flex: 1 1 calc(50% - 7px);
        min-height: 320px;
    }

    .trend-panel--soc,
    .trend-panel--load,
    .trend-panel--temperature {
        flex: 0 0 auto;
        min-height: 280px;
    }

    .trend-panel--soc :deep(.trend-area-chart),
    .trend-panel--load :deep(.trend-area-chart),
    .trend-panel--temperature :deep(.trend-area-chart) {
        min-height: 180px;
    }
}

@media (max-width: 760px), (orientation: portrait) and (max-width: 900px) {
    .trend-panel--primary {
        min-height: 360px;
    }

    .trend-row {
        flex-direction: column;
    }

    .trend-panel--half {
        flex-basis: auto;
        min-height: 300px;
    }

    .trend-panel--soc,
    .trend-panel--load,
    .trend-panel--temperature {
        min-height: 260px;
    }
}

</style>
