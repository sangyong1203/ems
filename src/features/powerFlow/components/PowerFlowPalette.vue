<template>
    <aside class="power-flow-palette" :class="{ 'is-disabled': !editable }">
        <header class="power-flow-palette__header">
            <h3>장비 목록</h3>
            <span class="power-flow-palette__count"><small>미배치 장비</small> {{ availableDevices.length }}대</span>
        </header>
        <div class="power-flow-palette__list">
            <article
                v-for="device in availableDevices"
                :key="device.id"
                class="power-flow-palette__item"
                :class="{ 'is-selected': selectedDeviceId === device.id }"
                role="button"
                tabindex="0"
                :aria-pressed="selectedDeviceId === device.id"
                :draggable="editable"
                @click="emit('select-device', device.id)"
                @dblclick.stop="emit('open-device-detail', device.id)"
                @keydown.enter.prevent="emit('select-device', device.id)"
                @keydown.space.prevent="emit('select-device', device.id)"
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
import AppIcon from '@/components/widget/AppIcon.vue'
import type { PowerFlowDeviceItem } from '../service/powerFlow.types'
import { deviceStatusLabel, deviceVisual } from '../service/powerFlow.utils'

const props = defineProps<{
    devices: PowerFlowDeviceItem[]
    placedDeviceIds: number[]
    editable?: boolean
    selectedDeviceId?: number | null // 상세 패널에 표시할 장비 ID
}>()

// 목록에서 상세정보를 표시할 장비를 선택합니다.
const emit = defineEmits<{
    'select-device': [deviceId: number]
    'open-device-detail': [deviceId: number] // 더블클릭한 장비의 상세 창 열기
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

.power-flow-palette__count {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    white-space: nowrap;
}

.power-flow-palette__count small {
    color: var(--text-color--secondary);
    font-size: 11px;
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

.power-flow-palette__item.is-selected {
    border-color: var(--primary-color);
    background: var(--layout-menu-active-bg-color);
}

.power-flow-palette__item:focus-visible {
    outline: 2px solid var(--accent-color);
    outline-offset: -2px;
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
