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
const chartGrid = { top: 36, right: 28, bottom: 30, left: 56 }
const dates = computed(() => props.data.map(item => item.date))
const formatDateLabel = (date: string) => date.slice(5)
const values = (key: keyof ReportStatisticsPoint) => props.data.map(item => Number(item[key] ?? 0))

const chartOption = computed<EChartsOption>(() => ({
    color: ['#15e0b7', '#e76dff'],
    tooltip: {
        trigger: 'axis',
        backgroundColor: 'rgba(255,255,255,0.92)',
        borderWidth: 0,
        textStyle: { color: '#18202b' },
    },
    legend: { top: 0, right: 0, textStyle: { color: chartTextColor, fontSize: 10 } },
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
        name: 'kWh',
        nameTextStyle: { color: chartTextColor, fontSize: 10 },
        axisLabel: { color: chartTextColor },
        splitLine: { lineStyle: { color: chartSplitLineColor } },
    },
    series: [
        {
            name: '송전',
            type: 'line',
            smooth: true,
            showSymbol: false,
            areaStyle: { color: 'rgba(21, 224, 183, 0.18)' },
            data: values('grid_export_kwh'),
        },
        {
            name: '수전',
            type: 'line',
            smooth: true,
            showSymbol: false,
            areaStyle: { color: 'rgba(231, 109, 255, 0.16)' },
            data: values('grid_import_kwh').map(value => -value),
        },
    ],
}))
</script>
