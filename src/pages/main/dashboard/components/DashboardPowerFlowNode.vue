<template>
    <article class="dashboard-power-flow-node" :class="`dashboard-power-flow-node--${variant}`">
        <div class="dashboard-power-flow-node__top">
            <span>{{ title }}</span>
            <AppIcon :name="icon" class="dashboard-power-flow-node__icon" />
        </div>
        <strong
            >{{ value }} <small>{{ unit }}</small></strong
        >
        <em>{{ status }}</em>
    </article>
</template>

<script setup lang="ts">
import AppIcon from '@/shared/components/widget/AppIcon.vue'
import type { AppIconName } from '@/shared/constants/appIcons'

defineProps<{
    variant: 'solar' | 'load' | 'grid'
    title: string
    value: string
    unit: string
    status: string
    icon: AppIconName
}>()
</script>

<style scoped lang="scss">
.dashboard-power-flow-node {
    position: absolute;
    z-index: 3;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 8px;
    width: 210px;
    height: 122px;
    padding: 18px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    background: linear-gradient(135deg, rgba(21, 224, 183, 0.12), rgba(231, 109, 255, 0.1)), rgba(255, 255, 255, 0.05);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.dashboard-power-flow-node__top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
}

.dashboard-power-flow-node span {
    color: var(--text-color--secondary);
    font-size: 15px;
    font-weight: 700;
}

.dashboard-power-flow-node__icon {
    flex: 0 0 auto;
    width: 34px;
    height: 34px;
    color: var(--secondary-color);
    filter: drop-shadow(0 0 8px rgba(21, 224, 183, 0.35));
}

.dashboard-power-flow-node strong {
    font-size: 28px;
    line-height: 32px;
}

.dashboard-power-flow-node strong small {
    font-size: 14px;
}

.dashboard-power-flow-node em {
    color: var(--secondary-color);
    font-size: 15px;
    font-weight: 700;
    font-style: normal;
}

.dashboard-power-flow-node--solar {
    top: calc(50% - 60px);
    left: 2%;
}

.dashboard-power-flow-node--load {
    top: 4%;
    left: 45%;
}

.dashboard-power-flow-node--grid {
    top: calc(50% - 60px);
    right: 2%;
}
</style>
