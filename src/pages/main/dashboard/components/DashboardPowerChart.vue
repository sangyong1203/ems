<template>
    <div ref="chartRef" class="dashboard-ess-power-chart"></div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
import { COLOR_TYPE, CHART_THEME } from '@/constants/colors'
import type { DashboardTelemetryPoint } from '../service/dashboard.types'

const props = withDefaults(
    defineProps<{
        firstPoints: DashboardTelemetryPoint[] // 1차 계열 시계열 데이터 (송전/충전)
        secondPoints: DashboardTelemetryPoint[] // 2차 계열 시계열 데이터 (수전/방전)
        firstName?: string // 1차 계열 범례명
        secondName?: string // 2차 계열 범례명
        unit: string // 표시 단위 (예: kW)
    }>(),
    {
        firstName: '충전',
        secondName: '방전',
    },
)

const chartRef = ref<HTMLDivElement | null>(null) // 차트 컨테이너 DOM 요소
let chart: echarts.ECharts | null = null
let resizeObserver: ResizeObserver | null = null

// 두 시계열 데이터의 측정 시각을 결합하여 정렬된 X축 타임라인을 생성합니다.
const categories = computed(() => {
    const measuredAtSet = new Set<string>()
    props.firstPoints.forEach(item => measuredAtSet.add(item.measured_at))
    props.secondPoints.forEach(item => measuredAtSet.add(item.measured_at))
    return Array.from(measuredAtSet).sort()
})

// X축 타임라인에 맞추어 시계열 측정값을 배열로 매핑합니다.
const valuesByTime = (points: DashboardTelemetryPoint[]) => {
    const values = new Map(points.map(item => [item.measured_at, item.metric_value]))
    return categories.value.map(measuredAt => values.get(measuredAt) ?? 0)
}

// ECharts 옵션을 구성하고 이중 영역 라인 차트를 렌더링합니다.
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
            top: 28,
            right: 4,
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
            axisLabel: {
                color: CHART_THEME.textColor,
                formatter: (value: string) => value.slice(11, 16),
            },
            data: categories.value,
        },
        yAxis: {
            type: 'value',
            name: props.unit,
            nameTextStyle: { color: CHART_THEME.textColor, fontSize: 11 },
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

// 데이터 변경 시 차트를 다시 그립니다.
watch(
    () => [props.firstPoints, props.secondPoints, props.firstName, props.secondName],
    () => {
        drawChart()
    },
    { deep: true },
)

// 차트 인스턴스를 초기화하고 반응형 리사이즈 감시자를 등록합니다.
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

// 컴포넌트 해제 시 리사이즈 옵저버와 차트 인스턴스를 정리합니다.
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
