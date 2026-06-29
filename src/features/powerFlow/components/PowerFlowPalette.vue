<template>
    <aside class="power-flow-palette" :class="{ 'is-disabled': !editable }">
        <header class="power-flow-palette__header">
            <h3>장비 목록</h3>
            <span>{{ availableDevices.length }}대</span>
        </header>
        <div class="power-flow-palette__list">
            <article
                v-for="device in availableDevices"
                :key="device.id"
                class="power-flow-palette__item"
                :draggable="editable"
                @dragstart="handleDragStart($event, device)"
            >
                <div class="power-flow-palette__icon">
                    <img v-if="device.image_path" :src="device.image_path" :alt="device.name" />
                    <AppIcon v-else :name="deviceVisual(device.device_type).icon" />
                </div>
                <div class="power-flow-palette__meta">
                    <strong>{{ device.name }}</strong>
                    <span>{{ deviceVisual(device.device_type).label }} · {{ displayValue(device) }}</span>
                </div>
                <em :class="`is-${device.status.toLowerCase()}`">{{ deviceStatusLabel(device) }}</em>
            </article>
            <p v-if="!availableDevices.length" class="power-flow-palette__empty">배치 가능한 장비가 없습니다.</p>
        </div>
    </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import AppIcon from '@/shared/components/widget/AppIcon.vue'
import type { PowerFlowDeviceItem } from '../service/powerFlow.types'
import { deviceStatusLabel, deviceVisual } from '../service/powerFlow.utils'

const props = defineProps<{
    devices: PowerFlowDeviceItem[]
    placedDeviceIds: number[]
    editable?: boolean
}>()

const availableDevices = computed(() => props.devices.filter(device => !props.placedDeviceIds.includes(device.id)))

const displayValue = (device: PowerFlowDeviceItem) => {
    if (device.display_value == null) {
        return `#${device.id}`
    }
    if (device.device_type === 'BATTERY_RACK') {
        return `${device.display_value.toLocaleString(undefined, { maximumFractionDigits: 1 })}%`
    }
    return `${device.display_value.toLocaleString(undefined, { maximumFractionDigits: 1 })} ${device.display_unit ?? ''}`.trim()
}

const handleDragStart = (event: DragEvent, device: PowerFlowDeviceItem) => {
    if (!props.editable) {
        event.preventDefault()
        return
    }
    event.dataTransfer?.setData('application/x-power-flow-device', String(device.id))
    if (event.dataTransfer) {
        event.dataTransfer.effectAllowed = 'copy'
    }
}
</script>

<style scoped lang="scss">
.power-flow-palette {
    display: flex;
    flex-direction: column;
    width: 230px;
    min-width: 230px;
    min-height: 0;
    overflow: hidden;
    border-right: 1px solid var(--border-color);
    background: rgba(7, 12, 22, 0.4);
    padding-bottom: 12px;
}

.power-flow-palette__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px;
    border-bottom: 1px solid var(--border-color);
}

.power-flow-palette__header h3 {
    margin: 0;
    font-size: 15px;
}

.power-flow-palette__header span {
    color: var(--secondary-color);
    font-size: 13px;
}

.power-flow-palette__list {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 0px 4px 0px 12px;
    overflow: auto;
    margin-top: 12px;
}

.power-flow-palette__item {
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 10px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 6px;
    cursor: grab;
    background: rgba(255, 255, 255, 0.04);
}

.power-flow-palette__item:active {
    cursor: grabbing;
}

.power-flow-palette__icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 30px;
    height: 30px;
    color: var(--secondary-color);
}

.power-flow-palette__icon img,
.power-flow-palette__icon :deep(svg) {
    width: 100%;
    height: 100%;
    object-fit: contain;
}

.power-flow-palette__meta {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 3px;
    min-width: 0;
}

.power-flow-palette__meta strong {
    overflow: hidden;
    font-size: 13px;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.power-flow-palette__meta span,
.power-flow-palette__item em,
.power-flow-palette__empty {
    color: var(--text-color--secondary);
    font-size: 11px;
    font-style: normal;
}

.power-flow-palette__item em.is-normal {
    color: var(--secondary-color);
}

.power-flow-palette__item em.is-warning {
    color: #f2b84b;
}

.power-flow-palette__item em.is-fault {
    color: #ff6b78;
}

.power-flow-palette.is-disabled {
    opacity: 0.8;
}

.power-flow-palette.is-disabled .power-flow-palette__item {
    cursor: default;
}
</style>
