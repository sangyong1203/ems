<template>
    <MainLayout :collapsed="appStore.isSidebarCollapsed">
        <template #sidebar="{ mobile }">
            <div class="main-sidebar" :class="!mobile && appStore.isSidebarCollapsed ? 'is-collapse' : 'is-expand'">
                <div class="side-brand" @click="toDashboard">
                    <span class="side-title">Solar ESS EMS</span>
                </div>
                <LeftMenu :mobile="mobile" />
            </div>
        </template>

        <template #header="{ mobileMenuOpen, toggleMobileMenu }">
            <MainHeader
                :title="currentMenuItem.title"
                :icon="currentMenuItem.icon"
                :user-name="userDisplayName"
                :mobile-menu-open="mobileMenuOpen"
                @toggle-menu="toggleMobileMenu"
                @logout="logOut"
                @change-password="changePasswordRef?.openDialog()"
            />
        </template>

        <RouterView v-slot="{ Component }">
            <component :is="Component"></component>
        </RouterView>
    </MainLayout>
    <ChangePassword ref="changePasswordRef" />
</template>

<script setup lang="ts">
import MainLayout from '@/layouts/MainLayout.vue'
import MainHeader from '@/layouts/MainHeader.vue'
import { computed, onMounted, onUnmounted, ref } from 'vue'
import ChangePassword from '@/pages/login/ChangePassword.vue'
import loginApi from '@/pages/login/service/login.api'
import { RouterView, useRoute, useRouter } from 'vue-router'
import { LeftMenu } from '@/components'
import { Notification } from '@/composables/useFeedback'
import { useAppStore } from '@/stores/app.store'
import { useAuthStore } from '@/stores/auth.store'
import { useMenuStore } from '@/stores/menu.store'
import { useNavStore } from '@/stores/nav.store'

const changePasswordRef = ref<InstanceType<typeof ChangePassword> | null>(null) // 비밀번호 변경 창
const loggingOut = ref(false) // 중복 로그아웃 방지

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

// 서버에서 세션 폐기를 확인한 뒤 프론트 인증 상태와 메뉴를 초기화합니다.
const logOut = async () => {
    if (loggingOut.value) return
    loggingOut.value = true
    try {
        const refreshToken = authStore.authState.tokens.refreshToken
        if (refreshToken) {
            await loginApi.logout(refreshToken)
        }
        authStore.clearSession()
        appStore.init()
        menuStore.init()
        navStore.init()
        await router.replace('/login')
    } catch {
        Notification.error('Logout failed. Please check your connection and try again.')
    } finally {
        loggingOut.value = false
    }
}
</script>

<style scoped lang="scss">
.main-sidebar {
    height: 100%;
    min-height: 0;
    display: flex;
    flex-direction: column;
    background: var(--layout-sidebar-bg-color);
}

.side-brand {
    height: 72px;
    flex-shrink: 0;
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

@media (max-width: 767px) {
    .side-brand {
        padding-right: 64px;
    }

    .side-title {
        overflow: hidden;
        font-size: 20px;
        text-overflow: ellipsis;
    }
}

.main-sidebar.is-collapse .side-title {
    opacity: 0;
    width: 0;
}
</style>
