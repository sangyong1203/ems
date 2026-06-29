<template>
    <div class="power-flow-editor">
        <PowerFlowPalette
            v-show="showPalette"
            :devices="devices"
            :placed-device-ids="placedDeviceIds"
            :editable="editable"
        />

        <div ref="canvasRef" class="power-flow-canvas" :class="{ 'is-readonly': !editable }">
            <div
                ref="scrollRef"
                class="power-flow-canvas__scroller"
                @dragover.prevent
                @drop="handleDrop"
                @pointerdown="startCanvasPan"
                @pointermove="handlePointerMove"
                @pointerup="handleCanvasPointerUp"
                @pointerleave="handleCanvasPointerUp"
                @click="handleCanvasClick"
            >
                <div class="power-flow-canvas__viewport" :style="viewportStyle">
                    <div class="power-flow-canvas__stage" :style="stageStyle">
                        <svg class="power-flow-canvas__wires">
                            <PowerFlowWire
                                v-for="wire in layout.wires"
                                :key="wire.client_id"
                                :wire="wire"
                                :path="wirePath(wire, layout.nodes, layout.junctions)"
                                :tone="wireTone(wire, layout.nodes, layout.wires, devices)"
                                :current-active="wireCurrentStateForTelemetry(wire).active"
                                :current-direction="wireCurrentStateForTelemetry(wire).direction"
                                :selected="selectedWireId === wire.client_id"
                                @select="selectWire"
                                @split="splitWire"
                            />
                            <path v-if="draftWirePath" class="power-flow-canvas__draft" :d="draftWirePath" />
                        </svg>

                        <PowerFlowDevice
                            v-for="node in layout.nodes"
                            :key="node.client_id"
                            :node="node"
                            :device="deviceById(node.device_id)"
                            :selected="selectedNodeIds.includes(node.client_id)"
                            :editable="editable"
                            :connected-anchors="connectedAnchors(node.client_id)"
                            @select="selectNode"
                            @drag-start="startNodeDrag"
                            @anchor-start="startWire"
                            @anchor-end="completeWireToNode"
                        />

                        <button
                            v-for="junction in layout.junctions"
                            :key="junction.client_id"
                            type="button"
                            class="power-flow-junction"
                            :class="{ 'is-selected': selectedJunctionId === junction.client_id }"
                            :style="{ left: `${junction.x - 8}px`, top: `${junction.y - 8}px` }"
                            title="분기점"
                            @pointerdown.stop="startJunctionDrag($event, junction.client_id)"
                            @pointerup.stop="handleJunctionPointerUp(junction.client_id)"
                            @click.stop="selectJunction(junction.client_id)"
                        ></button>
                    </div>
                </div>
            </div>

            <div class="power-flow-canvas__zoom">
                <button type="button" title="축소" @click.stop="zoomOut">-</button>
                <button type="button" title="원래 크기" @click.stop="resetZoom">{{ zoomLabel }}</button>
                <button type="button" title="확대" @click.stop="zoomIn">+</button>
            </div>

            <button
                v-if="editable"
                type="button"
                class="power-flow-canvas__undo"
                title="되돌리기 (Ctrl+Z)"
                :disabled="!canUndo"
                @click.stop="undoLayoutChange"
            >
                ↶
            </button>

            <div v-if="editable && selectedWire" class="power-flow-canvas__toolbar">
                <button
                    type="button"
                    :title="selectedWire.is_enabled ? '전선 비활성화' : '전선 활성화'"
                    @click.stop="toggleSelectedWire"
                >
                    {{ selectedWire.is_enabled ? '●' : '○' }}
                </button>
                <button type="button" title="전선 삭제" @click.stop="removeSelectedWire">×</button>
            </div>

            <div
                v-else-if="editable && (selectedNodeIds.length > 0 || selectedJunctionId)"
                class="power-flow-canvas__toolbar"
            >
                <div v-if="selectedNodeIds.length > 1" class="power-flow-canvas__align-tools">
                    <button
                        type="button"
                        class="power-flow-canvas__align-button"
                        title="가로 정렬"
                        @click.stop="alignSelectedNodes('horizontal')"
                    >
                        <AppIcon name="IconAlignHorizontal" />
                    </button>
                    <button
                        type="button"
                        class="power-flow-canvas__align-button"
                        title="세로 정렬"
                        @click.stop="alignSelectedNodes('vertical')"
                    >
                        <AppIcon name="IconAlignVertical" />
                    </button>
                    <button
                        type="button"
                        class="power-flow-canvas__align-button"
                        title="가로 평균 간격"
                        :disabled="selectedNodeIds.length < 3"
                        @click.stop="distributeSelectedNodes('horizontal')"
                    >
                        <AppIcon name="IconDistributeHorizontal" />
                    </button>
                    <button
                        type="button"
                        class="power-flow-canvas__align-button"
                        title="세로 평균 간격"
                        :disabled="selectedNodeIds.length < 3"
                        @click.stop="distributeSelectedNodes('vertical')"
                    >
                        <AppIcon name="IconDistributeVertical" />
                    </button>
                </div>
                <button type="button" title="선택 항목 삭제" @click.stop="removeSelectedItem">×</button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import AppIcon from '@/shared/components/widget/AppIcon.vue'
import PowerFlowDevice from './PowerFlowDevice.vue'
import PowerFlowPalette from './PowerFlowPalette.vue'
import PowerFlowWire from './PowerFlowWire.vue'
import type {
    PowerFlowAnchor,
    PowerFlowDeviceItem,
    PowerFlowEndpoint,
    PowerFlowJunction,
    PowerFlowLayout,
    PowerFlowPoint,
    PowerFlowWire as PowerFlowWireType,
} from '../service/powerFlow.types'
import {
    anchorPoint,
    createClientId,
    endpointPoint,
    wireCurrentState,
    wirePath,
    wireTone,
} from '../service/powerFlow.utils'

type NodeDragItem = {
    ref: string
    startX: number
    startY: number
}

type AlignAxis = 'horizontal' | 'vertical'

type DragState =
    | {
          type: 'NODE'
          ref: string
          offsetX: number
          offsetY: number
          activeStartX: number
          activeStartY: number
          nodes: NodeDragItem[]
      }
    | {
          type: 'JUNCTION'
          ref: string
          offsetX: number
          offsetY: number
      }

const props = withDefaults(
    defineProps<{
        modelValue: PowerFlowLayout
        devices: PowerFlowDeviceItem[]
        telemetry?: Record<string, number>
        deviceTelemetry?: Record<string, Record<string, number>>
        editable?: boolean
        showPalette?: boolean
    }>(),
    {
        showPalette: true,
    },
)

const emit = defineEmits<{
    'update:modelValue': [layout: PowerFlowLayout]
}>()

const cloneLayout = (layout: PowerFlowLayout): PowerFlowLayout => JSON.parse(JSON.stringify(layout))
const layout = ref<PowerFlowLayout>(cloneLayout(props.modelValue))
const canvasRef = ref<HTMLDivElement | null>(null)
const scrollRef = ref<HTMLDivElement | null>(null)
const viewportSize = ref({ width: 0, height: 0 })
const selectedNodeIds = ref<string[]>([])
const selectedWireId = ref('')
const selectedJunctionId = ref('')
const dragState = ref<DragState | null>(null)
const panState = ref<{ pointerId: number; startX: number; startY: number; scrollLeft: number; scrollTop: number } | null>(null)
const undoStack = ref<PowerFlowLayout[]>([])
const dragSnapshot = ref<PowerFlowLayout | null>(null)
const wireStart = ref<PowerFlowEndpoint | null>(null)
const pointer = ref<PowerFlowPoint>({ x: 0, y: 0 })
const hasAppliedInitialFit = ref(false)
const hasSyncedInitialModel = ref(false)
const wasCanvasPanning = ref(false)
const wasNodeDragging = ref(false)
const zoom = ref(1)
const MIN_ZOOM = 0.5
const MAX_ZOOM = 2
const ZOOM_STEP = 0.1
const CONTENT_PADDING = 140
const INITIAL_FIT_PADDING = 50
const MIN_STAGE_WIDTH = 3200
const MIN_STAGE_HEIGHT = 1920
let resizeObserver: ResizeObserver | null = null
let wheelListener: ((event: WheelEvent) => void) | null = null
let keydownListener: ((event: KeyboardEvent) => void) | null = null
let fitFrameId: number | null = null
let resizeFrameId: number | null = null
let lastSyncedLayout = ''

watch(
    () => props.modelValue,
    async value => {
        const nextLayout = cloneLayout(value)
        const nextLayoutJson = JSON.stringify(nextLayout)
        layout.value = nextLayout
        if (nextLayoutJson === lastSyncedLayout) {
            lastSyncedLayout = ''
        } else {
            undoStack.value = []
            dragSnapshot.value = null
        }
        if (!hasSyncedInitialModel.value) {
            hasSyncedInitialModel.value = true
            hasAppliedInitialFit.value = false
            await scheduleInitialFit()
        }
    },
)

const placedDeviceIds = computed(() => layout.value.nodes.map(node => node.device_id))
const selectedWire = computed(() => layout.value.wires.find(wire => wire.client_id === selectedWireId.value) ?? null)
const canUndo = computed(() => undoStack.value.length > 0)
const selectedNodes = computed(() => {
    const selectedNodeSet = new Set(selectedNodeIds.value)
    return layout.value.nodes.filter(node => selectedNodeSet.has(node.client_id))
})
const draftWirePath = computed(() => {
    if (!wireStart.value) {
        return ''
    }
    const source = endpointPoint(wireStart.value, layout.value.nodes, layout.value.junctions)
    return source ? `M ${source.x} ${source.y} L ${pointer.value.x} ${pointer.value.y}` : ''
})

const contentBounds = computed(() => {
    const xValues: number[] = []
    const yValues: number[] = []

    layout.value.nodes.forEach(node => {
        xValues.push(node.x, node.x + node.width)
        yValues.push(node.y, node.y + node.height)
    })

    layout.value.junctions.forEach(junction => {
        xValues.push(junction.x)
        yValues.push(junction.y)
    })

    if (xValues.length === 0 || yValues.length === 0) {
        return {
            minX: 0,
            minY: 0,
            maxX: layout.value.canvas_width,
            maxY: layout.value.canvas_height,
            width: layout.value.canvas_width,
            height: layout.value.canvas_height,
        }
    }

    const minX = Math.max(0, Math.min(...xValues) - CONTENT_PADDING)
    const minY = Math.max(0, Math.min(...yValues) - CONTENT_PADDING)
    const maxX = Math.max(...xValues) + CONTENT_PADDING
    const maxY = Math.max(...yValues) + CONTENT_PADDING

    return {
        minX,
        minY,
        maxX,
        maxY,
        width: Math.max(1, maxX - minX),
        height: Math.max(1, maxY - minY),
    }
})

const initialFitBounds = computed(() => {
    if (layout.value.nodes.length === 0) {
        return {
            minX: 0,
            minY: 0,
            maxX: layout.value.canvas_width,
            maxY: layout.value.canvas_height,
            width: layout.value.canvas_width,
            height: layout.value.canvas_height,
        }
    }

    const xValues: number[] = []
    const yValues: number[] = []

    layout.value.nodes.forEach(node => {
        xValues.push(node.x, node.x + node.width)
        yValues.push(node.y, node.y + node.height)
    })

    const minX = Math.max(0, Math.min(...xValues) - INITIAL_FIT_PADDING)
    const minY = Math.max(0, Math.min(...yValues) - INITIAL_FIT_PADDING)
    const maxX = Math.max(...xValues) + INITIAL_FIT_PADDING
    const maxY = Math.max(...yValues) + INITIAL_FIT_PADDING

    return {
        minX,
        minY,
        maxX,
        maxY,
        width: Math.max(1, maxX - minX),
        height: Math.max(1, maxY - minY),
    }
})

const stageWidth = computed(() => {
    return Math.max(
        layout.value.canvas_width,
        MIN_STAGE_WIDTH,
        contentBounds.value.maxX,
        viewportSize.value.width > 0 ? viewportSize.value.width / zoom.value : 0,
    )
})

const stageHeight = computed(() => {
    return Math.max(
        layout.value.canvas_height,
        MIN_STAGE_HEIGHT,
        contentBounds.value.maxY,
        viewportSize.value.height > 0 ? viewportSize.value.height / zoom.value : 0,
    )
})

const viewportStyle = computed(() => ({
    width: `${stageWidth.value * zoom.value}px`,
    height: `${stageHeight.value * zoom.value}px`,
}))

const stageStyle = computed(() => ({
    width: `${stageWidth.value}px`,
    height: `${stageHeight.value}px`,
    transform: `scale(${zoom.value})`,
}))

const zoomLabel = computed(() => `${Math.round(zoom.value * 100)}%`)

const wireCurrentStateForTelemetry = (wire: PowerFlowWireType) => {
    return wireCurrentState(
        wire,
        layout.value.nodes,
        layout.value.wires,
        props.devices,
        props.telemetry ?? {},
        props.deviceTelemetry ?? {},
    )
}

const connectedAnchors = (nodeId: string): PowerFlowAnchor[] => {
    const anchors = layout.value.wires.flatMap(wire => {
        const items: PowerFlowAnchor[] = []
        if (wire.source_type === 'NODE' && wire.source_ref === nodeId) {
            items.push(wire.source_anchor)
        }
        if (wire.target_type === 'NODE' && wire.target_ref === nodeId) {
            items.push(wire.target_anchor)
        }
        return items
    })

    return Array.from(new Set(anchors))
}

const deviceById = (deviceId: number) =>
    props.devices.find(device => device.id === deviceId) ?? {
        id: deviceId,
        device_type: 'UNKNOWN',
        name: `Device #${deviceId}`,
        status: 'UNKNOWN',
        is_active: false,
    }

const canvasPoint = (event: MouseEvent | PointerEvent | DragEvent): PowerFlowPoint => {
    const rect = scrollRef.value?.getBoundingClientRect()
    const scrollLeft = scrollRef.value?.scrollLeft ?? 0
    const scrollTop = scrollRef.value?.scrollTop ?? 0
    if (!rect) {
        return { x: 0, y: 0 }
    }
    return {
        x: Math.max(0, (event.clientX - rect.left + scrollLeft) / zoom.value),
        y: Math.max(0, (event.clientY - rect.top + scrollTop) / zoom.value),
    }
}

const clampZoom = (nextZoom: number) => Math.max(MIN_ZOOM, Math.min(MAX_ZOOM, Number(nextZoom.toFixed(2))))

const setZoom = (nextZoom: number) => {
    zoom.value = clampZoom(nextZoom)
}

const setZoomAroundPoint = async (nextZoom: number, screenPoint?: { x: number; y: number }) => {
    if (!scrollRef.value) {
        setZoom(nextZoom)
        return
    }

    const scroller = scrollRef.value
    const rect = scroller.getBoundingClientRect()
    const targetZoom = clampZoom(nextZoom)
    const anchorScreenX = screenPoint?.x ?? rect.left + scroller.clientWidth / 2
    const anchorScreenY = screenPoint?.y ?? rect.top + scroller.clientHeight / 2
    const anchorStageX = (anchorScreenX - rect.left + scroller.scrollLeft) / zoom.value
    const anchorStageY = (anchorScreenY - rect.top + scroller.scrollTop) / zoom.value

    zoom.value = targetZoom
    await nextTick()

    scroller.scrollLeft = Math.max(0, anchorStageX * targetZoom - (anchorScreenX - rect.left))
    scroller.scrollTop = Math.max(0, anchorStageY * targetZoom - (anchorScreenY - rect.top))
}

const zoomIn = () => setZoomAroundPoint(zoom.value + ZOOM_STEP)
const zoomOut = () => setZoomAroundPoint(zoom.value - ZOOM_STEP)
const resetZoom = () => setZoomAroundPoint(1)

const handleWheelZoom = (event: WheelEvent) => {
    setZoomAroundPoint(zoom.value + (event.deltaY < 0 ? ZOOM_STEP : -ZOOM_STEP), {
        x: event.clientX,
        y: event.clientY,
    })
}

const isCanvasPanTarget = (event: PointerEvent) => {
    const target = event.target as HTMLElement | SVGElement | null
    if (!target) {
        return false
    }
    return !target.closest(
        '.power-flow-device, .power-flow-junction, .power-flow-wire, .power-flow-canvas__toolbar, .power-flow-canvas__zoom, button',
    )
}

const updateViewportSize = () => {
    viewportSize.value = {
        width: canvasRef.value?.clientWidth ?? 0,
        height: canvasRef.value?.clientHeight ?? 0,
    }
}

const preserveViewportCenterOnResize = async () => {
    if (!canvasRef.value || !scrollRef.value) {
        updateViewportSize()
        return
    }

    const previousSize = viewportSize.value
    const nextSize = {
        width: canvasRef.value.clientWidth,
        height: canvasRef.value.clientHeight,
    }

    if (nextSize.width === previousSize.width && nextSize.height === previousSize.height) {
        return
    }

    if (!hasAppliedInitialFit.value || previousSize.width === 0 || previousSize.height === 0) {
        viewportSize.value = nextSize
        return
    }

    const scroller = scrollRef.value
    const centerStageX = (scroller.scrollLeft + previousSize.width / 2) / zoom.value
    const centerStageY = (scroller.scrollTop + previousSize.height / 2) / zoom.value

    viewportSize.value = nextSize
    await nextTick()

    scroller.scrollLeft = Math.max(0, centerStageX * zoom.value - nextSize.width / 2)
    scroller.scrollTop = Math.max(0, centerStageY * zoom.value - nextSize.height / 2)
}

const handleViewportResize = () => {
    if (resizeFrameId != null) {
        window.cancelAnimationFrame(resizeFrameId)
    }
    resizeFrameId = window.requestAnimationFrame(async () => {
        resizeFrameId = null
        await preserveViewportCenterOnResize()
    })
}

const fitToContent = async () => {
    if (!canvasRef.value || !scrollRef.value) {
        return
    }

    updateViewportSize()
    if (viewportSize.value.width === 0 || viewportSize.value.height === 0) {
        return
    }

    if (layout.value.nodes.length === 0 && layout.value.junctions.length === 0) {
        zoom.value = 1
        await nextTick()

        scrollRef.value.scrollLeft = Math.max(0, (stageWidth.value - viewportSize.value.width) / 2)
        scrollRef.value.scrollTop = Math.max(0, (stageHeight.value - viewportSize.value.height) / 2)
        return
    }

    const availableWidth = Math.max(1, viewportSize.value.width)
    const availableHeight = Math.max(1, viewportSize.value.height)
    const targetBounds = initialFitBounds.value
    const targetZoom = Math.min(
        MAX_ZOOM,
        Math.max(
            MIN_ZOOM,
            Math.min(availableWidth / targetBounds.width, availableHeight / targetBounds.height),
        ),
    )

    zoom.value = Number(targetZoom.toFixed(2))
    await nextTick()

    const contentWidth = targetBounds.width * zoom.value
    const contentHeight = targetBounds.height * zoom.value
    const centeredLeft = targetBounds.minX * zoom.value - (viewportSize.value.width - contentWidth) / 2
    const centeredTop = targetBounds.minY * zoom.value - (viewportSize.value.height - contentHeight) / 2

    scrollRef.value.scrollLeft = Math.max(0, centeredLeft)
    scrollRef.value.scrollTop = Math.max(0, centeredTop)
}

const scheduleInitialFit = async () => {
    if (!canvasRef.value) {
        return
    }
    await nextTick()
    if (fitFrameId != null) {
        window.cancelAnimationFrame(fitFrameId)
    }
    fitFrameId = window.requestAnimationFrame(async () => {
        updateViewportSize()
        if (viewportSize.value.width === 0 || viewportSize.value.height === 0 || hasAppliedInitialFit.value) {
            return
        }
        await fitToContent()
        hasAppliedInitialFit.value = true
        fitFrameId = null
    })
}

const syncLayout = () => {
    const nextLayout = cloneLayout(layout.value)
    lastSyncedLayout = JSON.stringify(nextLayout)
    emit('update:modelValue', nextLayout)
}

const isSameLayout = (a: PowerFlowLayout, b: PowerFlowLayout) => JSON.stringify(a) === JSON.stringify(b)

const pushUndoSnapshot = (snapshot = cloneLayout(layout.value)) => {
    undoStack.value = [...undoStack.value.slice(-29), snapshot]
}

const undoLayoutChange = () => {
    if (!props.editable || undoStack.value.length === 0) {
        return
    }
    const previousLayout = undoStack.value[undoStack.value.length - 1]
    undoStack.value = undoStack.value.slice(0, -1)
    layout.value = cloneLayout(previousLayout)
    clearSelection()
    dragState.value = null
    dragSnapshot.value = null
    wireStart.value = null
    syncLayout()
}

const clearNodeSelection = () => {
    selectedNodeIds.value = []
}

const selectSingleNode = (nodeId: string) => {
    selectedNodeIds.value = [nodeId]
    selectedWireId.value = ''
    selectedJunctionId.value = ''
}

const toggleNodeSelection = (nodeId: string) => {
    selectedWireId.value = ''
    selectedJunctionId.value = ''
    if (selectedNodeIds.value.includes(nodeId)) {
        selectedNodeIds.value = selectedNodeIds.value.filter(id => id !== nodeId)
        return
    }
    selectedNodeIds.value = [...selectedNodeIds.value, nodeId]
}

const startCanvasPan = (event: PointerEvent) => {
    if (event.button !== 0 || !scrollRef.value || !isCanvasPanTarget(event)) {
        return
    }
    panState.value = {
        pointerId: event.pointerId,
        startX: event.clientX,
        startY: event.clientY,
        scrollLeft: scrollRef.value.scrollLeft,
        scrollTop: scrollRef.value.scrollTop,
    }
    wasCanvasPanning.value = false
    scrollRef.value.setPointerCapture(event.pointerId)
}

const handleDrop = (event: DragEvent) => {
    if (!props.editable) {
        return
    }
    const deviceId = Number(event.dataTransfer?.getData('application/x-power-flow-device'))
    if (!deviceId || placedDeviceIds.value.includes(deviceId)) {
        return
    }
    pushUndoSnapshot()
    const point = canvasPoint(event)
    layout.value.nodes.push({
        client_id: createClientId('node'),
        device_id: deviceId,
        x: Math.max(0, point.x - 95),
        y: Math.max(0, point.y - 52),
        width: 190,
        height: 84,
    })
    syncLayout()
}

const startNodeDrag = (event: PointerEvent, nodeId: string) => {
    if (!props.editable) {
        return
    }
    if (event.ctrlKey) {
        return
    }
    const node = layout.value.nodes.find(item => item.client_id === nodeId)
    if (!node) {
        return
    }
    if (!selectedNodeIds.value.includes(nodeId)) {
        selectSingleNode(nodeId)
    } else {
        selectedWireId.value = ''
        selectedJunctionId.value = ''
    }

    const point = canvasPoint(event)
    const selectedNodeSet = new Set(selectedNodeIds.value)
    const dragNodes = layout.value.nodes
        .filter(item => selectedNodeSet.has(item.client_id))
        .map(item => ({ ref: item.client_id, startX: item.x, startY: item.y }))

    dragState.value = {
        type: 'NODE',
        ref: nodeId,
        offsetX: point.x - node.x,
        offsetY: point.y - node.y,
        activeStartX: node.x,
        activeStartY: node.y,
        nodes: dragNodes,
    }
    dragSnapshot.value = cloneLayout(layout.value)
    wasNodeDragging.value = false
}

const startJunctionDrag = (event: PointerEvent, junctionId: string) => {
    if (!props.editable) {
        return
    }
    if (wireStart.value) {
        return
    }
    const junction = layout.value.junctions.find(item => item.client_id === junctionId)
    if (!junction) {
        return
    }
    const point = canvasPoint(event)
    dragState.value = {
        type: 'JUNCTION',
        ref: junctionId,
        offsetX: point.x - junction.x,
        offsetY: point.y - junction.y,
    }
    dragSnapshot.value = cloneLayout(layout.value)
}

const handlePointerMove = (event: PointerEvent) => {
    if (panState.value && scrollRef.value) {
        const deltaX = event.clientX - panState.value.startX
        const deltaY = event.clientY - panState.value.startY
        if (Math.abs(deltaX) > 3 || Math.abs(deltaY) > 3) {
            wasCanvasPanning.value = true
        }
        scrollRef.value.scrollLeft = panState.value.scrollLeft - deltaX
        scrollRef.value.scrollTop = panState.value.scrollTop - deltaY
        return
    }
    pointer.value = canvasPoint(event)
    if (!dragState.value) {
        return
    }
    if (dragState.value.type === 'NODE') {
        const nextActiveX = pointer.value.x - dragState.value.offsetX
        const nextActiveY = pointer.value.y - dragState.value.offsetY
        const deltaX = nextActiveX - dragState.value.activeStartX
        const deltaY = nextActiveY - dragState.value.activeStartY
        const minStartX = Math.min(...dragState.value.nodes.map(node => node.startX))
        const minStartY = Math.min(...dragState.value.nodes.map(node => node.startY))
        const safeDeltaX = Math.max(deltaX, -minStartX)
        const safeDeltaY = Math.max(deltaY, -minStartY)

        if (Math.abs(safeDeltaX) > 3 || Math.abs(safeDeltaY) > 3) {
            wasNodeDragging.value = true
        }

        dragState.value.nodes.forEach(dragNode => {
            const node = layout.value.nodes.find(item => item.client_id === dragNode.ref)
            if (node) {
                node.x = dragNode.startX + safeDeltaX
                node.y = dragNode.startY + safeDeltaY
            }
        })

        if (dragState.value.nodes.length === 0) {
            const node = layout.value.nodes.find(item => item.client_id === dragState.value?.ref)
            if (node) {
                node.x = Math.max(0, nextActiveX)
                node.y = Math.max(0, nextActiveY)
            }
        }
        return
    }
    const junction = layout.value.junctions.find(item => item.client_id === dragState.value?.ref)
    if (junction) {
        junction.x = pointer.value.x - dragState.value.offsetX
        junction.y = pointer.value.y - dragState.value.offsetY
    }
}

const handleCanvasPointerUp = () => {
    if (panState.value && scrollRef.value) {
        scrollRef.value.releasePointerCapture(panState.value.pointerId)
        panState.value = null
    }
    if (dragState.value) {
        if (dragSnapshot.value && !isSameLayout(dragSnapshot.value, layout.value)) {
            pushUndoSnapshot(dragSnapshot.value)
        }
        dragState.value = null
        dragSnapshot.value = null
        syncLayout()
    }
    wireStart.value = null
}

const startWire = (event: PointerEvent, nodeId: string, anchor: PowerFlowAnchor) => {
    if (!props.editable) {
        return
    }
    pointer.value = canvasPoint(event)
    wireStart.value = { type: 'NODE', ref: nodeId, anchor }
}

const appendWire = (target: PowerFlowEndpoint) => {
    if (!wireStart.value || (wireStart.value.type === target.type && wireStart.value.ref === target.ref)) {
        wireStart.value = null
        return
    }
    pushUndoSnapshot()
    layout.value.wires.push({
        client_id: createClientId('wire'),
        source_type: wireStart.value.type,
        source_ref: wireStart.value.ref,
        source_anchor: wireStart.value.anchor,
        target_type: target.type,
        target_ref: target.ref,
        target_anchor: target.anchor,
        direction: 'FORWARD',
        metric_key: null,
        is_enabled: true,
        route_points: [],
    })
    wireStart.value = null
    syncLayout()
}

const completeWireToNode = (nodeId: string, anchor: PowerFlowAnchor) =>
    appendWire({ type: 'NODE', ref: nodeId, anchor })
const completeWireToJunction = (junctionId: string) =>
    appendWire({ type: 'JUNCTION', ref: junctionId, anchor: 'RIGHT' })

const handleJunctionPointerUp = (junctionId: string) => {
    if (!props.editable) {
        return
    }
    if (dragState.value?.type === 'JUNCTION' && dragState.value.ref === junctionId) {
        if (dragSnapshot.value && !isSameLayout(dragSnapshot.value, layout.value)) {
            pushUndoSnapshot(dragSnapshot.value)
        }
        dragState.value = null
        dragSnapshot.value = null
        syncLayout()
    }
    if (wireStart.value) {
        completeWireToJunction(junctionId)
    }
}

const selectNode = (event: MouseEvent, nodeId: string) => {
    if (wasNodeDragging.value) {
        wasNodeDragging.value = false
        return
    }
    if (event.ctrlKey) {
        toggleNodeSelection(nodeId)
        return
    }
    selectSingleNode(nodeId)
}

const selectWire = (wireId: string) => {
    selectedWireId.value = wireId
    clearNodeSelection()
    selectedJunctionId.value = ''
}

const selectJunction = (junctionId: string) => {
    selectedJunctionId.value = junctionId
    clearNodeSelection()
    selectedWireId.value = ''
}

const clearSelection = () => {
    clearNodeSelection()
    selectedWireId.value = ''
    selectedJunctionId.value = ''
}

const handleCanvasClick = () => {
    if (wasCanvasPanning.value) {
        wasCanvasPanning.value = false
        return
    }
    clearSelection()
}

const toggleSelectedWire = () => {
    if (!props.editable) {
        return
    }
    if (!selectedWire.value) {
        return
    }
    pushUndoSnapshot()
    selectedWire.value.is_enabled = !selectedWire.value.is_enabled
    syncLayout()
}

const alignSelectedNodes = (axis: AlignAxis) => {
    if (!props.editable || selectedNodes.value.length < 2) {
        return
    }
    pushUndoSnapshot()

    if (axis === 'horizontal') {
        const centerY =
            selectedNodes.value.reduce((sum, node) => sum + node.y + node.height / 2, 0) / selectedNodes.value.length
        selectedNodes.value.forEach(node => {
            node.y = Math.max(0, centerY - node.height / 2)
        })
    } else {
        const centerX =
            selectedNodes.value.reduce((sum, node) => sum + node.x + node.width / 2, 0) / selectedNodes.value.length
        selectedNodes.value.forEach(node => {
            node.x = Math.max(0, centerX - node.width / 2)
        })
    }

    syncLayout()
}

const distributeSelectedNodes = (axis: AlignAxis) => {
    if (!props.editable || selectedNodes.value.length < 3) {
        return
    }
    pushUndoSnapshot()

    const centerKey = axis === 'horizontal' ? 'x' : 'y'
    const sizeKey = axis === 'horizontal' ? 'width' : 'height'
    const orderedNodes = [...selectedNodes.value].sort(
        (a, b) => a[centerKey] + a[sizeKey] / 2 - (b[centerKey] + b[sizeKey] / 2),
    )
    const firstCenter = orderedNodes[0][centerKey] + orderedNodes[0][sizeKey] / 2
    const lastNode = orderedNodes[orderedNodes.length - 1]
    const lastCenter = lastNode[centerKey] + lastNode[sizeKey] / 2
    const spacing = (lastCenter - firstCenter) / (orderedNodes.length - 1)

    orderedNodes.forEach((node, index) => {
        node[centerKey] = Math.max(0, firstCenter + spacing * index - node[sizeKey] / 2)
    })

    syncLayout()
}

const removeSelectedWire = () => {
    if (!props.editable) {
        return
    }
    pushUndoSnapshot()
    layout.value.wires = layout.value.wires.filter(wire => wire.client_id !== selectedWireId.value)
    selectedWireId.value = ''
    syncLayout()
}

const removeSelectedItem = () => {
    if (!props.editable) {
        return
    }
    const selectedNodeSet = new Set(selectedNodeIds.value)
    const selectedJunctionSet = new Set(selectedJunctionId.value ? [selectedJunctionId.value] : [])
    if (selectedNodeSet.size === 0 && selectedJunctionSet.size === 0) {
        return
    }
    pushUndoSnapshot()
    layout.value.nodes = layout.value.nodes.filter(node => !selectedNodeSet.has(node.client_id))
    layout.value.junctions = layout.value.junctions.filter(junction => !selectedJunctionSet.has(junction.client_id))
    layout.value.wires = layout.value.wires.filter(
        wire =>
            !selectedNodeSet.has(wire.source_ref) &&
            !selectedNodeSet.has(wire.target_ref) &&
            !selectedJunctionSet.has(wire.source_ref) &&
            !selectedJunctionSet.has(wire.target_ref),
    )
    clearSelection()
    syncLayout()
}

const splitWire = (event: MouseEvent, wireId: string) => {
    if (!props.editable) {
        return
    }
    const wire = layout.value.wires.find(item => item.client_id === wireId)
    if (!wire) {
        return
    }
    pushUndoSnapshot()
    const junction: PowerFlowJunction = { client_id: createClientId('junction'), ...canvasPoint(event) }
    const originalTarget = { type: wire.target_type, ref: wire.target_ref, anchor: wire.target_anchor }
    wire.target_type = 'JUNCTION'
    wire.target_ref = junction.client_id
    wire.target_anchor = 'LEFT'
    layout.value.junctions.push(junction)
    layout.value.wires.push({
        ...wire,
        client_id: createClientId('wire'),
        source_type: 'JUNCTION',
        source_ref: junction.client_id,
        source_anchor: 'RIGHT',
        target_type: originalTarget.type,
        target_ref: originalTarget.ref,
        target_anchor: originalTarget.anchor,
        route_points: [],
    } as PowerFlowWireType)
    syncLayout()
}

const isTextInputTarget = (target: EventTarget | null) => {
    if (!(target instanceof HTMLElement)) {
        return false
    }
    return Boolean(target.closest('input, textarea, [contenteditable="true"]'))
}

const handleKeydown = (event: KeyboardEvent) => {
    if (!props.editable || isTextInputTarget(event.target)) {
        return
    }
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'z' && !event.shiftKey) {
        event.preventDefault()
        undoLayoutChange()
    }
}

watch(
    () => [
        layout.value.nodes.length,
        layout.value.junctions.length,
        viewportSize.value.width,
        viewportSize.value.height,
    ],
    async ([, , viewportWidth, viewportHeight]) => {
        if (hasAppliedInitialFit.value || viewportWidth === 0 || viewportHeight === 0) {
            return
        }
        await scheduleInitialFit()
    },
    { immediate: true },
)

onMounted(() => {
    scheduleInitialFit()
    keydownListener = handleKeydown
    window.addEventListener('keydown', keydownListener)
    if (scrollRef.value) {
        wheelListener = event => {
            event.preventDefault()
            handleWheelZoom(event)
        }
        scrollRef.value.addEventListener('wheel', wheelListener, { passive: false })
    }
    if (typeof ResizeObserver !== 'undefined' && canvasRef.value) {
        resizeObserver = new ResizeObserver(handleViewportResize)
        resizeObserver.observe(canvasRef.value)
    }
})

onBeforeUnmount(() => {
    if (scrollRef.value && wheelListener) {
        scrollRef.value.removeEventListener('wheel', wheelListener)
    }
    if (keydownListener) {
        window.removeEventListener('keydown', keydownListener)
    }
    if (fitFrameId != null) {
        window.cancelAnimationFrame(fitFrameId)
    }
    if (resizeFrameId != null) {
        window.cancelAnimationFrame(resizeFrameId)
    }
    resizeObserver?.disconnect()
    fitFrameId = null
    resizeFrameId = null
    resizeObserver = null
    wheelListener = null
    keydownListener = null
})
</script>

<style scoped lang="scss">
.power-flow-editor {
    display: flex;
    flex: 1;
    min-height: 0;
    overflow: hidden;
}

.power-flow-canvas {
    position: relative;
    flex: 1;
    min-width: 0;
    min-height: 0;
    overflow: hidden;
    background-color: rgba(4, 9, 18, 0.34);
}

.power-flow-canvas__scroller {
    position: absolute;
    inset: 0;
    overflow: auto;
    scrollbar-width: none;
    cursor: grab;
}

.power-flow-canvas__scroller::-webkit-scrollbar {
    display: none;
}

.power-flow-canvas__scroller:active {
    cursor: grabbing;
}

.power-flow-canvas__viewport {
    position: relative;
    min-width: 100%;
    min-height: 100%;
}

.power-flow-canvas__stage {
    position: relative;
    transform-origin: top left;
    background-image: linear-gradient(rgba(255, 255, 255, 0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.035) 1px, transparent 1px);
    background-size: 24px 24px;
}

.power-flow-canvas.is-readonly {
    cursor: default;
}

.power-flow-canvas__wires {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
}

.power-flow-canvas__draft {
    fill: none;
    stroke: var(--secondary-color);
    stroke-width: 2;
    stroke-dasharray: 6 6;
}

.power-flow-junction {
    position: absolute;
    z-index: 4;
    width: 16px;
    height: 16px;
    padding: 0;
    border: 2px solid var(--secondary-color);
    border-radius: 50%;
    cursor: move;
    background: #111827;
}

.power-flow-junction.is-selected {
    border-color: var(--primary-color);
    box-shadow: 0 0 10px rgba(231, 109, 255, 0.7);
}

.power-flow-canvas__toolbar {
    position: absolute;
    z-index: 8;
    top: 12px;
    right: 12px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.power-flow-canvas__toolbar button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border: 1px solid rgba(231, 109, 255, 0.42);
    border-radius: 6px;
    color: var(--secondary-color);
    cursor: pointer;
    background: rgba(11, 16, 28, 0.9);
}

.power-flow-canvas__toolbar button:disabled {
    color: var(--text-color--secondary);
    cursor: not-allowed;
    opacity: 0.45;
}

.power-flow-canvas__align-tools {
    display: flex;
    gap: 6px;
    padding-right: 6px;
    margin-right: 2px;
    border-right: 1px solid rgba(255, 255, 255, 0.12);
}

.power-flow-canvas__toolbar .power-flow-canvas__align-button {
    width: 32px;
    min-width: 32px;
    padding: 0;
}

.power-flow-canvas__align-button svg {
    width: 17px;
    height: 17px;
}

.power-flow-canvas__undo {
    position: absolute;
    z-index: 8;
    top: 12px;
    right: 12px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border: 1px solid rgba(231, 109, 255, 0.42);
    border-radius: 6px;
    color: var(--secondary-color);
    font-size: 18px;
    font-weight: 700;
    cursor: pointer;
    background: rgba(11, 16, 28, 0.72);
}

.power-flow-canvas__undo:disabled {
    color: var(--text-color--secondary);
    cursor: not-allowed;
    opacity: 0.42;
}

.power-flow-canvas__undo + .power-flow-canvas__toolbar {
    right: 50px;
}

.power-flow-canvas__zoom {
    position: absolute;
    z-index: 9;
    right: 12px;
    bottom: 12px;
    display: flex;
    flex-direction: row;
    gap: 6px;
}

.power-flow-canvas__zoom button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 34px;
    height: 30px;
    padding: 0 10px;
    border: 1px solid rgba(231, 109, 255, 0.42);
    border-radius: 6px;
    color: var(--text-color--primary);
    font-size: 12px;
    font-weight: 700;
    cursor: pointer;
    background: rgba(11, 16, 28, 0.56);
}
</style>
