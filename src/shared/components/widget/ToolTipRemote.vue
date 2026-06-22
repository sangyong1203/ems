<template>
    <el-tooltip
        ref="tooltipRef"
        :visible="isVisible"
        placement="top"
        :show-arrow="false"
        popper-class="tooltip-offset"
        :popper-options="{
            modifiers: [
                {
                    name: 'offset',
                    options: { offset: [90, -45] },
                },
                {
                    name: 'computeStyles',
                    options: { adaptive: false },
                },
            ],
        }"
    >
        <template #content>
            <div class="tooltip-body" @mouseenter="cancelClose" @mouseleave="closeTooltip">
                <div v-if="loading" class="loading-wrapper">
                    <el-icon class="is-loading"><Loading /></el-icon>
                    <span>Loading...</span>
                </div>
                <div v-else>{{ tooltipContent }}</div>
            </div>
        </template>

        <div class="trigger-wrapper" @click="loadContent" @mouseleave="closeTooltip" @mouseenter="cancelClose">
            <slot></slot>
        </div>
    </el-tooltip>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'

interface Props {
    userId: number | string
    type?: string
}

const props = defineProps<Props>()

const tooltipContent = ref('')
const loading = ref(false)
const isVisible = ref(false)
const tooltipRef = ref<any>(null)

let closeTimer: ReturnType<typeof setTimeout> | null = null

const loadContent = async () => {
    isVisible.value = true
    loading.value = true
    try {
        tooltipContent.value = await getUnmasking(props.userId, props.type)
    } catch (error) {
        tooltipContent.value = 'No data'
    } finally {
        loading.value = false

        nextTick(() => {
            if (tooltipRef.value?.updatePopper) {
                tooltipRef.value.updatePopper()
            }
        })
    }
}

const getUnmasking = async (userId: number | string, type: string = 'ALL'): Promise<string> => {
    await new Promise(resolve => setTimeout(resolve, 200))

    // const payload: PayloadModel = { query: { id: userId, type:'NAME' } }
    // const res = await fetchApi().get('/system/admins/unmasking', { payload })

    return 'test -mock data--?띻만??Hong Gil-dong)'
}
const closeTooltip = () => {
    closeTimer = setTimeout(() => {
        isVisible.value = false
    }, 150)
}

const cancelClose = () => {
    if (closeTimer) {
        clearTimeout(closeTimer)
        closeTimer = null
    }
}
</script>

<style lang="scss" scoped>
:global(.el-popper.tooltip-offset) {
    background: var(--common-tooltip-bg-color) !important;
    border: 1px solid var(--common-component-border-color) !important;
    color: var(--text-color--body) !important;
    font-size: 15px !important;
    font-weight: 400 !important;
    padding: 16px !important;
    border-radius: 8px !important;

    margin-left: 90px !important;
    margin-bottom: -45px !important;
}


.tooltip-body {
    min-width: 250px;
    min-height: 24px;
    display: flex;
    justify-content: flex-start;
    align-items: center;
}

.loading-wrapper {
    display: flex;
    align-items: center;
    gap: 8px;
}

.trigger-wrapper {
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    display: block; 
    cursor: pointer;
}
</style>
