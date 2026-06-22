<template>
    <div ref="chartRef" class="ess-power-chart"></div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'

export type EssPowerChartPoint = {
    measured_at: string
    metric_value: number
}

const props = defineProps<{
    chargeData: EssPowerChartPoint[]
    dischargeData: EssPowerChartPoint[]
    socData: EssPowerChartPoint[]
    unit: string
}>()

const chartRef = ref<HTMLDivElement | null>(null)
let chart: echarts.ECharts | null = null
let resizeObserver: ResizeObserver | null = null

const categories = computed(() => {
    const measuredAtSet = new Set<string>()
    props.chargeData.forEach(item => measuredAtSet.add(item.measured_at))
    props.dischargeData.forEach(item => measuredAtSet.add(item.measured_at))
    props.socData.forEach(item => measuredAtSet.add(item.measured_at))
    return Array.from(measuredAtSet).sort()
})

const valuesByTime = (data: EssPowerChartPoint[]) => {
    const values = new Map(data.map(item => [item.measured_at, item.metric_value]))
    return categories.value.map(measuredAt => values.get(measuredAt) ?? 0)
}

const powerAxisMax = computed(() => {
    const maxPower = Math.max(
        ...props.chargeData.map(item => Math.abs(item.metric_value)),
        ...props.dischargeData.map(item => Math.abs(item.metric_value)),
        0,
    )
    return Math.max(200, Math.ceil(maxPower / 100) * 100)
})

const drawChart = () => {
    if (!chart) {
        return
    }

    chart.setOption({
        color: ['#15e0b7', '#e76dff', '#35d8ff'],
        legend: {
            top: 0,
            right: 0,
            itemWidth: 12,
            itemHeight: 8,
            textStyle: {
                color: '#c9c1d4',
                fontSize: 12,
            },
            data: ['방전 전력 (kW)', '충전 전력 (kW)', 'SOC (%)'],
        },
        grid: {
            top: 52,
            right: 48,
            bottom: 30,
            left: 56,
        },
        tooltip: {
            trigger: 'axis',
            backgroundColor: 'rgba(255,255,255,0.92)',
            borderWidth: 0,
            textStyle: {
                color: '#18202b',
            },
        },
        xAxis: {
            type: 'category',
            boundaryGap: true,
            axisLine: { lineStyle: { color: 'rgba(255,255,255,0.16)' } },
            axisTick: { show: false },
            axisLabel: {
                color: '#c9c1d4',
                formatter: (value: string) => value.slice(11, 16),
            },
            data: categories.value,
        },
        yAxis: [
            {
                type: 'value',
                name: `${props.unit}`,
                nameLocation: 'end',
                nameGap: 16,
                min: -powerAxisMax.value,
                max: powerAxisMax.value,
                interval: powerAxisMax.value / 4,
                nameTextStyle: {
                    color: '#c9c1d4',
                    fontSize: 10,
                    align: 'right',
                    padding: [0, 0, 0, 0],
                },
                axisLabel: { color: '#c9c1d4' },
                splitLine: {
                    lineStyle: {
                        color: 'rgba(255,255,255,0.08)',
                        type: 'dashed',
                    },
                },
            },
            {
                type: 'value',
                name: '%',
                nameLocation: 'end',
                nameGap: 14,
                min: 0,
                max: 100,
                interval: 20,
                nameTextStyle: {
                    color: '#c9c1d4',
                    fontSize: 12,
                    align: 'left',
                    padding: [0, 0, 0, 0],
                },
                axisLabel: { color: '#c9c1d4' },
                splitLine: { show: false },
            },
        ],
        series: [
            {
                name: '방전 전력 (kW)',
                type: 'bar',
                barMaxWidth: 18,
                stack: 'power',
                itemStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: 'rgba(21, 224, 183, 0.82)' },
                        { offset: 1, color: 'rgba(21, 224, 183, 0.34)' },
                    ]),
                },
                data: valuesByTime(props.dischargeData),
            },
            {
                name: '충전 전력 (kW)',
                type: 'bar',
                barMaxWidth: 18,
                stack: 'power',
                itemStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: 'rgba(231, 109, 255, 0.78)' },
                        { offset: 1, color: 'rgba(231, 109, 255, 0.32)' },
                    ]),
                },
                data: valuesByTime(props.chargeData).map(value => -Math.abs(value)),
            },
            {
                name: 'SOC (%)',
                type: 'line',
                yAxisIndex: 1,
                smooth: true,
                showSymbol: false,
                lineStyle: {
                    width: 3,
                    color: '#35d8ff',
                    shadowBlur: 12,
                    shadowColor: 'rgba(53, 216, 255, 0.32)',
                },
                itemStyle: {
                    color: '#35d8ff',
                },
                data: valuesByTime(props.socData),
            },
        ],
    })
}

watch(
    () => [props.chargeData, props.dischargeData, props.socData],
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
.ess-power-chart {
    flex: 1;
    width: 100%;
    height: 100%;
    min-height: 0;
}
</style>
