<template>
    <section class="solar-page">
        <MetricCardRow :items="kpiItems" />

        <div class="solar-content">
            <div class="solar-content__main">
                <GlassPanel
                    class="solar-panel--chart"
                    title="태양광 발전 출력"
                    subtitle="시간대별 발전 전력 추이"
                    :value="`${formatNumber(overview?.summary.todayGenerationKwh)} kWh`"
                >
                    <TrendAreaChart
                        :data="overview?.history ?? []"
                        name="태양광 발전 출력"
                        unit="kW"
                        :line-width="2"
                        show-line-glow
                        :grid-top="34"
                        :grid-right="22"
                        :grid-left="48"
                    />
                </GlassPanel>

                <GlassPanel
                    class="solar-panel--status"
                    title="인버터 상태"
                    subtitle="정상 운전 기준"
                    :value="`${overview?.summary.inverterNormal ?? 0}/${overview?.summary.inverterTotal ?? 0}`"
                >
                    <div class="solar-status-content">
                        <div class="solar-status-content__info">
                            <ProgressGauge
                                :value="inverterNormalRate"
                                :value-text="`${formatNumber(inverterNormalRate)}%`"
                            />
                            <KeyValueList :items="inverterStatusItems" />
                        </div>
                        <DonutStatusChart
                            :normal="overview?.summary.inverterNormal ?? 0"
                            :warning="overview?.summary.inverterWarning ?? 0"
                            :total="overview?.summary.inverterTotal ?? 0"
                            layout="horizontal"
                            :size="190"
                            summary-label="정상"
                            aria-label="인버터 상태 범례"
                        />
                    </div>
                </GlassPanel>
            </div>

            <div class="solar-content__side">
                <GlassPanel
                    class="solar-panel--inverters"
                    title="태양광 패널별 발전량 모니터"
                    subtitle="인버터 단위 현재 출력"
                    :value="`Updated ${updatedAtLabel}`"
                >
                    <div class="solar-inverter-list">
                        <div
                            v-for="inverter in overview?.inverters ?? []"
                            :key="inverter.id"
                            class="solar-inverter-item"
                        >
                            <div class="solar-inverter-item__name">
                                <strong>{{ inverter.name }}</strong>
                                <StatusBadge
                                    :label="inverter.isActive ? statusLabel(inverter.status) : '비활성'"
                                    :variant="inverter.isActive ? statusVariant(inverter.status) : 'muted'"
                                />
                            </div>
                            <div class="solar-inverter-item__metric">
                                <span>현재 출력</span>
                                <strong>{{ formatNumber(inverter.currentPowerKw) }} kW</strong>
                            </div>
                            <div class="solar-inverter-item__metric">
                                <span>설비 대비</span>
                                <strong>{{ formatNumber(inverter.capacityRatio) }}%</strong>
                            </div>
                            <div class="solar-inverter-item__metric">
                                <span>정격 용량</span>
                                <strong
                                    >{{ formatNumber(inverter.capacityKw) }} {{ inverter.capacityUnit ?? 'kW' }}</strong
                                >
                            </div>
                        </div>
                        <p v-if="!isLoading && !overview?.inverters.length" class="solar-empty-text">
                            등록된 인버터가 없습니다.
                        </p>
                    </div>
                </GlassPanel>
            </div>
        </div>
    </section>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import {
    DonutStatusChart,
    GlassPanel,
    KeyValueList,
    MetricCardRow,
    ProgressGauge,
    StatusBadge,
    TrendAreaChart,
} from '@/shared/components'
import { isSuccessResponse } from '@/shared/utils'
import solarApi from './service/solar.api'
import type { SolarOverview } from './service/solar.types'

const DEFAULT_REFRESH_INTERVAL = 10000

const overview = ref<SolarOverview | null>(null)
const isLoading = ref(false)
let pollingTimer: number | undefined

const formatNumber = (value?: number) => {
    return Number(value ?? 0).toLocaleString(undefined, { maximumFractionDigits: 1 })
}

const updatedAtLabel = computed(() => {
    if (!overview.value?.updatedAt) {
        return '-'
    }
    return overview.value.updatedAt.slice(0, 19).replace('T', ' ')
})

const inverterNormalRate = computed(() => {
    const total = overview.value?.summary.inverterTotal ?? 0
    if (!total) {
        return 0
    }
    return ((overview.value?.summary.inverterNormal ?? 0) / total) * 100
})

const kpiItems = computed(() => [
    {
        label: '현재 발전 출력',
        value: formatNumber(overview.value?.summary.currentPowerKw),
        unit: 'kW',
        hint: `${formatNumber(overview.value?.project.solarCapacityKw)} kW 설비`,
        variant: 'is-solar',
    },
    {
        label: '설비 대비',
        value: formatNumber(overview.value?.summary.capacityRatio),
        unit: '%',
        hint: '현재 출력 기준',
        variant: 'is-ratio',
    },
    {
        label: '금일 발전량',
        value: formatNumber(overview.value?.summary.todayGenerationKwh),
        unit: 'kWh',
        hint: '오늘 누적',
        variant: 'is-energy',
    },
    {
        label: '누적 발전량',
        value: formatNumber(overview.value?.summary.totalGenerationKwh),
        unit: 'kWh',
        hint: overview.value?.project.siteName || '-',
        variant: 'is-total',
    },
    {
        label: '인버터 정상',
        value: `${overview.value?.summary.inverterNormal ?? 0}/${overview.value?.summary.inverterTotal ?? 0}`,
        unit: '대',
        hint: '정상 운전 수량',
        variant: 'is-inverter',
    },
])

const inverterStatusItems = computed(() => [
    { label: '정상', value: `${overview.value?.summary.inverterNormal ?? 0}대` },
    { label: '주의/장애', value: `${overview.value?.summary.inverterWarning ?? 0}대` },
    { label: '피크 출력', value: `${formatNumber(overview.value?.summary.peakPowerKw)} kW` },
    { label: '평균 출력', value: `${formatNumber(overview.value?.summary.averagePowerKw)} kW` },
])

const statusLabel = (status: string) => {
    if (status === 'NORMAL') {
        return '정상'
    }
    if (status === 'WARNING') {
        return '주의'
    }
    if (status === 'FAULT') {
        return '장애'
    }
    return status
}

const statusVariant = (status: string) => {
    return status === 'NORMAL' ? 'success' : 'progress'
}

const getSolarData = async () => {
    isLoading.value = true
    try {
        const res = await solarApi.getOverview()
        if (isSuccessResponse(res.result)) {
            overview.value = res.data
        }
    } finally {
        isLoading.value = false
    }
}

const startPolling = (interval: number) => {
    pollingTimer = window.setInterval(() => {
        getSolarData()
    }, interval)
}

onMounted(async () => {
    await getSolarData()
    startPolling(overview.value?.refreshInterval ?? DEFAULT_REFRESH_INTERVAL)
})

onBeforeUnmount(() => {
    if (pollingTimer) {
        window.clearInterval(pollingTimer)
    }
})
</script>

<style scoped lang="scss">
.solar-page {
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

.solar-content {
    z-index: 1;
    flex: 1 1 auto;
    display: flex;
    gap: 14px;
    min-height: 0;
}

.solar-content__main,
.solar-content__side {
    display: flex;
    flex-direction: column;
    gap: 14px;
    min-width: 0;
    min-height: 0;
}

.solar-content__main {
    flex: 1 1 60.5%;
}

.solar-content__side {
    flex: 0 0 39.5%;
}

.solar-panel--chart {
    flex: 1 1 62%;
}

.solar-panel--status {
    flex: 0 0 38%;
}

.solar-panel--inverters {
    flex: 1 1 auto;
}

.solar-status-content {
    display: flex;
    flex: 1 1 auto;
    align-items: center;
    gap: 28px;
    min-height: 0;
}

.solar-status-content__info {
    display: flex;
    flex: 0 0 55%;
    flex-direction: column;
    justify-content: center;
    min-width: 0;
    height: 100%;
}

.solar-inverter-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
    min-height: 0;
    overflow-y: auto;
    padding-right: 4px;
    margin-right: -12px;
}

.solar-inverter-item {
    display: flex;
    align-items: center;
    gap: 18px;
    min-height: 62px;
    flex: 0 0 auto;
    padding: 12px 14px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.05);
}

.solar-inverter-item__name {
    flex: 1 1 160px;
    display: flex;
    align-items: center;
    gap: 10px;
    min-width: 0;
}

.solar-inverter-item__name strong {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.solar-inverter-item__metric {
    flex: 0 0 104px;
    display: flex;
    flex-direction: column;
    gap: 4px;
    text-align: right;
}

.solar-inverter-item__metric span {
    color: var(--text-color--secondary);
    font-size: 12px;
}

.solar-inverter-item__metric strong {
    color: #ffffff;
    font-size: 15px;
    text-align: right;
}

.solar-empty-text {
    margin: 0;
    color: var(--text-color--secondary);
}

@media (max-width: 1180px), (orientation: portrait) {
    .solar-page {
        min-width: 0;
        overflow: auto;
    }

    .solar-content {
        flex: 0 0 auto;
        flex-direction: column;
        min-height: auto;
    }

    .solar-content__main,
    .solar-content__side {
        flex: 0 0 auto;
    }

    .solar-panel--inverters {
        flex: 0 0 auto;
        min-height: 420px;
    }

    .solar-inverter-list {
        max-height: 540px;
    }

    .solar-status-content {
        flex-direction: row;
        justify-content: space-between;
        gap: 18px;
        .solar-status-content__info,
        .donut-status-chart {
            flex: 1;
        }
    }
    .solar-panel--chart {
        min-height: 300px;
    }

    .solar-panel--status {
        min-height: 300px;
    }
}

@media (max-width: 760px), (orientation: portrait) and (max-width: 900px) {
    .solar-status-content__info {
        flex: 0 0 auto;
        height: auto;
    }

    .solar-inverter-item {
        gap: 12px;
    }

    .donut-status-chart {
        width: 60%;
        flex: unset !important;
    }
}
</style>
