<template>
    <div
        class="content-block"
        :class="className"
        :style="{ padding: padding, width: width, height: height, backgroundColor: backgroundColor }"
    >
        <slot></slot>
    </div>
</template>
<script lang="ts" setup>
import { toRefs } from 'vue'

export interface Props {
    className?: string
    padding?: string
    width?: string
    height?: string
    backgroundColor?: string
}
const props = defineProps<Props>()
const { className, padding, width, backgroundColor, height } = toRefs(props)
</script>
<style lang="scss" scoped>
.content-block {
    padding: 20px 24px;
    border: 1px solid var(--common-component-border-color);
    border-radius: 8px;
    background-color: var(--common-component-bg-color);
    color: var(--text-color--body);
    flex: 1;
    min-height: 0;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}
</style>
