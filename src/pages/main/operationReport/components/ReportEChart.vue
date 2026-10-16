<template>
    <div ref="chartRef" class="report-echart"></div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
import type { EChartsOption } from 'echarts'

const props = defineProps<{
    option: EChartsOption // ECharts 옵션 객체
}>()

const chartRef = ref<HTMLDivElement | null>(null) // 차트 컨테이너 엘리먼트
let chart: echarts.ECharts | null = null // ECharts 인스턴스
let resizeObserver: ResizeObserver | null = null // 화면 크기 변경 감지 옵저버

// drawChart ECharts 옵션 반영 렌더링
const drawChart = () => {
    if (!chart) {
        return
    }
    chart.setOption(props.option, true)
}

// watch(props.option) 옵션 변경 시 차트 재렌더링
watch(
    () => props.option,
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
.report-echart {
    width: 100%;
    height: 100%;
    min-height: 0;
}
</style>
