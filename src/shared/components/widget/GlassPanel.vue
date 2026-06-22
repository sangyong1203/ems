<template>
    <article class="glass-panel">
        <header v-if="title || subtitle || value || $slots.headerRight" class="glass-panel__header">
            <div class="glass-panel__heading" :class="`glass-panel__heading--${subtitlePosition}`">
                <h2 v-if="title">{{ title }}</h2>
                <span v-if="subtitle">{{ subtitle }}</span>
            </div>
            <div v-if="$slots.headerRight" class="glass-panel__header-right">
                <slot name="headerRight"></slot>
            </div>
            <strong v-else-if="value">{{ value }}</strong>
        </header>
        <div class="glass-panel__body">
            <slot></slot>
        </div>
    </article>
</template>

<script setup lang="ts">
withDefaults(
    defineProps<{
        title?: string
        subtitle?: string
        subtitlePosition?: 'right' | 'bottom'
        value?: string
    }>(),
    {
        subtitlePosition: 'bottom',
    },
)
</script>

<style scoped lang="scss">
.glass-panel {
    position: relative;
    display: flex;
    flex-direction: column;
    min-height: 0;
    padding: 20px;
    overflow: hidden;
    border: 1px solid rgb(61 61 61 / 24%);
    border-radius: 8px;
    box-shadow:
        0 7px 12px rgba(0, 0, 0, 0.28),
        0 0 18px rgba(231, 109, 255, 0.08),
        inset 0 1px 0 rgb(255 255 255 / 10%);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    background: #ffffff0a;
}

.glass-panel__header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 18px;
    margin-bottom: 14px;
}

.glass-panel__header h2 {
    margin: 0;
    font-size: 18px;
    letter-spacing: 0;
}

.glass-panel__header span {
    color: var(--text-color--secondary);
    font-size: 13px;
}

.glass-panel__header strong {
    color: var(--secondary-color);
    white-space: nowrap;
}

.glass-panel__header-right {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 10px;
    min-width: 0;
}

.glass-panel__heading {
    display: flex;
    min-width: 0;
}

.glass-panel__heading--bottom {
    flex-direction: column;
    gap: 5px;
}

.glass-panel__heading--right {
    display: flex;
    align-items: flex-end;
    gap: 10px;
    flex-wrap: wrap;
}

.glass-panel__heading--right h2,
.glass-panel__heading--right span {
    white-space: nowrap;
}

.glass-panel__body {
    display: flex;
    flex: 1 1 auto;
    flex-direction: column;
    min-width: 0;
    min-height: 0;
    overflow: auto;
    margin-right: -14px;
    padding-right: 6px;
}
</style>
