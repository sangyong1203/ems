<template>
    <article class="power-battery">
        <div class="power-battery__meta">
            <div class="power-battery__title">
                <span>ESS</span>
            </div>
            <strong>{{ powerValue }} <small>kW</small></strong>
            <em>{{ status }}</em>
        </div>

        <div class="power-battery__visual">
            <AppIcon
                name="IconBatteryCharging"
                class="power-battery__charge-icon"
                :class="{ 'is-charging': isCharging }"
            />
            <div class="power-battery__shape" :aria-label="`ESS SOC ${soc}%`">
                <div class="power-battery__body">
                    <span
                        v-for="cell in CELL_COUNT"
                        :key="cell"
                        class="power-battery__cell"
                        :class="{ 'is-active': cell <= activeCellCount }"
                    ></span>
                </div>
                <div class="power-battery__head"></div>
            </div>
        </div>

        <span class="power-battery__soc">SOC {{ normalizedSoc }}%</span>
    </article>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import AppIcon from '@/shared/components/widget/AppIcon.vue'

const CELL_COUNT = 5

const props = defineProps<{
    soc: number
    powerText: string
    status: string
    isCharging: boolean
}>()

const normalizedSoc = computed(() => {
    return Math.min(100, Math.max(0, Math.round(props.soc || 0)))
})

const activeCellCount = computed(() => {
    if (normalizedSoc.value <= 0) {
        return 0
    }
    return Math.ceil(normalizedSoc.value / 20)
})

const powerValue = computed(() => props.powerText.replace(/\s*kW$/i, ''))
</script>

<style scoped lang="scss">
.power-battery {
    position: absolute;
    z-index: 3;
    display: flex;
    align-items: center;
    gap: 8px;
    width: 300px;
    height: 128px;
    padding: 18px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    background: linear-gradient(135deg, rgba(21, 224, 183, 0.13), rgba(231, 109, 255, 0.1)), rgba(255, 255, 255, 0.05);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.power-battery__meta {
    flex: 1 1 auto;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 8px;
    min-width: 0;
}

.power-battery__title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
}

.power-battery__meta span,
.power-battery__soc {
    color: var(--text-color--secondary);
    font-size: 15px;
    font-weight: 700;
}

.power-battery__charge-icon {
    flex: 0 0 auto;
    width: 28px;
    height: 28px;
    color: rgba(255, 255, 255, 0.22);
}

.power-battery__charge-icon.is-charging {
    color: var(--secondary-color);
    filter: drop-shadow(0 0 8px rgba(21, 224, 183, 0.45));
}

.power-battery__meta strong {
    color: #ffffff;
    font-size: 28px;
    line-height: 32px;
}

.power-battery__meta strong small {
    font-size: 14px;
}

.power-battery__meta em {
    color: var(--secondary-color);
    font-size: 15px;
    font-weight: 700;
    font-style: normal;
}

.power-battery__visual {
    flex: 0 0 auto;
    display: flex;
    align-items: center;
}

.power-battery__shape {
    display: flex;
    align-items: center;
    gap: 4px;
}

.power-battery__body {
    display: flex;
    align-items: stretch;
    gap: 4px;
    width: 98px;
    height: 48px;
    padding: 5px;
    border: 2px solid rgba(255, 255, 255, 0.28);
    border-radius: 7px;
    background: rgba(6, 10, 20, 0.44);
    box-shadow:
        inset 0 0 12px rgba(0, 0, 0, 0.28),
        0 0 18px rgba(21, 224, 183, 0.1);
}

.power-battery__head {
    width: 8px;
    height: 22px;
    border-radius: 0 4px 4px 0;
    background: rgba(255, 255, 255, 0.32);
}

.power-battery__cell {
    flex: 1 1 0;
    border-radius: 3px;
    background: rgba(255, 255, 255, 0.1);
}

.power-battery__cell.is-active {
    background: linear-gradient(180deg, var(--secondary-color), var(--primary-color));
    box-shadow: 0 0 10px rgba(21, 224, 183, 0.45);
}

.power-battery__soc {
    position: absolute;
    right: 18px;
    bottom: 12px;
    color: var(--secondary-color);
    font-weight: 700;
}
</style>
