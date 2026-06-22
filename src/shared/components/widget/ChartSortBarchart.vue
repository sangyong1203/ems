<template>
    <div class="chart-box">
        <div class="chart-name">{{ title }}</div>
        <div class="chart" ref="chartRef"></div>
    </div>
</template>
<script lang="ts" setup>
import { CHART_COLOR } from '@/shared/constants/colors'
import * as echarts from 'echarts'
import { onMounted, reactive, ref, toRefs, watch } from 'vue'

export interface Props {
    title: string
    unit?: string
    legendData?: string[]
    xAxisData: string[]
    series: any[]
    color?: string[]
    boundaryGap?: boolean
    type: 'line' | 'bar'
    gridTop?: number
    gridRight?: number
    legendOrient?: string
    legendLeft?: number
}

const props = defineProps<Props>()
const { title, legendData, xAxisData, series, unit, color, type, gridTop, gridRight, legendOrient, legendLeft } =
    toRefs(props)

// chart
const chartRef = ref(null)
let myChart: any = null
let option = reactive({
    color: color.value ?? [
        CHART_COLOR.RED,
        CHART_COLOR.ORANGE,
        CHART_COLOR.GREEN,
        CHART_COLOR.TEAL,
        CHART_COLOR.BLUE,
        CHART_COLOR.GRAY,
    ],

    legend: {
        data: legendData.value,
        orient: legendOrient.value ?? 'horizontal',
        right: 32,
        left: legendLeft.value,
    },
    tooltip: {},
    xAxis: {
        type: 'value',
        name: unit.value,
        minInterval: 1,
        min: 0,
        max: (value: any) => Math.max(10, Math.ceil(value.max)),
    },
    yAxis: {
        type: 'category',
        boundaryGap: type.value === 'bar' ? true : false,
        data: xAxisData.value,
        inverse: true,
    },
    grid: {
        top: gridTop.value ?? 40,
        left: 32,
        right: gridRight.value ?? 32,
        bottom: 10,
        containLabel: true,
    },
    series: series.value,
})
function drawChart() {
    option.legend.data = legendData.value
    option.yAxis.data = xAxisData.value
    series.value.forEach(item => {
        item.realtimeSort = true
    })
    option.series = series.value
    console.log('draw short =-------option', series.value)
    option && myChart.setOption(option)
}
watch(series, () => {
    drawChart()
})
onMounted(() => {
    myChart = echarts.init(chartRef.value)
    drawChart()
    // Resize chart
    new ResizeObserver(() => {
        myChart.resize()
    }).observe(chartRef.value!)
})
</script>
<style scoped>
.chart-box {
    flex: 1;
    height: 100%;
    border: 1px solid var(--common-component-border-color);
    border-radius: 6px;
    background: var(--common-component-bg-color);
    color: var(--text-color--body);
    overflow: hidden;
}

.chart-name {
    width: 100%;
    padding: 24px 24px 12px 24px;
    border-bottom: none;
    text-align: left;
    font-weight: 700;
    color: var(--text-color--primary);
}

.chart {
    height: calc(100% - 68px);
    width: 100%;
}
</style>
