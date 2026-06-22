<template>
    <div
        class="label-form-item"
        :style="{ width: props.width ?? '' }"
        :class="props.labelPosition === 'top' ? 'label-position-top' : 'label-position-left'"
    >
        <div v-if="label" class="label-form-item_label" :style="{ width: props.labelWidth ?? '' }">
            {{ props.label }}
        </div>
        <div class="label-form-item_content">
            <slot></slot>
        </div>
    </div>
</template>

<script lang="ts" setup>
export interface Props {
    label?: string | null
    labelWidth?: string | null
    width?: string | null
    labelPosition?: 'top' | 'left'
}
const props = defineProps<Props>()
</script>
<style scoped>
.label-form-item {
    display: flex;
    align-items: center;
    gap: 20px;
    color: var(--label-text-color);
}
.label-form-item_label {
    color: var(--label-text-color);
    white-space: nowrap;
}
.label-form-item_content {
    display: flex;
    align-items: center;
    gap: 4px;
    flex: 1;
}
.label-position-top {
    flex-direction: column;
    align-items: flex-start;
}
</style>
