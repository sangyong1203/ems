<template>
    <el-container class="layout-shell">
        <aside v-if="!isMobile" class="left-wrapper" :class="collapsed ? 'is-collapse' : 'is-expand'">
            <slot name="sidebar" :mobile="false"></slot>
        </aside>
        <el-drawer
            v-if="isMobile"
            v-model="mobileMenuOpen"
            aria-label="메뉴 탐색"
            :with-header="false"
            :show-close="false"
            direction="ltr"
            size="min(320px, 88vw)"
            class="mobile-navigation-drawer"
            append-to-body
        >
            <button
                type="button"
                class="mobile-navigation-close"
                title="메뉴 닫기"
                aria-label="메뉴 닫기"
                @click="mobileMenuOpen = false"
            >
                <el-icon><ArrowLeft /></el-icon>
            </button>
            <slot name="sidebar" :mobile="true"></slot>
        </el-drawer>
        <el-container class="right-wrapper">
            <el-header>
                <slot name="header" :mobile-menu-open="mobileMenuOpen" :toggle-mobile-menu="toggleMobileMenu"></slot>
            </el-header>
            <el-main ref="mainRef">
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
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import type { MainInstance } from 'element-plus'

const mobileMedia = window.matchMedia('(max-width: 767px)') // 공통 모바일 메뉴 적용 구간
const isMobile = ref(mobileMedia.matches) // 모바일 화면 여부
const mobileMenuOpen = ref(false) // 모바일 오버레이 메뉴 표시 여부

// 모바일 메뉴는 데스크톱 사이드바의 접힘 상태와 독립적으로 열고 닫습니다.
const toggleMobileMenu = () => {
    mobileMenuOpen.value = !mobileMenuOpen.value
}

// 화면 구간 전환 시 메뉴를 닫아 데스크톱과 모바일 상태가 섞이지 않도록 합니다.
const syncMobileViewport = () => {
    isMobile.value = mobileMedia.matches
    mobileMenuOpen.value = false
}

// 모바일 구간 변경 감지를 등록합니다.
onMounted(() => mobileMedia.addEventListener('change', syncMobileViewport))

// 레이아웃 해제 시 화면 구간 감지를 해제합니다.
onBeforeUnmount(() => mobileMedia.removeEventListener('change', syncMobileViewport))

const route = useRoute() // 현재 화면 경로
const mainRef = ref<MainInstance | null>(null) // 공통 본문 스크롤 영역

withDefaults(
    defineProps<{
        collapsed?: boolean
    }>(),
    {
        collapsed: false,
    },
)

// 다른 화면의 렌더링이 끝나면 공통 본문의 세로·가로 스크롤을 초기화합니다.
watch(
    () => route.path,
    () => {
        mobileMenuOpen.value = false
        mainRef.value?.$el.scrollTo({ top: 0, left: 0, behavior: 'instant' })
    },
    { flush: 'post' },
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
    min-height: 0;
    height: 100%;
    display: flex;
    flex: 1;
    flex-direction: column;
}

.el-header {
    height: 60px;
    flex-shrink: 0;
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
    flex: 1;
    min-height: 0;
    color: var(--text-color--primary);
    scrollbar-gutter: stable;
    overflow: auto;
}

.contents-wrapper {
    position: relative;
    display: flex;
    flex-direction: row;
    height: 100%;
    min-height: 798px;
    background: transparent;
}

.contents-wrapper .contents {
    position: relative;
    z-index: 1;
    padding: 0px 10px 16px 16px;
    width: 100%;
    display: flex;
    flex-direction: column;
    height: 100%;
    min-height: 798px;
    overflow: visible;
}

.el-main::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

.el-main::-webkit-scrollbar-thumb {
    background-color: var(--overlay-scrollbar-thumb-color);
    border-radius: 6px;
}

.el-main::-webkit-scrollbar-thumb:hover,
.el-main::-webkit-scrollbar-track:hover,
.el-main::-webkit-scrollbar-corner:hover {
    cursor: pointer;
}
@media (max-width: 767px) {
    .layout-shell {
        height: 100dvh;
    }

    .el-header {
        height: 56px;
        padding: 0 10px;
    }

    .contents-wrapper,
    .contents-wrapper .contents {
        height: auto;
        min-height: 100%;
    }

    .contents-wrapper .contents {
        min-width: 0;
        padding: 0 0 16px;
    }

    .el-main {
        scrollbar-gutter: auto;
    }
}

:global(.mobile-navigation-drawer .el-drawer__body) {
    position: relative;
    padding: 0;
    overflow: hidden;
}

.mobile-navigation-close {
    position: absolute;
    z-index: 1;
    top: 14px;
    right: 10px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 44px;
    height: 44px;
    padding: 0;
    border: none;
    background: transparent;
    color: var(--text-color--primary);
    font-size: 22px;
    cursor: pointer;
}

.mobile-navigation-close:focus-visible {
    outline: 2px solid var(--accent-color);
    outline-offset: -2px;
}

</style>
