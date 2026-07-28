<template>
    <div class="media-preview">
        <el-popover
            v-for="(item, index) in items"
            :key="`${item.thumbnailSrc}-${index}`"
            placement="top"
            :width="220"
            :hide-after="0"
            trigger="hover"
            :teleported="true"
            popper-class="media-preview-popper"
        >
            <template #reference>
                <div class="media-preview__thumb" :class="[`is-${item.type}`]" @click="handleOpenDialog(index)">
                    <img class="media-preview__thumb-image" :src="item.thumbnailSrc" alt="" />
                    <div v-if="item.type === 'video'" class="media-preview__play">
                        <span class="media-preview__play-icon" />
                    </div>
                </div>
            </template>
            <div class="media-preview__hover-card">
                <img class="media-preview__hover-image" :src="item.thumbnailSrc" alt="" />
                <div v-if="item.type === 'video'" class="media-preview__hover-play">
                    <span class="media-preview__play-icon is-large" />
                </div>
            </div>
        </el-popover>
    </div>

    <BaseDialog
        v-model="dialogVisible"
        title="Media Preview"
        width="1000px"
        append-to-body
        class="media-preview-dialog"
        modal-class="media-preview-overlay"
        :z-index="10000"
    >
        <div v-if="activeItem" class="media-preview__dialog-body">
            <button
                v-if="items.length > 1"
                type="button"
                class="media-preview__nav is-left"
                :disabled="activeIndex === 0"
                @click="handlePrev"
            >
                <IconMoveButton class="media-preview__nav-icon" />
            </button>

            <div class="media-preview__viewer">
                <div class="media-preview__content" :class="`is-${activeItem.type}`">
                    <img
                        v-if="activeItem.type === 'image'"
                        class="media-preview__dialog-image"
                        :src="activeItem.sourceSrc || activeItem.thumbnailSrc"
                        alt=""
                    />
                    <div v-else class="media-preview__dialog-video-wrap">
                        <video
                            v-if="activeItem.sourceSrc"
                            class="media-preview__dialog-video"
                            :src="activeItem.sourceSrc"
                            controls
                            autoplay
                        />
                        <div v-else class="media-preview__video-fallback">
                            <img class="media-preview__dialog-image" :src="activeItem.thumbnailSrc" alt="" />
                            <div class="media-preview__dialog-fallback-play">
                                <span class="media-preview__play-icon is-large" />
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <button
                v-if="items.length > 1"
                type="button"
                class="media-preview__nav is-right"
                :disabled="activeIndex === items.length - 1"
                @click="handleNext"
            >
                <IconMoveButton class="media-preview__nav-icon" />
            </button>
        </div>

        <template #footer>
            <el-button @click="handleCloseDialog">Close</el-button>
        </template>
    </BaseDialog>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import IconMoveButton from '@/assets/icons/IconMoveButton.svg'

type MediaPreviewItem = {
    type: 'image' | 'video'
    thumbnailSrc: string
    sourceSrc?: string
}

const props = defineProps<{
    items: MediaPreviewItem[]
}>()

const dialogVisible = ref(false)
const activeIndex = ref(0)

const activeItem = computed<MediaPreviewItem | null>(() => props.items[activeIndex.value] ?? props.items[0] ?? null)

const handleOpenDialog = (index: number) => {
    if (props.items.length === 0) {
        return
    }

    activeIndex.value = index
    dialogVisible.value = true
}

const handleCloseDialog = () => {
    dialogVisible.value = false
}

const handlePrev = () => {
    if (activeIndex.value === 0) {
        return
    }

    activeIndex.value -= 1
}

const handleNext = () => {
    if (activeIndex.value >= props.items.length - 1) {
        return
    }

    activeIndex.value += 1
}
</script>

<style scoped lang="scss">
.media-preview {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    flex-wrap: wrap;
}

.media-preview__thumb {
    position: relative;
    width: 32px;
    height: 32px;
    border: 1px solid var(--common-component-border-color);
    border-radius: 8px;
    overflow: hidden;
    cursor: pointer;
    flex-shrink: 0;
    box-sizing: border-box;
}

.media-preview__thumb-image,
.media-preview__hover-image,
.media-preview__dialog-image {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.media-preview__play,
.media-preview__hover-play,
.media-preview__dialog-fallback-play {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    pointer-events: none;
}

.media-preview__play-icon {
    width: 0;
    height: 0;
    border-top: 6px solid transparent;
    border-bottom: 6px solid transparent;
    border-left: 10px solid rgba(255, 255, 255, 0.92);
    filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.3));
}

.media-preview__play-icon.is-large {
    border-top-width: 14px;
    border-bottom-width: 14px;
    border-left-width: 22px;
}

.media-preview__hover-card {
    width: 220px;
    height: 220px;
    overflow: hidden;
    background: var(--common-component-bg-color);
}

.media-preview__hover-image {
    width: 100%;
    height: 100%;
}

.media-preview__dialog-body {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 620px;
}

.media-preview__viewer {
    width: calc(100% - 120px);
    min-height: 560px;
    box-sizing: border-box;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}

.media-preview__content {
    width: 100%;
    max-width: 520px;
    min-height: 320px;
    padding: 20px;
    box-sizing: border-box;
    border-radius: 4px;
    background: var(--common-control-bg-color);
    display: flex;
    align-items: center;
    justify-content: center;
}

.media-preview__content.is-video {
    max-width: 720px;
    background: #111111;
}

.media-preview__dialog-image {
    max-width: 100%;
    width: auto;
    height: auto;
    max-height: 420px;
    object-fit: contain;
}

.media-preview__dialog-video-wrap {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.media-preview__dialog-video {
    width: 100%;
    max-height: 420px;
    border-radius: 8px;
    background: #000;
}

.media-preview__video-fallback {
    position: relative;
    width: 100%;
    height: 420px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.media-preview__nav {
    width: 60px;
    height: 60px;
    border: none;
    background: transparent;
    color: var(--primary-color);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    padding: 0;
}

.media-preview__nav:disabled {
    color: var(--text-color--muted);
    cursor: default;
}

.media-preview__nav.is-left .media-preview__nav-icon {
    transform: rotate(180deg);
}

.media-preview__nav-icon {
    width: 60px;
    height: 60px;
    display: block;
}

.media-preview__nav-icon :deep(path) {
    fill: currentColor;
}

:global(.media-preview-dialog .dialog-header) {
    padding: 16px 20px;
    background: var(--surface-elevated-color);
}

:global(.media-preview-dialog .dialog-header-title) {
    color: var(--text-color--primary);
    font-size: 22px;
    font-weight: 700;
    line-height: 1;
}

:global(.media-preview-dialog .dialog-header .el-icon) {
    color: var(--text-color--primary);
}

:global(.media-preview-dialog .el-dialog__header) {
    margin: 0;
    padding: 0;
}

:global(.media-preview-dialog .el-dialog__body) {
    padding: 24px;
    background: var(--surface-color);
}

:global(.media-preview-dialog .dialog-footer) {
    display: flex;
    justify-content: center;
}

:global(.media-preview-dialog .dialog-footer .el-button) {
    min-width: 82px;
    height: 40px;
    border-radius: 999px;
    background: var(--common-control-bg-color);
    border-color: var(--common-control-border-color);
    color: var(--text-color--secondary);
}

:global(.media-preview-popper) {
    padding: 0 !important;
    border: 1px solid var(--common-component-border-color) !important;
    border-radius: 4px !important;
    overflow: hidden !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.22) !important;
}
</style>
