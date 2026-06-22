<template>
    <GlassPanel class="dashboard-kpi-summary" title="운영 요약">
        <section class="dashboard-kpi-summary__section">
            <div class="dashboard-kpi-summary__section-heading">
                <div>
                    <h3>주요 지표</h3>
                </div>
            </div>
            <ul class="dashboard-kpi-summary__list dashboard-kpi-summary__list--primary">
                <li v-for="item in items" :key="item.label" class="dashboard-kpi-summary__item">
                    <div class="dashboard-kpi-summary__heading">
                        <span class="dashboard-kpi-summary__label">{{ item.label }}</span>
                        <span v-if="item.hint" class="dashboard-kpi-summary__hint">{{ item.hint }}</span>
                    </div>
                    <strong class="dashboard-kpi-summary__value" :class="item.variant">
                        {{ item.value }}
                        <small>{{ item.unit }}</small>
                    </strong>
                </li>
            </ul>
        </section>

        <section class="dashboard-kpi-summary__section">
            <div class="dashboard-kpi-summary__section-heading">
                <div>
                    <h3>ESS 상태</h3>
                    <span>운전 모드: {{ essMode }}</span>
                </div>
                <strong :class="`is-${essStatusTone}`">{{ essStatusLabel }}</strong>
            </div>
            <ProgressGauge :value="essSoc" label="SOC" :value-text="`${essSoc}%`" show-label prominent-value />
            <KeyValueList :items="essItems" />
        </section>

        <section class="dashboard-kpi-summary__section dashboard-kpi-summary__section--inverter">
            <div class="dashboard-kpi-summary__section-heading">
                <div>
                    <h3>인버터 상태</h3>
                    <span>정상 운전 기준</span>
                </div>
                <strong>{{ inverterNormal }}/{{ inverterTotal }}</strong>
            </div>
            <DonutStatusChart
                :normal="inverterNormal"
                :warning="inverterWarning"
                :total="inverterTotal"
                layout="horizontal"
                :size="150"
                summary-label="정상 동작"
                aria-label="인버터 상태 범례"
            />
        </section>
    </GlassPanel>
</template>

<script setup lang="ts">
import { DonutStatusChart, GlassPanel, KeyValueList, ProgressGauge } from '@/shared/components'
import type { MetricCardItem } from '@/shared/components/widget/MetricCardRow.vue'
import type { KeyValueItem } from '@/shared/components/widget/KeyValueList.vue'

defineProps<{
    items: MetricCardItem[]
    essSoc: number
    essMode: string
    essStatusLabel: string
    essStatusTone: 'normal' | 'warning' | 'fault' | 'unknown'
    essItems: KeyValueItem[]
    inverterNormal: number
    inverterWarning: number
    inverterTotal: number
}>()
</script>

<style scoped lang="scss">
.dashboard-kpi-summary {
    min-height: 0;
}

.dashboard-kpi-summary__group-title {
    margin: 0 0 6px;
    color: var(--text-color--secondary);
    font-size: 12px;
    font-weight: 600;
}

.dashboard-kpi-summary__list {
    display: flex;
    flex: 1;
    flex-direction: column;
    justify-content: space-between;
    padding: 0;
    margin: 0;
    min-height: 0;
    list-style: none;
}

.dashboard-kpi-summary__list--primary {
    flex: 0 0 auto;
}

.dashboard-kpi-summary__item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 8px 0;
    border-bottom: 1px solid var(--border-color);
}

.dashboard-kpi-summary__item:first-child {
    padding-top: 2px;
}

.dashboard-kpi-summary__item:last-child {
    padding-bottom: 0;
    border-bottom: none;
}

.dashboard-kpi-summary__heading {
    display: flex;
    flex-direction: column;
    gap: 3px;
    min-width: 0;
}

.dashboard-kpi-summary__label {
    color: var(--text-color--secondary);
    font-size: 13px;
}

.dashboard-kpi-summary__hint {
    overflow: hidden;
    color: var(--text-color--muted);
    font-size: 11px;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.dashboard-kpi-summary__value {
    flex: 0 0 auto;
    color: var(--secondary-color);
    font-size: 20px;
    line-height: 1;
}

.dashboard-kpi-summary__value small {
    margin-left: 3px;
    color: var(--text-color--secondary);
    font-size: 12px;
    font-weight: 600;
}

.dashboard-kpi-summary__value.is-alarm {
    color: var(--primary-color);
}

.dashboard-kpi-summary__section {
    padding-top: 14px;
    margin-bottom: 20px;
}

.dashboard-kpi-summary__section-heading {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 4px;
}

.dashboard-kpi-summary__section-heading h3 {
    margin: 0 0 4px;
    font-size: 15px;
}

.dashboard-kpi-summary__section-heading span {
    color: var(--text-color--secondary);
    font-size: 12px;
}

.dashboard-kpi-summary__section-heading strong {
    color: var(--secondary-color);
    font-size: 18px;
    white-space: nowrap;
}

.dashboard-kpi-summary__section-heading strong.is-warning {
    color: #f2b84b;
}

.dashboard-kpi-summary__section-heading strong.is-fault {
    color: #ff6b78;
}

.dashboard-kpi-summary__section-heading strong.is-unknown {
    color: var(--text-color--muted);
}

.dashboard-kpi-summary__section--inverter {
    // flex: 1 1 auto;
    min-height: 0;
}

.dashboard-kpi-summary__section--inverter :deep(.donut-status-chart) {
    min-width: 0;
    min-height: 154px;
    height: calc(100% - 22px);
}
</style>
