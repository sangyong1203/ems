<template>
    <div ref="chartRef" class="ess-rack-temperature-chart"></div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
import { COLOR_TYPE, CHART_THEME } from '@/constants/colors'
import type { EssRackTemperatureHistory } from '../service/ess.types'

const props = defineProps<{
    series: EssRackTemperatureHistory[] // 랙별 온도 시계열 데이터
    warningTemperature?: number // 주의 기준 온도 (°C)
    faultTemperature?: number // 장애 기준 온도 (°C)
}>()

const chartRef = ref<HTMLDivElement | null>(null) // 차트 DOM 엘리먼트
let chart: echarts.ECharts | null = null // ECharts 인스턴스
let resizeObserver: ResizeObserver | null = null // 화면 크기 변경 감지 옵저버

type ChartLabelParam = {
    name?: string
}

const lineColors = [
    COLOR_TYPE.SECONDARY,
    COLOR_TYPE.PRIMARY,
    COLOR_TYPE.BLUE,
    COLOR_TYPE.ORANGE,
    COLOR_TYPE.MINT,
    COLOR_TYPE.RED,
    COLOR_TYPE.GREEN,
    COLOR_TYPE.YELLOW,
]

const categories = computed(() => {
    const times = new Set<string>()
    props.series.forEach(rack => {
        rack.data.forEach(item => times.add(item.measured_at))
    })
    return Array.from(times).sort()
})

const temperatureAxisRange = computed(() => {
    const values = props.series.flatMap(rack => rack.data.map(item => item.metric_value))
    const limitValues = [props.warningTemperature, props.faultTemperature].filter(
        (value): value is number => typeof value === 'number',
    )
    const axisValues = [...values, ...limitValues]
    if (axisValues.length === 0) {
        return { min: 0, max: 50 }
    }

    const min = Math.min(...axisValues)
    const max = Math.max(...axisValues)
    const padding = Math.max((max - min) * 0.25, 3)
    return {
        min: Math.min(0, Math.floor(min - padding)),
        max: Math.ceil(max + padding),
    }
})

const temperatureLimitLines = computed(() => {
    return [
        ...(typeof props.warningTemperature === 'number'
            ? [
                  {
                      name: `주의 ${props.warningTemperature.toLocaleString(undefined, { maximumFractionDigits: 1 })}°C`,
                      yAxis: props.warningTemperature,
                      lineStyle: {
                          color: 'rgba(241, 156, 77, 0.72)',
                      },
                      label: {
                          color: '#f1c08a',
                      },
                  },
              ]
            : []),
        ...(typeof props.faultTemperature === 'number'
            ? [
                  {
                      name: `장애 ${props.faultTemperature.toLocaleString(undefined, { maximumFractionDigits: 1 })}°C`,
                      yAxis: props.faultTemperature,
                      lineStyle: {
                          color: 'rgba(249, 96, 96, 0.78)',
                      },
                      label: {
                          color: '#ff8b8b',
                      },
                  },
              ]
            : []),
    ]
})

// formatTime 시간 문자열(HH:mm) 포맷팅
const formatTime = (value: string) => {
    return value.slice(11, 16)
}

// drawChart 랙별 온도 라인 차트 렌더링
const drawChart = () => {
    if (!chart) {
        return
    }

    const times = categories.value

    chart.setOption({
        color: lineColors,
        grid: {
            top: 32,
            right: 10,
            bottom: 22,
            left: 24,
        },
        legend: {
            top: 0,
            type: 'scroll',
            itemWidth: 6,
            itemHeight: 6,
            textStyle: {
                color: CHART_THEME.textColor,
                fontSize: 10,
            },
            pageIconColor: COLOR_TYPE.PRIMARY,
            pageIconInactiveColor: 'rgba(255,255,255,0.18)',
            pageTextStyle: {
                color: CHART_THEME.textColor,
            },
            data: props.series.map(rack => rack.rackName),
        },
        tooltip: {
            trigger: 'axis',
            ...CHART_THEME.tooltip,
            valueFormatter: (value: unknown) => {
                return typeof value === 'number'
                    ? `${value.toLocaleString(undefined, { maximumFractionDigits: 1 })} °C`
                    : '-'
            },
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            axisLine: { lineStyle: { color: CHART_THEME.axisLineColor } },
            axisTick: { show: false },
            axisLabel: {
                color: CHART_THEME.textColor,
                formatter: formatTime,
            },
            data: times,
        },
        yAxis: {
            type: 'value',
            min: temperatureAxisRange.value.min,
            max: temperatureAxisRange.value.max,
            splitNumber: 5,
            nameTextStyle: {
                color: CHART_THEME.textColor,
                fontSize: 11,
                align: 'right',
                padding: [0, 0, 0, 0],
            },
            axisLabel: { color: CHART_THEME.textColor },
            splitLine: { lineStyle: { color: CHART_THEME.gridLineColor } },
        },
        series: props.series.map((rack, index) => {
            const dataByTime = new Map(rack.data.map(item => [item.measured_at, item.metric_value]))
            return {
                name: rack.rackName,
                type: 'line',
                smooth: true,
                showSymbol: false,
                connectNulls: true,
                data: times.map(time => dataByTime.get(time) ?? null),
                lineStyle: {
                    width: 1.2,
                    color: lineColors[index % lineColors.length],
                },
                itemStyle: {
                    color: lineColors[index % lineColors.length],
                },
                emphasis: {
                    focus: 'series',
                    lineStyle: {
                        width: 2,
                    },
                },
                markLine:
                    index === 0 && temperatureLimitLines.value.length > 0
                        ? {
                              silent: true,
                              symbol: 'none',
                              label: {
                                  fontSize: 9,
                                  fontWeight: 400,
                                  formatter: (params: ChartLabelParam) => String(params.name ?? ''),
                                  position: 'insideStartTop',
                                  distance: [0, 4],
                              },
                              lineStyle: {
                                  type: 'dashed',
                                  width: 1,
                              },
                              data: temperatureLimitLines.value,
                          }
                        : undefined,
            }
        }),
    })
}

// watch(props.series) 데이터 변경 시 차트 재렌더링
watch(
    () => props.series,
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

<style scoped lang="scss">
.ess-rack-temperature-chart {
    width: 100%;
    height: 100%;
    min-height: 0;
    flex: 1;
}
</style>
