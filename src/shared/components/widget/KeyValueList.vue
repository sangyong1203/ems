<template>
    <dl class="key-value-list">
        <div v-for="item in items" :key="item.label">
            <dt>{{ item.label }}</dt>
            <dd>{{ item.value }}</dd>
        </div>
    </dl>
</template>

<script setup lang="ts">
export type KeyValueItem = {
    label: string
    value: string
}

defineProps<{
    items: KeyValueItem[]
}>()
</script>

<style scoped lang="scss">
.key-value-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin: 0;
    min-height: 0;
}

.key-value-list div {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border-color);
}

.key-value-list dt,
.key-value-list dd {
    margin: 0;
}

.key-value-list dt {
    color: var(--text-color--secondary);
    font-size: 13px;
}

.key-value-list dd {
    color: #ffffff;
    font-size: 14px;
    text-align: right;
}
</style>
