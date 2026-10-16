<template>
    <ReportEChart :option="chartOption" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import * as echarts from 'echarts'
import type { EChartsOption } from 'echarts'
import type { ReportStatisticsPoint } from '../service/operationReport.types'
import ReportEChart from './ReportEChart.vue'
import { CHART_THEME, SEMANTIC_COLORS } from '@/constants/colors'

const props = defineProps<{
    data: ReportStatisticsPoint[] // 일별 에너지 자립률 통계 데이터
}>()

const chartTextColor = CHART_THEME.textColor
const chartSplitLineColor = CHART_THEME.gridLineColor
const chartAxisLineColor = CHART_THEME.axisLineColor
const chartGrid = { top: 36, right: 30, bottom: 30, left: 56 }
const dates = computed(() => props.data.map(item => item.date))

// formatDateLabel 날짜 라벨(MM-DD) 포맷팅
const formatDateLabel = (date: string) => date.slice(5)

const chartOption = computed<EChartsOption>(() => ({
    color: [SEMANTIC_COLORS.domain.solar],
    tooltip: {
        trigger: 'axis',
        ...CHART_THEME.tooltip,
    },
    grid: chartGrid,
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: dates.value,
        axisLabel: { color: chartTextColor, formatter: formatDateLabel },
        axisTick: { show: false },
        axisLine: { lineStyle: { color: chartAxisLineColor } },
    },
    yAxis: {
        type: 'value',
        min: 0,
        max: 100,
        axisLabel: { color: chartTextColor, formatter: '{value}%' },
        splitLine: { lineStyle: { color: chartSplitLineColor } },
    },
    series: [
        {
            name: '자립률',
            type: 'line',
            smooth: true,
            showSymbol: false,
            lineStyle: { width: 2, color: SEMANTIC_COLORS.domain.solar },
            areaStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: 'rgba(21, 224, 183, 0.72)' },
                    { offset: 1, color: 'rgba(21, 224, 183, 0.06)' },
                ]),
            },
            data: props.data.map(item => item.self_reliance_rate),
        },
    ],
}))
</script>
