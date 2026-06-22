<template>
    <div class="donut-status-chart" :class="`is-${layout}`">
        <div class="donut-status-chart__visual" :style="visualStyle">
            <div ref="chartRef" class="donut-status-chart__chart"></div>
            <div class="donut-status-chart__summary">
                <strong>{{ normal }}/{{ total }}</strong>
                <span>{{ summaryLabel }}</span>
            </div>
        </div>
        <ul class="donut-status-chart__legend" :aria-label="ariaLabel">
            <li>
                <span class="donut-status-chart__dot is-normal"></span>
                <span>{{ normalLabel }}</span>
                <strong>{{ normal }}{{ unit }}</strong>
            </li>
            <li>
                <span class="donut-status-chart__dot is-warning"></span>
                <span>{{ warningLabel }}</span>
                <strong>{{ warning }}{{ unit }}</strong>
            </li>
        </ul>
    </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
import { COLOR_TYPE } from '@/shared/constants/colors'

const props = withDefaults(
    defineProps<{
        normal: number
        warning: number
        total: number
        layout?: 'vertical' | 'horizontal'
        size?: number
        unit?: string
        normalLabel?: string
        warningLabel?: string
        summaryLabel?: string
        ariaLabel?: string
    }>(),
    {
        layout: 'vertical',
        size: 150,
        unit: '대',
        normalLabel: '정상',
        warningLabel: '주의/장애',
        summaryLabel: '정상',
        ariaLabel: '상태 차트 범례',
    },
)

const chartRef = ref<HTMLDivElement | null>(null)
let chart: echarts.ECharts | null = null
let resizeObserver: ResizeObserver | null = null

const visualStyle = computed(() => ({
    flexBasis: `${props.size}px`,
    width: `${props.size}px`,
    height: `${props.size}px`,
}))

const chartData = computed(() => {
    const normal = Math.max(props.normal, 0)
    const warning = Math.max(props.warning, 0)

    if (normal + warning === 0) {
        return [{ value: Math.max(props.total, 1), name: '데이터 없음' }]
    }

    return [
        { value: normal, name: props.normalLabel },
        { value: warning, name: props.warningLabel },
    ]
})

const drawChart = () => {
    if (!chart) {
        return
    }

    chart.setOption({
        color: [COLOR_TYPE.SECONDARY, COLOR_TYPE.PRIMARY],
        tooltip: {
            trigger: 'item',
            formatter: `{b}: {c}${props.unit}`,
        },
        series: [
            {
                type: 'pie',
                radius: ['66%', '84%'],
                center: ['50%', '50%'],
                avoidLabelOverlap: true,
                label: { show: false },
                labelLine: { show: false },
                itemStyle: {
                    borderColor: 'rgba(9, 13, 24, 0.92)',
                    borderWidth: 4,
                    borderRadius: 8,
                },
                emphasis: {
                    scaleSize: 4,
                },
                data: chartData.value,
            },
        ],
    })
}

watch(chartData, drawChart)

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
.donut-status-chart {
    display: flex;
    min-height: 0;
}

.donut-status-chart.is-vertical {
    flex: 1;
    flex-direction: column;
    gap: 10px;
}

.donut-status-chart.is-horizontal {
    flex: 0 0 45%;
    align-items: center;
    justify-content: center;
    gap: 22px;
    min-width: 260px;
    height: 100%;
}

.donut-status-chart__visual {
    position: relative;
    min-height: 0;
}

.donut-status-chart.is-vertical .donut-status-chart__visual {
    flex: 1;
    width: 100% !important;
}

.donut-status-chart__chart {
    width: 100%;
    height: 100%;
}

.donut-status-chart.is-vertical .donut-status-chart__chart {
    min-height: 118px;
}

.donut-status-chart__summary {
    position: absolute;
    inset: 50% auto auto 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    transform: translate(-50%, -50%);
    pointer-events: none;
}

.donut-status-chart__summary strong {
    color: #ffffff;
    font-size: 24px;
    line-height: 28px;
}

.donut-status-chart__summary span {
    margin-top: 3px;
    color: var(--text-color--secondary);
    font-size: 12px;
}

.donut-status-chart__legend {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 0;
    margin: 0;
    list-style: none;
}

.donut-status-chart.is-horizontal .donut-status-chart__legend {
    flex: 0 0 108px;
    gap: 10px;
}

.donut-status-chart__legend li {
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--text-color--secondary);
    font-size: 13px;
    line-height: 16px;
}

.donut-status-chart.is-horizontal .donut-status-chart__legend li {
    min-width: 108px;
}

.donut-status-chart__legend strong {
    margin-left: auto;
    color: #ffffff;
    font-size: 13px;
}

.donut-status-chart__dot {
    width: 8px;
    height: 8px;
    flex: 0 0 8px;
    border-radius: 999px;
}

.donut-status-chart__dot.is-normal {
    background: var(--secondary-color);
    box-shadow: 0 0 10px rgba(21, 224, 183, 0.45);
}

.donut-status-chart__dot.is-warning {
    background: var(--primary-color);
    box-shadow: 0 0 10px rgba(231, 109, 255, 0.42);
}
</style>
