<template>
    <div class="pagination">
        <div class="pagination__controls">
            <DropdownList
                class="pagination__sizes"
                width="120px"
                :model-value="rowSize"
                :list="pageSizeOptions"
                option-label="label"
                option-value="value"
                :clearable="false"
                @update:modelValue="handleSizeChange"
            />
            <button class="pagination__edge-button" type="button" :disabled="page <= 1" @click="moveToFirstPage">
                <IconDoubleArrow class="pagination__edge-icon" />
            </button>
            <el-pagination
                :pager-count="pagerCount"
                :current-page="page"
                :page-size="rowSize"
                :background="true"
                :total="totalRow"
                layout="prev, pager, next"
                @current-change="handleCurrentChange"
            />
            <button
                class="pagination__edge-button"
                type="button"
                :disabled="page >= totalPages"
                @click="moveToLastPage"
            >
                <IconDoubleArrow class="pagination__edge-icon is-last" />
            </button>
        </div>
        <slot></slot>
    </div>
</template>

<script setup lang="ts">
import { toRefs, ref, onMounted, onUnmounted, computed } from 'vue'
import { ElPagination } from 'element-plus'
import DropdownList from './DropdownList.vue'
import IconDoubleArrow from '@/assets/icons/IconDoubleArrow.svg'

export interface Props {
    totalRow: number
    page: number
    rowSize: number
}

const props = defineProps<Props>()
const { totalRow, page, rowSize } = toRefs(props)

const options = [10, 15, 20, 50]
const pageSizeOptions = options.map(option => ({ label: `${option}/page`, value: option }))
const emit = defineEmits(['current-change', 'size-change'])
const pagerCount = ref(window.innerWidth < 768 ? 4 : 7)
const totalPages = computed(() => Math.max(1, Math.ceil(totalRow.value / rowSize.value)))

const handleResize = () => {
    pagerCount.value = window.innerWidth < 768 ? 4 : 7
}

onMounted(() => {
    window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
})

const handleSizeChange = (val: number) => {
    emit('size-change', val)
}

const handleCurrentChange = (val: number) => {
    emit('current-change', val)
}

const moveToFirstPage = () => {
    if (page.value > 1) {
        emit('current-change', 1)
    }
}

const moveToLastPage = () => {
    if (page.value < totalPages.value) {
        emit('current-change', totalPages.value)
    }
}
</script>

<style lang="scss" scoped>
.pagination {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 16px;
    margin-bottom: 16px;
    width: 100%;
    gap: 16px;
}

.pagination__controls {
    display: flex;
    align-items: center;
    justify-content: center;
}

.pagination__edge-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 32px;
    height: 32px;
    padding: 0 8px;
    border: none;
    background: none;
    color: var(--text-color--primary);
    font-size: 14px;
    line-height: 1;
    cursor: pointer;
}

.pagination__edge-button:disabled {
    color: var(--el-disabled-text-color);
    cursor: not-allowed;
}

.pagination__edge-icon {
    width: 20px;
    height: 20px;
}

.pagination__edge-icon.is-last {
    transform: rotate(180deg);
}

.pagination__edge-button:disabled .pagination__edge-icon {
    opacity: 0.5;
}

.pagination__sizes {
    width: 120px;
    margin-right: 8px;
}

:deep(.el-pager li) {
    --el-pagination-button-bg-color: none;
}

:deep(.el-pager li.is-active) {
    font-weight: 700 !important;
    cursor: pointer;
}

:deep(.el-pagination.is-background .btn-prev),
:deep(.el-pagination.is-background .btn-next) {
    --el-pagination-button-bg-color: none;
}

:deep(.el-pagination.is-background .btn-prev:disabled),
:deep(.el-pagination.is-background .btn-next:disabled) {
    --el-disabled-bg-color: none;
}

:deep(.pagination__sizes .el-select__wrapper) {
    background: var(--common-control-bg-color);
    box-shadow: 0 0 0 1px var(--common-control-border-color) inset;
    min-height: 36px;
}

@media (max-width: 768px) {
    .pagination {
        gap: 8px;
    }

    .pagination__controls {
        gap: 8px;
    }

    .pagination__sizes {
        display: none;
    }

    :deep(.el-pagination) {
        width: 100%;
        display: flex;
        justify-content: space-around;
    }
}
</style>
