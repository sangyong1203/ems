import { useAuthStore } from '@/stores/auth.store'
import { createRouter, createWebHistory } from 'vue-router'
import { routes } from './routes'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
})


router.beforeEach(async (to, from) => {
    
    const authStore = useAuthStore()
    console.log(`to path: ${to.path}, from path: ${from.path}, auth Store: ${authStore.authState.user?.loginId}`)    

    if (
        !authStore.isAuthenticated &&
        to.path !== '/' &&
        to.path !== '/login'
    ) {
        window.location.replace('/login')
    }
})

export default router
