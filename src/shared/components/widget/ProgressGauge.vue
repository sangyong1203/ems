<template>
    <div class="progress-gauge">
        <span v-if="showLabel && label" class="progress-gauge__label">{{ label }}</span>
        <div class="progress-gauge__track">
            <div class="progress-gauge__bar" :style="{ width: `${boundedValue}%` }"></div>
        </div>
        <span class="progress-gauge__value" :class="{ 'is-prominent': prominentValue }">{{ valueText || label }}</span>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
    defineProps<{
        value: number
        label?: string
        valueText?: string
        showLabel?: boolean
        prominentValue?: boolean
    }>(),
    {
        showLabel: false,
        prominentValue: false,
    },
)

const boundedValue = computed(() => Math.min(100, Math.max(0, props.value || 0)))
</script>

<style scoped lang="scss">
.progress-gauge {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 14px;
}

.progress-gauge__track {
    flex: 1;
    height: 12px;
    border-radius: 999px;
    overflow: hidden;
    background: rgba(255, 255, 255, 0.1);
}

.progress-gauge__bar {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, var(--secondary-color), var(--primary-color));
}

.progress-gauge__label,
.progress-gauge__value {
    color: var(--text-color--secondary);
    font-size: 13px;
    font-weight: 700;
    white-space: nowrap;
}

.progress-gauge__value.is-prominent {
    color: var(--secondary-color);
    font-size: 20px;
    line-height: 24px;
}
</style>
