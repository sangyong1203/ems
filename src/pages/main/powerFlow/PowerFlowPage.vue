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
                    <button v-if="!isEditMode" type="button" class="power-flow-header-button" @click="startEdit">
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
                        <button type="button" class="power-flow-header-button" @click="saveEdit">저장</button>
                    </template>
                </template>
                <PowerFlowCanvas
                    v-if="draftLayout && editorData"
                    :model-value="draftLayout"
                    :devices="editorData.devices"
                    :telemetry="editorData.telemetry"
                    :device-telemetry="editorData.device_telemetry"
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
                    <div class="power-flow-balance">
                        <div class="power-flow-balance__metric">
                            <div class="power-flow-balance__metric-head">
                                <small class="power-flow-progress-label">태양광 직접 소비율</small>
                                <strong class="power-flow-balance__metric-value">{{ pvDirectUseRate }}%</strong>
                            </div>
                            <ProgressGauge class="power-flow-progress" :value="pvDirectUseRate" />
                        </div>
                        <div class="power-flow-balance__metric">
                            <div class="power-flow-balance__metric-head">
                                <small class="power-flow-progress-label">에너지 자립률</small>
                                <strong class="power-flow-balance__metric-value">{{ energyIndependenceRate }}%</strong>
                            </div>
                            <ProgressGauge class="power-flow-progress" :value="energyIndependenceRate" />
                        </div>
                        <div class="power-flow-balance__stats">
                            <div class="power-flow-balance__stat">
                                <span class="power-flow-balance__stat-label">SOC</span>
                                <strong class="power-flow-balance__stat-value">
                                    {{ formatNumber(powerFlow?.nodes.ess.soc) }}%
                                </strong>
                            </div>
                            <div class="power-flow-balance__stat">
                                <span class="power-flow-balance__stat-label">SOH</span>
                                <strong class="power-flow-balance__stat-value">
                                    {{ formatNumber(powerFlow?.nodes.ess.soh) }}%
                                </strong>
                            </div>
                            <div class="power-flow-balance__stat">
                                <span class="power-flow-balance__stat-label">배터리 온도</span>
                                <strong class="power-flow-balance__stat-value">
                                    {{ formatNumber(powerFlow?.nodes.ess.temperatureC) }}℃
                                </strong>
                            </div>
                            <div class="power-flow-balance__stat power-flow-balance__stat--status">
                                <span class="power-flow-balance__stat-label">ESS 상태</span>
                                <StatusBadge :label="essStatusText" :variant="essStatusVariant" min-width="64px" />
                            </div>
                        </div>
                    </div>
                </GlassPanel>
            </div>
        </div>
    </section>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { GlassPanel, KeyValueList, MetricCardRow, ProgressGauge, StatusBadge } from '@/shared/components'
import PowerFlowCanvas from '@/features/powerFlow/components/PowerFlowCanvas.vue'
import type {
    PowerFlowEditorData,
    PowerFlowLayout,
    PowerFlowLayoutSaveBody,
} from '@/features/powerFlow/service/powerFlow.types'
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

const pvDirectUseRate = computed(() => {
    const solarPower = powerFlow.value?.nodes.solar.powerKw ?? 0
    const solarToLoad = powerFlow.value?.flows.solarToLoadKw ?? 0
    if (solarPower <= 0) {
        return 0
    }
    return Math.min(100, Math.round((solarToLoad / solarPower) * 100))
})

const energyIndependenceRate = computed(() => {
    const loadPower = powerFlow.value?.nodes.load.powerKw ?? 0
    const solarToLoad = powerFlow.value?.flows.solarToLoadKw ?? 0
    const essToLoad = powerFlow.value?.flows.essToLoadKw ?? 0
    if (loadPower <= 0) {
        return 0
    }
    return Math.min(100, Math.round(((solarToLoad + essToLoad) / loadPower) * 100))
})

const essStatusText = computed(() => {
    return statusLabel(powerFlow.value?.nodes.ess.status)
})

const essStatusVariant = computed(() => {
    const status = powerFlow.value?.nodes.ess.status
    if (status === 'CHARGING') {
        return 'progress'
    }
    if (status === 'DISCHARGING') {
        return 'info'
    }
    if (status === 'STANDBY' || status === 'IDLE') {
        return 'muted'
    }
    return 'muted'
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
        label: '태양광 직접 소비율',
        value: String(pvDirectUseRate.value),
        unit: '%',
        hint: 'PV → 부하 / PV 발전',
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

const getEditor = async (syncDraftLayout = true) => {
    const res = await powerFlowApi.getEditor()
    if (isSuccessResponse(res.result)) {
        editorData.value = res.data
        if (syncDraftLayout) {
            draftLayout.value = cloneLayout(res.data.layout)
        }
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
        getEditor(false)
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
    padding: 20px;
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

.power-flow-panel--balance {
    flex: 1;
}

.power-flow-panel--summary {
    height: 320px;
}
.power-flow-balance {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.power-flow-balance__metric {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.power-flow-balance__metric-head {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 12px;
}

.power-flow-balance__metric-value {
    color: var(--secondary-color);
    font-size: 18px;
    font-weight: 800;
    line-height: 1;
}

.power-flow-balance__stats {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
    padding-top: 4px;
}

.power-flow-balance__stat {
    display: flex;
    flex-direction: column;
    gap: 6px;
    padding: 12px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.power-flow-balance__stat--status {
    justify-content: space-between;
    align-items: flex-start;
}

.power-flow-balance__stat-label {
    color: var(--text-color--secondary);
    font-size: 12px;
    font-weight: 700;
}

.power-flow-balance__stat-value {
    color: var(--text-color--primary);
    font-size: 18px;
    font-weight: 800;
    line-height: 1.1;
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
    margin-bottom: 0;
}

.power-flow-progress :deep(.progress-gauge) {
    gap: 0;
}

.power-flow-progress-label {
    display: block;
    margin-bottom: 0;
    color: var(--text-color--secondary);
    font-size: 14px;
    font-weight: 700;
    margin-top: 0;
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

    .power-flow-balance {
        gap: 16px;
    }

    .power-flow-balance__stats {
        grid-template-columns: 1fr;
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
        gap: 10px;
    }
}
</style>
