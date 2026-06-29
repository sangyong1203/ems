<template>
    <div ref="chartRef" class="trend-area-chart"></div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
import { COLOR_TYPE } from '@/shared/constants/colors'

export type TrendAreaChartDataItem = {
    measured_at: string
    metric_value: number
}

const props = withDefaults(
    defineProps<{
        data: TrendAreaChartDataItem[]
        name: string
        unit: string
        capacity?: number
        showPeak?: boolean
        lineWidth?: number
        showLineGlow?: boolean
        gridTop?: number
        gridRight?: number
        gridBottom?: number
        gridLeft?: number
        yAxisName?: string
        ySplitNumber?: number
    }>(),
    {
        showPeak: true,
        lineWidth: 1,
        showLineGlow: false,
        gridTop: 28,
        gridRight: 4,
        gridBottom: 20,
        gridLeft: 30,
        yAxisName: undefined,
        ySplitNumber: undefined,
    },
)

const chartRef = ref<HTMLDivElement | null>(null)
let chart: echarts.ECharts | null = null
let resizeObserver: ResizeObserver | null = null

const peakPoint = computed(() => {
    return props.data.reduce<TrendAreaChartDataItem | null>((peak, item) => {
        if (!peak || item.metric_value > peak.metric_value) {
            return item
        }
        return peak
    }, null)
})

const drawChart = () => {
    if (!chart) {
        return
    }

    chart.setOption({
        color: [COLOR_TYPE.SECONDARY],
        grid: {
            top: props.gridTop,
            right: props.gridRight,
            bottom: props.gridBottom,
            left: props.gridLeft,
        },
        tooltip: {
            trigger: 'axis',
            backgroundColor: 'rgba(255,255,255,0.92)',
            borderWidth: 0,
            textStyle: {
                color: '#18202b',
            },
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
            data: props.data.map(item => item.measured_at),
        },
        yAxis: {
            type: 'value',
            name: props.yAxisName ?? props.unit,
            nameTextStyle: {
                color: '#c9c1d4',
                fontSize: 11,
                align: 'right',
                padding: [0, 0, 0, 0],
            },
            axisLabel: { color: '#c9c1d4' },
            splitLine: { lineStyle: { color: 'rgba(255,255,255,0.08)' } },
            splitNumber: props.ySplitNumber,
        },
        series: [
            {
                name: props.name,
                type: 'line',
                smooth: true,
                showSymbol: false,
                lineStyle: {
                    width: props.lineWidth,
                    color: COLOR_TYPE.SECONDARY,
                    shadowBlur: props.showLineGlow ? 12 : 0,
                    shadowColor: props.showLineGlow ? 'rgba(21, 224, 183, 0.45)' : 'transparent',
                },
                itemStyle: {
                    color: COLOR_TYPE.SECONDARY,
                },
                areaStyle: {
                    opacity: 0.95,
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: 'rgba(21, 224, 183, 0.82)' },
                        { offset: 0.65, color: 'rgba(76, 165, 215, 0.42)' },
                        { offset: 1, color: 'rgba(231, 109, 255, 0.08)' },
                    ]),
                },
                markLine: props.capacity
                    ? {
                          silent: true,
                          symbol: 'none',
                          label: {
                              show: false,
                          },
                          lineStyle: {
                              color: COLOR_TYPE.PRIMARY,
                              type: 'dashed',
                              width: 1,
                              opacity: 0.72,
                          },
                          data: [{ yAxis: props.capacity }],
                      }
                    : undefined,
                markPoint:
                    props.showPeak && peakPoint.value
                        ? {
                              symbol: 'circle',
                              symbolSize: 9,
                              label: {
                                  formatter: `피크 ${peakPoint.value.metric_value.toLocaleString(undefined, {
                                      maximumFractionDigits: 1,
                                  })} ${props.unit}`,
                                  color: '#ffffff',
                                  fontSize: 11,
                                  offset: [0, -8],
                              },
                              itemStyle: {
                                  color: '#ffffff',
                                  borderColor: COLOR_TYPE.SECONDARY,
                                  borderWidth: 2,
                              },
                              data: [
                                  {
                                      coord: [peakPoint.value.measured_at, peakPoint.value.metric_value],
                                  },
                              ],
                          }
                        : undefined,
                data: props.data.map(item => item.metric_value),
            },
        ],
    })
}

watch(
    () => [props.data, props.capacity],
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
.trend-area-chart {
    width: 100%;
    flex: 1;
    min-height: 0;
    height: 100%;
}
</style>
