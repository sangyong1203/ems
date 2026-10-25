<template>
    <section class="maintenance-management-page">
        <MetricCardRow :items="kpiItems" />

        <div class="maintenance-management-content">
            <GlassPanel
                class="maintenance-panel maintenance-panel--list"
                title="정비 이력"
                :value="`${maintenanceList.length}건`"
            >
                <TableToolbar>
                    <SearchText
                        v-model="searchParams.keyword"
                        placeholder="장비명, 제목, 담당자 검색"
                        width="220px"
                        showSuffixIcon
                        @on-enter="searchMaintenance"
                    />
                    <DropdownList
                        v-model="searchParams.maintenanceType"
                        placeholder="정비 유형"
                        width="130px"
                        :list="maintenanceTypeFilterOptions"
                        option-label="label"
                        option-value="value"
                        @on-change="searchMaintenance"
                    />
                    <DropdownList
                        v-model="searchParams.status"
                        placeholder="상태"
                        width="130px"
                        :list="statusFilterOptions"
                        option-label="label"
                        option-value="value"
                        @on-change="searchMaintenance"
                    />
                    <DatePicker
                        v-model:mode="dateMode"
                        v-model:date="selectedDate"
                        v-model:range="dateRange"
                        class="maintenance-date-range"
                        date-placeholder="정비일"
                        start-placeholder="시작일"
                        end-placeholder="종료일"
                        @change="changeDateRange"
                    />

                    <template #actions>
                        <el-button class="maintenance-create-button" type="primary" @click="openCreateDialog">
                            정비 등록
                        </el-button>
                    </template>
                </TableToolbar>

                <div class="maintenance-table-wrap">
                    <el-table
                        class="maintenance-table"
                        :data="pagedMaintenance"
                        height="100%"
                        highlight-current-row
                        :current-row-key="selectedMaintenance?.id"
                        row-key="id"
                        :tooltip-options="{ hideAfter: 0 }"
                        @row-click="selectMaintenance"
                    >
                        <el-table-column prop="maintenance_date" label="정비일" min-width="120">
                            <template #default="{ row }">{{ row.maintenance_date || '-' }}</template>
                        </el-table-column>
                        <el-table-column prop="device_name" label="장비명" min-width="150" show-overflow-tooltip>
                            <template #default="{ row }">{{ row.device_name || '-' }}</template>
                        </el-table-column>
                        <el-table-column prop="device_type" label="장비 유형" min-width="110">
                            <template #default="{ row }">{{ deviceTypeLabel(row.device_type) }}</template>
                        </el-table-column>
                        <el-table-column prop="maintenance_type" label="정비 유형" min-width="120" />
                        <el-table-column prop="title" label="정비 제목" min-width="210" show-overflow-tooltip />
                        <el-table-column prop="status" label="상태" min-width="100" align="center">
                            <template #default="{ row }">
                                <StatusBadge
                                    :label="statusLabel(row.status)"
                                    :variant="statusVariant(row.status)"
                                    min-width="58px"
                                />
                            </template>
                        </el-table-column>
                        <el-table-column prop="manager_name" label="담당자" min-width="120">
                            <template #default="{ row }">{{ row.manager_name || '-' }}</template>
                        </el-table-column>
                        <el-table-column prop="next_maintenance_date" label="다음 점검일" min-width="130">
                            <template #default="{ row }">{{ row.next_maintenance_date || '-' }}</template>
                        </el-table-column>
                        <el-table-column label="동작" width="92" align="center" fixed="right">
                            <template #default="{ row }">
                                <TableRowActions
                                    @edit="openEditDialog(row as MaintenanceItem)"
                                    @delete="deleteMaintenance(row as MaintenanceItem)"
                                />
                            </template>
                        </el-table-column>
                    </el-table>
                </div>
                <Pagination
                    class="maintenance-list-pagination"
                    :total-row="maintenanceList.length"
                    :page="pagination.page"
                    :row-size="pagination.pageSize"
                    @current-change="changePage"
                    @size-change="changePageSize"
                />
            </GlassPanel>

            <MaintenanceDetailPanel :maintenance="selectedMaintenance" />
        </div>

        <MaintenanceFormDialog
            v-model="isFormDialogOpen"
            :maintenance="editingMaintenance"
            :device-options="deviceOptions"
            :maintenance-type-options="maintenanceTypeOptions"
            :status-options="statusOptions"
            @save="saveMaintenance"
        />
    </section>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { ElMessageBox } from 'element-plus'
import {
    DropdownList,
    GlassPanel,
    MetricCardRow,
    Pagination,
    SearchText,
    StatusBadge,
    TableRowActions,
    TableToolbar,
} from '@/components'
import DatePicker from '@/components/widget/DatePicker.vue'
import { isSuccessResponse } from '@/utils'
import MaintenanceDetailPanel from './components/MaintenanceDetailPanel.vue'
import MaintenanceFormDialog from './components/MaintenanceFormDialog.vue'
import maintenanceManagementApi from './service/maintenanceManagement.api'
import type {
    MaintenanceDeviceOption,
    MaintenanceItem,
    MaintenanceSaveParams,
} from './service/maintenanceManagement.types'

const maintenanceList = ref<MaintenanceItem[]>([]) // 정비 이력 목록
const selectedMaintenance = ref<MaintenanceItem | null>(null) // 선택된 정비 이력 상세
const editingMaintenance = ref<MaintenanceItem | null>(null) // 편집 중인 정비 이력 (수정/등록)
const isFormDialogOpen = ref(false) // 정비 등록/수정 모달 표시 여부
const deviceOptions = ref<MaintenanceDeviceOption[]>([]) // 정비 대상 장비 옵션 목록
const pagination = reactive({ page: 1, pageSize: 10 }) // 정비 목록 페이지와 표시 건수
const pagedMaintenance = computed(() => { // 현재 페이지의 정비 이력; 전체 검색 결과는 KPI 집계에 유지
    const start = (pagination.page - 1) * pagination.pageSize
    return maintenanceList.value.slice(start, start + pagination.pageSize)
})

const searchParams = reactive({ // 정비 이력 검색 파라미터
    keyword: '',
    maintenanceType: '',
    status: '',
    dateFrom: '',
    dateTo: '',
})
const dateMode = ref<'DAILY' | 'RANGE'>('RANGE') // 정비일 검색 방식
const selectedDate = ref('') // 일간 검색에 사용할 정비일
const dateRange = ref<[string, string] | null>(null) // 기간 검색에 사용할 시작일과 종료일

const maintenanceTypeOptions = [
    { label: '정기점검', value: '정기점검' },
    { label: '장애점검', value: '장애점검' },
    { label: '수리', value: '수리' },
    { label: '부품교체', value: '부품교체' },
    { label: '청소', value: '청소' },
    { label: '성능점검', value: '성능점검' },
    { label: '배터리점검', value: '배터리점검' },
    { label: '통신점검', value: '통신점검' },
    { label: '기타', value: '기타' },
]

const statusOptions = [
    { label: '예정', value: 'SCHEDULED' },
    { label: '진행중', value: 'IN_PROGRESS' },
    { label: '완료', value: 'COMPLETED' },
    { label: '보류', value: 'HOLD' },
    { label: '취소', value: 'CANCELED' },
]

const maintenanceTypeFilterOptions = computed(() => [{ label: '전체 유형', value: '' }, ...maintenanceTypeOptions])
const statusFilterOptions = computed(() => [{ label: '전체 상태', value: '' }, ...statusOptions])

const scheduledCount = computed(() => maintenanceList.value.filter(item => item.status === 'SCHEDULED').length)
const inProgressCount = computed(() => maintenanceList.value.filter(item => item.status === 'IN_PROGRESS').length)
const completedCount = computed(() => maintenanceList.value.filter(item => item.status === 'COMPLETED').length)

const kpiItems = computed(() => [
    {
        label: '전체 정비',
        value: String(maintenanceList.value.length),
        unit: '건',
        hint: '등록 이력',
        variant: 'is-total',
    },
    {
        label: '예정',
        value: String(scheduledCount.value),
        unit: '건',
        hint: '점검 대기',
        variant: 'is-scheduled',
    },
    {
        label: '진행중',
        value: String(inProgressCount.value),
        unit: '건',
        hint: '조치 중',
        variant: 'is-progress',
    },
    {
        label: '완료',
        value: String(completedCount.value),
        unit: '건',
        hint: '조치 완료',
        variant: 'is-completed',
    },
])

// deviceTypeLabel 장비 유형 코드 한국어 라벨 반환
const deviceTypeLabel = (value: string | null) => {
    const labels: Record<string, string> = {
        INVERTER: '인버터',
        PCS: 'PCS',
        ESS_BATTERY: '배터리 뱅크',
        BATTERY_RACK: '배터리 랙',
        BMS: 'BMS',
        AC_PANEL: 'AC 배전반',
        GRID_METER: '계통 계량기',
        LOAD_METER: '부하 계량기',
        WEATHER_SENSOR: '기상 센서',
        SENSOR: '일반 센서',
        ETC: '기타',
    }
    return value ? labels[value] || value : '-'
}

// statusLabel 정비 상태 코드 한국어 라벨 반환
const statusLabel = (value: string) => {
    return statusOptions.find(item => item.value === value)?.label || value || '-'
}

// statusVariant 정비 상태에 따른 배지 스타일 반환
const statusVariant = (value: string) => {
    if (value === 'COMPLETED') {
        return 'success'
    }
    if (value === 'IN_PROGRESS') {
        return 'progress'
    }
    if (value === 'HOLD' || value === 'CANCELED') {
        return 'warning'
    }
    return 'info'
}

// selectMaintenance 정비 이력 행 선택
const selectMaintenance = (maintenance: MaintenanceItem) => {
    selectedMaintenance.value = maintenance
}

// 일간은 시작일과 종료일을 같게 지정하고, 날짜 해제 시 기간 조건을 비웁니다.
const changeDateRange = () => {
    searchParams.dateFrom = dateMode.value === 'DAILY' ? selectedDate.value : dateRange.value?.[0] ?? ''
    searchParams.dateTo = dateMode.value === 'DAILY' ? selectedDate.value : dateRange.value?.[1] ?? ''
    searchMaintenance()
}

// getDevices 정비 대상 장비 목록 조회
const getDevices = async () => {
    const res = await maintenanceManagementApi.getDevices()
    if (isSuccessResponse(res.result)) {
        deviceOptions.value = res.data.list
    }
}

// getMaintenanceList 정비 이력 목록 조회
const getMaintenanceList = async () => {
    const res = await maintenanceManagementApi.getList({
        ...searchParams,
    })
    if (isSuccessResponse(res.result)) {
        maintenanceList.value = res.data.list
        // 삭제나 수정 후 현재 페이지가 사라지면 마지막 페이지로 보정합니다.
        pagination.page = Math.min(pagination.page, Math.max(1, Math.ceil(maintenanceList.value.length / pagination.pageSize)))
    }
}

// 검색 조건이나 정비일 범위가 변경되면 첫 페이지부터 조회합니다.
const searchMaintenance = async () => {
    pagination.page = 1
    await getMaintenanceList()
}

// 조회된 전체 검색 결과에서 표시할 페이지만 변경합니다.
const changePage = (page: number) => {
    pagination.page = page
}

// 페이지당 표시 건수를 변경하고 첫 페이지로 이동합니다.
const changePageSize = (pageSize: number) => {
    pagination.pageSize = pageSize
    pagination.page = 1
}

// 현재 페이지에서 선택 항목을 유지하고 없으면 첫 정비 이력을 상세 패널에 표시합니다.
watch(pagedMaintenance, items => {
    selectedMaintenance.value = items.find(item => item.id === selectedMaintenance.value?.id) ?? items[0] ?? null
})

// openCreateDialog 신규 정비 이력 등록 모달 열기
const openCreateDialog = () => {
    editingMaintenance.value = null
    isFormDialogOpen.value = true
}

// openEditDialog 기존 정비 이력 수정 모달 열기
const openEditDialog = (maintenance: MaintenanceItem) => {
    editingMaintenance.value = maintenance
    isFormDialogOpen.value = true
}

// saveMaintenance 정비 이력 저장 (생성 또는 수정)
const saveMaintenance = async (params: MaintenanceSaveParams) => {
    if (editingMaintenance.value) {
        await maintenanceManagementApi.updateMaintenance(editingMaintenance.value.id, params)
    } else {
        await maintenanceManagementApi.createMaintenance(params)
    }
    isFormDialogOpen.value = false
    await getMaintenanceList()
}

// deleteMaintenance 정비 이력 삭제 확인 및 처리
const deleteMaintenance = async (maintenance: MaintenanceItem) => {
    await ElMessageBox.confirm(`${maintenance.title} 정비 이력을 삭제할까요?`, 'Confirm', {
        confirmButtonText: '삭제',
        cancelButtonText: '취소',
        type: 'warning',
    })
    await maintenanceManagementApi.deleteMaintenance(maintenance.id)
    selectedMaintenance.value = null
    await getMaintenanceList()
}

// watch(searchParams.keyword) 키워드 초기화 시 목록 재조회
watch(
    () => searchParams.keyword,
    (keyword, prevKeyword) => {
        if (prevKeyword && !keyword.trim()) {
            searchMaintenance()
        }
    },
)

// onMounted 장비 목록 및 정비 이력 초기 로드
onMounted(async () => {
    await getDevices()
    await getMaintenanceList()
})
</script>

<style scoped lang="scss">
.maintenance-management-page {
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

.maintenance-management-content {
    flex: 1 1 auto;
    display: flex;
    gap: 14px;
    min-height: 0;
    overflow: hidden;
}

.maintenance-panel {
    min-height: 0;
}

.maintenance-panel--list {
    flex: 1;
    min-width: 0;
}

.maintenance-create-button {
    height: 32px;
    padding: 0 16px;
}

.maintenance-table-wrap {
    flex: 1;
    min-height: 0;
}

.maintenance-list-pagination {
    flex-shrink: 0;
    margin: 12px 0 0;
}

@media (max-width: 1180px), (orientation: portrait) {
    .maintenance-management-page {
        min-width: 0;
        height: auto;
        min-height: 100%;
        overflow: auto;
    }

    .maintenance-management-content {
        flex-direction: column;
        min-height: auto;
        overflow: visible;
    }

    .maintenance-panel--list {
        flex: 0 0 auto;
    }

    :deep(.table-toolbar__filters) {
        flex: 1 1 680px;
    }

    :deep(.table-toolbar__filters .search-text) {
        flex: 1 1 250px;
    }

    :deep(.table-toolbar__filters .dropdown-list) {
        flex: 1 1 140px;
    }

    .maintenance-table-wrap {
        min-height: 440px;
        max-height: 800px;
    }
}

@media (max-width: 760px), (orientation: portrait) and (max-width: 900px) {
    .maintenance-management-page {
        padding: 8px;
    }

    :deep(.table-toolbar__filters .search-text),
    :deep(.table-toolbar__filters .dropdown-list),
    .maintenance-date-range {
        flex: 1 1 100%;
        width: 100% !important;
    }

    .maintenance-create-button {
        width: 100%;
    }

    .maintenance-table-wrap {
        min-height: 380px;
    }
}
</style>
