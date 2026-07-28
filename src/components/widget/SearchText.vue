<template>
    <div
        class="search-text"
        :style="{ width: props.width ?? '' }"
        :class="props.labelPosition === 'top' ? 'label-position-top' : 'label-position-left'"
        @keyup.enter="onEnter"
    >
        <div v-if="label" class="search-text_label" :style="{ width: props.labelWidth ?? '' }">
            {{ props.label }}
        </div>
        <div class="search-text_content">
            <slot></slot>
            <el-input
                style="flex: 1; width: 100%"
                :model-value="props.modelValue"
                :placeholder="props.placeholder ?? ''"
                @input="onInput"
                :suffix-icon="props.showSuffixIcon === false ? undefined : Search"
                :size="props.size"
            >
            </el-input>

            <slot name="append"></slot>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { Search } from '@element-plus/icons-vue'
export interface Props {
    label?: string | null
    labelWidth?: string | null
    width?: string | null
    placeholder?: string | null
    modelValue: string | number | null
    size?: '' | 'default' | 'small' | 'large'
    labelPosition?: 'top' | 'left'
    showSuffixIcon?: boolean
}
const props = defineProps<Props>()
const emits = defineEmits(['update:modelValue', 'onEnter'])
const onInput = (value: any) => {
    emits('update:modelValue', value)
}
const onEnter = () => {
    emits('onEnter')
}
</script>
<style scoped>
.search-text {
    display: flex;
    align-items: center;
    gap: 16px;
    color: var(--text-color--primary);
    width: 100%;
}
.search-text_label {
    color: var(--text-color--primary);
    white-space: nowrap;
    font-size: 18px;
    font-weight: 600;
    line-height: 20px;
}
.search-text_content {
    display: flex;
    align-items: center;
    gap: 4px;
    flex: 1;
    width: 100%;
}
.search-text_content :deep(.el-input) {
    width: 100%;
}
.search-text_content :deep(.el-input__wrapper) {
    min-height: 36px;
    padding: 4px 20px;
    border-radius: 999px;
    background: var(--common-control-bg-color);
    box-shadow: 0 0 0 1px var(--common-control-border-color) inset;
}
.search-text_content :deep(.el-input__inner) {
    height: 28px;
    font-size: 15px;
    color: var(--text-color--primary);
}
.search-text_content :deep(.el-input__inner::placeholder) {
    color: var(--text-color--placeholder);
}
.input-with-select .el-input-group__prepend {
    background-color: var(--el-fill-color-blank);
}
.label-position-top {
    flex-direction: column;
    align-items: flex-start;
}
</style>
