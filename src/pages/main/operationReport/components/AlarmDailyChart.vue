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
    data: ReportStatisticsPoint[]
}>()

const chartTextColor = CHART_THEME.textColor
const chartSplitLineColor = CHART_THEME.gridLineColor
const chartAxisLineColor = CHART_THEME.axisLineColor
const chartGrid = { top: 36, right: 32, bottom: 30, left: 56 }
const dates = computed(() => props.data.map(item => item.date))
const formatDateLabel = (date: string) => date.slice(5)

const chartOption = computed<EChartsOption>(() => ({
    color: [SEMANTIC_COLORS.brand.primary],
    tooltip: {
        trigger: 'axis',
        ...CHART_THEME.tooltip,
    },
    grid: chartGrid,
    xAxis: {
        type: 'category',
        data: dates.value,
        axisLabel: { color: chartTextColor, formatter: formatDateLabel },
        axisTick: { show: false },
        axisLine: { lineStyle: { color: chartAxisLineColor } },
    },
    yAxis: {
        type: 'value',
        minInterval: 1,
        axisLabel: { color: chartTextColor },
        splitLine: { lineStyle: { color: chartSplitLineColor } },
    },
    series: [
        {
            name: '알람 수',
            type: 'bar',
            barMaxWidth: 50,
            itemStyle: {
                borderRadius: [4, 4, 0, 0],
                color: 'rgba(231, 109, 255, 0.5)',
            },
            data: props.data.map(item => item.alarm_count),
        },
    ],
}))
</script>
