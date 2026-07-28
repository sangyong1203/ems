<template>
    <div class="search-box" @keyup.enter="onSearch()" :style="{ padding: padding }">
        <div class="search-box-content">
            <div class="upper-row" :style="{ gap: gap }">
                <slot></slot>
            </div>
            <div class="text-right">
                <el-button v-if="!hideSearchButton" :size="size" type="primary" class="GET" @click="onSearch()">{{
                    'Search'
                }}</el-button>
                <slot name="extra-button"></slot>
            </div>
        </div>
        <el-row class="extra-row" v-show="extra">
            <slot name="extra"> </slot>
        </el-row>
    </div>
</template>

<script lang="ts" setup>
export interface Props {
    extra?: boolean
    size?: '' | 'default' | 'small' | 'large'
    gap?: string
    padding?: string
    hideSearchButton?: boolean
    onSearch: (params?: any) => void
}
const { onSearch, extra, size, padding, gap, hideSearchButton = false } = defineProps<Props>()
</script>

<style scoped lang="scss">
.search-box {
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    margin: 12px;
}
.search-box {
    background-color: var(--search-box-bg-color) !important;
    box-shadow: 0px 0px 12px var(--shadow-color);
    // border: 1px solid var(--common-component-border-color);
}
.search-box-content {
    justify-content: space-between;
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 8px;
    padding: 20px 24px;
    min-height: 76px;
}
.upper-row {
    flex: 1;
    min-width: 0;
    margin: 0px;
    gap: 12px 24px;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
}
.extra-row {
    gap: 12px 24px;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    background-color: var(--surface-muted-color);
    padding: 20px 24px;
    min-height: 76px;
    border-bottom-right-radius: 8px;
    border-bottom-left-radius: 8px;
    :deep(.dropdown-list .el-select__wrapper) {
        background-color: var(--common-control-bg-color) !important;
    }
}
.search-box .collaps {
    height: 32px;
    overflow: hidden;
}
.search-box .open {
    height: 100%;
}
.search-box .el-form-item--small.el-form-item {
    margin-bottom: 0px;
}
.search-box .search-btn {
    display: flex;
    justify-content: flex-end;
}
.search-box .el-form-item {
    margin-bottom: 2px;
}
.search-box .el-range-editor.el-input__wrapper {
    padding: 0px 0px 0px 5px;
}
.search-box .el-input-group__prepend {
    background-color: var(--surface-elevated-color);
    border: none;
    padding: 0 10px;
    box-shadow: none;
}
.search-box .text-right {
    display: flex;
    flex-shrink: 0;
    align-items: center;
}

@media (max-width: 768px) {
    .search-box-content {
        align-items: stretch;
        flex-direction: column;
    }

    .upper-row {
        align-items: stretch;
        flex-direction: column;
    }

    :deep(.search-text),
    :deep(.dropdown-list) {
        width: 100% !important;
    }

    .search-box .text-right {
        justify-content: flex-end;
    }
}
</style>
