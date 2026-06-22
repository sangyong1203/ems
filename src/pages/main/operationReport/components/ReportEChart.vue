<template>
    <div ref="chartRef" class="report-echart"></div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
import type { EChartsOption } from 'echarts'

const props = defineProps<{
    option: EChartsOption
}>()

const chartRef = ref<HTMLDivElement | null>(null)
let chart: echarts.ECharts | null = null
let resizeObserver: ResizeObserver | null = null

const drawChart = () => {
    if (!chart) {
        return
    }
    chart.setOption(props.option, true)
}

watch(
    () => props.option,
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
.report-echart {
    width: 100%;
    height: 100%;
    min-height: 0;
}
</style>
