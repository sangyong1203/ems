<template>
    <BaseDialog
        :model-value="modelValue"
        title="장비 상세정보"
        width="min(520px, calc(100vw - 24px))"
        :button-types="['Close']"
        append-to-body
        @update:model-value="emit('update:modelValue', $event)"
    >
        <div v-if="device" class="power-flow-device-detail">
            <div class="power-flow-device-detail__heading">
                <img v-if="device.image_path" :src="device.image_path" :alt="device.name" />
                <AppIcon v-else :name="deviceVisual(device.device_type).icon" />
                <strong>{{ device.name }}</strong>
            </div>
            <KeyValueList :items="detailItems" />
        </div>
    </BaseDialog>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { BaseDialog, KeyValueList } from '@/components'
import AppIcon from '@/components/widget/AppIcon.vue'
import type { PowerFlowDeviceItem, PowerFlowLayout } from '../service/powerFlow.types'
import { deviceStatusLabel, deviceVisual } from '../service/powerFlow.utils'

const props = defineProps<{
    modelValue: boolean // 상세 창 표시 여부
    device: PowerFlowDeviceItem | null // 상세정보를 표시할 장비
    layout: PowerFlowLayout | null // 배치 여부와 연결선 수를 확인할 흐름도
}>()

const emit = defineEmits<{
    'update:modelValue': [visible: boolean] // 공통 다이얼로그의 닫힘 상태 전달
}>()

// 실제 장비 응답과 현재 배치에서 확인할 수 있는 상세정보를 표시합니다.
const detailItems = computed(() => {
    const device = props.device
    if (!device) return []
    const nodes = props.layout?.nodes.filter(node => node.device_id === device.id) ?? []
    const nodeIds = new Set(nodes.map(node => node.client_id))
    const wireCount = props.layout?.wires.filter(wire =>
        (wire.source_type === 'NODE' && nodeIds.has(wire.source_ref)) ||
        (wire.target_type === 'NODE' && nodeIds.has(wire.target_ref)),
    ).length ?? 0
    const items = [
        { label: '장비 ID', value: String(device.id) },
        { label: '장비 이름', value: device.name },
        { label: '장비 종류', value: deviceVisual(device.device_type).label },
        { label: '장비 상태', value: deviceStatusLabel(device) },
        { label: '사용 여부', value: device.is_active ? '사용' : '미사용' },
        { label: '배치 여부', value: nodes.length ? '배치됨' : '미배치' },
        {
            label: '측정값',
            value: device.display_value == null
                ? '-'
                : `${device.display_value.toLocaleString(undefined, { maximumFractionDigits: 1 })} ${device.display_unit ?? ''}`.trim(),
        },
        { label: '연결선 수', value: `${wireCount}개` },
    ]
    if (device.device_type === 'INVERTER' && device.module_count != null) {
        items.push({ label: '모듈 수', value: `${device.module_count.toLocaleString()}장` })
    }
    return items
})
</script>

<style scoped lang="scss">
.power-flow-device-detail {
    max-height: 65dvh;
    overflow-y: auto;
    overflow-wrap: anywhere;
}

.power-flow-device-detail__heading {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
    color: var(--text-color--primary);
    font-size: 18px;
}

.power-flow-device-detail__heading img,
.power-flow-device-detail__heading :deep(svg) {
    flex: 0 0 36px;
    width: 36px;
    height: 36px;
    object-fit: contain;
    color: var(--secondary-color);
}
</style>
