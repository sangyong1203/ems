<template>
    <div
        class="double-date-picker"
        :style="{ width: props.width ?? '' }"
        :class="props.labelPosition === 'top' ? 'label-position-top' : 'label-position-left'"
    >
        <div v-if="props.label" class="double-date-picker_label" :style="{ width: props.labelWidth ?? '' }">
            {{ props.label }}
        </div>
        <div class="double-date-picker_content">
            <slot></slot>
            <div class="double-date-picker_content">
                <el-date-picker
                    v-model="startDate"
                    :type="dateType"
                    :value-format="valueFormat"
                    :format="dateFormat"
                    :placeholder="startPlaceholder ?? 'Start date'"
                    :style="{ flex: selectionWidth ? 'unset' : 1, width: selectionWidth }"
                    :disabled-date="disabledStartDate"
                    :disabled="disabled"
                    :clearable="props.clearable"
                />
                <span v-if="props.type !== 'week' && props.type !== 'hour'"> ~ </span>
                <el-date-picker
                    v-if="props.type !== 'week' && props.type !== 'hour'"
                    v-model="endDate"
                    :type="dateType"
                    :value-format="valueFormat"
                    :format="dateFormat"
                    :placeholder="endPlaceholder ?? 'End date'"
                    :style="{ flex: selectionWidth ? 'unset' : 1, width: selectionWidth }"
                    :disabled-date="disabledEndDate"
                    :disabled="disabled"
                    :clearable="props.clearable"
                />
            </div>
            <div class="week-range" v-if="props.type === 'week' && startDate">
                {{ weekDate }}
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { computed, ref, watch, type ComputedRef } from 'vue'
import dayjs from 'dayjs'
import { Notification } from '@/shared/composables/useFeedback'

export interface Props {
    label?: string | null
    labelWidth?: string | null
    width?: string | null
    selectionWidth?: string
    startDate: string | null
    endDate: string | null
    startPlaceholder?: string | null
    endPlaceholder?: string | null
    type?: 'year' | 'month' | 'week' | 'day' | 'hour' | null
    limit?: number
    disabled?: boolean
    clearable?: boolean
    labelPosition?: 'top' | 'left'
}
const props = defineProps<Props>()
const startDate: any = ref(props.startDate)
const endDate: any = ref(props.endDate)
const weekDate: any = computed(() => {
    return startDate.value + ' ~ ' + dayjs(startDate.value).add(6, 'day').format('YYYY-MM-DD')
})
const dateType: ComputedRef = computed(() => {
    let value = 'date'
    switch (props.type) {
        case 'day':
            value = 'date'
            break
        case 'week':
            value = 'week'
            break
        case 'month':
            value = 'month'
            break
        case 'year':
            value = 'year'
            break
        default:
            value = 'date'
    }
    console.log('value', value)
    return value
})
const valueFormat = computed(() => {
    let value = ''
    switch (props.type) {
        case 'day':
            value = 'YYYY-MM-DD'
            break
        case 'month':
            value = 'YYYY-MM'
            break
        case 'year':
            value = 'YYYY'
            break
        default:
            value = 'YYYY-MM-DD'
    }
    return value
})
const dateFormat = computed(() => {
    let value = ''
    switch (props.type) {
        case 'day':
            value = 'YYYY.MM.DD'
            break
        case 'month':
            value = 'YYYY.MM'
            break
        case 'year':
            value = 'YYYY'
            break
        default:
            value = 'YYYY.MM.DD'
    }
    return value
})
const emits = defineEmits(['update:startDate', 'update:endDate', 'getWeekDate'])

watch(
    () => props.startDate,
    newVal => {
        startDate.value = newVal
    },
)
watch(
    () => props.endDate,
    newVal => {
        endDate.value = newVal
    },
)

watch(startDate, () => {
    const start = dayjs(startDate.value)
    const end = dayjs(endDate.value)
    const difDay = end.diff(start, 'day')
    if (props.limit && difDay > props.limit) {
        Notification.warning(`기간은 최대 ${props.limit}일까지 지정할 수 있습니다.`)
    }
    emits('update:startDate', startDate.value)
})
watch(weekDate, () => {
    emits('getWeekDate', weekDate.value)
})
watch(endDate, () => {
    const start = dayjs(startDate.value)
    const end = dayjs(endDate.value)
    const difDay = end.diff(start, 'day')
    if (props.limit && difDay > props.limit) {
        Notification.warning(`기간은 최대 ${props.limit}일까지 지정할 수 있습니다.`)
    }
    emits('update:endDate', endDate.value)
})
watch(dateType, () => {
    startDate.value = startDate.value ? dayjs(startDate.value).format(valueFormat.value) : ''
    endDate.value = endDate.value ? dayjs(endDate.value).format(valueFormat.value) : ''
    emits('update:startDate', startDate.value)
    emits('update:endDate', endDate.value)
})

const disabledStartDate = (date: any) => {
    const start = new Date(date).getTime()
    const end = endDate.value ? new Date(endDate.value).getTime() : new Date().getTime()
    let result = false
    if (start > end) result = true
    return result
}
const disabledEndDate = (date: any) => {
    let result = false
    if (startDate.value) {
        const start = startDate.value ? new Date(startDate.value).getTime() : new Date().getTime()
        const endStr = dayjs(date).format('YYYY-MM-DD')
        const end = new Date(endStr).getTime()
        if (start > end) result = true
    }
    return result
}
</script>
<style scoped>
.double-date-picker {
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--text-color--primary);
}
.double-date-picker_label {
    color: var(--text-color--primary);
    white-space: nowrap;
    font-size: 18px;
    font-weight: 600;
    line-height: 20px;
}
.double-date-picker_content {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: nowrap;
    flex: 1;
    width: 100%;
}
.double-date-picker_content :deep(.el-date-editor) {
    width: 100%;
    height: 100%;
}
.double-date-picker_content :deep(.el-input__wrapper) {
    padding: 4px 20px;
    border-radius: 999px;
    background: var(--common-control-bg-color);
    box-shadow: 0 0 0 1px var(--common-control-border-color) inset;
}
.double-date-picker_content :deep(.el-input__inner) {
    height: 28px;
    font-size: 15px;
    color: var(--text-color--primary);
}
.double-date-picker_content :deep(.el-input__inner::placeholder) {
    color: var(--text-color--placeholder);
}
.double-date-picker_content :deep(.el-input__prefix),
.double-date-picker_content :deep(.el-input__suffix) {
    color: var(--text-color--secondary);
}
.week-range {
    border: none;
    border-radius: 999px;
    background-color: var(--common-control-bg-color);
    min-height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 4px 20px;
    font-size: 15px;
    color: var(--text-color--primary);
}
.label-position-top {
    flex-direction: column;
    align-items: flex-start;
}
</style>
