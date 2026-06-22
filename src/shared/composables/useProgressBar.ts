import iconLoadingSvg from '@/assets/icons/IconLoading.svg?raw'
import { defineStore } from 'pinia'
import { ref } from 'vue'

const viewBoxMatch = iconLoadingSvg.match(/viewBox="([^"]+)"/i)
const svgContentMatch = iconLoadingSvg.match(/<svg[^>]*>([\s\S]*?)<\/svg>/i)

export const loadingSvgViewBox = viewBoxMatch?.[1] ?? '0 0 100 100'
export const loadingSvgContent = svgContentMatch?.[1]?.trim() ?? ''

export const useProgress = defineStore('progress', () => {
    const isProgressing = ref(false)
    const percentCompleted = ref(0)

    const setPercentCompleted = (progressEventLoaded: number, progressEventTotal: number) => {
        if (!progressEventTotal) return
        const percent = Math.round((progressEventLoaded * 100) / progressEventTotal)
        percentCompleted.value = Math.max(0, Math.min(percent, 100))
    }

    const startProgress = () => {
        isProgressing.value = true
    }

    const endProgress = () => {
        isProgressing.value = false
        percentCompleted.value = 0
    }

    return {
        isProgressing,
        percentCompleted,
        setPercentCompleted,
        startProgress,
        endProgress,
    }
})
