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
const chartGrid = { top: 36, right: 42, bottom: 30, left: 56 }
const formatDateLabel = (date: string) => date.slice(5)
const dates = computed(() => props.data.map(item => item.date))
const values = (key: keyof ReportStatisticsPoint) => props.data.map(item => Number(item[key] ?? 0))

const chartOption = computed<EChartsOption>(() => ({
    color: ['#15e0b7', '#4ca5d7', '#e76dff'],
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
            name: '태양광 공급',
            type: 'line',
            stack: 'load',
            smooth: true,
            showSymbol: false,
            areaStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: 'rgba(21, 224, 183, 0.78)' },
                    { offset: 1, color: 'rgba(21, 224, 183, 0.08)' },
                ]),
            },
            data: values('load_solar_kwh'),
        },
        {
            name: '계통 공급',
            type: 'line',
            stack: 'load',
            smooth: true,
            showSymbol: false,
            areaStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: 'rgba(76, 165, 215, 0.62)' },
                    { offset: 1, color: 'rgba(76, 165, 215, 0.08)' },
                ]),
            },
            data: values('load_grid_kwh'),
        },
        {
            name: 'ESS 공급',
            type: 'line',
            stack: 'load',
            smooth: true,
            showSymbol: false,
            areaStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: 'rgba(231, 109, 255, 0.5)' },
                    { offset: 1, color: 'rgba(231, 109, 255, 0.08)' },
                ]),
            },
            data: values('load_ess_kwh'),
        },
    ],
}))
</script>
