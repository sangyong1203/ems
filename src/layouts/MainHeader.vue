<template>
    <el-row class="main-header">
        <el-col :span="14">
            <div class="header-left">
                <AppIcon v-if="icon" :name="icon" class="menu-icon"></AppIcon>
                <span class="title">
                    <span class="title-text">{{ title }}</span>
                </span>
            </div>
        </el-col>
        <el-col :span="10">
            <div class="header-right">
                <div class="header-user">
                    <el-icon class="header-user-icon"><User /></el-icon>
                    <span class="header-user-name">{{ userName }}</span>
                </div>
                <el-button type="primary" circle class="logout" @click="emit('logout')">
                    <el-icon><SwitchButton /></el-icon>
                </el-button>
            </div>
        </el-col>
    </el-row>
</template>

<script lang="ts" setup>
import { SwitchButton, User } from '@element-plus/icons-vue'

withDefaults(
    defineProps<{
        title?: string
        icon?: string
        userName?: string
    }>(),
    {
        title: '',
        icon: '',
        userName: 'User',
    },
)

const emit = defineEmits<{
    logout: []
}>()
</script>

<style scoped lang="scss">
.main-header,
.main-header :deep(.el-col),
.header-left,
.header-right {
    height: 100%;
}

.header-left {
    display: flex;
    align-items: center;
}

.header-left .title {
    color: #fff;
    text-decoration-line: none;
    text-decoration: none;
    display: flex;
    align-items: center;
}

.header-left .title-text {
    font-size: 20px;
    line-height: 24px;
    white-space: nowrap;
    font-weight: 700;
    font-family: 'Pretendard', sans-serif;
    letter-spacing: 0;
    color: var(--header-title-text-color);
}

.header-right {
    text-align: right;
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 4px;
}

.header-user {
    min-width: 0;
    max-width: 320px;
    height: 36px;
    padding: 0 14px;
    display: flex;
    align-items: center;
    gap: 8px;
    border: 1px solid var(--border-color);
    border-radius: 999px;
    background: var(--surface-control-color);
    color: var(--text-color--primary);
}

.header-user-icon {
    flex: 0 0 auto;
    width: 17px;
    height: 17px;
    color: var(--accent-color);
}

.header-user-icon svg {
    width: 17px;
    height: 17px;
}

.header-user-name {
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-size: 14px;
    font-weight: 500;
    letter-spacing: 0;
}

.logout {
    border: 1px solid var(--border-color);
    background-color: var(--surface-control-color);
    color: var(--text-color--white);
}

.logout:hover {
    background-color: var(--layout-menu-active-bg-color);
    border-color: var(--accent-color);
    color: var(--accent-color);
    cursor: pointer;
}

.logout .el-icon {
    width: 18px;
    height: 18px;
    transform: rotate(90deg);
}

.logout .el-icon svg {
    width: 18px;
    height: 18px;
}
.menu-icon {
    color: var(--primary-color) !important;
    width: 28px;
    height: 28px;
    margin-right: 4px;
}
</style>
