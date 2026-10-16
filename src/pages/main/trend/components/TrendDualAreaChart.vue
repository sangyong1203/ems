<template>
    <div ref="chartRef" class="trend-dual-area-chart"></div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
import { COLOR_TYPE, CHART_THEME } from '@/constants/colors'
import type { TrendTelemetryPoint } from '../service/trend.types'

const props = defineProps<{
    firstName: string // 첫 번째 시리즈 명칭
    secondName: string // 두 번째 시리즈 명칭
    firstData: TrendTelemetryPoint[] // 첫 번째 시계열 데이터
    secondData: TrendTelemetryPoint[] // 두 번째 시계열 데이터
    unit: string // 표시 단위
}>()

const chartRef = ref<HTMLDivElement | null>(null) // 차트 DOM 엘리먼트
let chart: echarts.ECharts | null = null // ECharts 인스턴스
let resizeObserver: ResizeObserver | null = null // 화면 크기 변경 감지 옵저버

const categories = computed(() => {
    const measuredAtSet = new Set<string>()
    props.firstData.forEach(item => measuredAtSet.add(item.measured_at))
    props.secondData.forEach(item => measuredAtSet.add(item.measured_at))
    return Array.from(measuredAtSet).sort()
})

// valuesByTime 시간대별 데이터 배열 매핑
const valuesByTime = (data: TrendTelemetryPoint[]) => {
    const valueMap = new Map(data.map(item => [item.measured_at, item.metric_value]))
    return categories.value.map(measuredAt => valueMap.get(measuredAt) ?? 0)
}

// drawChart 이중 영역 라인 차트 렌더링
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
                color: CHART_THEME.textColor,
                fontSize: 11,
            },
            data: [props.firstName, props.secondName],
        },
        grid: {
            top: 32,
            right: 20,
            bottom: 20,
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
            axisLine: { lineStyle: { color: CHART_THEME.axisLineColor } },
            axisTick: { show: false },
            axisLabel: {
                color: CHART_THEME.textColor,
                formatter: (value: string) => value.slice(11, 16),
            },
            data: categories.value,
        },
        yAxis: {
            type: 'value',
            name: props.unit,
            nameTextStyle: { color: CHART_THEME.textColor },
            axisLabel: { color: CHART_THEME.textColor },
            splitLine: { lineStyle: { color: CHART_THEME.gridLineColor } },
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

// watch(props) 데이터 변경 시 차트 재렌더링
watch(
    () => [props.firstData, props.secondData],
    () => {
        drawChart()
    },
    { deep: true },
)

// onMounted 차트 초기화 및 리사이즈 옵저버 등록
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

// onBeforeUnmount 차트 인스턴스 및 옵저버 해제
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
