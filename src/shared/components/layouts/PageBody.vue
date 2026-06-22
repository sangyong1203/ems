<template>
    <div class="page-body">
        <div class="page-body-content" :style="{ gap, flexDirection, flexWrap }">
            <slot></slot>
        </div>
        <slot name="footer"></slot>
    </div>
</template>
<script lang="ts" setup>
export interface Props {
    flexDirection?: 'row' | 'column'
    gap?: string
    flexWrap?: 'wrap' | 'nowrap'
}
withDefaults(defineProps<Props>(), {
    flexDirection: 'column',
})
</script>
<style scoped lang="scss">
.page-body {
    flex: 1;
    display: flex;
    flex-direction: column;
    border-radius: 8px;
    position: relative;
    overflow-x: auto;
    min-width: 1200px;
    min-height: 600px;
}
.page-body-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    height: 100%;
}
.flex-column {
    flex-direction: column;
}
.flex-row {
    flex-direction: row;
}

@media (max-width: 768px) {
    .page-body {
        margin-right: 8px;
        margin-bottom: 4px;
    }
}
</style>
