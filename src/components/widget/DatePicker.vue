<template>
    <div class="date-picker" :class="labelPosition === 'top' ? 'label-position-top' : 'label-position-left'" :style="{ width }">
        <div
            v-if="label"
            class="date-picker__label"
            :style="{ width: labelWidth ?? '', fontWeight: fontWeight ?? '', fontSize: fontSize ?? '' }"
        >
            {{ label }}
        </div>
        <div class="date-picker__content">
            <DropdownList
                v-model="selectedMode"
                :width="modeWidth"
                :list="modeOptions"
                option-label="label"
                option-value="value"
                :clearable="false"
                @on-change="changeMode"
            />
            <el-date-picker
                v-if="selectedMode === 'DAILY'"
                v-model="selectedDate"
                class="date-picker__date"
                type="date"
                value-format="YYYY-MM-DD"
                :placeholder="datePlaceholder"
                :style="{ width: dateWidth }"
                @change="changeDate"
            />
            <el-date-picker
                v-else
                v-model="selectedRange"
                class="date-picker__range"
                type="daterange"
                value-format="YYYY-MM-DD"
                :start-placeholder="startPlaceholder"
                :end-placeholder="endPlaceholder"
                :style="{ width: rangeWidth }"
                @change="changeRange"
            />
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import DropdownList from './DropdownList.vue'

export type DatePickerMode = 'DAILY' | 'RANGE'
export type DatePickerRange = [string, string] | null
export type DatePickerChangeSource = 'mode' | 'date' | 'range'

const props = withDefaults(
    defineProps<{
        mode: DatePickerMode
        date: string
        range: DatePickerRange
        label?: string | null
        labelWidth?: string
        width?: string
        fontWeight?: string
        fontSize?: string
        labelPosition?: 'top' | 'left'
        modeWidth?: string
        dateWidth?: string
        rangeWidth?: string
        datePlaceholder?: string
        startPlaceholder?: string
        endPlaceholder?: string
        modeOptions?: { label: string; value: DatePickerMode }[]
    }>(),
    {
        label: null,
        labelPosition: 'left',
        modeWidth: '110px',
        dateWidth: '170px',
        rangeWidth: '300px',
        datePlaceholder: '리포트 날짜',
        startPlaceholder: '시작일',
        endPlaceholder: '종료일',
        modeOptions: () => [
            { label: '일일', value: 'DAILY' },
            { label: '기간', value: 'RANGE' },
        ],
    },
)

const emit = defineEmits<{
    'update:mode': [value: DatePickerMode]
    'update:date': [value: string]
    'update:range': [value: DatePickerRange]
    change: [source: DatePickerChangeSource]
}>()

const selectedMode = ref<DatePickerMode>(props.mode)
const selectedDate = ref(props.date)
const selectedRange = ref<DatePickerRange>(props.range)

const changeMode = () => {
    emit('update:mode', selectedMode.value)
    emit('change', 'mode')
}

const changeDate = () => {
    emit('update:date', selectedDate.value || '')
    emit('change', 'date')
}

const changeRange = () => {
    emit('update:range', selectedRange.value)
    emit('change', 'range')
}

watch(
    () => props.mode,
    value => {
        selectedMode.value = value
    },
)

watch(
    () => props.date,
    value => {
        selectedDate.value = value
    },
)

watch(
    () => props.range,
    value => {
        selectedRange.value = value
    },
)
</script>

<style scoped>
.date-picker {
    display: flex;
    align-items: center;
    gap: 16px;
    color: var(--text-color--primary);
}

.date-picker__label {
    color: var(--text-color--primary);
    white-space: nowrap;
    font-size: 18px;
    font-weight: 600;
    line-height: 20px;
}

.date-picker__content {
    display: flex;
    align-items: center;
    gap: 10px;
    min-width: 0;
}

.label-position-top {
    flex-direction: column;
    align-items: flex-start;
}
</style>
