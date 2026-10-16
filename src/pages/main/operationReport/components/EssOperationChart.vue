<template>
    <ReportEChart :option="chartOption" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { EChartsOption } from 'echarts'
import type { ReportStatisticsPoint } from '../service/operationReport.types'
import ReportEChart from './ReportEChart.vue'
import { CHART_THEME, SEMANTIC_COLORS } from '@/constants/colors'

const props = defineProps<{
    data: ReportStatisticsPoint[] // 일별 ESS 운영 통계 데이터
}>()

const chartTextColor = CHART_THEME.textColor
const chartSplitLineColor = CHART_THEME.gridLineColor
const chartAxisLineColor = CHART_THEME.axisLineColor
const chartGrid = { top: 50, right: 38, bottom: 30, left: 56 }
const dates = computed(() => props.data.map(item => item.date))

// formatDateLabel 날짜 라벨(MM-DD) 포맷팅
const formatDateLabel = (date: string) => date.slice(5)

// values 특정 지표 키의 수치 데이터 배열 추출
const values = (key: keyof ReportStatisticsPoint) => props.data.map(item => Number(item[key] ?? 0))

const chartOption = computed<EChartsOption>(() => ({
    color: [SEMANTIC_COLORS.domain.solar, SEMANTIC_COLORS.domain.battery, SEMANTIC_COLORS.domain.grid],
    tooltip: {
        trigger: 'axis',
        ...CHART_THEME.tooltip,
    },
    legend: { top: 0, right: 5, textStyle: { color: chartTextColor, fontSize: 10 } },
    grid: chartGrid,
    xAxis: {
        type: 'category',
        data: dates.value,
        axisLabel: { color: chartTextColor, formatter: formatDateLabel },
        axisTick: { show: false },
        axisLine: { lineStyle: { color: chartAxisLineColor } },
    },
    yAxis: [
        {
            type: 'value',
            name: 'kWh',
            nameTextStyle: { color: chartTextColor, fontSize: 10 },
            axisLabel: { color: chartTextColor },
            splitLine: { lineStyle: { color: chartSplitLineColor } },
        },
        {
            type: 'value',
            name: '%',
            min: 0,
            max: 100,
            nameTextStyle: { color: chartTextColor, fontSize: 10 },
            axisLabel: { color: chartTextColor },
            splitLine: { show: false },
        },
    ],
    series: [
        {
            name: '충전량',
            type: 'bar',
            itemStyle: { color: 'rgba(21, 224, 183, 0.58)', borderRadius: [4, 4, 0, 0] },
            data: values('ess_charge_kwh'),
        },
        {
            name: '방전량',
            type: 'bar',
            itemStyle: { color: 'rgba(231, 109, 255, 0.5)', borderRadius: [4, 4, 0, 0] },
            data: values('ess_discharge_kwh'),
        },
        {
            name: 'SOC',
            type: 'line',
            yAxisIndex: 1,
            smooth: true,
            showSymbol: false,
            lineStyle: { width: 2, color: SEMANTIC_COLORS.domain.grid },
            data: values('ess_soc'),
        },
    ],
}))
</script>
