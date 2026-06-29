<template>
    <div ref="chartRef" class="ess-soc-voltage-chart"></div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
import { COLOR_TYPE } from '@/shared/constants/colors'
import type { EssTelemetryPoint } from '../service/ess.types'

const props = defineProps<{
    socData: EssTelemetryPoint[]
    voltageData: EssTelemetryPoint[]
    voltageMin?: number
    voltageMax?: number
}>()

const chartRef = ref<HTMLDivElement | null>(null)
let chart: echarts.ECharts | null = null
let resizeObserver: ResizeObserver | null = null

type ChartTooltipParam = {
    axisValueLabel?: string
    marker?: string
    seriesName?: string
    value?: unknown
}

type ChartLabelParam = {
    name?: string
}

const categories = computed(() => {
    const times = new Set<string>()
    props.socData.forEach(item => times.add(item.measured_at))
    props.voltageData.forEach(item => times.add(item.measured_at))
    return Array.from(times).sort()
})

const socByTime = computed(() => {
    return new Map(props.socData.map(item => [item.measured_at, item.metric_value]))
})

const voltageByTime = computed(() => {
    return new Map(props.voltageData.map(item => [item.measured_at, item.metric_value]))
})

const voltageAxisRange = computed(() => {
    const values = props.voltageData.map(item => item.metric_value)
    const limitValues = [props.voltageMin, props.voltageMax].filter(
        (value): value is number => typeof value === 'number',
    )
    const axisValues = [...values, ...limitValues]
    if (axisValues.length === 0) {
        return { min: 760, max: 880, interval: 40 }
    }

    const min = Math.min(...axisValues)
    const max = Math.max(...axisValues)
    const span = max - min
    const padding = Math.max(span * 0.2, 12)
    const interval = span <= 80 ? 40 : span <= 160 ? 50 : 100
    const axisMin = Math.max(0, Math.floor((min - padding) / interval) * interval)
    const axisMax = Math.ceil((max + padding) / interval) * interval

    return {
        min: axisMin,
        max: Math.max(axisMax, axisMin + interval * 2),
        interval,
    }
})

const voltageLimitLines = computed(() => {
    return [
        ...(typeof props.voltageMax === 'number'
            ? [
                  {
                      name: `전압 상한 ${props.voltageMax.toLocaleString(undefined, { maximumFractionDigits: 1 })} V`,
                      yAxis: props.voltageMax,
                  },
              ]
            : []),
        ...(typeof props.voltageMin === 'number'
            ? [
                  {
                      name: `전압 하한 ${props.voltageMin.toLocaleString(undefined, { maximumFractionDigits: 1 })} V`,
                      yAxis: props.voltageMin,
                  },
              ]
            : []),
    ]
})

const formatTime = (value: string) => {
    return value.slice(11, 16)
}

const drawChart = () => {
    if (!chart) {
        return
    }

    const times = categories.value

    chart.setOption({
        color: [COLOR_TYPE.PRIMARY, COLOR_TYPE.SECONDARY],
        grid: {
            top: 32,
            right: 34,
            bottom: 22,
            left: 28,
        },
        legend: {
            itemWidth: 10,
            itemHeight: 6,
            textStyle: {
                color: '#d9d4e3',
                fontSize: 10,
            },
            data: ['전압 (V)', 'SOC (%)'],
        },
        tooltip: {
            trigger: 'axis',
            backgroundColor: 'rgba(255,255,255,0.92)',
            borderWidth: 0,
            textStyle: {
                color: '#18202b',
            },
            formatter: (params: ChartTooltipParam | ChartTooltipParam[]) => {
                const items = Array.isArray(params) ? params : [params]
                const time = items[0]?.axisValueLabel ?? ''
                const rows = items.map(item => {
                    const value = typeof item.value === 'number' ? item.value : null
                    const unit = item.seriesName === '전압 (V)' ? 'V' : '%'
                    const text = value === null ? '-' : value.toLocaleString(undefined, { maximumFractionDigits: 1 })
                    return `${item.marker} ${item.seriesName} <b>${text} ${unit}</b>`
                })
                return [time, ...rows].join('<br/>')
            },
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            axisLine: { lineStyle: { color: 'rgba(255,255,255,0.16)' } },
            axisTick: { show: false },
            axisLabel: {
                color: '#c9c1d4',
                formatter: formatTime,
            },
            data: times,
        },
        yAxis: [
            {
                type: 'value',
                name: '%',
                min: 0,
                max: 100,
                interval: 25,
                nameTextStyle: {
                    color: '#c9c1d4',
                    fontSize: 11,
                    align: 'right',
                    padding: [0, 0, 0, 0],
                },
                axisLabel: { color: '#c9c1d4' },
                splitLine: { lineStyle: { color: 'rgba(255,255,255,0.08)' } },
            },
            {
                type: 'value',
                name: 'V',
                min: voltageAxisRange.value.min,
                max: voltageAxisRange.value.max,
                interval: voltageAxisRange.value.interval,
                nameTextStyle: {
                    color: '#c9c1d4',
                    fontSize: 11,
                    align: 'left',
                    padding: [0, 0, 0, 0],
                },
                axisLabel: { color: '#c9c1d4' },
                splitLine: { show: false },
            },
        ],
        series: [
            {
                name: '전압 (V)',
                type: 'line',
                smooth: true,
                showSymbol: false,
                yAxisIndex: 1,
                data: times.map(time => voltageByTime.value.get(time) ?? null),
                lineStyle: {
                    width: 1.4,
                    color: COLOR_TYPE.PRIMARY,
                    shadowBlur: 0,
                },
                itemStyle: {
                    color: COLOR_TYPE.PRIMARY,
                },
                emphasis: {
                    focus: 'series',
                    lineStyle: {
                        width: 2.2,
                    },
                },
                markLine:
                    voltageLimitLines.value.length > 0
                        ? {
                              silent: true,
                              symbol: 'none',
                              label: {
                                  color: 'rgba(0, 225, 225, 0.9)',
                                  fontSize: 9,
                                  fontWeight: 400,
                                  formatter: (params: ChartLabelParam) => String(params.name ?? ''),
                                  position: 'insideStartTop',
                                  distance: [0, 4],
                              },
                              lineStyle: {
                                  color: 'rgba(0, 225, 225, 0.45)',
                                  type: 'dashed',
                                  width: 1,
                              },
                              data: voltageLimitLines.value,
                          }
                        : undefined,
            },
            {
                name: 'SOC (%)',
                type: 'line',
                smooth: true,
                showSymbol: false,
                yAxisIndex: 0,
                data: times.map(time => socByTime.value.get(time) ?? null),
                lineStyle: {
                    width: 1.2,
                    color: COLOR_TYPE.SECONDARY,
                    shadowBlur: 6,
                    shadowColor: 'rgba(21, 224, 183, 0.3)',
                },
                itemStyle: {
                    color: COLOR_TYPE.SECONDARY,
                },
                areaStyle: {
                    opacity: 0.45,
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: 'rgba(21, 224, 183, 0.32)' },
                        { offset: 0.55, color: 'rgba(76, 165, 215, 0.16)' },
                        { offset: 1, color: 'rgba(76, 165, 215, 0)' },
                    ]),
                },
            },
        ],
    })
}

watch(
    () => [props.socData, props.voltageData],
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

<style scoped lang="scss">
.ess-soc-voltage-chart {
    width: 100%;
    height: 100%;
    min-height: 0;
    flex: 1;
}
</style>
