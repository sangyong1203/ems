<template>
    <div ref="chartRef" class="trend-dual-area-chart"></div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
import { COLOR_TYPE } from '@/shared/constants/colors'
import type { TrendTelemetryPoint } from '../service/trend.types'

const props = defineProps<{
    firstName: string
    secondName: string
    firstData: TrendTelemetryPoint[]
    secondData: TrendTelemetryPoint[]
    unit: string
}>()

const chartRef = ref<HTMLDivElement | null>(null)
let chart: echarts.ECharts | null = null
let resizeObserver: ResizeObserver | null = null

const categories = computed(() => {
    const measuredAtSet = new Set<string>()
    props.firstData.forEach(item => measuredAtSet.add(item.measured_at))
    props.secondData.forEach(item => measuredAtSet.add(item.measured_at))
    return Array.from(measuredAtSet).sort()
})

const valuesByTime = (data: TrendTelemetryPoint[]) => {
    const valueMap = new Map(data.map(item => [item.measured_at, item.metric_value]))
    return categories.value.map(measuredAt => valueMap.get(measuredAt) ?? 0)
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
            top: 32,
            right: 20,
            bottom: 28,
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
            axisTick: { show: false },
            axisLabel: {
                color: '#c9c1d4',
                formatter: (value: string) => value.slice(11, 16),
            },
            data: categories.value,
        },
        yAxis: {
            type: 'value',
            name: props.unit,
            nameTextStyle: { color: '#c9c1d4' },
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
                    width: 2,
                    color: COLOR_TYPE.SECONDARY,
                    shadowBlur: 10,
                    shadowColor: 'rgba(21, 224, 183, 0.4)',
                },
                itemStyle: { color: COLOR_TYPE.SECONDARY },
                areaStyle: {
                    opacity: 0.72,
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: 'rgba(21, 224, 183, 0.72)' },
                        { offset: 1, color: 'rgba(21, 224, 183, 0.08)' },
                    ]),
                },
                data: valuesByTime(props.firstData),
            },
            {
                name: props.secondName,
                type: 'line',
                smooth: true,
                showSymbol: false,
                lineStyle: {
                    width: 2,
                    color: COLOR_TYPE.PRIMARY,
                    shadowBlur: 10,
                    shadowColor: 'rgba(231, 109, 255, 0.36)',
                },
                itemStyle: { color: COLOR_TYPE.PRIMARY },
                areaStyle: {
                    opacity: 0.62,
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: 'rgba(231, 109, 255, 0.62)' },
                        { offset: 1, color: 'rgba(231, 109, 255, 0.08)' },
                    ]),
                },
                data: valuesByTime(props.secondData),
            },
        ],
    })
}

watch(
    () => [props.firstData, props.secondData],
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
.trend-dual-area-chart {
    width: 100%;
    height: 100%;
    min-height: 0;
    flex: 1;
}
</style>
