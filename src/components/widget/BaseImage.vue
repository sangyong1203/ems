<template>
    <div class="image-wrapper" :style="{ width, height }">
        <el-image
            v-if="src && status !== 'empty' && status !== 'error'"
            class="image-element"
            :class="{ 'is-hidden': status !== 'ready' }"
            :src="src"
            style="width: 100%; height: 100%"
            :fit="fit"
            :alt="alt"
            lazy
            @load="handleLoad"
            @error="handleError"
        />
        <div v-if="status === 'loading'" class="image-loading">
            Loading<span v-if="showLoading" class="dots"></span>
        </div>
        <div v-else-if="status === 'empty' || status === 'error'" class="fallback-container">
            <el-icon class="fallback-icon"><Picture /></el-icon>
        </div>
    </div>
</template>
<script setup lang="ts">
import { onBeforeUnmount, ref, toRefs, watch } from 'vue'
interface Props {
    src: string
    width?: string
    height?: string
    alt?: string
    fit?: 'cover' | 'contain'
    showLoading?: boolean
}
const props = withDefaults(defineProps<Props>(), {
    src: '',
    width: '100%',
    height: '100%',
    alt: '',
    fit: 'cover',
    showLoading: true,
})
const { src, width, height, showLoading, alt, fit } = toRefs(props)
const status = ref<'loading' | 'empty' | 'ready' | 'error'>('loading')
let emptyCheckTimer: ReturnType<typeof setTimeout> | null = null

const EMPTY_SRC_CHECK_MS = 5000

const clearEmptyCheckTimer = () => {
    if (emptyCheckTimer) {
        clearTimeout(emptyCheckTimer)
        emptyCheckTimer = null
    }
}

const scheduleEmptyCheck = () => {
    clearEmptyCheckTimer()
    emptyCheckTimer = setTimeout(() => {
        if (!src.value) {
            status.value = 'empty'
        }
        emptyCheckTimer = null
    }, EMPTY_SRC_CHECK_MS)
}

const handleLoad = () => {
    status.value = 'ready'
    clearEmptyCheckTimer()
}

const handleError = () => {
    status.value = 'error'
    clearEmptyCheckTimer()
}

watch(
    src,
    value => {
        clearEmptyCheckTimer()

        if (value) {
            status.value = 'loading'
            return
        }

        status.value = 'loading'
        scheduleEmptyCheck()
    },
    { immediate: true },
)

onBeforeUnmount(() => {
    clearEmptyCheckTimer()
})
</script>
<style lang="scss" scoped>
.image-wrapper {
    position: relative;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background-color: var(--common-control-bg-color);
}
.image {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
/* fallback 以묒븰 諛곗튂 */
.image-element {
    width: 100%;
    height: 100%;
}

.is-hidden {
    visibility: hidden;
}

.fallback-container {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;

    .fallback-icon {
        width: 24px;
        height: 24px;

        svg {
            width: 24px; 
            height: 24px; 
            opacity: 0.3; 
            color: var(--text-color--muted);
        }
    }
}

.image-loading {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    color: var(--text-color--muted);
}

.dots {
    width: 20px;
    display: inline-block;
    text-align: left;
    margin-left: 4px;
}

.dots::after {
    content: '';
    animation: dots 1s steps(4, end) infinite;
}

@keyframes dots {
    0% {
        content: '';
    }
    25% {
        content: '.';
    }
    50% {
        content: '..';
    }
    75% {
        content: '...';
    }
    100% {
        content: '';
    }
}
</style>
