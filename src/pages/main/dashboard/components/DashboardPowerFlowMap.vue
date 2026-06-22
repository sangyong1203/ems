<template>
    <div class="dashboard-power-flow-map">
        <DashboardPowerFlowLine variant="solar-load" :value="data?.flows.solarToLoadKw ?? 0" />
        <DashboardPowerFlowLine variant="solar-ess" :value="data?.flows.solarToEssKw ?? 0" />
        <DashboardPowerFlowLine variant="ess-load" :value="data?.flows.essToLoadKw ?? 0" />
        <DashboardPowerFlowLine variant="grid-load" :value="data?.flows.gridImportKw ?? 0" suffix="수전" />
        <DashboardPowerFlowLine variant="solar-grid" :value="data?.flows.solarToGridKw ?? 0" />
        <DashboardPowerFlowLine variant="ess-grid" :value="data?.flows.essToGridKw ?? 0" />

        <DashboardPowerFlowNode
            variant="solar"
            title="태양광"
            :value="formatNumber(data?.nodes.solar.powerKw)"
            unit="kW"
            :status="statusLabel(data?.nodes.solar.status)"
            icon="IconSolar"
        />

        <DashboardPowerBattery
            class="dashboard-power-flow-map__battery"
            :soc="data?.nodes.ess.soc ?? 0"
            :power-text="`${formatNumber(essPower)} kW`"
            :status="statusLabel(data?.nodes.ess.status)"
            :is-charging="data?.nodes.ess.status === 'CHARGING'"
        />

        <DashboardPowerFlowNode
            variant="load"
            title="부하"
            :value="formatNumber(data?.nodes.load.powerKw)"
            unit="kW"
            :status="statusLabel(data?.nodes.load.status)"
            icon="IconEnergyLoad"
        />

        <DashboardPowerFlowNode
            variant="grid"
            title="계통"
            :value="gridPowerValue"
            unit="kW"
            :status="statusLabel(data?.nodes.grid.status)"
            icon="IconElectricGrid"
        />
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import DashboardPowerBattery from './DashboardPowerBattery.vue'
import DashboardPowerFlowLine from './DashboardPowerFlowLine.vue'
import DashboardPowerFlowNode from './DashboardPowerFlowNode.vue'
import type { DashboardPowerFlow } from '../service/dashboard.types'

const props = defineProps<{
    data: DashboardPowerFlow | null
}>()

const formatNumber = (value?: number) => {
    return Number(value ?? 0).toLocaleString(undefined, { maximumFractionDigits: 1 })
}

const essPower = computed(() => {
    return props.data?.nodes.ess.chargeKw || props.data?.nodes.ess.dischargeKw || 0
})

const gridPowerValue = computed(() => {
    return formatNumber(props.data?.nodes.grid.exportKw || props.data?.nodes.grid.importKw)
})

const statusLabel = (status?: string) => {
    const labels: Record<string, string> = {
        GENERATING: '발전 중',
        CONSUMING: '사용 중',
        CHARGING: '충전',
        DISCHARGING: '방전',
        IMPORT: '수전',
        EXPORT: '송전',
        BALANCED: '균형',
        IDLE: '대기',
        STANDBY: '대기',
    }
    return labels[status ?? ''] ?? status ?? '-'
}
</script>

<style scoped lang="scss">
.dashboard-power-flow-map {
    position: relative;
    flex: 1;
    min-height: 0;
    overflow: hidden;
}

.dashboard-power-flow-map__battery {
    bottom: 2%;
    left: 45%;
}
</style>
