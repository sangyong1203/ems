<template>
    <section class="power-flow-page">
        <MetricCardRow :items="kpiItems" />

        <div class="power-flow-content">
            <GlassPanel
                class="power-flow-panel power-flow-panel--map"
                title="전력 흐름"
                subtitle="PV / ESS / 부하 / 계통 실시간 흐름"
                subtitle-position="right"
            >
                <template #headerRight>
                    <button
                        v-if="!isEditMode"
                        type="button"
                        class="power-flow-header-button"
                        @click="startEdit"
                    >
                        편집
                    </button>
                    <template v-else>
                        <button
                            type="button"
                            class="power-flow-header-button power-flow-header-button--ghost"
                            @click="cancelEdit"
                        >
                            취소
                        </button>
                        <button
                            type="button"
                            class="power-flow-header-button"
                            @click="saveEdit"
                        >
                            저장
                        </button>
                    </template>
                </template>
                <PowerFlowCanvas
                    v-if="draftLayout && editorData"
                    :model-value="draftLayout"
                    :devices="editorData.devices"
                    :telemetry="editorData.telemetry"
                    :editable="isEditMode"
                    @update:model-value="handleDraftLayoutChange"
                />
            </GlassPanel>

            <div class="power-flow-side">
                <GlassPanel class="power-flow-panel power-flow-panel--summary" title="흐름 요약">
                    <KeyValueList :items="flowItems" />
                    <div class="grid-status-chip">
                        <span>계통 상태</span>
                        <strong>{{ gridStatusText }}</strong>
                    </div>
                </GlassPanel>

                <GlassPanel
                    class="power-flow-panel power-flow-panel--balance"
                    title="운전 상태"
                    :subtitle="operationMode"
                >
                    <ProgressGauge class="power-flow-progress" :value="selfUseRate" :value-text="`${selfUseRate}%`" />
                    <small class="power-flow-progress-label">PV 부하 공급률</small>
                    <KeyValueList :items="balanceItems" />
                </GlassPanel>
            </div>
        </div>
    </section>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { GlassPanel, KeyValueList, MetricCardRow, ProgressGauge } from '@/shared/components'
import PowerFlowCanvas from '@/features/powerFlow/components/PowerFlowCanvas.vue'
import type { PowerFlowEditorData, PowerFlowLayout, PowerFlowLayoutSaveBody } from '@/features/powerFlow/service/powerFlow.types'
import { isSuccessResponse } from '@/shared/utils'
import powerFlowApi from './service/powerFlow.api'
import type { PowerFlowData } from './service/powerFlow.types'

const DEFAULT_REFRESH_INTERVAL = 10000

const powerFlow = ref<PowerFlowData | null>(null)
const editorData = ref<PowerFlowEditorData | null>(null)
const draftLayout = ref<PowerFlowLayout | null>(null)
const isEditMode = ref(false)
let pollingTimer: number | undefined

const formatNumber = (value?: number) => {
    return Number(value ?? 0).toLocaleString(undefined, { maximumFractionDigits: 1 })
}

const cloneLayout = (layout: PowerFlowLayout): PowerFlowLayout => JSON.parse(JSON.stringify(layout))

const essPower = computed(() => {
    return powerFlow.value?.nodes.ess.chargeKw || powerFlow.value?.nodes.ess.dischargeKw || 0
})

const updatedAtText = computed(() => {
    if (!powerFlow.value?.updatedAt) {
        return 'Updated -'
    }
    return `Updated ${powerFlow.value.updatedAt.replace('T', ' ').slice(0, 19)}`
})

const gridStatusText = computed(() => {
    return statusLabel(powerFlow.value?.nodes.grid.status)
})

const operationMode = computed(() => {
    if (!powerFlow.value) {
        return '대기'
    }
    if (powerFlow.value.nodes.ess.dischargeKw > 0) {
        return 'ESS 방전으로 부하 공급'
    }
    if (powerFlow.value.nodes.grid.importKw > 0) {
        return '계통 수전으로 부하 공급'
    }
    if (powerFlow.value.nodes.ess.chargeKw > 0) {
        return '태양광 잉여 전력 ESS 충전'
    }
    return '자체 공급 운전'
})

const selfUseRate = computed(() => {
    const solarPower = powerFlow.value?.nodes.solar.powerKw ?? 0
    const solarToLoad = powerFlow.value?.flows.solarToLoadKw ?? 0
    if (solarPower <= 0) {
        return 0
    }
    return Math.min(100, Math.round((solarToLoad / solarPower) * 100))
})

const kpiItems = computed(() => [
    {
        label: '태양광 발전',
        value: formatNumber(powerFlow.value?.nodes.solar.powerKw),
        unit: 'kW',
        hint: statusLabel(powerFlow.value?.nodes.solar.status),
        variant: 'is-solar',
    },
    {
        label: 'ESS 전력',
        value: formatNumber(essPower.value),
        unit: 'kW',
        hint: `${statusLabel(powerFlow.value?.nodes.ess.status)} / SOC ${formatNumber(powerFlow.value?.nodes.ess.soc)}%`,
        variant: 'is-ess',
    },
    {
        label: '부하 전력',
        value: formatNumber(powerFlow.value?.nodes.load.powerKw),
        unit: 'kW',
        hint: '현재 사용',
        variant: 'is-load',
    },
    {
        label: '계통 전력',
        value: formatNumber(powerFlow.value?.nodes.grid.exportKw || powerFlow.value?.nodes.grid.importKw),
        unit: 'kW',
        hint: gridStatusText.value,
        variant: 'is-grid',
    },
    {
        label: 'PV 부하 공급률',
        value: String(selfUseRate.value),
        unit: '%',
        hint: 'PV → Load',
        variant: 'is-rate',
    },
])

const flowItems = computed(() => [
    { label: 'PV → 부하', value: `${formatNumber(powerFlow.value?.flows.solarToLoadKw)} kW` },
    { label: 'PV → ESS', value: `${formatNumber(powerFlow.value?.flows.solarToEssKw)} kW` },
    { label: 'ESS → 부하', value: `${formatNumber(powerFlow.value?.flows.essToLoadKw)} kW` },
    { label: '계통 → 부하', value: `${formatNumber(powerFlow.value?.flows.gridImportKw)} kW` },
    { label: 'PV → 계통', value: `${formatNumber(powerFlow.value?.flows.solarToGridKw)} kW` },
    { label: 'ESS → 계통', value: `${formatNumber(powerFlow.value?.flows.essToGridKw)} kW` },
])

const balanceItems = computed(() => [
    { label: 'ESS SOC', value: `${formatNumber(powerFlow.value?.nodes.ess.soc)}%` },
    { label: 'ESS 충전', value: `${formatNumber(powerFlow.value?.nodes.ess.chargeKw)} kW` },
    { label: 'ESS 방전', value: `${formatNumber(powerFlow.value?.nodes.ess.dischargeKw)} kW` },
])

const statusLabel = (status?: string) => {
    if (status === 'GENERATING') {
        return '발전 중'
    }
    if (status === 'CONSUMING') {
        return '사용 중'
    }
    if (status === 'CHARGING') {
        return '충전'
    }
    if (status === 'DISCHARGING') {
        return '방전'
    }
    if (status === 'IMPORT') {
        return '수전'
    }
    if (status === 'EXPORT') {
        return '송전'
    }
    if (status === 'BALANCED') {
        return '균형'
    }
    if (status === 'IDLE' || status === 'STANDBY') {
        return '대기'
    }
    return status || '-'
}

const getPowerFlow = async () => {
    const res = await powerFlowApi.getPowerFlow()
    if (isSuccessResponse(res.result)) {
        powerFlow.value = res.data
    }
}

const getEditor = async () => {
    const res = await powerFlowApi.getEditor()
    if (isSuccessResponse(res.result)) {
        editorData.value = res.data
        draftLayout.value = cloneLayout(res.data.layout)
    }
}

const handleDraftLayoutChange = (layout: PowerFlowLayout) => {
    draftLayout.value = cloneLayout(layout)
}

const startEdit = () => {
    if (!editorData.value) {
        return
    }
    draftLayout.value = cloneLayout(editorData.value.layout)
    isEditMode.value = true
}

const cancelEdit = () => {
    if (!editorData.value) {
        return
    }
    draftLayout.value = cloneLayout(editorData.value.layout)
    isEditMode.value = false
}

const saveEdit = async () => {
    if (!draftLayout.value) {
        return
    }
    const body: PowerFlowLayoutSaveBody = {
        canvas_width: draftLayout.value.canvas_width,
        canvas_height: draftLayout.value.canvas_height,
        nodes: draftLayout.value.nodes,
        junctions: draftLayout.value.junctions,
        wires: draftLayout.value.wires,
    }
    const res = await powerFlowApi.saveEditor(body)
    if (isSuccessResponse(res.result)) {
        editorData.value = res.data
        draftLayout.value = cloneLayout(res.data.layout)
        isEditMode.value = false
    }
}

const startPolling = (interval: number) => {
    pollingTimer = window.setInterval(() => {
        getPowerFlow()
    }, interval)
}

onMounted(async () => {
    await Promise.all([getPowerFlow(), getEditor()])
    startPolling(powerFlow.value?.refreshInterval ?? DEFAULT_REFRESH_INTERVAL)
})

onBeforeUnmount(() => {
    if (pollingTimer) {
        window.clearInterval(pollingTimer)
    }
})
</script>

<style scoped lang="scss">
.power-flow-page {
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 14px;
    width: 100%;
    height: 100%;
    min-width: 1180px;
    min-height: 0;
    padding: 10px 12px 14px;
    overflow: hidden;
    color: var(--text-color--primary);
}

.power-flow-content {
    z-index: 1;
    flex: 1 1 auto;
    display: flex;
    gap: 14px;
    min-height: 0;
}

.power-flow-panel--map {
    flex: 1;
    padding: 0;
}

.power-flow-panel--map :deep(.glass-panel__header) {
    padding: 20px 20px 0;
}

.power-flow-header-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 58px;
    height: 30px;
    padding: 0 12px;
    border: 1px solid rgba(231, 109, 255, 0.56);
    border-radius: 999px;
    color: var(--button-primary-text-color);
    font-size: 12px;
    font-weight: 700;
    cursor: pointer;
    background: var(--primary-color);
}

.power-flow-header-button--ghost {
    color: var(--primary-color);
    background: rgba(231, 109, 255, 0.12);
}

.power-flow-side {
    flex: 0 0 19.3%;
    display: flex;
    flex-direction: column;
    gap: 14px;
    min-width: 0;
    min-height: 0;
}

.power-flow-panel--summary,
.power-flow-panel--balance {
    flex: 1 1 0;
}

.power-flow-panel--summary {
    flex-grow: 0.9;
    min-height: 330px;
}

.power-flow-panel--balance {
    flex-grow: 0.86;
}

.grid-status-chip {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-top: 16px;
}

.grid-status-chip span {
    color: var(--text-color--secondary);
    font-size: 14px;
    font-weight: 700;
}

.grid-status-chip strong {
    color: var(--secondary-color);
    font-size: 16px;
    font-weight: 800;
}

.power-flow-progress {
    margin-bottom: 6px;
}

.power-flow-progress :deep(span) {
    color: var(--secondary-color);
    font-size: 30px;
    line-height: 34px;
}

.power-flow-progress-label {
    display: block;
    margin-bottom: 18px;
    color: var(--text-color--secondary);
    font-size: 18px;
    margin-top: 8px;
}

@media (max-width: 1180px), (orientation: portrait) {
    .power-flow-page {
        min-width: 0;
        overflow: auto;
    }

    .power-flow-content {
        flex: 0 0 auto;
        flex-direction: column;
        min-height: auto;
    }

    .power-flow-panel--map {
        flex: 0 0 auto;
        min-height: 560px;
    }

    .power-flow-side {
        flex: 0 0 auto;
        flex-direction: row;
        width: 100%;
    }

    .power-flow-panel--summary,
    .power-flow-panel--balance {
        flex: 1 1 0;
        min-height: 300px;
    }
}

@media (max-width: 760px), (orientation: portrait) and (max-width: 900px) {
    .power-flow-panel--map {
        min-height: 440px;
    }

    .power-flow-side {
        flex-direction: column;
    }

    .power-flow-panel--summary,
    .power-flow-panel--balance {
        flex-basis: auto;
        min-height: 280px;
    }

    .power-flow-panel--map :deep(.glass-panel__header) {
        align-items: flex-start;
        flex-direction: column;
        gap: 10px;
    }
}
</style>
