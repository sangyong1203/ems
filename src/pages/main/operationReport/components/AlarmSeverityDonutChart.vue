<template>
    <ReportEChart :option="chartOption" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { EChartsOption } from 'echarts'
import type { AlarmSeverityDistribution } from '../service/operationReport.types'
import ReportEChart from './ReportEChart.vue'
import { CHART_THEME } from '@/constants/colors'

const props = defineProps<{
    data: AlarmSeverityDistribution[] // 알람 등급별 발생 분포 데이터
}>()

const chartTextColor = CHART_THEME.textColor
const severityColors: Record<string, string> = CHART_THEME.severity

// severityLabel 알람 등급 코드 한국어 라벨 반환
const severityLabel = (severity: string) => {
    const labels: Record<string, string> = {
        CRITICAL: '심각',
        WARNING: '주의',
        INFO: '정보',
    }
    return labels[severity] ?? severity
}

// severityColor 알람 등급별 테마 색상 반환
const severityColor = (severity: string) => {
    return severityColors[severity] ?? severityColors.INFO
}

const chartOption = computed<EChartsOption>(() => ({
    tooltip: {
        trigger: 'item',
        ...CHART_THEME.tooltip,
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
