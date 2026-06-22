<template>
    <component
        :is="iconComponent"
        v-if="iconComponent"
        class="app-icon"
        :style="iconStyle"
        v-bind="$attrs"
    ></component>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { AppIcons, type AppIconName } from '@/shared/constants/appIcons'

defineOptions({
    inheritAttrs: false,
})

const props = defineProps<{
    name: AppIconName | string
    color?: string
}>()

const iconComponent = computed(() => AppIcons[props.name as AppIconName] ?? null)
const iconStyle = computed(() => (props.color ? { color: props.color } : undefined))
</script>

<style lang="scss" scoped>
.app-icon {
    display: inline-block;
    width: 1em;
    height: 1em;
    color: currentColor;
}

.app-icon :deep(path),
.app-icon :deep(rect),
.app-icon :deep(circle),
.app-icon :deep(polygon) {
    fill: currentColor;
}
</style>
