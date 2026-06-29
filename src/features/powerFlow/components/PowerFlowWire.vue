<template>
    <g class="power-flow-wire" :class="[`is-${tone}`, { 'is-selected': selected }]">
        <path class="power-flow-wire__hit" :d="path" @click.stop="emit('select', wire.client_id)" @dblclick.stop="emit('split', $event, wire.client_id)" />
        <path class="power-flow-wire__line" :d="path" />
        <path v-if="currentActive" class="power-flow-wire__current" :class="`is-${currentDirection.toLowerCase()}`" :d="path" />
    </g>
</template>

<script setup lang="ts">
import type { PowerFlowDirection, PowerFlowWire, PowerFlowWireTone } from '../service/powerFlow.types'

defineProps<{
    wire: PowerFlowWire
    path: string
    tone: PowerFlowWireTone
    selected: boolean
    currentActive: boolean
    currentDirection: PowerFlowDirection
}>()

const emit = defineEmits<{
    select: [wireId: string]
    split: [event: MouseEvent, wireId: string]
}>()
</script>

<style scoped lang="scss">
.power-flow-wire__line,
.power-flow-wire__current,
.power-flow-wire__hit {
    fill: none;
    stroke-linecap: round;
    stroke-linejoin: round;
}

.power-flow-wire__hit {
    stroke: transparent;
    stroke-width: 18;
    cursor: pointer;
}

.power-flow-wire__line {
    stroke: rgba(255, 255, 255, 0.18);
    stroke-width: 3;
}

.power-flow-wire.is-active .power-flow-wire__line {
    stroke: rgba(21, 224, 183, 0.62);
}

.power-flow-wire.is-warning .power-flow-wire__line {
    stroke: #f2b84b;
}

.power-flow-wire.is-fault .power-flow-wire__line {
    stroke: #ff6b78;
}

.power-flow-wire.is-selected .power-flow-wire__line {
    stroke-width: 5;
    filter: drop-shadow(0 0 5px rgba(231, 109, 255, 0.72));
}

.power-flow-wire__current {
    stroke: var(--primary-color);
    stroke-width: 3;
    stroke-dasharray: 3 14;
    animation: current-forward 0.72s linear infinite;
}

.power-flow-wire__current.is-reverse {
    animation-name: current-reverse;
}

.power-flow-wire__current.is-bidirectional {
    stroke-dasharray: 3 9;
    animation-duration: 1.1s;
}

@keyframes current-forward {
    to {
        stroke-dashoffset: -34;
    }
}

@keyframes current-reverse {
    to {
        stroke-dashoffset: 34;
    }
}
</style>
