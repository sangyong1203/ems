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
const chartGrid = { top: 50, right: 38, bottom: 30, left: 56 }
const dates = computed(() => props.data.map(item => item.date))
const formatDateLabel = (date: string) => date.slice(5)
const values = (key: keyof ReportStatisticsPoint) => props.data.map(item => Number(item[key] ?? 0))

const chartOption = computed<EChartsOption>(() => ({
    color: ['#15e0b7', '#e76dff', '#4ca5d7'],
    tooltip: {
        trigger: 'axis',
        backgroundColor: 'rgba(255,255,255,0.92)',
        borderWidth: 0,
        textStyle: { color: '#18202b' },
    },
    legend: { top: 0, right: 5, textStyle: { color: chartTextColor, fontSize: 10 } },
    grid: chartGrid,
    xAxis: {
        type: 'category',
        data: dates.value,
        axisLabel: { color: chartTextColor, formatter: formatDateLabel },
        axisTick: { show: false },
        axisLine: { lineStyle: { color: 'rgba(255,255,255,0.16)' } },
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
            lineStyle: { width: 2, color: '#4ca5d7' },
            data: values('ess_soc'),
        },
    ],
}))
</script>
