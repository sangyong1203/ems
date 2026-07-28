<template>
    <div class="segmented-selection" :style="{width: width, height:height??'52px'}">
        <el-segmented v-model="selectedValue" :options="options" :size="size??'default'" :style="{padding: padding??'4px'}">
          <template #default="scope">
            <div >{{ scope.item.label }}</div>
          </template>
        </el-segmented>

    </div>
</template>
<script setup lang="ts">
import { ref, toRefs, watch } from 'vue';
export interface Props {
    options:{ 
        label :string
        value: any
    }[]
    modelValue: any
    size?: '' | 'small' | 'default' | 'large',
    width?: string
    height?: string
    padding?: string
}

const props = defineProps<Props>()
const { options, modelValue, size, width, height } = toRefs(props)
const selectedValue:any = ref(modelValue.value)

const emits = defineEmits(['update:modelValue'])
watch(modelValue, () => {
    selectedValue.value = modelValue.value 
})
watch(selectedValue, () => {
    emits('update:modelValue', selectedValue.value)
})
</script>
<style scoped lang="scss">
.segmented-selection .el-segmented {
  --el-segmented-item-selected-color: var(--text-color--white);
  --el-segmented-item-selected-bg-color: var(--primary-color);
  --el-border-radius-base: 100px;
  --el-segmented-bg-color: var(--common-component-bg-color);
    box-shadow: var(--panel-shadow);
    border: 1px solid var(--common-component-border-color);
}

:deep(.el-segmented ){
    height: inherit;
    .el-segmented__group{
        gap: 8px;
    }
    .el-segmented__item{
        background-color: var(--common-control-bg-color);
        color: var(--text-color--secondary);
        padding: 12px 24px;
    }
    
}
</style>
