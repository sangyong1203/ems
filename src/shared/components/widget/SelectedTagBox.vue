<template>
    <div class="selected-tag-box" :class="[`selected-tag-box--${variant}`, { 'selected-tag-box--inherited': inherited }]">
        <div class="selected-tag-box__items-wrap">
            <div class="selected-tag-box__items">
                <el-tag
                    v-for="(item, index) in items"
                    :key="item.key"
                    :closable="closable"
                    :disable-transitions="true"
                    @close="handleRemoveItem(index)"
                >
                    <el-icon v-if="variant === 'restriction'" class="selected-tag-box__item-icon"><Lock /></el-icon>
                    {{ item.label }}
                </el-tag>
            </div>
        </div>

        <div class="selected-tag-box__actions">
            <el-button
                v-if="showEdit"
                type="primary"
                :disabled="actionsDisabled || editDisabled"
                class="selected-tag-box__action-btn is-solid"
                @click="handleEdit"
            >
                Edit
            </el-button>
            <el-button
                v-if="showClearAll"
                :disabled="actionsDisabled || items.length === 0"
                class="selected-tag-box__action-btn is-outline"
                @click="handleClearAll"
            >
                Clear All
            </el-button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { Lock } from '@element-plus/icons-vue'

type SelectedTagItem = {
    key: string | number
    label: string
}

withDefaults(
    defineProps<{
        items: SelectedTagItem[]
        closable?: boolean
        actionsDisabled?: boolean
        showEdit?: boolean
        editDisabled?: boolean
        showClearAll?: boolean
        variant?: 'default' | 'restriction'
        inherited?: boolean
    }>(),
    {
        closable: false,
        actionsDisabled: false,
        showEdit: true,
        editDisabled: false,
        showClearAll: true,
        variant: 'default',
        inherited: false,
    },
)

const emit = defineEmits<{
    'remove-item': [index: number]
    edit: []
    'clear-all': []
}>()

const handleRemoveItem = (index: number) => {
    emit('remove-item', index)
}

const handleEdit = () => {
    emit('edit')
}

const handleClearAll = () => {
    emit('clear-all')
}
</script>

<style scoped lang="scss">
.selected-tag-box {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 16px;
}

.selected-tag-box--inherited {
    background: var(--surface-muted-color);
}

.selected-tag-box__items-wrap {
    display: flex;
    align-items: flex-start;
    flex: 1;
    min-width: 0;
}

.selected-tag-box__items {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    flex: 1;
    min-width: 0;
    max-height: 72px;
    overflow-y: scroll;
    overflow-x: hidden;
    scrollbar-gutter: stable;
    padding-right: 4px;
}

.selected-tag-box__items::-webkit-scrollbar-thumb {
    background-color: var(--overlay-scrollbar-thumb-color);
}

.selected-tag-box__items:hover::-webkit-scrollbar-thumb {
    background-color: var(--overlay-scrollbar-thumb-color);
}

.selected-tag-box :deep(.el-tag) {
    display: inline-flex;
    align-items: center;
    border-radius: 4px;
    background: var(--common-control-bg-color);
    color: var(--text-color--primary);
    border: 1px solid var(--common-control-border-color);
    height: 32px;
    padding: 0 12px;
    font-size: 15px;
}

.selected-tag-box :deep(.el-tag .el-tag__close) {
    width: 18px;
    height: 18px;
    margin-left: 8px;
    border-radius: 999px;
    background: var(--surface-elevated-color);
    color: var(--text-color--primary);
    font-size: 12px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.selected-tag-box :deep(.el-tag .el-tag__close:hover) {
    background: var(--primary-color);
    color: var(--text-color--white);
}

.selected-tag-box__item-icon {
    margin-right: 4px;
    font-size: 16px;
}

.selected-tag-box--restriction :deep(.el-tag) {
    border: 1px solid var(--secondary-color);
    background: rgba(21, 224, 183, 0.12);
    color: var(--secondary-color);
    font-weight: 700;
}

.selected-tag-box--restriction :deep(.el-tag .el-tag__close) {
    background: var(--surface-elevated-color);
}

.selected-tag-box__actions {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.selected-tag-box__actions :deep(.el-button) {
    width: 92px;
    height: 36px;
    margin-left: 0;
    border-radius: 999px;
    font-size: 15px;
    font-weight: 600;
}

.selected-tag-box__action-btn.is-solid {
    color: var(--button-primary-text-color);
    border: 1px solid var(--primary-color);
}

.selected-tag-box__actions :deep(.el-button.selected-tag-box__action-btn.is-solid.is-disabled),
.selected-tag-box__actions :deep(.el-button.selected-tag-box__action-btn.is-solid.is-disabled:hover) {
    --el-button-disabled-bg-color: rgba(231, 109, 255, 0.2);
    border: none;
}

.selected-tag-box__action-btn.is-outline {
    color: var(--primary-color);
    border: 1px solid var(--primary-color);
}

.selected-tag-box__actions :deep(.el-button.selected-tag-box__action-btn.is-outline.is-disabled),
.selected-tag-box__actions :deep(.el-button.selected-tag-box__action-btn.is-outline.is-disabled:hover) {
    --el-button-disabled-bg-color: rgba(231, 109, 255, 0.2);
    color: var(--text-color--muted);
    border: none;
}
:deep(.el-tag__content) {
    display: flex;
}

@media (max-width: 980px) {
    .selected-tag-box {
        flex-direction: column;
        align-items: stretch;
    }

    .selected-tag-box__actions {
        flex-direction: row;
    }

    .selected-tag-box__actions :deep(.el-button) {
        width: auto;
    }
}
</style>
