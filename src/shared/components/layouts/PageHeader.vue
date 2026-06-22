<template>
    <el-page-header class="page-header" :class="hideIcon ? 'hide-icon' : nav.length > 2 ? '' : 'hide-icon'">
        <template #icon>
            <el-icon @click="navStore.backTo()"><ArrowLeft /></el-icon>
        </template>
        <template #title>
            <span class="back-text">{{ title }}</span>
        </template>
        <template #content>
            <span class="description">{{ description }}</span>
        </template>
        <template #extra> </template>
    </el-page-header>
</template>
<script lang="ts" setup>
import { useNavStore } from '@/stores/nav.store'
import { computed } from 'vue'

export interface Props {
    title: string
    description?: string
    hideIcon?: boolean
}
const { title, description, hideIcon } = defineProps<Props>()
const navStore = useNavStore()
const nav = computed(() => {
    return navStore.getNav() ?? []
})
</script>
<style lang="scss" scoped>
.page-header {
    padding: 8px 32px;
    min-height: 44px;
    box-shadow: var(--panel-shadow);
    margin-bottom: 12px;
    border-radius: 8px;
    background-color: var(--common-component-bg-color);
    border: 1px solid var(--common-component-border-color);
    color: var(--text-color--primary);
    display: flex;
    position: relative;
}

.back-text {
    font-size: 22px;
    cursor: default;
    white-space: nowrap;
}
.description {
    height: 24px;
    font-size: 22px;
    display: inline-block;
    font-weight: bold;
}
.disabled-link > :deep(.el-breadcrumb__inner) {
    cursor: not-allowed;
}
:deep(.el-page-header__left .el-divider--vertical) {
    margin: 0 12px !important;
}
:deep(.el-page-header__content) {
    font-size: 20px;
}
:deep(.el-page-header__header) {
    line-height: unset;
    flex: 1;
}
:deep(.el-page-header__extra) {
    padding-top: 2px;
}
:deep(.el-page-header__left) {
    margin-right: 8px;
}
.hide-icon :deep(.el-page-header__icon) {
    display: none;
}
.custom-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    /* padding: 16px 20px 0px 20px; */
}
.loading {
    background-color: transparent;
    position: absolute;
    left: 0;
    top: 14px;
    font-size: 24px;
    margin-left: 0px;
    border: none;
    color: var(--text-color--muted);
}

@media (max-width: 768px) {
    .page-header {
        margin-right: 8px;
        padding-left: 16px;
    }
}
</style>
