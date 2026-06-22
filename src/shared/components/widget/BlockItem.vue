<template>
    <div class="block-item-wrap" :class="className">
        <div class="block-item">
            <div class="block-item-header">
                <slot name="header"></slot>
            </div>
            <div class="block-item-body">
                <slot></slot>
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { toRefs } from 'vue'

export interface Props {
    className?: string
}
const props = defineProps<Props>()
const { className } = toRefs(props)
</script>
<style lang="scss" scoped>
.block-item-wrap {
    margin: 12px 0;
    display: flex;
    flex: 1;
    border-radius: 8px;
    background: var(--surface-glass-color);
    border: 1px solid var(--border-glass-color);
    box-shadow: var(--panel-shadow);
}

.block-item {
    height: 100%;
    width: 100%;
    display: flex;
    flex-direction: column;
}
.block-item-header {
    display: flex;
    flex-direction: row;
    position: relative;
    font-weight: bold;
    background-color: var(--surface-glass-color);
    padding: 8px;
    align-items: center;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    border: none;
    border-bottom: none;
    color: var(--text-color--primary);
}
.block-item-body {
    height: calc(100% - 35px);
    display: flex;
    flex-direction: row;
    border-bottom-left-radius: 8px;
    border-bottom-right-radius: 8px;
    border: none;
    border-top: none;
    color: var(--text-color--body);
}
</style>
