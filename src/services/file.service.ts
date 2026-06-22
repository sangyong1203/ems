import { useAuthStore } from '@/stores/auth.store'

export const getAuthImage = async (apiUrl: string) => {
    const authStore = useAuthStore()

    if (!apiUrl || apiUrl.includes('Blob')) {
        return
    }

    try {
        const response = await fetch(apiUrl, {
            headers: {
                Authorization: `Bearer ${authStore.authState.tokens.accessToken}`,
            },
        })

        if (!response.ok) {
            throw new Error(`HTTP error status :${response.status}`)
        }

        const blob = await response.blob()
        return URL.createObjectURL(blob)
    } catch (error: any) {
        console.error('Failed to fetch image:', error)
    }
}

export default {
    getAuthImage,
}
