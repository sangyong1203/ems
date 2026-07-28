<template>
    <el-tag class="common-tag" :class="tagClass" round>
        <slot>{{ label }}</slot>
    </el-tag>
</template>

<script lang="ts" setup>
import { computed } from 'vue'

const props = withDefaults(
    defineProps<{
        label?: string
        variant?: string
    }>(),
    {
        label: '',
        variant: 'default',
    }
)

const tagClass = computed(() => {
    const normalizedVariant = props.variant.trim().toLowerCase().replace(/\s+/g, '-')
    return `common-tag--${normalizedVariant || 'default'}`
})
</script>

<style lang="scss" scoped>
.common-tag {
    min-width: var(--tag-min-width);
    height: var(--tag-height);
    justify-content: center;
    border-radius: var(--tag-border-radius);
    border-width: 1px;
    background: var(--tag-default-bg-color);
    border-color: var(--tag-default-border-color);
    color: var(--tag-default-text-color);
    font-size: var(--tag-font-size);
    font-weight: var(--tag-font-weight);
    letter-spacing: 0;
}

.common-tag--active {
    background: var(--tag-active-bg-color);
    border-color: var(--tag-active-border-color);
    color: var(--tag-active-text-color);
}

.common-tag--inactive {
    background: var(--tag-inactive-bg-color);
    border-color: var(--tag-inactive-border-color);
    color: var(--tag-inactive-text-color);
}

.common-tag--locked {
    background: var(--tag-locked-bg-color);
    border-color: var(--tag-locked-border-color);
    color: var(--tag-locked-text-color);
}

.common-tag--online,
.common-tag--enabled {
    background: rgba(21, 224, 183, 0.14);
    border-color: rgba(21, 224, 183, 0.48);
    color: #15e0b7;
}

.common-tag--offline,
.common-tag--disabled {
    background: rgba(190, 190, 190, 0.1);
    border-color: rgba(190, 190, 190, 0.28);
    color: var(--text-color--secondary);
}

.common-tag--error {
    background: rgba(245, 108, 108, 0.16);
    border-color: rgba(245, 108, 108, 0.48);
    color: var(--el-color-danger);
}

.common-tag--maintenance {
    background: rgba(231, 109, 255, 0.14);
    border-color: rgba(231, 109, 255, 0.48);
    color: var(--accent-color);
}
</style>
