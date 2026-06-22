<template>
    <div class="table-row-actions">
        <button
            class="table-row-actions__button"
            type="button"
            aria-label="수정"
            title="수정"
            @click.stop="emit('edit')"
        >
            <el-icon><Edit /></el-icon>
        </button>
        <button
            class="table-row-actions__button is-danger"
            type="button"
            aria-label="삭제"
            title="삭제"
            @click.stop="emit('delete')"
        >
            <el-icon><Delete /></el-icon>
        </button>
    </div>
</template>

<script setup lang="ts">
import { Delete, Edit } from '@element-plus/icons-vue'

const emit = defineEmits<{
    edit: []
    delete: []
}>()
</script>

<style scoped lang="scss">
.table-row-actions {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    width: 100%;
    min-height: 48px;
}

.table-row-actions__button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    padding: 0;
    border: 0;
    border-radius: 8px;
    background: transparent;
    color: var(--secondary-color);
    font-size: 16px;
    cursor: pointer;
    transition:
        background 0.18s ease,
        color 0.18s ease;
}

.table-row-actions__button.is-danger {
    color: #ff8a8a;
}

.table-row-actions__button:hover {
    background: rgba(21, 224, 183, 0.16);
}

.table-row-actions__button.is-danger:hover {
    background: rgba(255, 107, 107, 0.16);
}
</style>
