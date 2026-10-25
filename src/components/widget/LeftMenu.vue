<template>
    <div class="menu-bar" :class="[isCollapsed ? 'collapse' : 'not-collapse', { 'is-mobile': mobile }]" ref="leftWrapperRef">
        <button v-if="hasOverflow" type="button" class="menu-scroll-button" aria-label="메뉴 위로 스크롤" :disabled="!canScrollUp" @click="scrollMenu(-1)">
            <el-icon><ArrowUp /></el-icon>
        </button>
        <div ref="menuViewportRef" class="menu-scroll-viewport" @scroll="updateScrollState">
        <el-menu
            :default-active="defaultMenu"
            mode="vertical"
            class="left-menu"
            :collapse="isCollapsed"
            :collapse-transition="false"
            :unique-opened="true"
            :router="true"
            @select="handleSelect"
            @click.stop="onClickMenu"
        >
            <template v-for="(item, idx) in menu" :key="idx">
                <template v-if="item.useYn === 'Y'">
                    <el-menu-item v-if="item.children.length === 0" :index="item.path">
                        <span class="menu-icon-wrap">
                            <AppIcon :name="item.icon" class="menu-icon"></AppIcon>
                        </span>
                        <template #title>
                            <span class="menu-title">{{ item.title }}</span>
                        </template>
                    </el-menu-item>

                    <el-sub-menu
                        v-else
                        :index="item.path || item.id.toString()"
                        :popper-offset="-10"
                        popper-class="left-menu-popper"
                    >
                        <template #title>
                            <AppIcon :name="item.icon" class="menu-icon"></AppIcon>
                            <span class="menu-title">{{ item.title }}</span>
                        </template>

                        <template v-for="(child, idx2) in item.children" :key="idx2">
                            <template v-if="child.useYn === 'Y'">
                                <el-menu-item
                                    v-if="child.children.length === 0"
                                    :index="child.path || child.id.toString()"
                                >
                                    <template #title>
                                        <span class="menu-title">{{ child.title }}</span>
                                    </template>
                                </el-menu-item>
                                <el-sub-menu
                                    v-else
                                    :index="child.path || child.id.toString()"
                                    :popper-offset="-10"
                                    popper-class="left-menu-popper"
                                >
                                    <template #title>
                                        <span class="menu-title">{{ child.title }}</span>
                                    </template>

                                    <template v-for="(grandChild, idx3) in child.children" :key="idx3">
                                        <el-menu-item
                                            :index="grandChild.path || grandChild.id.toString()"
                                            v-if="grandChild.useYn === 'Y'"
                                        >
                                            {{ grandChild.title }}
                                        </el-menu-item>
                                    </template>
                                </el-sub-menu>
                            </template>
                        </template>
                    </el-sub-menu>
                </template>
            </template>
        </el-menu>
        </div>
        <button v-if="hasOverflow" type="button" class="menu-scroll-button" aria-label="메뉴 아래로 스크롤" :disabled="!canScrollDown" @click="scrollMenu(1)">
            <el-icon><ArrowDown /></el-icon>
        </button>
        <el-icon
            v-if="!mobile"
            class="collapse-btn"
            @click="onClickCollapseBtn"
            :class="isCollapsed ? 'btn-collapse' : 'btn-expand'"
        >
            <ArrowLeft />
        </el-icon>
    </div>
</template>

<script lang="ts" setup>
import { computed, onMounted, onBeforeUnmount, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useAppStore } from '@/stores/app.store'
import { useMenuStore } from '@/stores/menu.store'

const props = withDefaults(defineProps<{ mobile?: boolean }>(), { mobile: false }) // 모바일 메뉴에서는 이름까지 펼쳐 표시
const menuStore = useMenuStore()
const appStore = useAppStore()
const isCollapsed = computed(() => !props.mobile && appStore.isSidebarCollapsed) // 실제 메뉴 접힘 여부
const route = useRoute()
const defaultMenu = computed(() => route.path)

const menu = computed(() => menuStore.getMenu())

const menuViewportRef = ref<HTMLElement | null>(null) // 메뉴 전용 스크롤 영역
const hasOverflow = ref(false) // 상하 이동 버튼 표시 여부
const canScrollUp = ref(false) // 위로 이동 가능한 상태
const canScrollDown = ref(false) // 아래로 이동 가능한 상태
let menuResizeObserver: ResizeObserver | null = null // 메뉴와 표시 영역 높이 변경 감지

// 현재 스크롤 위치와 메뉴 높이에 맞춰 이동 버튼 상태를 갱신합니다.
const updateScrollState = () => {
    const viewport = menuViewportRef.value
    if (!viewport) return
    hasOverflow.value = viewport.scrollHeight > viewport.clientHeight + 1
    canScrollUp.value = viewport.scrollTop > 1
    canScrollDown.value = viewport.scrollTop + viewport.clientHeight < viewport.scrollHeight - 1
}

// 표시 영역 높이를 기준으로 메뉴를 부드럽게 위아래로 이동합니다.
const scrollMenu = (direction: number) => {
    const viewport = menuViewportRef.value
    if (!viewport) return
    viewport.scrollBy({ top: direction * Math.max(56, viewport.clientHeight * 0.7), behavior: 'smooth' })
}

// 화면 크기와 하위 메뉴 펼침에 따른 스크롤 가능 범위를 동기화합니다.
onMounted(() => {
    const viewport = menuViewportRef.value
    if (!viewport) return
    menuResizeObserver = new ResizeObserver(updateScrollState)
    menuResizeObserver.observe(viewport)
    if (viewport.firstElementChild) {
        menuResizeObserver.observe(viewport.firstElementChild)
    }
    updateScrollState()
})

// 메뉴가 해제되면 크기 감지를 정리합니다.
onBeforeUnmount(() => {
    menuResizeObserver?.disconnect()
})

const onClickMenu = () => {}
const onClickCollapseBtn = () => {
    appStore.toggleSidebar()
}

const setCollapse = () => {
    if (window.innerWidth < 768) {
        appStore.setSidebarCollapsed(true)
    }
}
defineExpose({ setCollapse })

const handleSelect = (path: any) => {
    menuStore.handleClickMenu(path, menu.value)
}

const leftWrapperRef = ref<HTMLElement | null>(null)
const handleClickOutside = (event: MouseEvent) => {
    if (props.mobile) return
    if (leftWrapperRef.value && !leftWrapperRef.value.contains(event.target as Node)) {
        if (appStore.isSidebarCollapsed === false) {
            setCollapse()
        }
    }
}

onMounted(() => {
    document.addEventListener('click', handleClickOutside)
    onResize()
})

onBeforeUnmount(() => {
    document.removeEventListener('click', handleClickOutside)
    window.removeEventListener('resize', onResize)
})

const onResize = () => {
    if (window.innerWidth < 768) {
        appStore.setSidebarCollapsed(true)
    }
}

onMounted(() => {
    window.addEventListener('resize', onResize)
})
</script>

<style lang="scss" scoped>
.menu-bar {
    position: relative;
    display: flex;
    flex-direction: column;
    flex: 1 1 0;
    min-height: 0;
    overflow: hidden;
    background: var(--layout-sidebar-bg-color);
    border-right: none;
    box-shadow: none;
    backdrop-filter: none;
}

.menu-bar.collapse {
    width: 60px;
    animation: collapse 0.5s;
}

.menu-bar.not-collapse {
    width: 320px;
    animation: notCollapse 0.5s;
}

.left-menu {
    display: flex;
    flex: 0 0 auto;
    flex-direction: column;
    gap: 6px;
    width: 100%;
    min-height: 100%;
    background: transparent;
    border: none;
    border-color: transparent;
}

.menu-scroll-viewport {
    flex: 1 1 0;
    min-height: 0;
    overflow-x: hidden;
    overflow-y: auto;
    scrollbar-width: none;
}

.menu-scroll-viewport::-webkit-scrollbar {
    display: none;
}

.menu-scroll-button {
    display: flex;
    flex: 0 0 32px;
    align-items: center;
    justify-content: center;
    width: 100%;
    padding: 0;
    border: none;
    background: transparent;
    color: var(--primary-color);
    cursor: pointer;
}

.menu-scroll-button:disabled {
    opacity: 0.25;
    cursor: default;
}

.menu-scroll-button:focus-visible {
    outline: 2px solid var(--accent-color);
    outline-offset: -2px;
}

.left-menu:not(.el-menu--collapse) {
    border: none;
}

.left-menu::-webkit-scrollbar {
    width: 0;
    height: 0;
    background-color: transparent;
}

.left-menu::-webkit-scrollbar-thumb {
    background-color: transparent;
}

.left-menu .el-button.is-text {
    height: 40px;
    padding: 0;
    border: none;
}

:deep(.el-menu-item),
:deep(.el-sub-menu) {
    flex-shrink: 0;
    gap: 4px;
    font-size: 15px;
    height: 50px;
}

:deep(.el-menu-item),
:deep(.el-sub-menu__title) {
    min-height: 50px;
}

:deep(.el-sub-menu) {
    height: auto;
}

:deep(.el-menu-item),
:deep(.el-sub-menu__title) {
    position: relative;
    color: var(--text-color--secondary);
    transition:
        color 160ms ease,
        background-color 160ms ease;
}

:deep(.el-menu-item) {
    display: flex;
}

:deep(.el-sub-menu .el-menu) {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

:deep(.el-sub-menu .el-menu--inline) {
}

:deep(.el-sub-menu__title) {
    width: 300px;
    gap: 4px;
    margin-bottom: 4px;
    font-size: 15px;
}

:deep(.el-sub-menu__icon-arrow) {
    right: 0;
    width: 30px;
}

.menu-icon-wrap {
    display: flex;
    flex: 0 0 auto;
    align-items: center;
    justify-content: center;
    width: 36px;
}

:deep(.menu-icon) {
    flex: 0 0 auto;
    width: 24px;
    height: 24px;
    color: var(--text-color--secondary);
}

:deep(.menu-icon path),
:deep(.menu-icon rect),
:deep(.menu-icon circle),
:deep(.menu-icon polygon) {
    fill: var(--text-color--secondary) !important;
    transition: fill 160ms ease;
}

:deep(.menu-title),
:deep(.el-sub-menu__icon-arrow) {
    min-width: 0;
    opacity: 1;
    transform: translateX(0);
    transition:
        opacity 220ms ease,
        transform 220ms ease,
        max-width 220ms ease;
}

:deep(.el-menu-item:hover),
:deep(.el-sub-menu:hover) {
    background: rgba(255, 255, 255, 0.04);
    color: var(--text-color--white);
}
:deep(.el-sub-menu__title:hover) {
    background: none;
}

:deep(.el-menu-item:hover .menu-icon path),
:deep(.el-menu-item:hover .menu-icon rect),
:deep(.el-menu-item:hover .menu-icon circle),
:deep(.el-menu-item:hover .menu-icon polygon),
:deep(.el-sub-menu__title:hover .menu-icon path),
:deep(.el-sub-menu__title:hover .menu-icon rect),
:deep(.el-sub-menu__title:hover .menu-icon circle),
:deep(.el-sub-menu__title:hover .menu-icon polygon) {
    fill: var(--text-color--white) !important;
}

:deep(.el-menu-item.is-active),
:deep(.el-sub-menu.is-active > .el-sub-menu__title) {
    color: var(--accent-color) !important;
}

:deep(.el-menu-item.is-active) {
    background: var(--layout-menu-active-bg-color);
}

:deep(.el-menu-item.is-active .menu-icon path),
:deep(.el-menu-item.is-active .menu-icon rect),
:deep(.el-menu-item.is-active .menu-icon circle),
:deep(.el-menu-item.is-active .menu-icon polygon),
:deep(.el-sub-menu.is-active > .el-sub-menu__title .menu-icon path),
:deep(.el-sub-menu.is-active > .el-sub-menu__title .menu-icon rect),
:deep(.el-sub-menu.is-active > .el-sub-menu__title .menu-icon circle),
:deep(.el-sub-menu.is-active > .el-sub-menu__title .menu-icon polygon) {
    fill: var(--primary-color) !important;
}

.collapse :deep(.el-sub-menu.is-active > .el-sub-menu__title) {
    background: var(--layout-menu-active-bg-color);
}

.collapse :deep(.menu-title),
.collapse :deep(.el-sub-menu__icon-arrow) {
    max-width: 0;
    opacity: 0;
    overflow: hidden;
    transform: translateX(-8px);
    pointer-events: none;
}

.collapse .menu-icon-wrap {
    width: 100%;
}

.collapse :deep(.el-menu--collapse) {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    overflow: hidden;
}

.collapse :deep(.el-menu-item .el-menu-tooltip__trigger) {
    justify-content: center;
    padding: 0;
}

.collapse :deep(.el-sub-menu),
.collapse :deep(.el-sub-menu__title) {
    display: flex;
    justify-content: center;
    width: 100px;
    height: 50px;
    margin: 0;
    padding: 0;
}

.collapse :deep(.el-menu-item) {
    width: 100%;
    height: 50px;
}

.collapse-btn {
    position: static;
    flex-shrink: 0;
    align-self: flex-end;
    margin: 8px 16px 12px 0;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 30px;
    height: 30px;
    color: var(--primary-color);
    background: var(--layout-menu-active-bg-color);
    border: none;
    border-radius: 999px;
    cursor: pointer;
    transition:
        background-color 160ms ease,
        color 160ms ease,
        transform 400ms ease;
}

.collapse-btn:hover {
    color: var(--text-color--white);
    background: var(--layout-purple-glow-color);
}

.collapse-btn svg {
    width: 18px;
    height: 18px;
    stroke-width: 2.4;
}

.btn-collapse {
    transform: rotate(180deg);
}

.btn-expand {
    transform: rotate(0deg);
}

:global(.left-menu-popper),
:global(.left-menu-popper .el-menu--popup),
:global(.left-menu-popper .el-menu-item),
:global(.left-menu-popper .el-sub-menu__title) {
    border: none !important;
    border-radius: 0 !important;
}

:global(.left-menu-popper .el-popper__arrow::before) {
    border: none !important;
}

@keyframes collapse {
    from {
        width: 320px;
    }

    to {
        width: 60px;
    }
}

@keyframes notCollapse {
    from {
        width: 60px;
    }

    to {
        width: 320px;
    }
}
.menu-bar.is-mobile {
    width: 100%;
    animation: none;
}

.menu-bar.is-mobile :deep(.el-sub-menu__title) {
    width: 100%;
}
</style>
