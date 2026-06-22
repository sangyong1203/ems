<template>
    <section class="ess-page">
        <MetricCardRow :items="kpiItems" />

        <div class="ess-layout">
            <EssSystemListPanel
                :systems="systems"
                :summary="systemsSummary"
                :selected-system-id="selectedSystemId"
                @select="selectSystem"
            />

            <div class="ess-detail">
                <div class="ess-detail__main">
                    <GlassPanel
                        class="ess-panel ess-panel--power"
                        title="ESS 충전/방전 전력"
                        subtitle="충전(-) / 방전(+)"
                        :value="`현재 충전 ${formatNumber(overview?.summary.chargePowerKw)} kW / 방전 ${formatNumber(
                            overview?.summary.dischargePowerKw,
                        )} kW`"
                    >
                        <EssPowerChart
                            :charge-data="overview?.history.charge ?? []"
                            :discharge-data="overview?.history.discharge ?? []"
                            :soc-data="overview?.history.soc ?? []"
                            unit="kW"
                        />
                    </GlassPanel>

                    <div class="ess-chart-row">
                        <GlassPanel
                            class="ess-panel ess-panel--soc"
                            title="ESS SOC 추이"
                            subtitle="시간대별 배터리 충전율"
                            :value="`${formatNumber(overview?.summary.soc)}%`"
                        >
                            <TrendAreaChart
                                :data="overview?.history.soc ?? []"
                                name="ESS SOC"
                                unit="%"
                                :show-peak="false"
                                :line-width="2"
                                show-line-glow
                            />
                        </GlassPanel>

                        <GlassPanel
                            class="ess-panel ess-panel--temperature"
                            title="배터리 온도 추이"
                            subtitle="BMS 측정 온도"
                            :value="`${formatNumber(overview?.summary.batteryTemperatureC)}°C`"
                        >
                            <TrendAreaChart
                                :data="overview?.history.temperature ?? []"
                                name="배터리 온도"
                                unit="°C"
                                :show-peak="false"
                                :line-width="2"
                                show-line-glow
                            />
                        </GlassPanel>
                    </div>
                </div>
            </div>
            <EssOperationSummaryPanel :overview="overview" />
        </div>
    </section>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { GlassPanel, MetricCardRow, TrendAreaChart } from '@/shared/components'
import EssPowerChart from '@/shared/components/custom/EssPowerChart.vue'
import { isSuccessResponse } from '@/shared/utils'
import EssOperationSummaryPanel from './components/EssOperationSummaryPanel.vue'
import EssSystemListPanel from './components/EssSystemListPanel.vue'
import essApi from './service/ess.api'
import type { EssOverview, EssSystemItem, EssSystemSummary } from './service/ess.types'

const DEFAULT_REFRESH_INTERVAL = 10000

const overview = ref<EssOverview | null>(null)
const systems = ref<EssSystemItem[]>([])
const systemsSummary = ref<EssSystemSummary | null>(null)
const selectedSystemId = ref<number | null>(null)
let pollingTimer: number | undefined

const formatNumber = (value?: number) => {
    return Number(value ?? 0).toLocaleString(undefined, { maximumFractionDigits: 1 })
}

const currentPowerText = computed(() => {
    const charge = overview.value?.summary.chargePowerKw ?? 0
    const discharge = overview.value?.summary.dischargePowerKw ?? 0
    if (charge > 0) {
        return `${formatNumber(charge)} kW 충전`
    }
    if (discharge > 0) {
        return `${formatNumber(discharge)} kW 방전`
    }
    return '0 kW 대기'
})

const kpiItems = computed(() => [
    {
        label: 'ESS 수',
        value: formatNumber(systemsSummary.value?.total),
        unit: '대',
        hint: `정상 ${formatNumber(systemsSummary.value?.normal)} / 주의 ${formatNumber(systemsSummary.value?.warning)}`,
        variant: 'is-count',
    },
    {
        label: '평균 SOC',
        value: formatNumber(systemsSummary.value?.averageSoc),
        unit: '%',
        hint: `${formatNumber(systemsSummary.value?.capacityKwh)} kWh 운영 용량`,
        variant: 'is-soc',
    },
    {
        label: '현재 전력',
        value: formatNumber(
            (overview.value?.summary.chargePowerKw ?? 0) || (overview.value?.summary.dischargePowerKw ?? 0),
        ),
        unit: 'kW',
        hint: currentPowerText.value,
        variant: 'is-power',
    },
    {
        label: '금일 충전량',
        value: formatNumber(overview.value?.summary.todayChargeKwh),
        unit: 'kWh',
        hint: '선택 ESS 기준',
        variant: 'is-charge',
    },
    {
        label: '금일 방전량',
        value: formatNumber(overview.value?.summary.todayDischargeKwh),
        unit: 'kWh',
        hint: '선택 ESS 기준',
        variant: 'is-discharge',
    },
])

const getSystems = async () => {
    const res = await essApi.getSystems()
    if (!isSuccessResponse(res.result)) {
        systems.value = []
        systemsSummary.value = null
        return
    }

    systems.value = res.data.list
    systemsSummary.value = res.data.summary
    if (!selectedSystemId.value && systems.value.length > 0) {
        selectedSystemId.value = systems.value[0].id
    }
}

const getEssData = async () => {
    if (!selectedSystemId.value) {
        return
    }

    const res = await essApi.getSystemOverview(selectedSystemId.value)
    if (isSuccessResponse(res.result)) {
        overview.value = res.data
    }
}

const refreshData = async () => {
    await getSystems()
    await getEssData()
}

const selectSystem = async (systemId: number) => {
    selectedSystemId.value = systemId
    await getEssData()
}

const startPolling = (interval: number) => {
    pollingTimer = window.setInterval(() => {
        refreshData()
    }, interval)
}

onMounted(async () => {
    await refreshData()
    startPolling(overview.value?.refreshInterval ?? DEFAULT_REFRESH_INTERVAL)
})

onBeforeUnmount(() => {
    if (pollingTimer) {
        window.clearInterval(pollingTimer)
    }
})
</script>

<style scoped lang="scss">
.ess-page {
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

.ess-layout {
    z-index: 1;
    flex: 1 1 auto;
    display: flex;
    gap: 14px;
    min-height: 0;
}

.ess-detail {
    width: 59.7%;
    display: flex;
    gap: 14px;
    min-width: 0;
    min-height: 0;
}

.ess-detail__main {
    flex: 1 1 auto;
    display: flex;
    flex-direction: column;
    gap: 14px;
    min-width: 0;
    min-height: 0;
}

.ess-panel {
    min-height: 0;
}

.ess-panel--power {
    flex: 1 1 auto;
    min-height: 320px;
    :deep(.glass-panel__body) {
        margin-top: -12px;
    }
}

.ess-chart-row {
    flex: 0 0 260px;
    display: flex;
    gap: 14px;
    min-height: 0;
}

.ess-panel--soc,
.ess-panel--temperature {
    flex: 1 1 0;
}

@media (max-width: 1180px), (orientation: portrait) {
    .ess-page {
        min-width: 0;
        overflow: auto;
    }

    .ess-layout,
    .ess-detail,
    .ess-chart-row {
        flex: 0 0 auto;
        flex-direction: column;
        min-height: auto;
    }
    .ess-detail {
        width: 100%;
    }
    .ess-panel--power {
        flex: 0 0 auto;
        min-height: 360px;
    }

    .ess-chart-row {
        flex-basis: auto;
    }

    .ess-panel--soc,
    .ess-panel--temperature {
        min-height: 300px;
    }
}
</style>
