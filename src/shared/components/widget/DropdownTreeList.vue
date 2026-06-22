<template>
    <div class="dropdown-tree-list" :style="{ width: width ?? '270px' }">
        <div v-if="label" class="dropdown-tree-list_label" :style="{ width: labelWidth ?? '' }">
            {{ label }}
        </div>
        <el-tree-select
            :model-value="modelValue"
            :data="dataList"
            :render-after-expand="false"
            :disabled="disabled"
            :placeholder="placeholder"
            @change="onChange"
            @clear="onClear"
            clearable
        />
    </div>
</template>

<script lang="ts" setup>
import { toRefs, ref, watch } from 'vue'

export interface Props {
    label?: string | null
    labelWidth?: string | null
    width?: string | null
    placeholder?: string
    disabled?: boolean
    optionLabel: string
    optionValue: string
    optionIcon?: string
    list: any[]
    modelValue: string | number | null
}

const props = defineProps<Props>()
const { label, labelWidth, width, placeholder, disabled, optionLabel, optionValue, list } = toRefs(props)

const dataList = ref([])
const setData = () => {
    const arr: any = []
    list.value.forEach((item: any) => {
        setArray(item.children, arr)
        function setArray(arryList: [], objArr: any[]) {
            if (arryList.length > 0) {
                arryList.forEach((itemA: any) => {
                    let dataA = {
                        label: itemA[optionLabel.value],
                        value: itemA[optionValue.value],
                        children: [],
                    }
                    objArr.push(dataA)
                    if (itemA.children.length > 0) {
                        setArray(itemA.children, dataA.children)
                    }
                })
            }
        }
    })
    dataList.value = arr
}
const emits = defineEmits(['update:modelValue', 'onChange'])
watch(list, () => {
    setData()
})

const onChange = (value: any) => {
    emits('update:modelValue', value)
    emits('onChange', value)
}
const onClear = () => {
    emits('update:modelValue', '')
    emits('onChange', null)
}
</script>
<style scoped>
.dropdown-tree-list {
    display: flex;
    align-items: center;
    gap: 10px;
    color: var(--label-text-color);
}
.dropdown-tree-list_label {
    color: var(--label-text-color);
}
</style>
