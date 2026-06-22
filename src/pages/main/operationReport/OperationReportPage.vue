<template>
    <section class="operation-report-page">
        <MetricCardRow :items="kpiItems" />

        <div class="operation-report-content">
            <div class="operation-report-main">
                <GlassPanel
                    class="operation-report-panel operation-report-panel--charts"
                    title="운전 통계 리포트"
                    subtitle="선택 기간 발전 / ESS / 계통 누적"
                >
                    <template #headerRight>
                        <DatePicker
                            v-model:mode="reportMode"
                            v-model:date="selectedDate"
                            v-model:range="selectedRange"
                            @change="changeReportDate"
                        />
                    </template>

                    <div v-if="statistics" class="report-chart-board">
                        <section class="report-chart-section report-chart-section--wide">
                            <div class="report-chart-section__header">
                                <div>
                                    <h3>부하 통계</h3>
                                    <span>총 전기 사용량과 공급원별 사용량</span>
                                </div>
                                <strong>{{ formatNumber(loadEnergy) }} kWh</strong>
                            </div>
                            <LoadStatisticsChart :data="reportSeries" />
                        </section>

                        <section class="report-chart-section">
                            <div class="report-chart-section__header">
                                <div>
                                    <h3>태양광 발전량 통계</h3>
                                    <span>발전량과 외기온 추이</span>
                                </div>
                                <strong>{{ formatNumber(generation) }} kWh</strong>
                            </div>
                            <SolarGenerationChart :data="reportSeries" />
                        </section>

                        <section class="report-chart-section">
                            <div class="report-chart-section__header">
                                <div>
                                    <h3>ESS 충방전 통계</h3>
                                    <span>충전량 / 방전량 / SOC</span>
                                </div>
                                <strong>{{ essModeLabel }}</strong>
                            </div>
                            <EssOperationChart :data="reportSeries" />
                        </section>

                        <section class="report-chart-section">
                            <div class="report-chart-section__header">
                                <div>
                                    <h3>계통 송전/수전 통계</h3>
                                    <span>송전 양수 / 수전 음수</span>
                                </div>
                                <strong>{{ gridModeLabel }}</strong>
                            </div>
                            <GridExchangeChart :data="reportSeries" />
                        </section>

                        <section class="report-chart-section">
                            <div class="report-chart-section__header">
                                <div>
                                    <h3>에너지 자립률 추이</h3>
                                    <span>태양광 공급 / 총 부하</span>
                                </div>
                                <strong>{{ formatNumber(averageSelfReliance) }}%</strong>
                            </div>
                            <SelfRelianceChart :data="reportSeries" />
                        </section>

                        <section class="report-chart-section">
                            <div class="report-chart-section__header">
                                <div>
                                    <h3>알람 통계</h3>
                                    <span>날짜별 알람 총수</span>
                                </div>
                                <strong>{{ summary?.alarm_count ?? 0 }}건</strong>
                            </div>
                            <AlarmDailyChart :data="reportSeries" />
                        </section>

                        <section class="report-chart-section">
                            <div class="report-chart-section__header">
                                <div>
                                    <h3>알람 등급 분포</h3>
                                    <span>심각 / 주의 / 정보</span>
                                </div>
                                <strong>{{ summary?.alarm_count ?? 0 }}건</strong>
                            </div>
                            <AlarmSeverityDonutChart :data="statistics.alarm_severity_distribution" />
                        </section>
                    </div>
                    <div v-else class="operation-report-empty">선택한 기간의 운전 리포트가 없습니다.</div>
                </GlassPanel>
            </div>

            <div class="operation-report-side">
                <GlassPanel
                    class="operation-report-panel operation-report-panel--summary"
                    title="운전 요약"
                    :value="operationStatusLabel"
                >
                    <div class="operation-summary">
                        <div class="operation-summary__badge-row">
                            <StatusBadge :label="alarmStatusLabel" :variant="alarmStatusVariant" min-width="88px" />
                            <StatusBadge
                                :label="maintenanceStatusLabel"
                                :variant="maintenanceStatusVariant"
                                min-width="88px"
                            />
                        </div>
                        <section>
                            <h3>ESS 운전 요약</h3>
                            <KeyValueList :items="essItems" />
                        </section>
                        <section>
                            <h3>계통 운전 요약</h3>
                            <KeyValueList :items="gridItems" />
                        </section>
                        <section>
                            <h3>운영 상태</h3>
                            <KeyValueList :items="operationItems" />
                        </section>
                    </div>
                </GlassPanel>
            </div>
        </div>
    </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { DatePicker, GlassPanel, KeyValueList, MetricCardRow, StatusBadge } from '@/shared/components'
import { isSuccessResponse } from '@/shared/utils'
import AlarmDailyChart from './components/AlarmDailyChart.vue'
import AlarmSeverityDonutChart from './components/AlarmSeverityDonutChart.vue'
import EssOperationChart from './components/EssOperationChart.vue'
import GridExchangeChart from './components/GridExchangeChart.vue'
import LoadStatisticsChart from './components/LoadStatisticsChart.vue'
import SelfRelianceChart from './components/SelfRelianceChart.vue'
import SolarGenerationChart from './components/SolarGenerationChart.vue'
import operationReportApi from './service/operationReport.api'
import type { DatePickerChangeSource } from '@/shared/components/widget/DatePicker.vue'
import type { ReportStatistics, ReportSummary } from './service/operationReport.types'
import dayjs from 'dayjs'

const summary = ref<ReportSummary | null>(null)
const statistics = ref<ReportStatistics | null>(null)
const reportMode = ref<'DAILY' | 'RANGE'>('RANGE')
const selectedDate = ref('')
const selectedRange = ref<[string, string] | null>([
    dayjs().subtract(7, 'day').format('YYYY-MM-DD'),
    dayjs().format('YYYY-MM-DD'),
])

const formatNumber = (value?: number) => Number(value ?? 0).toLocaleString(undefined, { maximumFractionDigits: 1 })

const reportRangeLabel = computed(() => {
    if (!summary.value) {
        if (reportMode.value === 'DAILY') {
            return selectedDate.value || '-'
        }
        return selectedRange.value ? `${selectedRange.value[0]} ~ ${selectedRange.value[1]}` : '-'
    }
    if (reportMode.value === 'DAILY' || summary.value.date_from === summary.value.date_to) {
        return summary.value.date_from
    }
    return `${summary.value.date_from} ~ ${summary.value.date_to}`
})

const generation = computed(() => summary.value?.generation_kwh ?? 0)
const essCharge = computed(() => summary.value?.ess_charge_kwh ?? 0)
const essDischarge = computed(() => summary.value?.ess_discharge_kwh ?? 0)
const gridExport = computed(() => summary.value?.grid_export_kwh ?? 0)
const gridImport = computed(() => summary.value?.grid_import_kwh ?? 0)
const totalEssThroughput = computed(() => essCharge.value + essDischarge.value)
const totalGridThroughput = computed(() => gridExport.value + gridImport.value)
const loadEnergy = computed(() =>
    Math.max(generation.value + gridImport.value + essDischarge.value - essCharge.value - gridExport.value, 0),
)
const reportSeries = computed(() => statistics.value?.series ?? [])
const averageSelfReliance = computed(() => {
    if (reportSeries.value.length === 0) {
        return 0
    }
    return reportSeries.value.reduce((sum, item) => sum + item.self_reliance_rate, 0) / reportSeries.value.length
})

const essModeLabel = computed(() => {
    if (essCharge.value > essDischarge.value) {
        return '충전 우세'
    }
    if (essDischarge.value > essCharge.value) {
        return '방전 우세'
    }
    return '균형'
})

const gridModeLabel = computed(() => {
    if (gridExport.value > gridImport.value) {
        return '송전 우세'
    }
    if (gridImport.value > gridExport.value) {
        return '수전 우세'
    }
    return '균형'
})

const alarmStatusLabel = computed(() => `알림 ${summary.value?.alarm_count ?? 0}건`)
const maintenanceStatusLabel = computed(() => `정비 ${summary.value?.maintenance_count ?? 0}건`)
const alarmStatusVariant = computed(() => (summary.value && summary.value.alarm_count > 0 ? 'warning' : 'success'))
const maintenanceStatusVariant = computed(() =>
    summary.value && summary.value.maintenance_count > 0 ? 'info' : 'success',
)
const operationStatusLabel = computed(() => {
    if (!summary.value) {
        return '-'
    }
    return summary.value.alarm_count > 0 ? '확인 필요' : '정상'
})

const kpiItems = computed(() => [
    { label: '발전량', value: formatNumber(generation.value), unit: 'kWh', hint: '기간 누적', variant: 'is-solar' },
    { label: '부하', value: formatNumber(loadEnergy.value), unit: 'kWh', hint: '기간 사용', variant: 'is-load' },
    { label: 'ESS 충전', value: formatNumber(essCharge.value), unit: 'kWh', hint: '기간 누적', variant: 'is-ess' },
    { label: 'ESS 방전', value: formatNumber(essDischarge.value), unit: 'kWh', hint: '기간 누적', variant: 'is-load' },
    {
        label: '계통 송전',
        value: formatNumber(gridExport.value),
        unit: 'kWh',
        hint: gridModeLabel.value,
        variant: 'is-grid',
    },
    {
        label: '계통 수전',
        value: formatNumber(gridImport.value),
        unit: 'kWh',
        hint: gridModeLabel.value,
        variant: 'is-grid',
    },
    {
        label: '알림/정비',
        value: `${summary.value?.alarm_count ?? 0}/${summary.value?.maintenance_count ?? 0}`,
        unit: '건',
        hint: '알림 / 정비',
        variant: 'is-warning',
    },
])

const essItems = computed(() => [
    { label: '충전량', value: `${formatNumber(essCharge.value)} kWh` },
    { label: '방전량', value: `${formatNumber(essDischarge.value)} kWh` },
    { label: '총 처리량', value: `${formatNumber(totalEssThroughput.value)} kWh` },
    { label: '운전 방향', value: essModeLabel.value },
])

const gridItems = computed(() => [
    { label: '송전량', value: `${formatNumber(gridExport.value)} kWh` },
    { label: '수전량', value: `${formatNumber(gridImport.value)} kWh` },
    { label: '총 계통 거래량', value: `${formatNumber(totalGridThroughput.value)} kWh` },
    { label: '계통 방향', value: gridModeLabel.value },
])

const operationItems = computed(() => [
    { label: '조회 기간', value: reportRangeLabel.value },
    { label: '집계 일수', value: `${summary.value?.day_count ?? 0}일` },
    { label: '알림 발생', value: `${summary.value?.alarm_count ?? 0}건` },
    { label: '정비 이력', value: `${summary.value?.maintenance_count ?? 0}건` },
    { label: '운영 판정', value: operationStatusLabel.value },
])

const normalizeReportDate = () => {
    if (reportMode.value === 'DAILY') {
        selectedDate.value = selectedRange.value?.[1] || summary.value?.date_to || summary.value?.date_from || ''
    } else {
        const startDate = selectedDate.value || summary.value?.date_from || ''
        const endDate = selectedDate.value || summary.value?.date_to || startDate
        selectedRange.value = startDate && endDate ? [startDate, endDate] : null
    }
}

const changeReportDate = (source: DatePickerChangeSource) => {
    if (source === 'mode') {
        normalizeReportDate()
    }
    getReportStatistics()
}

const getReportStatistics = async () => {
    const dateFrom = reportMode.value === 'DAILY' ? selectedDate.value : selectedRange.value?.[0] || ''
    const dateTo = reportMode.value === 'DAILY' ? selectedDate.value : selectedRange.value?.[1] || ''
    const res = await operationReportApi.getStatistics(dateFrom, dateTo)
    if (isSuccessResponse(res.result)) {
        statistics.value = res.data
        summary.value = res.data?.summary ?? null
        if (res.data) {
            selectedDate.value = res.data.summary.date_to
            selectedRange.value = [res.data.summary.date_from, res.data.summary.date_to]
        }
    }
}

onMounted(() => {
    getReportStatistics()
})
</script>

<style scoped lang="scss">
.operation-report-page {
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 14px;
    width: 100%;
    min-height: 100%;
    min-width: 1180px;
    padding: 10px 12px 14px;
    overflow-y: auto;
    overflow-x: hidden;
    color: var(--text-color--primary);
}

.operation-report-content {
    display: flex;
    gap: 14px;
    align-items: flex-start;
}

.operation-report-main,
.operation-report-side {
    display: flex;
    flex-direction: column;
    gap: 14px;
    min-width: 0;
    min-height: 0;
}

.operation-report-main {
    flex: 1;
}

.operation-report-side {
    flex: 0 0 28%;
}

.operation-report-panel {
    flex: 0 0 auto;
    min-height: 0;
}

.operation-report-panel :deep(.report-echart) {
    flex: 1;
}

.operation-report-panel--charts {
    height: 1280px;
}

.operation-report-panel--summary {
    height: 1280px;
}

.operation-summary {
    display: flex;
    flex-direction: column;
    gap: 18px;
    overflow-y: auto;
    min-height: 0;
}

.operation-summary__badge-row {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}

.operation-summary section {
    padding-top: 14px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.operation-summary h3 {
    margin: 0 0 12px;
    color: var(--text-color--primary);
    font-size: 15px;
}

.report-chart-board {
    display: flex;
    flex-wrap: wrap;
    gap: 14px;
    min-height: 0;
}

.report-chart-section {
    flex: 1 1 calc(50% - 7px);
    display: flex;
    flex-direction: column;
    min-width: 360px;
    height: 280px;
    padding: 14px;
    border-radius: 8px;
    background: #00041a38;
}

.report-chart-section--wide {
    flex-basis: 100%;
    height: 300px;
}

.report-chart-section__header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 14px;
    margin-bottom: 8px;
}

.report-chart-section__header h3 {
    margin: 0 0 4px;
    color: var(--text-color--primary);
    font-size: 16px;
}

.report-chart-section__header span {
    color: var(--text-color--secondary);
    font-size: 12px;
}

.report-chart-section__header strong {
    color: var(--secondary-color);
    white-space: nowrap;
}

.operation-report-empty {
    margin: 0;
    color: var(--text-color--secondary);
    font-size: 14px;
    line-height: 22px;
}

.operation-report-empty {
    display: flex;
    align-items: center;
    justify-content: center;
    flex: 1;
}
</style>
