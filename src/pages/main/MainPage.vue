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
import { LeftMenu } from '@/shared/components'
import { useAppStore } from '@/stores/app.store'
import { useAuthStore } from '@/stores/auth.store'
import { useMenuStore } from '@/stores/menu.store'
import { useNavStore } from '@/stores/nav.store'

const appStore = useAppStore()
const authStore = useAuthStore()
const menuStore = useMenuStore()
const navStore = useNavStore()
const route = useRoute()
const router = useRouter()

onMounted(() => {
    // browser back button event
    window.addEventListener('popstate', backButtonEvent)
})
onUnmounted(() => {
    window.removeEventListener('popstate', backButtonEvent)
})
// browser back button event
function backButtonEvent(event: any) {
    console.log('popstate event triggered:', event.state)
    const nav = navStore.getNav()
    const lastNav = nav.at(-1)
    if (nav.length <= 2 && route.path !== '/login' && route.path !== '/dashboard') {
        history.pushState(null, '', '')
        navStore.navTo(lastNav.name, lastNav.path)
    }
}

const toDashboard = () => {
    if (authStore.authState.user?.landingPage) {
        navStore.navTo('landingPage', authStore.authState.user.landingPage)
    }
}

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

const currentMenuItem = computed(() => {
    const menuItem = findMenuItem(menuStore.getMenu(), route.path)
    return menuItem

    // const nav = navStore.getNav()
    // const lastNav = nav.at(-1)
    // if (lastNav?.name && lastNav.name !== 'landingPage') return lastNav.name

    // return String(route.name ?? 'Dashboard')
})

const userDisplayName = computed(() => {
    const user = authStore.authState.user
    return user?.name || user?.email || user?.loginId || 'User'
})

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
