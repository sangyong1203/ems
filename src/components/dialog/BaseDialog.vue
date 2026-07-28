<template>
    <el-dialog
        :model-value="modelValue"
        :width="width"
        style="overflow: hidden"
        :style="{ overflow: 'hidden', height: height, maxHeight: maxHeight ?? '95vh' }"
        :before-close="handleClose"
        :center="footerCenter"
        :close-on-click-modal="false"
        :draggable="false"
        :align-center="true"
        :destroy-on-close="true"
        :show-close="false"
        :close-on-press-escape="false"
        :header-class="hideHeader ? 'hide-header' : ''"
    >
        <template #header>
            <div class="dialog-header">
                <div class="dialog-header-content">
                    <slot name="title"></slot>
                    <span class="dialog-header-title">{{ title }}</span>
                    <span class="dialog-description" v-show="description"> {{ '* ' + description }}</span>
                </div>
                <el-icon style="cursor: pointer" color="var(--text-color--primary)" @click="onClose"><Close /></el-icon>
            </div>
        </template>

        <slot />

        <template #footer>
            <div class="dialog-footer">
                <div class="delete-btn" v-if="!isEdit">
                    <el-button v-if="buttonTypes?.includes('Delete')" @click="onDelete">Delete</el-button>
                </div>
                <el-button v-if="buttonTypes?.includes('Close')" @click="onClose">Close</el-button>
                <el-button v-if="buttonTypes?.includes('Cancel')" @click="onCancel">Cancel</el-button>
                <el-button
                    type="primary"
                    v-if="buttonTypes?.includes('Save') && (isEdit || !buttonTypes?.includes('Edit'))"
                    @click="onSave"
                    >Save</el-button
                >
                <el-button type="primary" v-if="buttonTypes?.includes('Edit') && !isEdit" @click="onEdit"
                    >Edit</el-button
                >
                <el-button type="primary" v-if="buttonTypes?.includes('Confirm')" @click="onConfirm">Confirm</el-button>
                <el-button type="primary" v-if="buttonTypes?.includes('Select')" @click="onSelect">Select</el-button>
                <el-button type="primary" v-if="buttonTypes?.includes('Add')" @click="onAdd">Add</el-button>
                <el-button type="primary" v-if="buttonTypes?.includes('Reset')" @click="onReset">Reset</el-button>
                <el-button type="primary" v-if="buttonTypes?.includes('Review')" @click="onSave">Review</el-button>
                <el-button type="primary" v-if="buttonTypes?.includes('Reject')" @click="onReject">Reject</el-button>
                <el-button type="primary" v-if="buttonTypes?.includes('Approve')" @click="onApprove">Approve</el-button>
                <slot name="footer"></slot>
            </div>
        </template>
    </el-dialog>
</template>

<script lang="ts" setup>
import { toRefs } from 'vue'

export interface Props {
    title: string
    description?: string
    maxHeight?: string
    height?: string
    width?: string | number
    buttonTypes?: ButtonType[]
    footerCenter?: boolean
    modelValue: boolean
    isEdit?: boolean
    hideHeader?: boolean
}
type ButtonType =
    | 'Save'
    | 'Cancel'
    | 'Edit'
    | 'Delete'
    | 'Confirm'
    | 'Close'
    | 'Select'
    | 'Add'
    | 'Reset'
    | 'Review'
    | 'Reject'
    | 'Approve'

const props = defineProps<Props>()
const { title, description, maxHeight, width, height, buttonTypes, modelValue, isEdit, hideHeader } = toRefs(props)
const emits = defineEmits([
    'update:modelValue',
    'onSave',
    'onEdit',
    'onDelete',
    'onCancel',
    'onConfirm',
    'onSelect',
    'onReset',
    'onClose',
    'onAdd',
    'onReject',
    'onApprove',
])

const onSave = () => {
    emits('onSave')
}
const onEdit = () => {
    emits('onEdit')
}
const onConfirm = () => {
    emits('onConfirm')
}
const onSelect = () => {
    emits('onSelect')
    onClose()
}
const onCancel = () => {
    emits('onCancel')
    onClose()
}
const onDelete = () => {
    emits('onDelete')
}
const onClose = () => {
    emits('update:modelValue', false)
    emits('onClose')
}
const handleClose = (done: () => void) => {
    done()
}
const onReset = () => {
    emits('onReset')
}
const onAdd = () => {
    emits('onAdd')
}
const onReject = () => {
    emits('onReject')
}
const onApprove = () => {
    emits('onApprove')
}
</script>
<style lang="scss" scoped>
.dialog-header-title {
    font-size: 24px;
    line-height: 24px;
    font-weight: 600;
    color: var(--text-color--primary);
}
.dialog-description {
    font-size: 12px;
    margin-left: 16px;
    margin-bottom: 2px;
    color: var(--text-color--muted);
}
.dialog-footer {
    display: flex;
    justify-content: center;
    position: relative;
}
.delete-btn {
    position: absolute;
    left: 20px;
}
.dialog-header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    :deep(.el-icon) {
        width: 28px;
        height: 28px;
        svg {
            width: 28px;
            height: 28px;
        }
    }
}
.dialog-footer :deep(.el-button.el-button--primary) {
    background: var(--primary-color);
    border-color: var(--primary-color);
    color: var(--button-primary-text-color);
}
.dialog-footer :deep(.el-button:not(.el-button--primary)) {
    background: var(--common-control-bg-color);
    border-color: var(--common-control-border-color);
    color: var(--text-color--secondary);
}
.dialog-footer :deep(.el-button) {
    border-radius: 999px;
    min-width: 90px;
    height: 46px;
    font-size: 15px;
}
</style>
