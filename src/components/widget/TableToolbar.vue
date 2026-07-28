<template>
    <div class="table-toolbar">
        <div class="table-toolbar__filters">
            <slot />
        </div>
        <div v-if="$slots.actions" class="table-toolbar__actions">
            <slot name="actions" />
        </div>
    </div>
</template>

<style scoped>
.table-toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    margin-bottom: 14px;
}

.table-toolbar__filters {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
    min-width: 0;
}

.table-toolbar__actions {
    display: flex;
    align-items: center;
    gap: 10px;
    flex: 0 0 auto;
}

@media (max-width: 1180px), (orientation: portrait) {
    .table-toolbar {
        align-items: flex-start;
        flex-wrap: wrap;
    }

    .table-toolbar__filters {
        flex: 1 1 540px;
    }
}

@media (max-width: 760px), (orientation: portrait) and (max-width: 900px) {
    .table-toolbar {
        gap: 10px;
    }

    .table-toolbar__filters,
    .table-toolbar__actions {
        width: 100%;
    }
}
</style>
