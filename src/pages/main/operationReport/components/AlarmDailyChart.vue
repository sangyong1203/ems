<template>
    <ReportEChart :option="chartOption" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { EChartsOption } from 'echarts'
import type { ReportStatisticsPoint } from '../service/operationReport.types'
import ReportEChart from './ReportEChart.vue'

const props = defineProps<{
    data: ReportStatisticsPoint[]
}>()

const chartTextColor = '#c9c1d4'
const chartSplitLineColor = 'rgba(255,255,255,0.08)'
const chartGrid = { top: 36, right: 32, bottom: 30, left: 56 }
const dates = computed(() => props.data.map(item => item.date))
const formatDateLabel = (date: string) => date.slice(5)

const chartOption = computed<EChartsOption>(() => ({
    color: ['#e76dff'],
    tooltip: {
        trigger: 'axis',
        backgroundColor: 'rgba(255,255,255,0.92)',
        borderWidth: 0,
        textStyle: { color: '#18202b' },
    },
    grid: chartGrid,
    xAxis: {
        type: 'category',
        data: dates.value,
        axisLabel: { color: chartTextColor, formatter: formatDateLabel },
        axisTick: { show: false },
        axisLine: { lineStyle: { color: 'rgba(255,255,255,0.16)' } },
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
