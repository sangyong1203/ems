<template>
    <article
        class="power-flow-device"
        :class="[
            `is-${device.status.toLowerCase()}`,
            { 'is-selected': selected, 'is-inactive': !device.is_active, 'is-readonly': !editable },
        ]"
        :style="nodeStyle"
        @pointerdown.stop="emit('drag-start', $event, node.client_id)"
        @click.stop="emit('select', $event, node.client_id)"
    >
        <div class="power-flow-device__icon">
            <img v-if="device.image_path" :src="device.image_path" :alt="device.name" />
            <AppIcon v-else :name="deviceVisual(device.device_type).icon" />
        </div>
        <div class="power-flow-device__content">
            <strong>{{ device.name }}</strong>
            <b v-if="showDisplayValue">{{ displayValue }}</b>
            <span class="power-flow-device__meta">
                <small>{{ deviceVisual(device.device_type).label }}</small>
                <em>{{ deviceStatusLabel(device) }}</em>
            </span>
            <span v-if="moduleCountText" class="power-flow-device__meta">
                <small>모듈</small>
                <em>{{ moduleCountText }}</em>
            </span>
        </div>
        <button
            v-for="anchor in anchors"
            :key="anchor"
            v-show="editable || connectedAnchors.includes(anchor)"
            type="button"
            class="power-flow-device__anchor"
            :class="`is-${anchor.toLowerCase()}`"
            :title="`${anchor} 연결점`"
            :disabled="!editable"
            @pointerdown.stop="emit('anchor-start', $event, node.client_id, anchor)"
            @pointerup.stop="emit('anchor-end', node.client_id, anchor)"
        ></button>
    </article>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import AppIcon from '@/shared/components/widget/AppIcon.vue'
import type { PowerFlowAnchor, PowerFlowDeviceItem, PowerFlowLayoutNode } from '../service/powerFlow.types'
import { deviceStatusLabel, deviceVisual } from '../service/powerFlow.utils'

const props = defineProps<{
    node: PowerFlowLayoutNode
    device: PowerFlowDeviceItem
    selected: boolean
    editable?: boolean
    connectedAnchors: PowerFlowAnchor[]
}>()

const emit = defineEmits<{
    'drag-start': [event: PointerEvent, nodeId: string]
    select: [event: MouseEvent, nodeId: string]
    'anchor-start': [event: PointerEvent, nodeId: string, anchor: PowerFlowAnchor]
    'anchor-end': [nodeId: string, anchor: PowerFlowAnchor]
}>()

const anchors: PowerFlowAnchor[] = ['TOP', 'RIGHT', 'BOTTOM', 'LEFT']
const showDisplayValue = computed(() => props.device.device_type !== 'AC_PANEL')
const displayValue = computed(() => {
    if (props.device.display_value == null) {
        return `#${props.device.id}`
    }
    return `${props.device.display_value.toLocaleString(undefined, { maximumFractionDigits: 1 })} ${props.device.display_unit ?? ''}`.trim()
})
const moduleCountText = computed(() => {
    if (props.device.device_type !== 'INVERTER' || !props.device.module_count) {
        return ''
    }
    return `${props.device.module_count.toLocaleString()}장`
})
const nodeStyle = computed(() => ({
    left: `${props.node.x}px`,
    top: `${props.node.y}px`,
    width: `${props.node.width}px`,
    height: `${props.node.height}px`,
}))
</script>

<style scoped lang="scss">
.power-flow-device {
    position: absolute;
    z-index: 3;
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px;
    border: 1px solid rgba(21, 224, 183, 0.3);
    border-radius: 7px;
    cursor: move;
    background: linear-gradient(135deg, rgba(21, 224, 183, 0.12), rgba(231, 109, 255, 0.1)), rgba(14, 20, 34, 0.92);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.24);
    user-select: none;
}

.power-flow-device.is-readonly {
    cursor: default;
}

.power-flow-device.is-selected {
    border-color: var(--primary-color);
    box-shadow: 0 0 16px rgba(231, 109, 255, 0.34);
}

.power-flow-device.is-warning {
    border-color: rgba(242, 184, 75, 0.8);
}

.power-flow-device.is-fault {
    border-color: rgba(255, 107, 120, 0.88);
}

.power-flow-device.is-inactive {
    opacity: 0.54;
}

.power-flow-device__icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 38px;
    height: 38px;
    color: var(--secondary-color);
}

.power-flow-device__icon img,
.power-flow-device__icon :deep(svg) {
    width: 100%;
    height: 100%;
    object-fit: contain;
}

.power-flow-device__content {
    display: flex;
    flex-direction: column;
    gap: 3px;
    min-width: 0;
    max-width: 110px;
}

.power-flow-device__content em {
    color: var(--text-color--secondary);
    font-size: 11px;
    font-style: normal;
}

.power-flow-device__content strong {
    overflow: hidden;
    font-size: 15px;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.power-flow-device__content b {
    color: var(--secondary-color);
    font-size: 14px;
}

.power-flow-device__meta {
    display: flex;
    align-items: center;
    gap: 7px;
    min-width: 0;
}

.power-flow-device__meta small {
    overflow: hidden;
    color: var(--text-color--secondary);
    font-size: 11px;
    font-weight: 600;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.power-flow-device__anchor {
    position: absolute;
    width: 12px;
    height: 12px;
    padding: 0;
    border: 2px solid rgba(21, 224, 183, 0.86);
    border-radius: 50%;
    background: #111827;
    cursor: crosshair;
}

.power-flow-device__anchor:hover {
    background: var(--secondary-color);
}

.power-flow-device__anchor:disabled {
    cursor: default;
    opacity: 0.45;
}

.power-flow-device__anchor.is-top {
    top: -7px;
    left: calc(50% - 6px);
}

.power-flow-device__anchor.is-right {
    top: calc(50% - 6px);
    right: -7px;
}

.power-flow-device__anchor.is-bottom {
    bottom: -7px;
    left: calc(50% - 6px);
}

.power-flow-device__anchor.is-left {
    top: calc(50% - 6px);
    left: -7px;
}
</style>
