<template>
    <article
        class="ess-battery"
        :class="[
            `ess-battery--icon-${iconPosition}`,
            `ess-battery--visual-${batteryPosition}`,
            { 'is-compact': compact },
        ]"
    >
        <div v-if="!compact" class="ess-battery__main">
            <span class="ess-battery__label">SOC</span>
            <strong>{{ normalizedSoc }}<small>%</small></strong>
            <em>{{ modeLabel }}</em>
        </div>

        <div class="ess-battery__visual">
            <AppIcon
                name="IconBatteryCharging"
                class="ess-battery__charge-icon"
                :class="{ 'is-active': mode === 'CHARGING' }"
            />
            <div class="ess-battery__shape" :aria-label="`ESS SOC ${normalizedSoc}%`">
                <div class="ess-battery__body">
                    <span
                        v-for="cell in CELL_COUNT"
                        :key="cell"
                        class="ess-battery__cell"
                        :class="{ 'is-active': cell <= activeCellCount }"
                    ></span>
                </div>
                <div class="ess-battery__head"></div>
            </div>
        </div>
    </article>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import AppIcon from '@/shared/components/widget/AppIcon.vue'

const CELL_COUNT = 5

const props = withDefaults(
    defineProps<{
        soc: number
        mode: string
        compact?: boolean
        iconPosition?: 'left' | 'right'
        batteryPosition?: 'left' | 'right'
    }>(),
    {
        compact: false,
        iconPosition: 'left',
        batteryPosition: 'right',
    },
)

const normalizedSoc = computed(() => Math.min(100, Math.max(0, Math.round(props.soc || 0))))

const activeCellCount = computed(() => {
    if (normalizedSoc.value <= 0) {
        return 0
    }
    return Math.ceil(normalizedSoc.value / 20)
})

const modeLabel = computed(() => {
    if (props.mode === 'CHARGING') {
        return '충전 중'
    }
    if (props.mode === 'DISCHARGING') {
        return '방전 중'
    }
    return '대기'
})
</script>

<style scoped lang="scss">
.ess-battery {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 22px;
    min-height: 138px;
    padding: 18px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    background: linear-gradient(135deg, rgba(21, 224, 183, 0.13), rgba(231, 109, 255, 0.1)), rgba(255, 255, 255, 0.05);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.ess-battery--visual-left {
    flex-direction: row-reverse;
}

.ess-battery__main {
    display: flex;
    flex-direction: column;
    gap: 7px;
    min-width: 0;
}

.ess-battery__label {
    color: var(--text-color--secondary);
    font-size: 13px;
    font-weight: 700;
}

.ess-battery__main strong {
    color: #ffffff;
    font-size: 48px;
    line-height: 52px;
}

.ess-battery__main small {
    margin-left: 3px;
    color: var(--text-color--secondary);
    font-size: 18px;
}

.ess-battery__main em {
    color: var(--secondary-color);
    font-size: 15px;
    font-style: normal;
    font-weight: 700;
}

.ess-battery__visual {
    display: flex;
    align-items: center;
    gap: 10px;
}

.ess-battery--icon-right .ess-battery__visual {
    flex-direction: row-reverse;
}

.ess-battery__charge-icon {
    width: 30px;
    height: 30px;
    color: rgba(255, 255, 255, 0.24);
}

.ess-battery__charge-icon.is-active {
    color: var(--secondary-color);
    filter: drop-shadow(0 0 8px rgba(21, 224, 183, 0.45));
}

.ess-battery__shape {
    display: flex;
    align-items: center;
    gap: 5px;
}

.ess-battery__body {
    display: flex;
    align-items: stretch;
    gap: 5px;
    width: 150px;
    height: 70px;
    padding: 7px;
    border: 2px solid rgba(255, 255, 255, 0.28);
    border-radius: 8px;
    background: rgba(6, 10, 20, 0.44);
    box-shadow:
        inset 0 0 12px rgba(0, 0, 0, 0.28),
        0 0 18px rgba(21, 224, 183, 0.1);
}

.ess-battery__head {
    width: 10px;
    height: 32px;
    border-radius: 0 5px 5px 0;
    background: rgba(255, 255, 255, 0.32);
}

.ess-battery__cell {
    flex: 1 1 0;
    border-radius: 4px;
    background: rgba(255, 255, 255, 0.1);
}

.ess-battery__cell.is-active {
    background: linear-gradient(180deg, var(--secondary-color), var(--primary-color));
    box-shadow: 0 0 10px rgba(21, 224, 183, 0.45);
}

.ess-battery.is-compact {
    justify-content: flex-start;
    gap: 0;
    min-height: 0;
    padding: 0;
    border: 0;
    background: transparent;
    box-shadow: none;
}

.ess-battery.is-compact .ess-battery__visual {
    gap: 5px;
}

.ess-battery.is-compact .ess-battery__charge-icon {
    width: 18px;
    height: 18px;
}

.ess-battery.is-compact .ess-battery__body {
    gap: 3px;
    width: 74px;
    height: 34px;
    padding: 4px;
    border-width: 1px;
    border-radius: 5px;
}

.ess-battery.is-compact .ess-battery__head {
    width: 5px;
    height: 16px;
    border-radius: 0 3px 3px 0;
}

.ess-battery.is-compact .ess-battery__cell {
    border-radius: 2px;
}

@media (max-width: 760px) {
    .ess-battery {
        align-items: flex-start;
        flex-direction: column;
    }

    .ess-battery--visual-left {
        flex-direction: column-reverse;
    }
}
</style>
