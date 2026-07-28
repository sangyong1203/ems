<template>
    <div class="operation-box" :class="{ topLine: topLine }">
        <el-divider class="top-line" v-if="topLine"></el-divider>
        <div class="operation-box-content">
            <el-row style="width: 100%; height: 100%">
                <div class="operation-box-left" v-if="!topLine">
                    <div v-if="title !== undefined" class="operation-box-title">{{ title }}</div>
                    <div v-if="total !== undefined" class="operation-box-total">
                        <span>{{ total }} &nbsp;</span>{{ unit }}
                    </div>
                    <slot name="left"></slot>
                </div>
                <div class="operation-box-right" :class="topLine ? 'align-center' : 'align-right'">
                    <slot></slot>
                </div>
            </el-row>
        </div>
    </div>
</template>

<script lang="ts" setup>
export interface Props {
    total?: number | string
    title?: string
    topLine?: boolean
    unit?: string
}

const { total, title, topLine, unit } = defineProps<Props>()
</script>

<style lang="scss" scoped>
.operation-box {
}

.operation-box-content {
    padding: 0px 0 8px 0;
    display: flex;
    align-items: center;
    height: 36px;
}
:deep(.el-button) {
    height: 28px !important;
    font-size: 12px;
}
:deep(.dropdown-list) {
    .el-select__wrapper {
        min-height: 28px !important;
    }
    .el-select__selected-item {
        font-size: 14px;
    }
    .dropdown-list_label {
        font-size: 14px;
    }
}
.operation-box-left {
    flex: 1;
    display: flex;
    align-items: flex-end;
    flex-wrap: wrap;
    margin-bottom: 8px;
}
.operation-box-title {
    margin-right: 2px;
    white-space: nowrap;
    font-size: 14px;
    color: var(--text-color--primary);
}
.operation-box-right {
    display: flex;
    flex: 1;
}
.top-line {
    margin: 12px 0 0 0;
}

.operation-box .el-form-item--small.el-form-item {
    margin-bottom: 0px;
}
.operation-box .operation-btn {
    display: flex;
    justify-content: flex-end;
}
.operation-box .el-button {
    height: 34px;
    align-self: center;
}
.operation-box .el-form-item {
    margin-bottom: 2px;
}
.operation-box .el-range-editor.el-input__wrapper {
    padding: 0px 0px 0px 5px;
}
.operation-box .el-input-group__prepend {
    background-color: var(--surface-elevated-color);
    border: none;
    padding: 0 10px;
    box-shadow: none;
}
.text-right {
    display: flex;
    justify-content: flex-end;
}

.operation-box-total {
    display: flex;
    align-items: flex-end;
    font-size: 14px;
    color: var(--secondary-color);
}
.operation-box-total span {
    display: inline-block;
    text-align: right;
    margin-left: 8px;
    display: flex;
    align-items: flex-end;
}
.el-col {
    display: flex;
    align-items: center;
}
.align-center {
    justify-content: center;
}
.align-right {
    justify-content: flex-end;
    height: 100%;
}
@media (max-width: 768px) {
    .operation-box {
        .operation-box-total {
            display: none;
        }
        .operation-box-right {
            flex-wrap: wrap;
            gap: 4px;
            :deep(.el-button) {
                margin-left: 0;
            }
        }
    }
    .topLine {
        .operation-box-right {
            justify-content: center;
            :deep(.el-button) {
                flex: 1;
            }
        }
    }
}
</style>
