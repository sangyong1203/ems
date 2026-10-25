<template>
    <section class="alarm-history-page">
        <MetricCardRow :items="kpiItems" />

        <div class="alarm-history-content">
            <GlassPanel class="alarm-panel alarm-panel--list" title="알림 이력" :value="`${alarms.length}건`">
                <TableToolbar>
                    <SearchText
                        v-model="searchParams.keyword"
                        placeholder="장비명, 유형, 메시지 검색"
                        width="220px"
                        @on-enter="searchAlarms"
                    />
                    <DropdownList
                        v-model="searchParams.deviceId"
                        placeholder="대상 장비"
                        width="130px"
                        :list="deviceFilterOptions"
                        option-label="label"
                        option-value="value"
                        @on-change="searchAlarms"
                    />
                    <DropdownList
                        v-model="searchParams.severity"
                        placeholder="등급"
                        width="95px"
                        :list="severityFilterOptions"
                        option-label="label"
                        option-value="value"
                        @on-change="searchAlarms"
                    />
                    <DropdownList
                        v-model="searchParams.alarmType"
                        placeholder="알림 유형"
                        width="120px"
                        :list="alarmTypeFilterOptions"
                        option-label="label"
                        option-value="value"
                        @on-change="searchAlarms"
                    />
                    <DropdownList
                        v-model="searchParams.status"
                        placeholder="조치 상태"
                        width="120px"
                        :list="statusFilterOptions"
                        option-label="label"
                        option-value="value"
                        @on-change="searchAlarms"
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
                </TableToolbar>

                <div class="alarm-table-wrap">
                    <el-table
                        class="alarm-table"
                        :data="pagedAlarms"
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
                                    :label="actionStatusLabel(row as AlarmItem)"
                                    :variant="actionStatusVariant(row as AlarmItem)"
                                    min-width="56px"
                                />
                            </template>
                        </el-table-column>
                        <el-table-column label="동작" width="140" align="center" fixed="right">
                            <template #default="{ row }">
                                <AlarmRowActions
                                    :alarm="row as AlarmItem"
                                    @ack="ackAlarm(row as AlarmItem)"
                                    @maintenance="createMaintenance(row as AlarmItem)"
                                />
                            </template>
                        </el-table-column>
                    </el-table>
                </div>
                <Pagination
                    class="alarm-list-pagination"
                    :total-row="alarms.length"
                    :page="pagination.page"
                    :row-size="pagination.pageSize"
                    @current-change="changePage"
                    @size-change="changePageSize"
                />
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
import { DropdownList, GlassPanel, MetricCardRow, Pagination, SearchText, StatusBadge, TableToolbar } from '@/components'
import { isSuccessResponse } from '@/utils'
import AlarmDetailPanel from './components/AlarmDetailPanel.vue'
import AlarmRowActions from './components/AlarmRowActions.vue'
import alarmHistoryApi from './service/alarmHistory.api'
import type { AlarmActionStatus, AlarmDeviceOption, AlarmItem } from './service/alarmHistory.types'

const alarms = ref<AlarmItem[]>([]) // 알림 이력 목록
const selectedAlarm = ref<AlarmItem | null>(null) // 상세 패널에 표시할 선택 알림
const deviceOptions = ref<AlarmDeviceOption[]>([]) // 장비 필터 옵션 목록
const pagination = reactive({ page: 1, pageSize: 10 }) // 알림 이력 페이지와 표시 건수
const pagedAlarms = computed(() => { // 현재 페이지에 표시할 알림; 전체 검색 결과는 KPI 집계에 유지
    const start = (pagination.page - 1) * pagination.pageSize
    return alarms.value.slice(start, start + pagination.pageSize)
})

// 검색 및 필터 조건
const searchParams = reactive({
    keyword: '', // 장비명·유형·메시지 검색어
    deviceId: '' as number | '', // 선택한 대상 장비 ID
    severity: '', // 알림 등급 (INFO, WARNING, CRITICAL)
    alarmType: '', // 알림 유형명
    status: '', // 조치 상태 코드
    dateFrom: '', // 발생 기간 시작일 (YYYY-MM-DD)
    dateTo: '', // 발생 기간 종료일 (YYYY-MM-DD)
})
const dateRange = ref<[string, string] | null>(null) // 발생 기간 선택값

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
    { label: '전체 장비', value: '' },
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

// 알림 등급 코드를 한글 라벨로 변환합니다.
const severityLabel = (value: string) => severityOptions.find(item => item.value === value)?.label || value || '-'

// 알림 등급에 대응하는 뱃지 색상 variant를 반환합니다.
const severityVariant = (value: string) => {
    if (value === 'CRITICAL') {
        return 'danger'
    }
    if (value === 'WARNING') {
        return 'warning'
    }
    return 'info'
}

// 정비 상태를 우선 반영하여 알림의 최종 조치 상태를 계산합니다.
const getActionStatus = (alarm: AlarmItem): AlarmActionStatus => {
    if (alarm.maintenance_status) {
        return alarm.maintenance_status as AlarmActionStatus
    }
    return alarm.status === 'OPEN' ? 'OPEN' : 'ACKED'
}

// 최종 조치 상태 코드를 한글 라벨로 변환합니다.
const actionStatusLabel = (alarm: AlarmItem) => {
    const status = getActionStatus(alarm)
    return statusOptions.find(item => item.value === status)?.label || status || '-'
}

// 조치 상태에 대응하는 뱃지 색상 variant를 반환합니다.
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

// ISO 일시 문자열을 'YYYY-MM-DD HH:mm:ss' 형식으로 변환합니다.
const formatDateTime = (value: string | null | undefined) => {
    return value ? value.replace('T', ' ').slice(0, 19) : '-'
}

// 목록에서 알림 행 클릭 시 상세 패널 표시 대상을 변경합니다.
const selectAlarm = (alarm: AlarmItem) => {
    selectedAlarm.value = alarm
}

// 발생 기간 변경 시 검색 조건을 갱신하고 목록을 재조회합니다.
const changeDateRange = (value: [string, string] | null) => {
    searchParams.dateFrom = value?.[0] || ''
    searchParams.dateTo = value?.[1] || ''
    searchAlarms()
}

// 필터 드롭다운에 표시할 장비 마스터 목록을 조회합니다.
const getDevices = async () => {
    const res = await alarmHistoryApi.getDevices()
    if (isSuccessResponse(res.result)) {
        deviceOptions.value = res.data.list
    }
}

// 검색 조건에 맞는 알림 목록을 조회하고 상세 선택 상태를 동기화합니다.
const getAlarms = async () => {
    const res = await alarmHistoryApi.getList({
        ...searchParams,
        deviceId: searchParams.deviceId || undefined,
    })
    if (isSuccessResponse(res.result)) {
        alarms.value = res.data.list
        // 조치 후 검색 결과가 줄어 현재 페이지가 사라지면 마지막 페이지로 보정합니다.
        pagination.page = Math.min(pagination.page, Math.max(1, Math.ceil(alarms.value.length / pagination.pageSize)))
    }
}

// 검색 조건이 변경되면 첫 페이지부터 조회합니다.
const searchAlarms = async () => {
    pagination.page = 1
    await getAlarms()
}

// 조회된 전체 결과에서 표시할 페이지만 변경합니다.
const changePage = (page: number) => {
    pagination.page = page
}

// 페이지당 표시 건수를 바꾸고 첫 페이지로 이동합니다.
const changePageSize = (pageSize: number) => {
    pagination.pageSize = pageSize
    pagination.page = 1
}

// 현재 페이지에 선택 항목이 없으면 첫 알림을 상세 패널에 표시합니다.
watch(pagedAlarms, items => {
    selectedAlarm.value = items.find(item => item.id === selectedAlarm.value?.id) ?? items[0] ?? null
})

// 조치 완료 후 목록을 재조회하고 해당 알림의 상세 선택을 유지합니다.
const refreshAfterAction = async (alarmId: number) => {
    await getAlarms()
    selectedAlarm.value = pagedAlarms.value.find(item => item.id === alarmId) ?? pagedAlarms.value[0] ?? null
}

// 알림을 확인(ACKED) 처리합니다.
const ackAlarm = async (alarm: AlarmItem) => {
    await alarmHistoryApi.acknowledge(alarm.id)
    await refreshAfterAction(alarm.id)
}

// 알림에 대한 정비 이력을 생성하고 연계 상태를 갱신합니다.
const createMaintenance = async (alarm: AlarmItem) => {
    await alarmHistoryApi.createMaintenance(alarm.id)
    ElMessage.success('정비 이력이 등록되었습니다.')
    await refreshAfterAction(alarm.id)
}

// 검색어를 모두 지웠을 때 별도 입력 없이 전체 목록을 자동 재조회합니다.
watch(
    () => searchParams.keyword,
    (keyword, prevKeyword) => {
        if (prevKeyword && !keyword.trim()) {
            searchAlarms()
        }
    },
)

// 화면 초기 진입 시 장비 옵션과 알림 목록을 조회합니다.
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

:deep(.alarm-date-range) {
    flex: 1;
    max-width: 360px !important;
}

.alarm-table-wrap {
    flex: 1;
    min-height: 0;
}

.alarm-list-pagination {
    flex-shrink: 0;
    margin: 12px 0 0;
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

    :deep(.table-toolbar__filters) {
        width: 100%;
    }

    :deep(.table-toolbar__filters .search-text) {
        flex: 1 1 220px;
    }

    :deep(.table-toolbar__filters .dropdown-list) {
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

    :deep(.table-toolbar__filters) {
        gap: 8px;
    }

    :deep(.table-toolbar__filters .search-text),
    :deep(.table-toolbar__filters .dropdown-list),
    :deep(.alarm-date-range) {
        flex: 1 1 100%;
        width: 100% !important;
    }

    .alarm-table-wrap {
        min-height: 360px;
    }
}
</style>
