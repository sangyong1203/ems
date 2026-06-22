<template>
    <section class="alarm-history-page">
        <MetricCardRow :items="kpiItems" />

        <div class="alarm-history-content">
            <GlassPanel class="alarm-panel alarm-panel--list" title="알림 이력" :value="`${alarms.length}건`">
                <div class="alarm-toolbar">
                    <div class="alarm-toolbar__filters">
                        <SearchText
                            v-model="searchParams.keyword"
                            placeholder="장비명, 유형, 메시지 검색"
                            width="220px"
                            @on-enter="getAlarms"
                        />
                        <DropdownList
                            v-model="searchParams.deviceId"
                            placeholder="대상 장비"
                            width="130px"
                            :list="deviceFilterOptions"
                            option-label="label"
                            option-value="value"
                            @on-change="getAlarms"
                        />
                        <DropdownList
                            v-model="searchParams.severity"
                            placeholder="등급"
                            width="95px"
                            :list="severityFilterOptions"
                            option-label="label"
                            option-value="value"
                            @on-change="getAlarms"
                        />
                        <DropdownList
                            v-model="searchParams.alarmType"
                            placeholder="알림 유형"
                            width="120px"
                            :list="alarmTypeFilterOptions"
                            option-label="label"
                            option-value="value"
                            @on-change="getAlarms"
                        />
                        <DropdownList
                            v-model="searchParams.status"
                            placeholder="조치 상태"
                            width="120px"
                            :list="statusFilterOptions"
                            option-label="label"
                            option-value="value"
                            @on-change="getAlarms"
                        />
                        <el-date-picker
                            v-model="dateRange"
                            class="alarm-date-range"
                            type="daterange"
                            value-format="YYYY-MM-DD"
                            start-placeholder="시작일"
                            end-placeholder="종료일"
                            @change="changeDateRange"
                        />
                    </div>
                </div>

                <div class="alarm-table-wrap">
                    <el-table
                        class="alarm-table"
                        :data="alarms"
                        height="100%"
                        highlight-current-row
                        :current-row-key="selectedAlarm?.id"
                        row-key="id"
                        :tooltip-options="{ hideAfter: 0 }"
                        @row-click="selectAlarm"
                    >
                        <el-table-column prop="occurred_at" label="발생 시간" min-width="150">
                            <template #default="{ row }">{{ formatDateTime(row.occurred_at) }}</template>
                        </el-table-column>
                        <el-table-column prop="severity" label="등급" min-width="80" align="center">
                            <template #default="{ row }">
                                <StatusBadge
                                    :label="severityLabel(row.severity)"
                                    :variant="severityVariant(row.severity)"
                                    min-width="56px"
                                />
                            </template>
                        </el-table-column>
                        <el-table-column prop="alarm_type" label="유형" min-width="110" />
                        <el-table-column prop="device_name" label="장비명" min-width="120" show-overflow-tooltip>
                            <template #default="{ row }">{{ row.device_name || '-' }}</template>
                        </el-table-column>
                        <el-table-column prop="message" label="메시지" min-width="220" show-overflow-tooltip />
                        <el-table-column label="조치 상태" min-width="100" align="center">
                            <template #default="{ row }">
                                <StatusBadge
                                    :label="actionStatusLabel(row)"
                                    :variant="actionStatusVariant(row)"
                                    min-width="56px"
                                />
                            </template>
                        </el-table-column>
                        <el-table-column label="동작" width="140" align="center" fixed="right">
                            <template #default="{ row }">
                                <AlarmRowActions
                                    :alarm="row"
                                    @ack="ackAlarm(row)"
                                    @maintenance="createMaintenance(row)"
                                />
                            </template>
                        </el-table-column>
                    </el-table>
                </div>
            </GlassPanel>

            <AlarmDetailPanel
                :alarm="selectedAlarm"
                @ack="selectedAlarm && ackAlarm(selectedAlarm)"
                @maintenance="selectedAlarm && createMaintenance(selectedAlarm)"
            />
        </div>
    </section>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { DropdownList, GlassPanel, MetricCardRow, SearchText, StatusBadge } from '@/shared/components'
import { isSuccessResponse } from '@/shared/utils'
import AlarmDetailPanel from './components/AlarmDetailPanel.vue'
import AlarmRowActions from './components/AlarmRowActions.vue'
import alarmHistoryApi from './service/alarmHistory.api'
import type { AlarmActionStatus, AlarmDeviceOption, AlarmItem } from './service/alarmHistory.types'

const alarms = ref<AlarmItem[]>([])
const selectedAlarm = ref<AlarmItem | null>(null)
const deviceOptions = ref<AlarmDeviceOption[]>([])

const searchParams = reactive({
    keyword: '',
    deviceId: null as number | null,
    severity: '',
    alarmType: '',
    status: '',
    dateFrom: '',
    dateTo: '',
})
const dateRange = ref<[string, string] | null>(null)

const severityOptions = [
    { label: '정보', value: 'INFO' },
    { label: '주의', value: 'WARNING' },
    { label: '심각', value: 'CRITICAL' },
]

const statusOptions = [
    { label: '미확인', value: 'OPEN' },
    { label: '확인됨', value: 'ACKED' },
    { label: '정비등록', value: 'SCHEDULED' },
    { label: '조치중', value: 'IN_PROGRESS' },
    { label: '조치완료', value: 'COMPLETED' },
    { label: '보류', value: 'HOLD' },
    { label: '취소', value: 'CANCELED' },
]

const alarmTypeOptions = [
    { label: '인버터 장애', value: '인버터 장애' },
    { label: '통신 장애', value: '통신 장애' },
    { label: '발전량 저하', value: '발전량 저하' },
    { label: 'ESS 과온', value: 'ESS 과온' },
    { label: 'SOC 낮음', value: 'SOC 낮음' },
    { label: 'PCS 장애', value: 'PCS 장애' },
    { label: 'PCS 상태', value: 'PCS 상태' },
    { label: 'BMS 경고', value: 'BMS 경고' },
    { label: '계량기 오류', value: '계량기 오류' },
    { label: '데이터 수신 지연', value: '데이터 수신 지연' },
]

const deviceFilterOptions = computed(() => [
    { label: '전체 장비', value: null },
    ...deviceOptions.value.map(item => ({ label: item.name, value: item.id })),
])
const severityFilterOptions = computed(() => [{ label: '전체 등급', value: '' }, ...severityOptions])
const alarmTypeFilterOptions = computed(() => [{ label: '전체 유형', value: '' }, ...alarmTypeOptions])
const statusFilterOptions = computed(() => [{ label: '전체 상태', value: '' }, ...statusOptions])

const openCount = computed(() => alarms.value.filter(item => getActionStatus(item) === 'OPEN').length)
const ackedCount = computed(() => alarms.value.filter(item => getActionStatus(item) === 'ACKED').length)
const activeMaintenanceCount = computed(
    () => alarms.value.filter(item => ['SCHEDULED', 'IN_PROGRESS'].includes(getActionStatus(item))).length,
)

const kpiItems = computed(() => [
    { label: '전체 알림', value: String(alarms.value.length), unit: '건', hint: '발생 이력', variant: 'is-total' },
    { label: '미확인', value: String(openCount.value), unit: '건', hint: '확인 필요', variant: 'is-open' },
    { label: '확인됨', value: String(ackedCount.value), unit: '건', hint: '확인 완료', variant: 'is-acked' },
    {
        label: '정비진행',
        value: String(activeMaintenanceCount.value),
        unit: '건',
        hint: '등록/진행',
        variant: 'is-progress',
    },
])

const severityLabel = (value: string) => severityOptions.find(item => item.value === value)?.label || value || '-'

const severityVariant = (value: string) => {
    if (value === 'CRITICAL') {
        return 'danger'
    }
    if (value === 'WARNING') {
        return 'warning'
    }
    return 'info'
}

const getActionStatus = (alarm: AlarmItem): AlarmActionStatus => {
    if (alarm.maintenance_status) {
        return alarm.maintenance_status as AlarmActionStatus
    }
    return alarm.status === 'OPEN' ? 'OPEN' : 'ACKED'
}

const actionStatusLabel = (alarm: AlarmItem) => {
    const status = getActionStatus(alarm)
    return statusOptions.find(item => item.value === status)?.label || status || '-'
}

const actionStatusVariant = (alarm: AlarmItem) => {
    const status = getActionStatus(alarm)
    if (status === 'COMPLETED') {
        return 'success'
    }
    if (status === 'SCHEDULED' || status === 'IN_PROGRESS') {
        return 'progress'
    }
    if (status === 'HOLD' || status === 'CANCELED') {
        return 'muted'
    }
    if (status === 'ACKED') {
        return 'info'
    }
    return 'warning'
}

const formatDateTime = (value: string | null | undefined) => {
    return value ? value.replace('T', ' ').slice(0, 19) : '-'
}

const selectAlarm = (alarm: AlarmItem) => {
    selectedAlarm.value = alarm
}

const changeDateRange = (value: [string, string] | null) => {
    searchParams.dateFrom = value?.[0] || ''
    searchParams.dateTo = value?.[1] || ''
    getAlarms()
}

const getDevices = async () => {
    const res = await alarmHistoryApi.getDevices()
    if (isSuccessResponse(res.result)) {
        deviceOptions.value = res.data.list
    }
}

const getAlarms = async () => {
    const res = await alarmHistoryApi.getList(searchParams)
    if (isSuccessResponse(res.result)) {
        alarms.value = res.data.list
        if (!alarms.value.length) {
            selectedAlarm.value = null
            return
        }
        const selectedId = selectedAlarm.value?.id
        selectedAlarm.value = alarms.value.find(item => item.id === selectedId) ?? alarms.value[0]
    }
}

const refreshAfterAction = async (alarmId: number) => {
    await getAlarms()
    selectedAlarm.value = alarms.value.find(item => item.id === alarmId) ?? selectedAlarm.value
}

const ackAlarm = async (alarm: AlarmItem) => {
    await alarmHistoryApi.acknowledge(alarm.id)
    await refreshAfterAction(alarm.id)
}

const createMaintenance = async (alarm: AlarmItem) => {
    await alarmHistoryApi.createMaintenance(alarm.id)
    ElMessage.success('정비 이력이 등록되었습니다.')
    await refreshAfterAction(alarm.id)
}

watch(
    () => searchParams.keyword,
    (keyword, prevKeyword) => {
        if (prevKeyword && !keyword.trim()) {
            getAlarms()
        }
    },
)

onMounted(async () => {
    await getDevices()
    await getAlarms()
})
</script>

<style scoped lang="scss">
.alarm-history-page {
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 14px;
    width: 100%;
    height: 100%;
    min-width: 1180px;
    min-height: 0;
    padding: 10px 12px 14px;
    overflow: hidden;
    color: var(--text-color--primary);
}

.alarm-history-content {
    flex: 1 1 auto;
    display: flex;
    gap: 14px;
    overflow: hidden;
    min-height: 0;
}

.alarm-panel {
    min-height: 0;
}

.alarm-panel--list {
    flex: 1;
    min-width: 0;
}

.alarm-toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    margin-bottom: 14px;
}

.alarm-toolbar__filters {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
    min-width: 0;
}

:deep(.alarm-date-range) {
    flex: 1;
    max-width: 360px !important;
}

.alarm-table-wrap {
    flex: 1;
    min-height: 0;
}

@media (max-width: 1180px), (orientation: portrait) {
    .alarm-history-page {
        min-width: 0;
        height: auto;
        min-height: 100%;
        overflow: auto;
    }

    .alarm-history-content {
        flex-direction: column;
        overflow: visible;
        min-height: auto;
    }

    .alarm-panel--list {
        flex: 0 0 auto;
    }

    .alarm-toolbar {
        align-items: stretch;
    }

    .alarm-toolbar__filters {
        width: 100%;
    }

    :deep(.alarm-toolbar__filters .search-text) {
        flex: 1 1 220px;
    }

    :deep(.alarm-toolbar__filters .dropdown-list) {
        flex: 1 1 120px;
    }

    :deep(.alarm-date-range) {
        flex: 1 1 280px;
        max-width: none !important;
    }

    .alarm-table-wrap {
        min-height: 420px;
        max-height: 800px;
    }
}

@media (max-width: 760px), (orientation: portrait) and (max-width: 900px) {
    .alarm-history-page {
        padding: 8px;
    }

    .alarm-toolbar__filters {
        gap: 8px;
    }

    :deep(.alarm-toolbar__filters .search-text),
    :deep(.alarm-toolbar__filters .dropdown-list),
    :deep(.alarm-date-range) {
        flex: 1 1 100%;
        width: 100% !important;
    }

    .alarm-table-wrap {
        min-height: 360px;
    }
}
</style>
