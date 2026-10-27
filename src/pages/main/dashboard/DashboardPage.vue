<template>
    <section class="dashboard-page">
        <div class="dashboard-content">
            <div class="dashboard-main">
                <div class="dashboard-power-flow-row">
                    <!-- <GlassPanel
                        class="dashboard-panel--power-flow-devices"
                        title="장비 목록"
                        :value="powerFlowDeviceCountText"
                    >
                        <PowerFlowPalette
                            v-if="powerFlowEditorData"
                            class="dashboard-power-flow-palette"
                            :devices="powerFlowEditorData.devices"
                            :placed-device-ids="dashboardPalettePlacedDeviceIds"
                            :editable="false"
                        />
                    </GlassPanel> -->
                    <GlassPanel
                        class="dashboard-panel--power-flow"
                        v-loading="isFlowLoading"
                        :aria-busy="isFlowLoading"
                        element-loading-text="전력 흐름을 불러오는 중입니다..."
                        :element-loading-svg="loadingSvgContent"
                        :element-loading-svg-view-box="loadingSvgViewBox"
                        element-loading-background="rgba(15, 18, 30, 0.88)"
                        title="전력 흐름"
                        subtitle="PV / ESS / 부하 / 계통 실시간 흐름"
                        subtitle-position="right"
                    >
                        <div v-if="flowLoadError" class="dashboard-flow-status" role="status">
                            <p>{{ flowLoadError }}</p>
                            <el-button @click="getDashboardData">다시 시도</el-button>
                        </div>
                        <div
                            v-else-if="isFlowReady && !powerFlowLayout?.nodes.length && !powerFlowLayout?.junctions.length"
                            class="dashboard-flow-status"
                            role="status"
                        >
                            등록된 전력 흐름 배치가 없습니다.
                        </div>
                        <PowerFlowPalette
                            v-if="powerFlowEditorData"
                            class="dashboard-power-flow-palette"
                            :devices="powerFlowEditorData.devices"
                            :placed-device-ids="dashboardPalettePlacedDeviceIds"
                            :selected-device-id="selectedFlowDeviceId"
                            @select-device="powerFlowCanvasRef?.selectDevice($event)"
                            @open-device-detail="openDeviceDetail"
                            :editable="false"
                        />
                        <!-- <DashboardPowerFlowMap :data="powerFlow" /> -->
                        <PowerFlowCanvas
                            ref="powerFlowCanvasRef"
                            class="dashboard-flow-canvas"
                            v-if="powerFlowLayout && powerFlowEditorData"
                            :model-value="powerFlowLayout"
                            :devices="powerFlowEditorData.devices"
                            :telemetry="powerFlowEditorData.telemetry"
                            :device-telemetry="powerFlowEditorData.device_telemetry"
                            :editable="false"
                            :show-palette="false"
                            @ready="isFlowReady = true"
                            @selection-change="handleFlowSelection"
                            @open-device-detail="openDeviceDetail"
                        >
                            <template #actions>
                                <button
                                    type="button"
                                    class="dashboard-flow-expand-button"
                                    title="전체 화면으로 펼치기"
                                    aria-label="전체 화면으로 펼치기"
                                    @click.stop="isFlowExpanded = true"
                                >
                                    <el-icon><FullScreen /></el-icon>
                                </button>
                            </template>
                        </PowerFlowCanvas>
                    </GlassPanel>
                </div>

                <div class="dashboard-chart-row">
                    <GlassPanel
                        class="dashboard-panel--chart"
                        title="태양광 발전 출력"
                        subtitle="오늘 시간대별 발전 추이"
                        :value="`${formatNumber(summary?.solar.currentPowerKw)} kW`"
                    >
                        <TrendAreaChart
                            :data="solarHistory"
                            :capacity="summary?.project.solarCapacityKw ?? 0"
                            name="태양광 발전 출력"
                            unit="kW"
                        />
                    </GlassPanel>

                    <GlassPanel
                        class="dashboard-panel--grid-chart"
                        title="계통 송전/수전 전력"
                        subtitle="시간대별 계통 전력 추이"
                        :value="gridPowerText"
                    >
                        <DashboardPowerChart
                            :first-points="gridExportHistory"
                            :second-points="gridImportHistory"
                            first-name="송전"
                            second-name="수전"
                            unit="kW"
                        />
                    </GlassPanel>

                    <GlassPanel
                        class="dashboard-panel--ess-chart"
                        title="ESS 충전/방전 전력"
                        :value="`충전 ${formatNumber(summary?.ess.chargePowerKw)} kW / 방전 ${formatNumber(
                            summary?.ess.dischargePowerKw,
                        )} kW`"
                    >
                        <EssPowerChart
                            :charge-data="essChargeHistory"
                            :discharge-data="essDischargeHistory"
                            :soc-data="essSocHistory"
                            :left-split-number="2"
                            :right-split-number="4"
                            unit="kW"
                        />
                    </GlassPanel>
                </div>
            </div>

            <DashboardKpiSummary
                class="dashboard-panel--kpi"
                :items="kpiItems"
                :ess-soc="summary?.ess.soc ?? 0"
                :ess-mode="essModeLabel"
                :ess-status-label="essStatus.label"
                :ess-status-tone="essStatus.tone"
                :ess-items="essStatusItems"
                :inverter-normal="summary?.solar.inverterNormal ?? 0"
                :inverter-warning="summary?.solar.inverterFault ?? 0"
                :inverter-total="summary?.solar.inverterTotal ?? 0"
            />
        </div>
    </section>
    <PowerFlowFullscreenDialog
        v-model="isFlowExpanded"
        :layout="powerFlowLayout"
        :editor-data="powerFlowEditorData"
        @open-device-detail="openDeviceDetail"
    />
    <PowerFlowDeviceDetailDialog
        v-model="isDeviceDetailOpen"
        :device="detailDevice"
        :layout="powerFlowLayout"
    />
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { vLoading } from 'element-plus'
import { loadingSvgContent, loadingSvgViewBox } from '@/composables/useProgressBar'
import { EssPowerChart, GlassPanel, TrendAreaChart } from '@/components'
import PowerFlowCanvas from '@/features/powerFlow/components/PowerFlowCanvas.vue'
import PowerFlowFullscreenDialog from '@/features/powerFlow/components/PowerFlowFullscreenDialog.vue'
import PowerFlowPalette from '@/features/powerFlow/components/PowerFlowPalette.vue'
import PowerFlowDeviceDetailDialog from '@/features/powerFlow/components/PowerFlowDeviceDetailDialog.vue'
import type { PowerFlowEditorData, PowerFlowLayout, PowerFlowSelection } from '@/features/powerFlow/service/powerFlow.types'
import { isSuccessResponse } from '@/utils'
import DashboardPowerChart from './components/DashboardPowerChart.vue'
import DashboardKpiSummary from './components/DashboardKpiSummary.vue'
// import DashboardPowerFlowMap from './components/DashboardPowerFlowMap.vue'
import dashboardApi from './service/dashboard.api'
import type { DashboardPowerFlow, DashboardSummary, DashboardTelemetryPoint } from './service/dashboard.types'

const DEFAULT_REFRESH_INTERVAL = 10000 // 기본 데이터 갱신 주기 (10초)
const dashboardPalettePlacedDeviceIds: number[] = []
const powerFlowCanvasRef = ref<InstanceType<typeof PowerFlowCanvas> | null>(null) // 목록 선택을 전달할 흐름도
const selectedFlowDeviceId = ref<number | null>(null) // 흐름도와 목록에서 강조할 장비 ID
const isDeviceDetailOpen = ref(false) // 장비 상세 창 표시 여부
const detailDeviceId = ref<number | null>(null) // 상세 창에 표시할 장비 ID
const detailDevice = computed(() => powerFlowEditorData.value?.devices.find(device => device.id === detailDeviceId.value) ?? null) // 갱신된 장비 상세정보

// 목록이나 흐름도에서 더블클릭한 장비의 상세 창을 엽니다.
const openDeviceDetail = (deviceId: number) => {
    detailDeviceId.value = deviceId
    isDeviceDetailOpen.value = true
}

// 흐름도에서 직접 선택하거나 선택을 해제하면 목록의 강조 상태도 동기화합니다.
const handleFlowSelection = (selection: PowerFlowSelection) => {
    const node = powerFlowLayout.value?.nodes.find(item => item.client_id === selection.nodeIds[0])
    selectedFlowDeviceId.value = selection.deviceId ?? node?.device_id ?? null
}

const isFlowReady = ref(false) // 최초 캔버스 배치 완료 여부
const flowLoadError = ref('') // 최초 전력 흐름 조회 실패 안내
const isFlowLoading = computed(() => !isFlowReady.value && !flowLoadError.value) // 데이터 조회와 최초 배치 중 표시
const isFlowExpanded = ref(false) // 전력 흐름 전체 화면 표시 여부
const summary = ref<DashboardSummary | null>(null) // 대시보드 요약 지표
const powerFlow = ref<DashboardPowerFlow | null>(null) // 실시간 전력 흐름 데이터
const powerFlowEditorData = ref<PowerFlowEditorData | null>(null) // 전력 흐름 편집 데이터
const powerFlowLayout = ref<PowerFlowLayout | null>(null) // 전력 흐름 캔버스 레이아웃
const solarHistory = ref<DashboardTelemetryPoint[]>([]) // 시간대별 태양광 발전 출력 이력
const essChargeHistory = ref<DashboardTelemetryPoint[]>([]) // 시간대별 ESS 충전 전력 이력
const essDischargeHistory = ref<DashboardTelemetryPoint[]>([]) // 시간대별 ESS 방전 전력 이력
const essSocHistory = ref<DashboardTelemetryPoint[]>([]) // 시간대별 ESS SOC 이력
const gridExportHistory = ref<DashboardTelemetryPoint[]>([]) // 시간대별 계통 송전 전력 이력
const gridImportHistory = ref<DashboardTelemetryPoint[]>([]) // 시간대별 계통 수전 전력 이력
let pollingTimer: number | undefined // 데이터 주기 갱신 타이머 ID

// 숫자를 소수점 1자리 로케일 형식으로 변환합니다.
const formatNumber = (value?: number) => {
    return Number(value ?? 0).toLocaleString(undefined, { maximumFractionDigits: 1 })
}

// 충방전 전력 상태에 따라 ESS 운전 모드(충전/방전/대기) 라벨을 반환합니다.
const essModeLabel = computed(() => {
    if (!summary.value) {
        return '대기'
    }
    if (summary.value.ess.chargePowerKw > 0) {
        return '충전'
    }
    if (summary.value.ess.dischargePowerKw > 0) {
        return '방전'
    }
    return '대기'
})

// PCS 및 BMS 상태 코드를 종합하여 ESS 상태 라벨과 톤을 반환합니다.
const essStatus = computed<{ label: string; tone: 'normal' | 'warning' | 'fault' | 'unknown' }>(() => {
    const statuses = [summary.value?.ess.pcsStatus, summary.value?.ess.bmsStatus].filter(Boolean)
    if (!statuses.length) {
        return { label: '확인 필요', tone: 'unknown' }
    }
    if (statuses.some(status => ['FAULT', 'ERROR', 'FAIL'].includes(status ?? ''))) {
        return { label: '장애', tone: 'fault' }
    }
    if (statuses.some(status => ['WARNING', 'WARN', 'CAUTION'].includes(status ?? ''))) {
        return { label: '주의', tone: 'warning' }
    }
    if (statuses.every(status => status === 'NORMAL')) {
        return { label: '정상', tone: 'normal' }
    }
    return { label: '확인 필요', tone: 'unknown' }
})

// 계통 송전/수전 상태 및 전력량을 텍스트로 반환합니다.
const gridPowerText = computed(() => {
    if (!summary.value) {
        return '0 kW'
    }
    if (summary.value.grid.exportPowerKw > 0) {
        return `${formatNumber(summary.value.grid.exportPowerKw)} kW 송전`
    }
    if (summary.value.grid.importPowerKw > 0) {
        return `${formatNumber(summary.value.grid.importPowerKw)} kW 수전`
    }
    return '0 kW'
})

const gridPowerValue = computed(() => {
    if (!summary.value) {
        return '0'
    }
    return formatNumber(summary.value.grid.exportPowerKw || summary.value.grid.importPowerKw)
})

const gridPowerStatus = computed(() => {
    if (!summary.value) {
        return '대기'
    }
    if (summary.value.grid.exportPowerKw > 0) {
        return '계통 송전'
    }
    if (summary.value.grid.importPowerKw > 0) {
        return '계통 수전'
    }
    return '계통 대기'
})


const powerFlowDeviceCountText = computed(() => `${powerFlowEditorData.value?.devices.length ?? 0}대`)

const kpiItems = computed(() => [
    {
        label: '현재 발전 출력',
        value: formatNumber(summary.value?.solar.currentPowerKw),
        unit: 'kW',
        hint: `${formatNumber(summary.value?.project.solarCapacityKw)} kW 설비`,
        variant: 'is-solar',
    },
    {
        label: '금일 발전량',
        value: formatNumber(summary.value?.solar.todayGenerationKwh),
        unit: 'kWh',
        hint: '오늘 누적',
        variant: 'is-energy',
    },
    {
        label: '부하 전력',
        value: formatNumber(summary.value?.grid.loadPowerKw),
        unit: 'kW',
        hint: '현재 사용량',
        variant: 'is-load',
    },
    {
        label: '계통 전력',
        value: gridPowerValue.value,
        unit: 'kW',
        hint: gridPowerStatus.value,
        variant: 'is-grid',
    },
    {
        label: '미처리 알림',
        value: String(summary.value?.alarms.openCount ?? 0),
        unit: '건',
        hint: summary.value?.operationStatus === 'NORMAL' ? '정상' : '확인 필요',
        variant: 'is-alarm',
    },
])

const essStatusItems = computed(() => [
    { label: 'SOH', value: `${formatNumber(summary.value?.ess.soh)}%` },
    { label: 'PCS', value: summary.value?.ess.pcsStatus || '-' },
    { label: 'BMS', value: summary.value?.ess.bmsStatus || '-' },
    { label: '배터리 온도', value: `${formatNumber(summary.value?.ess.batteryTemperatureC)}°C` },
])

// 대시보드 요약, 전력 흐름, 시계열 추이 데이터를 일괄 조회합니다.
const loadDashboardData = async () => {
    const [
        summaryRes,
        powerFlowRes,
        powerFlowEditorRes,
        solarHistoryRes,
        essChargeHistoryRes,
        essDischargeHistoryRes,
        essSocHistoryRes,
        gridExportHistoryRes,
        gridImportHistoryRes,
    ] = await Promise.all([
        dashboardApi.getSummary(),
        dashboardApi.getPowerFlow(),
        dashboardApi.getPowerFlowEditor(),
        dashboardApi.getTelemetryHistory('solar_power_kw'),
        dashboardApi.getTelemetryHistory('ess_charge_kw'),
        dashboardApi.getTelemetryHistory('ess_discharge_kw'),
        dashboardApi.getTelemetryHistory('ess_soc'),
        dashboardApi.getTelemetryHistory('grid_export_kw'),
        dashboardApi.getTelemetryHistory('grid_import_kw'),
    ])

    if (isSuccessResponse(summaryRes.result)) {
        summary.value = summaryRes.data
    }

    if (isSuccessResponse(powerFlowRes.result)) {
        powerFlow.value = powerFlowRes.data
    }

    if (isSuccessResponse(powerFlowEditorRes.result)) {
        powerFlowEditorData.value = powerFlowEditorRes.data
        powerFlowLayout.value = JSON.parse(JSON.stringify(powerFlowEditorRes.data.layout))
        flowLoadError.value = ''
    } else if (!powerFlowEditorData.value) {
        flowLoadError.value = '전력 흐름을 불러오지 못했습니다. 다시 시도해 주세요.'
    }

    if (isSuccessResponse(solarHistoryRes.result)) {
        solarHistory.value = solarHistoryRes.data
    }

    if (isSuccessResponse(essChargeHistoryRes.result)) {
        essChargeHistory.value = essChargeHistoryRes.data
    }

    if (isSuccessResponse(essDischargeHistoryRes.result)) {
        essDischargeHistory.value = essDischargeHistoryRes.data
    }

    if (isSuccessResponse(essSocHistoryRes.result)) {
        essSocHistory.value = essSocHistoryRes.data
    }

    if (isSuccessResponse(gridExportHistoryRes.result)) {
        gridExportHistory.value = gridExportHistoryRes.data
    }

    if (isSuccessResponse(gridImportHistoryRes.result)) {
        gridImportHistory.value = gridImportHistoryRes.data
    }
}

// 초기 조회 실패 시 안내를 표시하고 이후 재시도와 자동 갱신을 유지합니다.
const getDashboardData = async () => {
    if (!powerFlowEditorData.value) {
        flowLoadError.value = ''
    }
    try {
        await loadDashboardData()
    } catch {
        if (!powerFlowEditorData.value) {
            flowLoadError.value = '전력 흐름을 불러오지 못했습니다. 다시 시도해 주세요.'
        }
    }
}

// 지정된 주기로 대시보드 데이터를 자동 갱신하는 폴링 타이머를 시작합니다.
const startPolling = (interval: number) => {
    pollingTimer = window.setInterval(() => {
        getDashboardData()
    }, interval)
}

// 화면 마운트 시 초기 데이터를 조회하고 실시간 폴링을 등록합니다.
onMounted(async () => {
    await getDashboardData()
    startPolling(summary.value?.refreshInterval ?? DEFAULT_REFRESH_INTERVAL)
})

// 컴포넌트 해제 시 실행 중인 폴링 타이머를 해제합니다.
onBeforeUnmount(() => {
    if (pollingTimer) {
        window.clearInterval(pollingTimer)
    }
})
</script>

<style scoped lang="scss">
.dashboard-page {
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 14px;
    width: 100%;
    height: 100%;
    min-height: 0;
    min-width: 1180px;
    padding: 10px 12px 14px;
    overflow: hidden;
    color: var(--text-color--primary);
}

.dashboard-content {
    z-index: 1;
    flex: 1 1 auto;
    display: grid;
    grid-template-columns: minmax(0, 1fr) 320px;
    gap: 14px;
    min-height: 0;
}

.dashboard-main {
    display: flex;
    flex-direction: column;
    gap: 14px;
    min-width: 0;
    min-height: 0;
}

.dashboard-power-flow-row {
    flex: 1.25 1 0;
    display: flex;
    gap: 14px;
    min-width: 0;
    min-height: 0;
    :deep(.glass-panel__body) {
        flex-direction: row;
    }
}

.dashboard-panel--power-flow-devices {
    flex: 0 0 240px;
    min-width: 0;
}

.dashboard-panel--power-flow {
    flex: 1 1 0;
    min-width: 0;
    min-height: 0;
    :deep(.glass-panel__body) {
        gap: 8px;
    }
}

.dashboard-flow-status {
    position: absolute;
    inset: 64px 20px 20px;
    z-index: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 12px;
    color: var(--text-color--primary);
    text-align: center;
}

.dashboard-power-flow-palette {
    width: 220px;
    padding: 0 2px 12px 4px;
    border-right: none;

    // :deep(.power-flow-palette__header) {
    //     display: none;
    // }
    // :deep(.power-flow-palette__list) {
    //     padding: 0 2px 2px 0;
    // }
    // :deep(.power-flow-palette__item) {
    //     cursor: default;
    // }
}

.dashboard-chart-row {
    display: flex;
    gap: 14px;
    height: 31%;
}

.dashboard-panel--chart,
.dashboard-panel--ess-chart,
.dashboard-panel--grid-chart {
    flex: 1 1 0;
    min-width: 0;
}

.dashboard-panel--kpi {
    min-width: 0;
}
.dashboard-panel--kpi :deep(.glass-panel__body) {
    justify-content: space-around !important;
}

.dashboard-flow-expand-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    padding: 0;
    border: none;
    background: transparent;
    color: var(--text-color--primary);
    font-size: 18px;
    cursor: pointer;
}

.dashboard-flow-expand-button:focus-visible {
    outline: 2px solid var(--accent-color);
    outline-offset: -2px;
}


@media (max-width: 1180px) {
    .dashboard-page {
        min-width: 0;
        height: auto;
        overflow: visible;
    }

    .dashboard-content {
        display: flex;
        flex-direction: column;
        min-height: 0;
    }

    .dashboard-main {
        flex: 0 0 auto;
    }

    .dashboard-power-flow-row {
        flex: 0 0 auto;
        height: 440px;
        min-height: 440px;
    }

    .dashboard-chart-row {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        height: auto;
    }

    .dashboard-panel--chart,
    .dashboard-panel--ess-chart,
    .dashboard-panel--grid-chart {
        height: 320px;
        min-height: 320px;
    }

    .dashboard-panel--ess-chart {
        grid-column: 1 / -1;
    }

    .dashboard-panel--kpi :deep(.glass-panel__body) {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 24px;
    }
}

@media (max-width: 767px) {
    .dashboard-page {
        padding: 8px;
    }

    .dashboard-power-flow-row {
        height: 400px;
        min-height: 400px;
    }

    .dashboard-power-flow-palette {
        display: none;
    }

    .dashboard-panel--power-flow :deep(.glass-panel__body) {
        flex-direction: column;
    }

    .dashboard-chart-row {
        grid-template-columns: minmax(0, 1fr);
    }

    .dashboard-panel--chart,
    .dashboard-panel--ess-chart,
    .dashboard-panel--grid-chart {
        height: 300px;
        min-height: 300px;
    }

    .dashboard-panel--power-flow,
    .dashboard-panel--chart,
    .dashboard-panel--ess-chart,
    .dashboard-panel--grid-chart,
    .dashboard-panel--kpi {
        padding: 14px;
    }

    .dashboard-page :deep(.glass-panel__header),
    .dashboard-page :deep(.glass-panel__heading--right) {
        flex-wrap: wrap;
        gap: 6px;
    }

    .dashboard-page :deep(.glass-panel__header h2) {
        font-size: 16px;
    }

    .dashboard-page :deep(.glass-panel__header strong),
    .dashboard-page :deep(.glass-panel__heading--right span) {
        white-space: normal;
        overflow-wrap: anywhere;
    }

    .dashboard-panel--kpi :deep(.glass-panel__body) {
        display: flex;
        flex-direction: column;
        gap: 24px;
    }

    .dashboard-flow-canvas :deep(.power-flow-canvas__scroller) {
        touch-action: none;
    }

    .dashboard-flow-canvas :deep(.power-flow-canvas__zoom button) {
        min-width: 44px;
        min-height: 44px;
    }
}
</style>
