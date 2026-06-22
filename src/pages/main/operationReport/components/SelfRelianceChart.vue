<template>
    <ReportEChart :option="chartOption" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import * as echarts from 'echarts'
import type { EChartsOption } from 'echarts'
import type { ReportStatisticsPoint } from '../service/operationReport.types'
import ReportEChart from './ReportEChart.vue'

const props = defineProps<{
    data: ReportStatisticsPoint[]
}>()

const chartTextColor = '#c9c1d4'
const chartSplitLineColor = 'rgba(255,255,255,0.08)'
const chartGrid = { top: 36, right: 30, bottom: 30, left: 56 }
const dates = computed(() => props.data.map(item => item.date))
const formatDateLabel = (date: string) => date.slice(5)

const chartOption = computed<EChartsOption>(() => ({
    color: ['#15e0b7'],
    tooltip: {
        trigger: 'axis',
        backgroundColor: 'rgba(255,255,255,0.92)',
        borderWidth: 0,
        textStyle: { color: '#18202b' },
    },
    grid: chartGrid,
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: dates.value,
        axisLabel: { color: chartTextColor, formatter: formatDateLabel },
        axisTick: { show: false },
        axisLine: { lineStyle: { color: 'rgba(255,255,255,0.16)' } },
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
            lineStyle: { width: 2, color: '#15e0b7' },
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
