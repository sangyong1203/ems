<template>
    <div class="chart-box">
        <div class="chart-name">{{ title }}</div>
        <div class="chart" ref="chartRef"></div>
    </div>
</template>
<script lang="ts" setup>
import { onMounted, reactive, ref, toRefs, watch } from 'vue'
import * as echarts from 'echarts'
import { CHART_COLOR } from '@/shared/constants/colors'

export interface Props {
    title?: string
    xAxisData: string[]
    series: any[]
    type: 'line' | 'bar'
    unit?: string
    legendData?: string[]
    color?: string[]
    boundaryGap?: boolean
    gridTop?: number
    gridRight?: number
    gridLeft?: number
    girdBottom?: number
    legendOrient?: string // legend 諛⑺뼢
    legendLeft?: number
    yMax?: number
}

const props = defineProps<Props>()
const {
    title,
    legendData,
    xAxisData,
    series,
    unit,
    color,
    type,
    gridTop,
    gridRight,
    gridLeft,
    girdBottom,
    legendOrient,
    legendLeft,
    yMax,
} = toRefs(props)

// chart
const chartRef = ref(null)
let myChart: any = null
let option = reactive({
    color: color.value ?? ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4'],

    legend: {
        data: legendData.value,
        orient: legendOrient.value ?? 'horizontal',
        right: 32,
        left: legendLeft.value,
    },
    tooltip: {},
    xAxis: {
        type: 'category',
        boundaryGap: type.value === 'bar' ? true : false,
        data: xAxisData.value,
        axisLabel: {
            rotate: 0,
        },
    },
    yAxis: {
        type: 'value',
        name: unit.value,
        max: yMax.value,
    },
    grid: {
        top: gridTop.value ?? 40,
        left: gridLeft.value ?? 32,
        right: gridRight.value ?? 32,
        bottom: girdBottom.value ?? 10,
        containLabel: true,
    },
    series: series.value,
})
const getAxsisLabelRotate = () => {
    let axisLabelRotate = 0
    if (xAxisData.value.length > 10) {
        axisLabelRotate = 50
    }
    return axisLabelRotate
}
function drawChart() {
    option.legend.data = legendData.value
    option.xAxis.data = xAxisData.value
    option.series = series.value
    option.xAxis.axisLabel.rotate = getAxsisLabelRotate()
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
