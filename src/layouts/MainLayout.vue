<template>
    <el-container class="layout-shell">
        <aside class="left-wrapper" :class="collapsed ? 'is-collapse' : 'is-expand'">
            <slot name="sidebar"></slot>
        </aside>
        <el-container class="right-wrapper">
            <el-header>
                <slot name="header"></slot>
            </el-header>
            <el-main>
                <div class="contents-wrapper">
                    <div class="contents">
                        <slot></slot>
                    </div>
                </div>
            </el-main>
        </el-container>
    </el-container>
</template>

<script lang="ts" setup>
withDefaults(
    defineProps<{
        collapsed?: boolean
    }>(),
    {
        collapsed: false,
    },
)
</script>

<style scoped lang="scss">
.layout-shell {
    height: 100%;
    display: flex;
    flex-direction: row;
    background: radial-gradient(circle at 78% 12%, rgba(231, 109, 255, 0.16), transparent 30%),
        radial-gradient(circle at 18% 84%, rgba(21, 224, 183, 0.08), transparent 34%),
        linear-gradient(135deg, #0a0d17 0%, #111421 42%, #090b12 100%);
    overflow: hidden;
}

.left-wrapper {
    position: relative;
    z-index: 2;
    display: flex;
    flex-direction: column;
    height: 100%;
    background: var(--layout-sidebar-bg-color);
    transition: width 400ms ease;
    overflow: hidden;
}

.left-wrapper.is-expand {
    width: 320px;
}

.left-wrapper.is-collapse {
    width: 60px;
}

.right-wrapper {
    min-width: 0;
    height: 100%;
    display: flex;
    flex: 1;
    flex-direction: column;
}

.el-header {
    height: 60px;
    width: 100%;
    align-items: center;
    padding-left: 32px;
    padding-right: 28px;
    background: var(--layout-header-bg-color);
    border-bottom: none;
    box-shadow: var(--layout-header-shadow);
    backdrop-filter: none;
}

.el-main {
    --el-main-padding: 0px;
    color: var(--text-color--primary);
    overflow: hidden;
}

.contents-wrapper {
    position: relative;
    display: flex;
    flex-direction: row;
    height: 100%;
    background: transparent;
}

.contents-wrapper .contents {
    position: relative;
    z-index: 1;
    padding: 0px 10px 16px 16px;
    width: 100%;
    display: flex;
    flex-direction: column;
    scrollbar-gutter: stable;
    min-height: 800px;
    overflow: auto;
}

.contents-wrapper .contents::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

.contents-wrapper .contents::-webkit-scrollbar-thumb:hover,
.contents-wrapper .contents::-webkit-scrollbar-track:hover,
.contents-wrapper .contents::-webkit-scrollbar-corner:hover {
    cursor: pointer;
}
</style>
