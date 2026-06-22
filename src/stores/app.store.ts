import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore(
    'app',
    () => {
        const isLoading = ref(false)
        const isSidebarCollapsed = ref(true)

        const setLoading = (value: boolean) => {
            isLoading.value = value
        }

        const setSidebarCollapsed = (value: boolean) => {
            isSidebarCollapsed.value = value
        }

        const toggleSidebar = () => {
            isSidebarCollapsed.value = !isSidebarCollapsed.value
        }

        const init = () => {
            isLoading.value = false
            isSidebarCollapsed.value = true
        }

        return {
            isLoading,
            isSidebarCollapsed,
            setLoading,
            setSidebarCollapsed,
            toggleSidebar,
            init,
        }
    },
    { persist: true },
)
