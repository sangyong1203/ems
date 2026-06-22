<template>
    <el-tooltip :content="content" :placement="placement" :show-arrow="false" popper-class="tooltip-custom">
        <template #content>
            <div v-html="content"></div>
        </template>
        <slot></slot>
    </el-tooltip>
</template>

<script setup lang="ts">
import { toRefs } from 'vue'

interface Props {
    content: string
    placement?: 'top' | 'bottom' | 'left' | 'right'
}

const props = withDefaults(defineProps<Props>(), {
    placement: 'top',
})

const { content, placement } = toRefs(props)
</script>

<style lang="scss" scoped>
:global(.el-popper.tooltip-custom) {
    background: var(--common-tooltip-bg-color) !important;
    border: 1px solid var(--common-component-border-color) !important;
    color: var(--text-color--body) !important;
    font-size: 15px !important;
    font-weight: 400 !important;
    padding: 16px !important;
    border-radius: 8px !important;
    max-width: 35vw;
    max-height: 45vh;
    overflow: scroll;
}
</style>
