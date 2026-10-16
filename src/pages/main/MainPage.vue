<template>
    <MainLayout :collapsed="appStore.isSidebarCollapsed">
        <template #sidebar>
            <div class="main-sidebar" :class="appStore.isSidebarCollapsed ? 'is-collapse' : 'is-expand'">
                <div class="side-brand" @click="toDashboard">
                    <span class="side-title">Solar ESS EMS</span>
                </div>
                <LeftMenu />
            </div>
        </template>

        <template #header>
            <MainHeader
                :title="currentMenuItem.title"
                :icon="currentMenuItem.icon"
                :user-name="userDisplayName"
                @logout="logOut"
            />
        </template>

        <RouterView v-slot="{ Component }">
            <component :is="Component"></component>
        </RouterView>
    </MainLayout>
</template>

<script setup lang="ts">
import MainLayout from '@/layouts/MainLayout.vue'
import MainHeader from '@/layouts/MainHeader.vue'
import { computed, onMounted, onUnmounted } from 'vue'
import { RouterView, useRoute, useRouter } from 'vue-router'
import { LeftMenu } from '@/components'
import { useAppStore } from '@/stores/app.store'
import { useAuthStore } from '@/stores/auth.store'
import { useMenuStore } from '@/stores/menu.store'
import { useNavStore } from '@/stores/nav.store'

const appStore = useAppStore() // 앱 상태 스토어
const authStore = useAuthStore() // 인증 상태 스토어
const menuStore = useMenuStore() // 메뉴 상태 스토어
const navStore = useNavStore() // 네비게이션 히스토리 스토어
const route = useRoute() // 현재 라우트 객체
const router = useRouter() // 라우터 인스턴스

// 뒤로가기 제어 이벤트 등록
onMounted(() => {
    window.addEventListener('popstate', backButtonEvent)
})

// 뒤로가기 제어 이벤트 해제
onUnmounted(() => {
    window.removeEventListener('popstate', backButtonEvent)
})

// 브라우저 뒤로가기 방지 및 이전 네비게이션 복원
function backButtonEvent(event: any) {
    console.log('popstate event triggered:', event.state)
    const nav = navStore.getNav()
    const lastNav = nav.at(-1)
    if (nav.length <= 2 && route.path !== '/login' && route.path !== '/dashboard') {
        history.pushState(null, '', '')
        navStore.navTo(lastNav.name, lastNav.path)
    }
}

// 사용자 설정 랜딩 페이지로 이동
const toDashboard = () => {
    if (authStore.authState.user?.landingPage) {
        navStore.navTo('landingPage', authStore.authState.user.landingPage)
    }
}

// 현재 경로에 일치하는 메뉴 항목 재귀 검색
const findMenuItem = (items: any[], path: string): { title: string; icon: string } => {
    for (const item of items) {
        if (item.path === path) return item
        if (item.children?.length) {
            const title = findMenuItem(item.children, path)
            if (title) return item
        }
    }
    return { title: '', icon: '' }
}

// 현재 활성화된 메뉴 정보 계산
const currentMenuItem = computed(() => {
    const menuItem = findMenuItem(menuStore.getMenu(), route.path)
    return menuItem
})

// 상단 헤더 표시용 사용자 이름 계산
const userDisplayName = computed(() => {
    const user = authStore.authState.user
    return user?.name || user?.email || user?.loginId || 'User'
})

// 로그아웃 및 스토어 초기화
const logOut = () => {
    authStore.clearSession()
    appStore.init()
    menuStore.init()
    navStore.init()
    router.push('/login')
}
</script>

<style scoped lang="scss">
.main-sidebar {
    height: 100%;
    display: flex;
    flex-direction: column;
    background: var(--layout-sidebar-bg-color);
}

.side-brand {
    height: 72px;
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 0 24px;
    background: var(--layout-sidebar-bg-color);
    color: var(--text-color--white);
    white-space: nowrap;
    cursor: pointer;
}

.side-title {
    min-width: 0;
    overflow: hidden;
    font-family: 'Pretendard', sans-serif;
    font-size: 24px;
    font-weight: lighter;
    line-height: 38px;
    opacity: 1;
    transition: opacity 160ms ease;
}

.main-sidebar.is-collapse .side-brand {
    justify-content: center;
    width: 60px;
    padding: 0;
}

.main-sidebar.is-collapse .side-title {
    opacity: 0;
    width: 0;
}
</style>
