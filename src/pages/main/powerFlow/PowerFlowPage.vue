<template>
    <section class="power-flow-page">
        <div class="power-flow-content">
            <GlassPanel
                class="power-flow-panel power-flow-panel--map"
                title="전력 흐름 편집"
                subtitle="장비 배치 및 연결 구성"
                subtitle-position="right"
            >
                <template #headerRight>
                    <span class="power-flow-edit-mode">{{ isEditMode ? '편집 중' : '보기 모드' }}</span>
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
                    @selection-change="selection = $event"
                />
            </GlassPanel>

            <GlassPanel class="power-flow-side" title="편집 정보">
                <template #headerRight>
                    <el-popover
                        trigger="click"
                        placement="bottom-end"
                        title="편집 안내"
                        :width="320"
                        :popper-style="{ maxWidth: 'calc(100vw - 24px)' }"
                    >
                        <template #reference>
                            <button type="button" class="editor-info__help" title="편집 안내" aria-label="편집 안내 보기">
                                <span aria-hidden="true">?</span>
                            </button>
                        </template>
                        <ul class="editor-info__guide">
                            <li>상단 편집 버튼을 눌러 편집을 시작합니다.</li>
                            <li>장비 목록에서 장비를 흐름도로 끌어 배치합니다.</li>
                            <li>배치한 장비를 끌어 위치를 변경합니다.</li>
                            <li>장비 연결점을 끌어 다른 장비 연결점에 놓으면 연결됩니다.</li>
                            <li>Ctrl을 누른 채 장비를 선택하면 여러 장비를 선택할 수 있습니다.</li>
                            <li>선택 도구로 정렬·삭제하고 Ctrl+Z로 되돌립니다.</li>
                            <li>저장을 누르면 적용되고, 취소하면 저장된 배치로 돌아갑니다.</li>
                        </ul>
                    </el-popover>
                </template>
                <div class="editor-info">
                    <section class="editor-info__section">
                        <h3>배치 현황</h3>
                        <KeyValueList :items="placementItems" />
                    </section>
                    <section class="editor-info__section">
                        <h3>선택 항목</h3>
                        <KeyValueList v-if="selectionItems.length" :items="selectionItems" />
                        <p v-else class="editor-info__empty">장비나 연결선을 선택하면 상세 정보가 표시됩니다.</p>
                    </section>
                </div>
            </GlassPanel>
        </div>
    </section>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { GlassPanel, KeyValueList } from '@/components'
import PowerFlowCanvas from '@/features/powerFlow/components/PowerFlowCanvas.vue'
import type {
    PowerFlowEditorData,
    PowerFlowLayout,
    PowerFlowLayoutSaveBody,
    PowerFlowSelection,
    PowerFlowEndpointType,
} from '@/features/powerFlow/service/powerFlow.types'
import { isSuccessResponse } from '@/utils'
import powerFlowApi from './service/powerFlow.api'
import { deviceStatusLabel, deviceVisual } from '@/features/powerFlow/service/powerFlow.utils'

const DEFAULT_REFRESH_INTERVAL = 10000 // 기본 폴링 주기(ms)

const editorData = ref<PowerFlowEditorData | null>(null) // 다이어그램 레이아웃 편집기 데이터
const draftLayout = ref<PowerFlowLayout | null>(null) // 편집 중인 임시 레이아웃
const isEditMode = ref(false) // 다이어그램 편집 모드 여부
let pollingTimer: number | undefined // 주기적 데이터 갱신 타이머

const selection = ref<PowerFlowSelection>({ nodeIds: [], wireId: '', junctionId: '' }) // 캔버스 선택 항목 ID

// 저장된 레이아웃과 편집 초안을 분리합니다.
const cloneLayout = (layout: PowerFlowLayout): PowerFlowLayout => JSON.parse(JSON.stringify(layout))

// 중복 배치를 제외한 장비 수와 현재 연결 구성을 표시합니다.
const placementItems = computed(() => {
    const placedIds = new Set(draftLayout.value?.nodes.map(node => node.device_id) ?? [])
    return [
        { label: '배치된 장비', value: `${placedIds.size}대` },
        { label: '미배치 장비', value: `${editorData.value?.devices.filter(device => !placedIds.has(device.id)).length ?? 0}대` },
        { label: '연결선', value: `${draftLayout.value?.wires.length ?? 0}개` },
        { label: '분기점', value: `${draftLayout.value?.junctions.length ?? 0}개` },
    ]
})

// 연결 끝점에 대응하는 장비명 또는 분기점을 표시합니다.
const endpointLabel = (type: PowerFlowEndpointType, refId: string) => {
    if (type === 'JUNCTION') return '분기점'
    const node = draftLayout.value?.nodes.find(item => item.client_id === refId)
    return editorData.value?.devices.find(device => device.id === node?.device_id)?.name ?? '장비 없음'
}

// 선택 상태를 현재 초안과 대조하여 삭제·취소 후에도 유효한 정보만 표시합니다.
const selectionItems = computed(() => {
    const layout = draftLayout.value
    if (!layout) return []
    const wire = layout.wires.find(item => item.client_id === selection.value.wireId)
    if (wire) {
        return [
            { label: '선택 종류', value: '연결선' },
            { label: '시작', value: endpointLabel(wire.source_type, wire.source_ref) },
            { label: '끝', value: endpointLabel(wire.target_type, wire.target_ref) },
            { label: '활성 여부', value: wire.is_enabled ? '활성' : '비활성' },
        ]
    }
    const nodes = layout.nodes.filter(node => selection.value.nodeIds.includes(node.client_id))
    if (nodes.length > 1) return [{ label: '선택 장비', value: `${nodes.length}대` }]
    if (nodes.length === 1) {
        const node = nodes[0]
        const device = editorData.value?.devices.find(item => item.id === node?.device_id)
        if (device && node) {
            const items = [
                { label: '장비 ID', value: String(device.id) },
                { label: '장비 이름', value: device.name },
                { label: '장비 종류', value: deviceVisual(device.device_type).label },
                { label: '장비 상태', value: deviceStatusLabel(device) },
                { label: '사용 여부', value: device.is_active ? '사용' : '미사용' },
                {
                    label: '측정값',
                    value: device.display_value == null
                        ? '-'
                        : `${device.display_value.toLocaleString(undefined, { maximumFractionDigits: 1 })} ${device.display_unit ?? ''}`.trim(),
                },
                {
                    label: '연결선 수',
                    value: `${layout.wires.filter(item =>
                        (item.source_type === 'NODE' && item.source_ref === node.client_id) ||
                        (item.target_type === 'NODE' && item.target_ref === node.client_id),
                    ).length}개`,
                },
            ]
            if (device.device_type === 'INVERTER' && device.module_count != null) {
                items.push({ label: '모듈 수', value: `${device.module_count.toLocaleString()}장` })
            }
            return items
        }
    }
    if (layout.junctions.some(item => item.client_id === selection.value.junctionId)) {
        return [{ label: '선택 종류', value: '분기점' }]
    }
    return []
})

// getEditor 다이어그램 레이아웃 데이터 조회
const getEditor = async (syncDraftLayout = true) => {
    const res = await powerFlowApi.getEditor()
    if (isSuccessResponse(res.result)) {
        editorData.value = res.data
        if (syncDraftLayout) {
            draftLayout.value = cloneLayout(res.data.layout)
        }
    }
}

// handleDraftLayoutChange 캔버스 편집 내용 임시 레이아웃 반영
const handleDraftLayoutChange = (layout: PowerFlowLayout) => {
    draftLayout.value = cloneLayout(layout)
}

// startEdit 다이어그램 레이아웃 편집 시작
const startEdit = () => {
    if (!editorData.value) {
        return
    }
    draftLayout.value = cloneLayout(editorData.value.layout)
    isEditMode.value = true
}

// cancelEdit 다이어그램 레이아웃 편집 취소 및 복원
const cancelEdit = () => {
    if (!editorData.value) {
        return
    }
    draftLayout.value = cloneLayout(editorData.value.layout)
    isEditMode.value = false
}

// saveEdit 편집된 다이어그램 레이아웃 저장
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

// 편집 초안을 유지하면서 장비 목록과 실시간 표시 데이터를 갱신합니다.
const startPolling = (interval: number) => {
    pollingTimer = window.setInterval(() => {
        getEditor(false)
    }, interval)
}

// onMounted 초기 데이터 로드 및 폴링 시작
onMounted(async () => {
    await getEditor()
    startPolling(DEFAULT_REFRESH_INTERVAL)
})

// onBeforeUnmount 컴포넌트 해제 시 폴링 타이머 정리
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
    flex-shrink: 0;
    min-width: 1180px;
    min-height: 0;
    padding: 10px 12px 14px;
    overflow: visible;  
    color: var(--text-color--primary);
}

.power-flow-content {
    z-index: 1;
    flex: 1 0 auto;
    display: flex;
    gap: 14px;
    min-height: 738px;
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
    flex: 0 0 300px;
    min-width: 0;
}

.editor-info {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.editor-info__section h3 {
    margin: 0 0 12px;
    font-size: 15px;
}

.editor-info__section :deep(.key-value-list),
.editor-info__section {
    min-width: 0;
    overflow-wrap: anywhere;
}

.editor-info__empty,
.editor-info__guide {
    margin: 0;
    color: var(--text-color--secondary);
    font-size: 13px;
    line-height: 1.8;
}

.editor-info__guide {
    max-height: 60vh;
    overflow-y: auto;
    padding-left: 18px;
}

.power-flow-edit-mode {
    color: var(--secondary-color);
    font-size: 14px;
    font-weight: 700;
    white-space: nowrap;
}

.editor-info__help {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    padding: 0;
    border: none;
    color: var(--text-color--secondary);
    background: transparent;
    cursor: pointer;
}

.editor-info__help span {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 18px;
    height: 18px;
    border: 1px solid currentColor;
    border-radius: 50%;
    font-size: 12px;
    font-weight: 700;
}

.editor-info__help:hover {
    color: var(--primary-color);
}

.editor-info__help:focus-visible {
    outline: 2px solid var(--accent-color);
    outline-offset: -2px;
}

.editor-info__guide li + li {
    margin-top: 8px;
}

@media (max-width: 1180px) {
    .power-flow-page {
        min-width: 0;
        height: auto;
    }

    .power-flow-content {
        flex: 0 0 auto;
        flex-direction: column;
        min-height: 0;
    }

    .power-flow-panel--map {
        flex: 0 0 auto;
        height: 600px;
    }

    .power-flow-side {
        flex: 0 0 auto;
    }

    .editor-info {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

}

@media (max-width: 767px) {
    .power-flow-page {
        padding: 8px;
    }

    .power-flow-panel--map {
        height: 500px;
        padding: 14px;
    }

    .power-flow-panel--map :deep(.glass-panel__header) {
        flex-wrap: wrap;
        gap: 10px;
    }

    .power-flow-panel--map :deep(.glass-panel__heading) {
        flex-wrap: wrap;
    }

    .power-flow-panel--map :deep(.glass-panel__heading span) {
        white-space: normal;
    }

    .editor-info {
        grid-template-columns: minmax(0, 1fr);
    }
}
</style>
