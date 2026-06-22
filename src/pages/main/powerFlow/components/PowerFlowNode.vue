<template>
    <article class="power-flow-node" :class="`power-flow-node--${variant}`">
        <div class="power-flow-node__top">
            <span>{{ title }}</span>
            <AppIcon :name="icon" class="power-flow-node__icon" />
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
.power-flow-node {
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

.power-flow-node__top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
}

.power-flow-node span {
    color: var(--text-color--secondary);
    font-size: 15px;
    font-weight: 700;
}

.power-flow-node__icon {
    flex: 0 0 auto;
    width: 34px;
    height: 34px;
    color: var(--secondary-color);
    filter: drop-shadow(0 0 8px rgba(21, 224, 183, 0.35));
}

.power-flow-node strong {
    font-size: 28px;
    line-height: 32px;
}

.power-flow-node strong small {
    font-size: 14px;
}

.power-flow-node em {
    color: var(--secondary-color);
    font-size: 15px;
    font-weight: 700;
    font-style: normal;
}

.power-flow-node--solar {
    top: 10%;
    left: 7%;
}

.power-flow-node--load {
    top: 10%;
    right: 7%;
}

.power-flow-node--grid {
    right: 7%;
    bottom: 10%;
}
</style>
