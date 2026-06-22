<template>
    <el-table
        ref="tableRef"
        class="grid-table no-border"
        :data="tableData"
        :height="tableHeight"
        :row-key="getRowKey"
        :empty-text="placeholder"
        :multiple="multiple"
        @selection-change="handleSelectionChange"
        @row-click="handleRowClick"
        @sort-change="handleSortChange"
    >
        <el-table-column
            v-if="hasSelection"
            type="selection"
            width="48"
            align="center"
            :selectable="() => !disabled"
        />
        <el-table-column
            v-for="column in columns"
            :key="column.name"
            :prop="column.name"
            :label="column.header"
            :width="column.width"
            :min-width="column.minWidth"
            :align="column.align ?? 'center'"
            :sortable="column.sortable ? 'custom' : false"
            show-overflow-tooltip
        >
            <template #default="{ row }">
                <el-select
                    v-if="isSelectColumn(column)"
                    v-model="row[column.name]"
                    :disabled="disabled"
                    @change="(value: any) => handleCellChange(row, column, value)"
                >
                    <el-option
                        v-for="item in getListItems(column)"
                        :key="String(item.value)"
                        :label="item.text"
                        :value="item.value"
                    />
                </el-select>
                <el-input
                    v-else-if="isTextColumn(column)"
                    v-model="row[column.name]"
                    :disabled="disabled"
                    @keyup.enter="handleCellChange(row, column, row[column.name])"
                    @blur="handleCellChange(row, column, row[column.name])"
                />
                <span v-else>{{ formatCell(row, column) }}</span>
            </template>
        </el-table-column>
    </el-table>
</template>

<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import { dateFormat } from '@/shared/utils'

type Align = 'left' | 'center' | 'right'
type ListItem = {
    text: string
    value: string | number | boolean
}
type GridColumn = {
    header: string
    name: string
    align?: Align
    width?: number | string
    minWidth?: number | string
    sortable?: boolean
    formatter?: string | ((value: any) => string)
    editor?:
        | 'text'
        | {
              type?: string
              options?: {
                  listItems?: ListItem[]
              }
          }
}

export interface Props {
    columns: GridColumn[]
    complexColumns?: any[]
    cell?: any
    language?: string
    placeholder?: string
    presetName?: 'default' | 'striped' | 'clean'
    width?: number
    headerAlign?: Align
    rowHeight?: number
    rowHeaders?: Array<string | { type?: string }>
    headerHeight?: number
    rowSize: number
    totalCount: number
    currentPage: number
    disabled?: boolean
    multiple?: boolean
    sortColumn?: string
    sortAscending?: boolean
}

const props = withDefaults(defineProps<Props>(), {
    multiple: true,
    placeholder: '',
})
const emits = defineEmits([
    'afterChange',
    'check',
    'checkAll',
    'uncheck',
    'uncheckAll',
    'onCheck',
    'click',
    'row-click',
    'afterSort',
    'beforeSort',
    'sort-change',
    'afterFilter',
    'dblclick',
])

const tableRef = ref()
const tableData = ref<any[]>([])
const tableHeight = ref('100%')
const checkedRows = ref<any[]>([])
let resizeObserver: ResizeObserver | null = null

const hasSelection = computed(() =>
    props.rowHeaders?.some(header => header === 'checkbox' || (typeof header === 'object' && header.type === 'checkbox')),
)

const getRowKey = (row: any) => row.rowKey ?? row.id ?? row.indexNum
const isTextColumn = (column: GridColumn) => column.editor === 'text'
const isSelectColumn = (column: GridColumn) => typeof column.editor === 'object' && column.editor?.type === 'select'
const getListItems = (column: GridColumn) => column.editor && typeof column.editor === 'object' ? column.editor.options?.listItems ?? [] : []

const formatCell = (row: any, column: GridColumn) => {
    const value = row[column.name]

    if (column.formatter === 'listItemText') {
        return getListItems(column).find(item => item.value === value)?.text ?? value ?? ''
    }
    if (typeof column.formatter === 'function') {
        return column.formatter(value)
    }
    return value ?? ''
}

const normalizeRows = (data: any[]) => {
    data.forEach((item: any) => {
        if (item.viewYn) item.viewYn = item.viewYn === 'Y' ? 'Visible' : 'Hidden'
        if (item.createDate) item.createDate = dateFormat(item.createDate, 'YYYY-MM-DD HH:mm:ss')
        if (item.updateDate) item.updateDate = dateFormat(item.updateDate, 'YYYY-MM-DD HH:mm:ss')
        if (item.stopDate) item.stopDate = dateFormat(item.stopDate, 'YYYY-MM-DD HH:mm:ss')
        if (item.completeDate) item.completeDate = dateFormat(item.completeDate, 'YYYY-MM-DD HH:mm:ss')
        if (item.installDate) item.installDate = dateFormat(item.installDate, 'YYYY-MM-DD HH:mm:ss')
        if (item.releaseDate) item.releaseDate = dateFormat(item.releaseDate, 'YYYY-MM-DD HH:mm:ss')
    })
}

const emitCheckedState = (nextRows: any[]) => {
    const prevRows = checkedRows.value
    const selectedSet = new Set(nextRows.map(getRowKey))
    const previousSet = new Set(prevRows.map(getRowKey))

    nextRows.forEach(row => {
        if (!previousSet.has(getRowKey(row))) emits('check', row, true)
    })
    prevRows.forEach(row => {
        if (!selectedSet.has(getRowKey(row))) emits('check', row, false)
    })

    if (nextRows.length === tableData.value.length && prevRows.length !== nextRows.length) {
        emits('checkAll', tableData.value, true)
    }
    if (nextRows.length === 0 && prevRows.length > 0) {
        emits('checkAll', [], false)
    }

    checkedRows.value = [...nextRows]
    emits('onCheck', checkedRows.value)
}

const handleSelectionChange = (rows: any[]) => {
    emitCheckedState(rows)
}

const handleRowClick = (row: any, column: any, event: MouseEvent) => {
    emits('row-click', row, event)
}

const handleSortChange = ({ prop, order }: { prop: string; order: string | null }) => {
    if (!prop) return
    const event = {
        columnName: prop,
        ascending: order === 'ascending',
        order,
    }
    emits('beforeSort', event)
    emits('sort-change', event)
    emits('afterSort', event)
}

const handleCellChange = (row: any, column: GridColumn, value: any) => {
    if (!row.id) return
    emits('afterChange', {
        id: row.id,
        columName: column.name.replace(/([A-Z])/g, '_$1').toLowerCase(),
        columValue: value,
    })
}

const createGrid = () => {
    refreshLayout()
}
const destroyGrid = () => {
    tableData.value = []
    checkedRows.value = []
}
const setTableData = (data: any[]) => {
    normalizeRows(data)
    checkedRows.value = []
    tableData.value = data.map((item: any, index: number) => ({
        ...item,
        rowKey: item.rowKey ?? item.id ?? index,
        indexNum: (props.currentPage - 1) * props.rowSize + index + 1,
    }))
}
const getData = () => tableData.value
const appendRow = (row: any) => {
    tableData.value.push({
        ...row,
        rowKey: row.rowKey ?? new Date().getTime(),
        indexNum: row.indexNum ?? tableData.value.length + 1,
    })
}
const clear = () => {
    tableData.value = []
    checkedRows.value = []
}
const resetData = (data: any[]) => {
    setTableData(data)
}
const removeRow = (rowKey: any) => {
    tableData.value = tableData.value.filter(row => getRowKey(row) !== rowKey)
    checkedRows.value = checkedRows.value.filter(row => getRowKey(row) !== rowKey)
}
const refreshLayout = () => {
    nextTick(() => tableRef.value?.doLayout?.())
}
const setBodyHeight = () => {
    refreshLayout()
}
const getGridInstance = () => ({
    getData,
    appendRow,
    clear,
    resetData,
    removeRow,
    refreshLayout,
    setBodyHeight,
    destroy: destroyGrid,
})
const initCheckedRows = () => {
    checkedRows.value = []
    tableRef.value?.clearSelection?.()
}
const deleteRow = (rowKey: any) => {
    removeRow(rowKey)
}

onMounted(() => {
    createGrid()
    if (tableRef.value?.$el) {
        resizeObserver = new ResizeObserver(refreshLayout)
        resizeObserver.observe(tableRef.value.$el)
    }
})
onBeforeUnmount(() => {
    resizeObserver?.disconnect()
    destroyGrid()
})

defineExpose({ createGrid, destroyGrid, setTableData, getGridInstance, initCheckedRows, deleteRow })
</script>

<style lang="scss" scoped>
.grid-table {
    width: 100%;
    flex: 1;
}

.grid-table :deep(.el-input__wrapper),
.grid-table :deep(.el-select__wrapper) {
    box-shadow: none;
    background: transparent;
}
</style>
