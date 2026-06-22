<template>
    <div class="dashboard-power-flow-line" :class="[`dashboard-power-flow-line--${variant}`, { 'is-active': active }]">
        <span v-if="active">{{ valueText }}</span>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
    variant: 'solar-load' | 'solar-ess' | 'ess-load' | 'grid-load' | 'solar-grid' | 'ess-grid'
    value: number
    suffix?: string
}>()

const active = computed(() => Number(props.value || 0) > 0)
const valueText = computed(
    () =>
        `${Number(props.value || 0).toLocaleString(undefined, { maximumFractionDigits: 1 })} kW${props.suffix ? ` ${props.suffix}` : ''}`,
)
</script>

<style scoped lang="scss">
.dashboard-power-flow-line {
    position: absolute;
    z-index: 1;
    height: 2px;
    border-radius: 999px;
    opacity: 0.16;
    background: rgba(255, 255, 255, 0.16);
    transform-origin: center;
}

.dashboard-power-flow-line::after {
    content: '';
    position: absolute;
    top: 50%;
    right: -5px;
    width: 9px;
    height: 9px;
    border-top: 2px solid rgba(255, 255, 255, 0.18);
    border-right: 2px solid rgba(255, 255, 255, 0.18);
    transform: translateY(-50%) rotate(45deg);
}

.dashboard-power-flow-line span {
    position: absolute;
    top: -20px;
    left: 50%;
    color: var(--text-color--secondary);
    font-size: 12px;
    font-weight: 700;
    white-space: nowrap;
    transform: translateX(-50%);
}

.dashboard-power-flow-line.is-active {
    height: 3px;
    opacity: 1;
    background: linear-gradient(90deg, var(--secondary-color), var(--primary-color));
    box-shadow: 0 0 16px rgba(21, 224, 183, 0.4);
}

.dashboard-power-flow-line.is-active::after {
    border-color: var(--primary-color);
}

.dashboard-power-flow-line.is-active span {
    color: #ffffff;
}

.dashboard-power-flow-line--solar-load {
    top: 33%;
    left: 21%;
    width: 22%;
    transform: rotate(-18deg);
}

.dashboard-power-flow-line--solar-ess {
    top: 67%;
    left: 21%;
    width: 22%;
    transform: rotate(18deg);
}

.dashboard-power-flow-line--ess-load {
    top: 51%;
    left: 51%;
    width: 5.5%;
    transform: rotate(-90deg);
}

.dashboard-power-flow-line--grid-load {
    top: 31%;
    left: 64%;
    width: 15%;
    transform: rotate(-162deg);
}

.dashboard-power-flow-line--solar-grid {
    top: 50%;
    left: 22%;
    width: 55%;
}

.dashboard-power-flow-line--ess-grid {
    top: 75%;
    left: 71%;
    width: 8%;
    transform: rotate(-28deg);
}
</style>
