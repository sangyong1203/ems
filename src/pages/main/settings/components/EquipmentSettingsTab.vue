<template>
    <div class="settings-equipment">
        <section class="settings-equipment__section">
            <h3>설비 용량</h3>
            <p>장비 관리 화면의 정격 용량과 운영 활성화 상태를 기준으로 자동 집계합니다.</p>
            <div class="equipment-card-list">
                <article v-for="item in capacities" :key="item.key" class="equipment-card equipment-card--capacity">
                    <span>{{ item.label }}</span>
                    <strong
                        >{{ formatNumber(item.value) }}<small>{{ item.unit }}</small></strong
                    >
                </article>
            </div>
        </section>

        <section class="settings-equipment__section">
            <h3>등록 장비 현황</h3>
            <p>장비 수량은 장비 관리 화면의 등록 데이터를 기준으로 집계합니다.</p>
            <div class="equipment-card-list">
                <article v-for="item in counts" :key="item.key" class="equipment-card">
                    <span>{{ item.label }}</span>
                    <strong>{{ item.active }}/{{ item.total }}<small>대</small></strong>
                </article>
            </div>
        </section>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { DeviceCounts, EquipmentCapacities } from '../service/settings.types'

const props = defineProps<{
    deviceCounts: DeviceCounts
    activeDeviceCounts: DeviceCounts
    capacitySummary: EquipmentCapacities
}>()

const counts = computed(() => [
    { key: 'INVERTER', label: '인버터', active: props.activeDeviceCounts.INVERTER, total: props.deviceCounts.INVERTER },
    { key: 'PCS', label: 'PCS', active: props.activeDeviceCounts.PCS, total: props.deviceCounts.PCS },
    {
        key: 'ESS_BATTERY',
        label: '배터리 뱅크',
        active: props.activeDeviceCounts.ESS_BATTERY,
        total: props.deviceCounts.ESS_BATTERY,
    },
    {
        key: 'BATTERY_RACK',
        label: '배터리 랙',
        active: props.activeDeviceCounts.BATTERY_RACK,
        total: props.deviceCounts.BATTERY_RACK,
    },
    { key: 'BMS', label: 'BMS', active: props.activeDeviceCounts.BMS, total: props.deviceCounts.BMS },
    { key: 'AC_PANEL', label: 'AC 배전반', active: props.activeDeviceCounts.AC_PANEL, total: props.deviceCounts.AC_PANEL },
    { key: 'METER', label: '계량기', active: props.activeDeviceCounts.METER, total: props.deviceCounts.METER },
])

const capacities = computed(() => [
    { key: 'solarInstalled', label: '태양광 설치 용량', value: props.capacitySummary.solarInstalledKw, unit: 'kW' },
    {
        key: 'solarOperating',
        label: '태양광 운영 가능 용량',
        value: props.capacitySummary.solarOperatingKw,
        unit: 'kW',
    },
    { key: 'essInstalled', label: 'ESS 설치 용량', value: props.capacitySummary.essInstalledKwh, unit: 'kWh' },
    { key: 'essOperating', label: 'ESS 운영 가능 용량', value: props.capacitySummary.essOperatingKwh, unit: 'kWh' },
])

const formatNumber = (value: number) => Number(value).toLocaleString(undefined, { maximumFractionDigits: 1 })
</script>

<style scoped lang="scss">
.settings-equipment {
    max-width: 980px;
}

.settings-equipment__section + .settings-equipment__section {
    margin-top: 26px;
}

.settings-equipment h3 {
    margin: 0 0 8px;
    font-size: 16px;
}

.settings-equipment p {
    margin: 0;
    color: var(--text-color--secondary);
    font-size: 13px;
}

.equipment-card-list {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 16px;
}

.equipment-card {
    display: flex;
    width: 46%;
    align-items: center;
    justify-content: space-between;
    gap: 18px;
    min-height: 76px;
    padding: 16px;
    border: 1px solid rgb(255 255 255 / 10%);
    border-radius: 6px;
    background: rgb(255 255 255 / 4%);
}

.equipment-card span {
    color: var(--text-color--secondary);
}

.equipment-card--capacity span {
    min-width: 124px;
    white-space: nowrap;
}

.equipment-card strong {
    color: var(--secondary-color);
    font-size: 24px;
    white-space: nowrap;
}

.equipment-card small {
    margin-left: 4px;
    font-size: 13px;
}
</style>
