<template>
    <div ref="chartRef" class="dashboard-ess-power-chart"></div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
import { COLOR_TYPE } from '@/shared/constants/colors'
import type { DashboardTelemetryPoint } from '../service/dashboard.types'

const props = withDefaults(
    defineProps<{
        firstPoints: DashboardTelemetryPoint[]
        secondPoints: DashboardTelemetryPoint[]
        firstName?: string
        secondName?: string
        unit: string
    }>(),
    {
        firstName: '충전',
        secondName: '방전',
    },
)

const chartRef = ref<HTMLDivElement | null>(null)
let chart: echarts.ECharts | null = null
let resizeObserver: ResizeObserver | null = null

const categories = computed(() => {
    const measuredAtSet = new Set<string>()
    props.firstPoints.forEach(item => measuredAtSet.add(item.measured_at))
    props.secondPoints.forEach(item => measuredAtSet.add(item.measured_at))
    return Array.from(measuredAtSet).sort()
})

const valuesByTime = (points: DashboardTelemetryPoint[]) => {
    const values = new Map(points.map(item => [item.measured_at, item.metric_value]))
    return categories.value.map(measuredAt => values.get(measuredAt) ?? 0)
}

const drawChart = () => {
    if (!chart) {
        return
    }

    chart.setOption({
        color: [COLOR_TYPE.SECONDARY, COLOR_TYPE.PRIMARY],
        legend: {
            top: 0,
            right: 0,
            itemWidth: 10,
            itemHeight: 6,
            textStyle: {
                color: '#c9c1d4',
                fontSize: 11,
            },
            data: [props.firstName, props.secondName],
        },
        grid: {
            top: 28,
            right: 4,
            bottom: 24,
            left: 44,
        },
        tooltip: {
            trigger: 'axis',
            valueFormatter: (value: number) =>
                `${value.toLocaleString(undefined, { maximumFractionDigits: 1 })} ${props.unit}`,
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            axisLine: { lineStyle: { color: 'rgba(255,255,255,0.16)' } },
            axisLabel: {
                color: '#c9c1d4',
                formatter: (value: string) => value.slice(11, 16),
            },
            data: categories.value,
        },
        yAxis: {
            type: 'value',
            name: props.unit,
            nameTextStyle: { color: '#c9c1d4', fontSize: 11 },
            axisLabel: { color: '#c9c1d4' },
            splitLine: { lineStyle: { color: 'rgba(255,255,255,0.08)' } },
        },
        series: [
            {
                name: props.firstName,
                type: 'line',
                smooth: true,
                showSymbol: false,
                lineStyle: {
                    width: 1,
                    color: COLOR_TYPE.SECONDARY,
                },
                itemStyle: {
                    color: COLOR_TYPE.SECONDARY,
                },
                areaStyle: {
                    opacity: 0.8,
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: COLOR_TYPE.SECONDARY },
                        { offset: 1, color: 'rgba(21, 224, 183, 0.16)' },
                    ]),
                },
                data: valuesByTime(props.firstPoints),
            },
            {
                name: props.secondName,
                type: 'line',
                smooth: true,
                showSymbol: false,
                lineStyle: {
                    width: 1,
                    color: COLOR_TYPE.PRIMARY,
                },
                itemStyle: {
                    color: COLOR_TYPE.PRIMARY,
                },
                areaStyle: {
                    opacity: 0.8,
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: COLOR_TYPE.PRIMARY },
                        { offset: 1, color: 'rgba(231, 109, 255, 0.16)' },
                    ]),
                },
                data: valuesByTime(props.secondPoints),
            },
        ],
    })
}

watch(
    () => [props.firstPoints, props.secondPoints, props.firstName, props.secondName],
    () => {
        drawChart()
    },
    { deep: true },
)

onMounted(() => {
    if (!chartRef.value) {
        return
    }

    chart = echarts.init(chartRef.value)
    resizeObserver = new ResizeObserver(() => {
        chart?.resize()
    })
    resizeObserver.observe(chartRef.value)
    drawChart()
})

onBeforeUnmount(() => {
    resizeObserver?.disconnect()
    chart?.dispose()
})
</script>

<style scoped>
.dashboard-ess-power-chart {
    width: 100%;
    flex: 1;
    min-height: 0;
    height: 100%;
}
</style>
