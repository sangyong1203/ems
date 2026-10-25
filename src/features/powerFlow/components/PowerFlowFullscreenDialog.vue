<template>
    <el-dialog
        :model-value="modelValue"
        title="전력 흐름"
        fullscreen
        append-to-body
        destroy-on-close
        class="power-flow-fullscreen-dialog"
        @update:model-value="emit('update:modelValue', $event)"
    >
        <PowerFlowCanvas
            v-if="layout && editorData"
            class="power-flow-fullscreen-dialog__canvas"
            :model-value="layout"
            :devices="editorData.devices"
            :telemetry="editorData.telemetry"
            :device-telemetry="editorData.device_telemetry"
            :editable="false"
            :show-palette="false"
            @open-device-detail="emit('open-device-detail', $event)"
        />
    </el-dialog>
</template>

<script setup lang="ts">
import PowerFlowCanvas from './PowerFlowCanvas.vue'
import type { PowerFlowEditorData, PowerFlowLayout } from '../service/powerFlow.types'

defineProps<{
    modelValue: boolean // 전체 화면 표시 여부
    layout: PowerFlowLayout | null // 확대해서 표시할 배치
    editorData: PowerFlowEditorData | null // 장비 및 실시간 계측 데이터
}>()

const emit = defineEmits<{
    'update:modelValue': [visible: boolean] // 다이얼로그 닫힘 상태 동기화
    'open-device-detail': [deviceId: number] // 확대 흐름도에서 더블클릭한 장비 상세 요청
}>()
</script>

<style scoped lang="scss">
:global(.power-flow-fullscreen-dialog .el-dialog__title) {
    color: var(--text-color--primary);
}

:global(.power-flow-fullscreen-dialog .el-dialog__body) {
    display: flex;
    height: calc(100dvh - 76px);
    min-height: 0;
    padding: 8px;
}

@media (max-width: 767px) {
    .power-flow-fullscreen-dialog__canvas :deep(.power-flow-canvas__scroller) {
        touch-action: none;
    }

    .power-flow-fullscreen-dialog__canvas :deep(.power-flow-canvas__zoom button) {
        min-width: 44px;
        min-height: 44px;
    }
}
</style>
