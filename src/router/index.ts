import { useAuthStore } from '@/stores/auth.store'
import { createRouter, createWebHistory } from 'vue-router'
import { routes } from './routes'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
})


// 업무 화면은 관리자 로그인 상태에서만 진입하며 실제 API 권한은 서버에서도 검증합니다.
router.beforeEach(to => {
    const authStore = useAuthStore()
    const publicPaths = ['/login', '/403', '/404', '/500']
    if (publicPaths.includes(to.path) || to.name === 'passwordReset') return
    if (!authStore.isAuthenticated) return { name: 'login' }
    if (authStore.authState.user?.userLevel !== 'PLATFORM_ADMIN') return { name: '403' }
})

export default router
