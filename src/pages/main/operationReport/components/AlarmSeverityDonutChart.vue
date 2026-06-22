<template>
    <ReportEChart :option="chartOption" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { EChartsOption } from 'echarts'
import type { AlarmSeverityDistribution } from '../service/operationReport.types'
import ReportEChart from './ReportEChart.vue'

const props = defineProps<{
    data: AlarmSeverityDistribution[]
}>()

const chartTextColor = '#c9c1d4'
const severityColors: Record<string, string> = {
    CRITICAL: 'rgba(255, 107, 143, 0.72)',
    WARNING: 'rgba(231, 109, 255, 0.72)',
    INFO: 'rgba(21, 224, 183, 0.72)',
}

const severityLabel = (severity: string) => {
    const labels: Record<string, string> = {
        CRITICAL: '심각',
        WARNING: '주의',
        INFO: '정보',
    }
    return labels[severity] ?? severity
}

const severityColor = (severity: string) => {
    return severityColors[severity] ?? severityColors.INFO
}

const chartOption = computed<EChartsOption>(() => ({
    tooltip: {
        trigger: 'item',
        backgroundColor: 'rgba(255,255,255,0.92)',
        borderWidth: 0,
        textStyle: { color: '#18202b' },
    },
    legend: { top: 0, right: 0, textStyle: { color: chartTextColor, fontSize: 10 } },
    series: [
        {
            name: '알람 등급',
            type: 'pie',
            radius: ['60%', '80%'],
            center: ['50%', '50%'],
            label: { color: chartTextColor, formatter: '{b} {c}건' },
            data: props.data.map(item => ({
                name: severityLabel(item.severity),
                value: item.count,
                itemStyle: {
                    color: severityColor(item.severity),
                },
            })),
        },
    ],
}))
</script>
