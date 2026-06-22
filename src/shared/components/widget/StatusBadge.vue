<template>
    <span class="status-badge" :class="variantClass" :style="{ minWidth }">
        {{ label || '-' }}
    </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

type StatusBadgeVariant = 'success' | 'warning' | 'danger' | 'info' | 'progress' | 'muted'

const props = withDefaults(
    defineProps<{
        label: string
        variant?: StatusBadgeVariant
        minWidth?: string
    }>(),
    {
        variant: 'muted',
        minWidth: '52px',
    },
)

const variantClass = computed(() => `is-${props.variant}`)
</script>

<style scoped lang="scss">
.status-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex: 0 0 auto;
    height: 24px;
    padding: 0 10px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 800;
    line-height: 1;
    text-align: center;
    white-space: nowrap;
}

.status-badge.is-success {
    color: var(--secondary-color);
    border: 1px solid rgba(21, 224, 183, 0.42);
    background: rgba(21, 224, 183, 0.1);
}

.status-badge.is-warning {
    color: #f6bd60;
    border: 1px solid rgba(246, 189, 96, 0.44);
    background: rgba(246, 189, 96, 0.1);
}

.status-badge.is-danger {
    color: #ff6b6b;
    border: 1px solid rgba(255, 107, 107, 0.46);
    background: rgba(255, 107, 107, 0.1);
}

.status-badge.is-info {
    color: #8cc8ff;
    border: 1px solid rgba(140, 200, 255, 0.38);
    background: rgba(140, 200, 255, 0.1);
}

.status-badge.is-progress {
    color: var(--primary-color);
    border: 1px solid rgba(231, 109, 255, 0.46);
    background: rgba(231, 109, 255, 0.12);
}

.status-badge.is-muted {
    color: var(--text-color--secondary);
    border: 1px solid rgba(255, 255, 255, 0.18);
    background: rgba(255, 255, 255, 0.06);
}
</style>
