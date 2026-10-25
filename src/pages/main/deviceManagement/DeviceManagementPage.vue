<template>
    <section class="device-management-page">
        <MetricCardRow :items="kpiItems" />

        <div class="device-management-content">
            <GlassPanel class="device-panel device-panel--list" title="목록" :value="activeTabValue">
                <div class="device-view-tabs">
                    <button
                        type="button"
                        :class="{ 'is-active': activeTab === 'devices' }"
                        @click="activeTab = 'devices'"
                    >
                        장비
                    </button>
                    <button
                        type="button"
                        :class="{ 'is-active': activeTab === 'pvStrings' }"
                        @click="activeTab = 'pvStrings'"
                    >
                        PV 스트링
                    </button>
                </div>

                <TableToolbar>
                    <template v-if="activeTab === 'devices'">
                        <SearchText
                            v-model="searchParams.keyword"
                            placeholder="장비명, 모델명, 위치 검색"
                            width="240px"
                            showSuffixIcon
                            @on-enter="searchDevices"
                        />
                        <DropdownList
                            v-model="searchParams.deviceType"
                            placeholder="장비 유형"
                            width="150px"
                            :list="deviceTypeFilterOptions"
                            option-label="label"
                            option-value="value"
                            @on-change="searchDevices"
                        />
                        <DropdownList
                            v-model="searchParams.status"
                            placeholder="상태"
                            width="150px"
                            :list="statusFilterOptions"
                            option-label="label"
                            option-value="value"
                            @on-change="searchDevices"
                        />
                    </template>
                    <template v-else>
                        <SearchText
                            v-model="pvStringSearchParams.keyword"
                            placeholder="스트링명, 위치, 인버터 검색"
                            width="240px"
                            showSuffixIcon
                            @on-enter="searchPvStrings"
                        />
                        <DropdownList
                            v-model="pvStringSearchParams.status"
                            placeholder="상태"
                            width="150px"
                            :list="statusFilterOptions"
                            option-label="label"
                            option-value="value"
                            @on-change="searchPvStrings"
                        />
                        <DropdownList
                            v-model="pvStringSearchParams.connection"
                            placeholder="연결 상태"
                            width="150px"
                            :list="connectionFilterOptions"
                            option-label="label"
                            option-value="value"
                            @on-change="searchPvStrings"
                        />
                    </template>

                    <template #actions>
                        <el-button
                            v-if="activeTab === 'devices'"
                            class="device-create-button"
                            type="primary"
                            @click="openCreateDialog"
                            >장비 등록</el-button
                        >
                        <el-button v-else class="device-create-button" type="primary" @click="openCreatePvStringDialog">
                            스트링 등록
                        </el-button>
                    </template>
                </TableToolbar>

                <div v-if="activeTab === 'devices'" class="device-table-wrap">
                    <el-table
                        class="device-table"
                        :data="pagedDevices"
                        height="100%"
                        highlight-current-row
                        :current-row-key="selectedDevice?.id"
                        row-key="id"
                        @row-click="selectDevice"
                        :tooltip-options="{ hideAfter: 0 }"
                    >
                        <el-table-column prop="name" label="장비명" min-width="180" show-overflow-tooltip />
                        <el-table-column prop="device_type" label="유형" min-width="110">
                            <template #default="{ row }">{{ deviceTypeLabel(row.device_type) }}</template>
                        </el-table-column>
                        <el-table-column prop="model_name" label="모델명" min-width="140" show-overflow-tooltip>
                            <template #default="{ row }">{{ row.model_name || '-' }}</template>
                        </el-table-column>
                        <el-table-column prop="capacity" label="정격/범위" min-width="90" align="right">
                            <template #default="{ row }">{{ capacityText(row as DeviceItem) }}</template>
                        </el-table-column>
                        <el-table-column
                            prop="install_location"
                            label="설치 위치"
                            min-width="120"
                            show-overflow-tooltip
                        >
                            <template #default="{ row }">{{ row.install_location || '-' }}</template>
                        </el-table-column>
                        <el-table-column prop="is_active" label="운영" width="76" align="center">
                            <template #default="{ row }">
                                <el-switch
                                    v-model="row.is_active"
                                    :loading="updatingActiveDeviceIds.has(row.id)"
                                    :disabled="updatingActiveDeviceIds.has(row.id)"
                                    @click.stop
                                    @change="toggleDeviceActive(row as DeviceItem)"
                                />
                            </template>
                        </el-table-column>
                        <el-table-column prop="status" label="상태" min-width="96" align="center">
                            <template #default="{ row }">
                                <StatusBadge :label="statusLabel(row.status)" :variant="statusVariant(row.status)" />
                            </template>
                        </el-table-column>
                        <el-table-column prop="communication_type" label="통신" min-width="100">
                            <template #default="{ row }">{{ row.communication_type || '-' }}</template>
                        </el-table-column>
                        <el-table-column prop="manufacturer" label="제조사" min-width="100">
                            <template #default="{ row }">
                                <el-tooltip v-if="row.manufacturer" :content="row.manufacturer" placement="top">
                                    {{ row.manufacturer }}
                                </el-tooltip>
                                <span v-else>-</span>
                            </template>
                        </el-table-column>
                        <el-table-column label="동작" width="92" align="center" fixed="right">
                            <template #default="{ row }">
                                <TableRowActions
                                    @edit="openEditDialog(row as DeviceItem)"
                                    @delete="deleteDevice(row as DeviceItem)"
                                />
                            </template>
                        </el-table-column>
                    </el-table>
                </div>

                <div v-else class="device-table-wrap">
                    <el-table
                        class="device-table"
                        :data="pagedPvStrings"
                        height="100%"
                        highlight-current-row
                        :current-row-key="selectedPvString?.id"
                        row-key="id"
                        @row-click="selectPvString"
                        :tooltip-options="{ hideAfter: 0 }"
                    >
                        <el-table-column prop="name" label="스트링명" min-width="170" show-overflow-tooltip />
                        <el-table-column prop="rated_capacity_kw" label="정격 용량" min-width="100" align="right">
                            <template #default="{ row }">{{ numberText(row.rated_capacity_kw, 'kW') }}</template>
                        </el-table-column>
                        <el-table-column prop="panel_count" label="패널" width="84" align="right">
                            <template #default="{ row }">{{ row.panel_count ?? '-' }}</template>
                        </el-table-column>
                        <el-table-column
                            prop="install_location"
                            label="설치 위치"
                            min-width="130"
                            show-overflow-tooltip
                        >
                            <template #default="{ row }">{{ row.install_location || '-' }}</template>
                        </el-table-column>
                        <el-table-column prop="inverter_name" label="연결 인버터" min-width="140" show-overflow-tooltip>
                            <template #default="{ row }">{{ row.inverter_name || '미연결' }}</template>
                        </el-table-column>
                        <el-table-column label="MPPT/CH" min-width="90" align="center">
                            <template #default="{ row }">
                                {{ row.mppt_no ?? '-' }} / {{ row.channel_no ?? '-' }}
                            </template>
                        </el-table-column>
                        <el-table-column prop="is_active" label="운영" width="76" align="center">
                            <template #default="{ row }">
                                <StatusBadge
                                    :label="row.is_active ? '활성' : '비활성'"
                                    :variant="row.is_active ? 'success' : 'muted'"
                                />
                            </template>
                        </el-table-column>
                        <el-table-column prop="status" label="상태" min-width="96" align="center">
                            <template #default="{ row }">
                                <StatusBadge :label="statusLabel(row.status)" :variant="statusVariant(row.status)" />
                            </template>
                        </el-table-column>
                        <el-table-column label="동작" width="92" align="center" fixed="right">
                            <template #default="{ row }">
                                <TableRowActions
                                    @edit="openEditPvStringDialog(row as PvStringItem)"
                                    @delete="deletePvString(row as PvStringItem)"
                                />
                            </template>
                        </el-table-column>
                    </el-table>
                </div>
                <Pagination
                    :key="activeTab"
                    class="device-list-pagination"
                    :total-row="activeTab === 'devices' ? devices.length : pvStrings.length"
                    :page="activePagination.page"
                    :row-size="activePagination.pageSize"
                    @current-change="changePage"
                    @size-change="changePageSize"
                />
            </GlassPanel>

            <DeviceDetailPanel v-if="activeTab === 'devices'" :device="selectedDevice" />
            <PvStringDetailPanel v-else :pv-string="selectedPvString" />
        </div>

        <DeviceFormDialog
            v-model="isFormDialogOpen"
            :device="editingDevice"
            :pv-strings="allPvStrings"
            @save="saveDevice"
        />
        <PvStringFormDialog v-model="isPvStringFormDialogOpen" :pv-string="editingPvString" @save="savePvString" />
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
import { Message } from '@/composables/useFeedback'
import { isSuccessResponse } from '@/utils'
import DeviceDetailPanel from './components/DeviceDetailPanel.vue'
import DeviceFormDialog from './components/DeviceFormDialog.vue'
import PvStringDetailPanel from './components/PvStringDetailPanel.vue'
import PvStringFormDialog from './components/PvStringFormDialog.vue'
import deviceManagementApi from './service/deviceManagement.api'
import type { DeviceItem, DeviceSaveParams, PvStringItem, PvStringSaveParams } from './service/deviceManagement.types'

const devices = ref<DeviceItem[]>([]) // 장비 목록
const pvStrings = ref<PvStringItem[]>([]) // PV 스트링 목록
const allPvStrings = ref<PvStringItem[]>([]) // 전체 PV 스트링 목록 (인버터 매핑용)
const selectedDevice = ref<DeviceItem | null>(null) // 선택된 장비 상세
const selectedPvString = ref<PvStringItem | null>(null) // 선택된 PV 스트링 상세
const editingDevice = ref<DeviceItem | null>(null) // 편집 중인 장비 정보
const editingPvString = ref<PvStringItem | null>(null) // 편집 중인 PV 스트링 정보
const isFormDialogOpen = ref(false) // 장비 등록/수정 모달 표시 여부
const isPvStringFormDialogOpen = ref(false) // PV 스트링 등록/수정 모달 표시 여부
const updatingActiveDeviceIds = ref(new Set<number>()) // 활성화 상태 변경 중인 장비 ID 셋
const activeTab = ref<'devices' | 'pvStrings'>('devices') // 활성 탭 (장비 관리 / PV 스트링 관리)
const devicePagination = reactive({ page: 1, pageSize: 10 }) // 장비 목록 페이지와 표시 개수
const pvStringPagination = reactive({ page: 1, pageSize: 10 }) // 스트링 목록 페이지와 표시 개수
const activePagination = computed(() => activeTab.value === 'devices' ? devicePagination : pvStringPagination) // 현재 탭의 페이지 상태
const pagedDevices = computed(() => { // 현재 페이지에 표시할 장비; 전체 검색 결과는 집계에 유지
    const start = (devicePagination.page - 1) * devicePagination.pageSize
    return devices.value.slice(start, start + devicePagination.pageSize)
})
const pagedPvStrings = computed(() => { // 현재 페이지에 표시할 스트링
    const start = (pvStringPagination.page - 1) * pvStringPagination.pageSize
    return pvStrings.value.slice(start, start + pvStringPagination.pageSize)
})

const searchParams = reactive({ // 장비 검색 조건
    keyword: '',
    deviceType: '',
    status: '',
})

const pvStringSearchParams = reactive({ // PV 스트링 검색 조건
    keyword: '',
    status: '',
    connection: '',
})

const deviceTypeFilterOptions = [
    { label: '전체 유형', value: '' },
    { label: '인버터', value: 'INVERTER' },
    { label: 'PCS', value: 'PCS' },
    { label: '배터리 뱅크', value: 'ESS_BATTERY' },
    { label: '배터리 랙', value: 'BATTERY_RACK' },
    { label: 'BMS', value: 'BMS' },
    { label: 'AC 배전반', value: 'AC_PANEL' },
    { label: '계통 계량기', value: 'GRID_METER' },
    { label: '부하 계량기', value: 'LOAD_METER' },
    { label: '기상 센서', value: 'WEATHER_SENSOR' },
    { label: '일반 센서', value: 'SENSOR' },
]

const statusFilterOptions = [
    { label: '전체 상태', value: '' },
    { label: '정상', value: 'NORMAL' },
    { label: '주의', value: 'WARNING' },
    { label: '장애', value: 'FAULT' },
    { label: '점검', value: 'MAINTENANCE' },
]

const connectionFilterOptions = [
    { label: '전체 연결', value: '' },
    { label: '연결됨', value: 'LINKED' },
    { label: '미연결', value: 'UNLINKED' },
]

const normalCount = computed(() => devices.value.filter(item => item.status === 'NORMAL').length)
const warningCount = computed(
    () => devices.value.filter(item => item.status === 'WARNING' || item.status === 'FAULT').length,
)
const inverterCount = computed(() => devices.value.filter(item => item.device_type === 'INVERTER').length)
const communicationCount = computed(
    () => devices.value.filter(item => item.communication_type || item.ip_address).length,
)
const activeTabValue = computed(() =>
    activeTab.value === 'devices' ? `${devices.value.length}대` : `${pvStrings.value.length}개`,
)

const kpiItems = computed(() => [
    {
        label: '전체 장비',
        value: String(devices.value.length),
        unit: '대',
        hint: '등록 장비',
        variant: 'is-total',
    },
    {
        label: '정상',
        value: String(normalCount.value),
        unit: '대',
        hint: '운전 가능',
        variant: 'is-normal',
    },
    {
        label: '주의/장애',
        value: String(warningCount.value),
        unit: '대',
        hint: '확인 필요',
        variant: 'is-warning',
    },
    {
        label: '인버터',
        value: String(inverterCount.value),
        unit: '대',
        hint: '태양광 장비',
        variant: 'is-inverter',
    },
    {
        label: '통신 설정',
        value: String(communicationCount.value),
        unit: '대',
        hint: 'IP 또는 통신 방식 보유',
        variant: 'is-communication',
    },
])

// deviceTypeLabel 장비 유형 코드 한국어 라벨 반환
const deviceTypeLabel = (value: string) => {
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
    return labels[value] || value || '-'
}

// statusLabel 장비 운영 상태 코드 한국어 라벨 반환
const statusLabel = (value: string) => {
    const labels: Record<string, string> = {
        NORMAL: '정상',
        WARNING: '주의',
        FAULT: '장애',
        MAINTENANCE: '점검',
        UNKNOWN: '미확인',
    }
    return labels[value] || value || '-'
}

// statusVariant 장비 운영 상태에 따른 배지 스타일 반환
const statusVariant = (value: string) => {
    if (value === 'NORMAL') {
        return 'success'
    }
    if (value === 'WARNING' || value === 'MAINTENANCE') {
        return 'warning'
    }
    if (value === 'FAULT') {
        return 'danger'
    }
    return 'muted'
}

// capacityText 정격 용량 및 단위 문자열 포맷팅
const capacityText = (device: DeviceItem) => {
    if (device.capacity === null || device.capacity === undefined) {
        return '-'
    }
    return `${Number(device.capacity).toLocaleString(undefined, { maximumFractionDigits: 1 })} ${device.capacity_unit || ''}`.trim()
}

// selectDevice 장비 행 선택
const selectDevice = (device: DeviceItem) => {
    selectedDevice.value = device
}

// selectPvString PV 스트링 행 선택
const selectPvString = (pvString: PvStringItem) => {
    selectedPvString.value = pvString
}

// getDevices 조건에 따른 장비 목록 조회
const getDevices = async () => {
    const res = await deviceManagementApi.getList(searchParams)
    if (isSuccessResponse(res.result)) {
        devices.value = res.data.list
        // 삭제나 검색 결과 감소로 현재 페이지가 사라지면 마지막 페이지로 이동합니다.
        devicePagination.page = Math.min(devicePagination.page, Math.max(1, Math.ceil(devices.value.length / devicePagination.pageSize)))
    }
}

// getPvStrings 조건에 따른 PV 스트링 목록 조회
const getPvStrings = async () => {
    const res = await deviceManagementApi.getPvStrings(pvStringSearchParams)
    if (isSuccessResponse(res.result)) {
        pvStrings.value = res.data.list
        pvStringPagination.page = Math.min(pvStringPagination.page, Math.max(1, Math.ceil(pvStrings.value.length / pvStringPagination.pageSize)))
    }
}

// 장비 검색 조건을 적용할 때 첫 페이지부터 표시합니다.
const searchDevices = async () => {
    devicePagination.page = 1
    await getDevices()
}

// 스트링 검색 조건을 적용할 때 첫 페이지부터 표시합니다.
const searchPvStrings = async () => {
    pvStringPagination.page = 1
    await getPvStrings()
}

// 현재 탭의 페이지를 변경하며 다른 탭의 페이지 상태는 유지합니다.
const changePage = (page: number) => {
    activePagination.value.page = page
}

// 현재 탭의 표시 개수를 변경하고 첫 페이지로 이동합니다.
const changePageSize = (pageSize: number) => {
    activePagination.value.pageSize = pageSize
    activePagination.value.page = 1
}

// 현재 페이지에서 선택 항목을 유지하고 없으면 첫 장비를 상세 패널에 표시합니다.
watch(pagedDevices, items => {
    selectedDevice.value = items.find(item => item.id === selectedDevice.value?.id) ?? items[0] ?? null
})

// 스트링도 현재 페이지에 있는 항목만 상세 패널에 표시합니다.
watch(pagedPvStrings, items => {
    selectedPvString.value = items.find(item => item.id === selectedPvString.value?.id) ?? items[0] ?? null
})

// getAllPvStrings 인버터 연결용 전체 PV 스트링 목록 조회
const getAllPvStrings = async () => {
    const res = await deviceManagementApi.getPvStrings()
    if (isSuccessResponse(res.result)) {
        allPvStrings.value = res.data.list
    }
}

// openCreateDialog 신규 장비 등록 모달 열기
const openCreateDialog = () => {
    editingDevice.value = null
    getAllPvStrings()
    isFormDialogOpen.value = true
}

// openEditDialog 기존 장비 수정 모달 열기
const openEditDialog = (device: DeviceItem) => {
    editingDevice.value = device
    getAllPvStrings()
    isFormDialogOpen.value = true
}

// openCreatePvStringDialog 신규 PV 스트링 등록 모달 열기
const openCreatePvStringDialog = () => {
    editingPvString.value = null
    isPvStringFormDialogOpen.value = true
}

// openEditPvStringDialog 기존 PV 스트링 수정 모달 열기
const openEditPvStringDialog = (pvString: PvStringItem) => {
    editingPvString.value = pvString
    isPvStringFormDialogOpen.value = true
}

// saveDevice 장비 정보 저장 (생성 또는 수정)
const saveDevice = async (params: DeviceSaveParams) => {
    if (editingDevice.value) {
        await deviceManagementApi.updateDevice(editingDevice.value.id, params)
    } else {
        await deviceManagementApi.createDevice(params)
    }
    isFormDialogOpen.value = false
    await getDevices()
    await getPvStrings()
    await getAllPvStrings()
}

// savePvString PV 스트링 정보 저장 (생성 또는 수정)
const savePvString = async (params: PvStringSaveParams) => {
    if (editingPvString.value) {
        await deviceManagementApi.updatePvString(editingPvString.value.id, params)
    } else {
        await deviceManagementApi.createPvString(params)
    }
    isPvStringFormDialogOpen.value = false
    await getPvStrings()
    await getAllPvStrings()
}

// toggleDeviceActive 장비 운영 활성화/비활성화 토글
const toggleDeviceActive = async (device: DeviceItem) => {
    const previousValue = !device.is_active
    updatingActiveDeviceIds.value.add(device.id)
    try {
        const res = await deviceManagementApi.updateDevice(device.id, { ...device })
        if (isSuccessResponse(res.result)) {
            Object.assign(device, res.data)
            if (selectedDevice.value?.id === device.id) {
                selectedDevice.value = device
            }
            Message.success(device.is_active ? '장비를 운영 활성화했습니다.' : '장비를 운영 비활성화했습니다.')
        } else {
            device.is_active = previousValue
        }
    } catch {
        device.is_active = previousValue
    } finally {
        updatingActiveDeviceIds.value.delete(device.id)
    }
}

// deleteDevice 장비 삭제 확인 및 처리
const deleteDevice = async (device: DeviceItem) => {
    await ElMessageBox.confirm(`${device.name} 장비를 삭제할까요?`, 'Confirm', {
        confirmButtonText: '삭제',
        cancelButtonText: '취소',
        type: 'warning',
    })
    await deviceManagementApi.deleteDevice(device.id)
    selectedDevice.value = null
    await getDevices()
    await getPvStrings()
    await getAllPvStrings()
}

// deletePvString PV 스트링 삭제 확인 및 처리
const deletePvString = async (pvString: PvStringItem) => {
    await ElMessageBox.confirm(`${pvString.name} 스트링을 삭제할까요?`, 'Confirm', {
        confirmButtonText: '삭제',
        cancelButtonText: '취소',
        type: 'warning',
    })
    await deviceManagementApi.deletePvString(pvString.id)
    selectedPvString.value = null
    await getPvStrings()
    await getDevices()
    await getAllPvStrings()
}

// numberText 수치 및 단위 문자열 포맷팅
const numberText = (value: number | null, unit: string) => {
    if (value === null || value === undefined) {
        return '-'
    }
    return `${Number(value).toLocaleString(undefined, { maximumFractionDigits: 2 })} ${unit}`
}

// watch(searchParams.keyword) 키워드 초기화 시 장비 목록 재조회
watch(
    () => searchParams.keyword,
    (keyword, prevKeyword) => {
        if (prevKeyword && !keyword.trim()) {
            searchDevices()
        }
    },
)

// watch(pvStringSearchParams.keyword) 키워드 초기화 시 스트링 목록 재조회
watch(
    () => pvStringSearchParams.keyword,
    (keyword, prevKeyword) => {
        if (prevKeyword && !keyword.trim()) {
            searchPvStrings()
        }
    },
)

// onMounted 초기 장비 및 PV 스트링 목록 조회
onMounted(() => {
    getDevices()
    getPvStrings()
    getAllPvStrings()
})
</script>

<style scoped lang="scss">
.device-management-page {
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

.device-management-content {
    flex: 1 1 auto;
    display: flex;
    gap: 14px;
    min-height: 0;
    overflow: hidden;
}

.device-panel {
    min-height: 0;
}

.device-panel--list {
    flex: 1 1 68%;
    min-width: 0;
}

.device-view-tabs {
    display: flex;
    align-items: center;
    gap: 18px;
    margin: -2px 0 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.device-view-tabs button {
    position: relative;
    height: 30px;
    padding: 0;
    border: 0;
    color: var(--text-color--secondary);
    font-size: 14px;
    font-weight: 700;
    cursor: pointer;
    background: transparent;
}

.device-view-tabs button.is-active {
    color: var(--primary-color);
}

.device-view-tabs button.is-active::after {
    position: absolute;
    right: 0;
    bottom: -1px;
    left: 0;
    height: 2px;
    background: var(--primary-color);
    content: '';
}

.device-create-button {
    height: 32px;
    padding: 0 16px;
}

.device-table-wrap {
    flex: 1;
    min-height: 0;
}

.device-list-pagination {
    flex-shrink: 0;
    margin: 12px 0 0;
}

@media (max-width: 1180px), (orientation: portrait) {
    .device-management-page {
        min-width: 0;
        height: auto;
        overflow: auto;
        margin-bottom: 40px;
    }

    .device-management-content {
        flex-direction: column;
        overflow: visible;
    }

    .device-panel--list {
        flex: 0 0 auto;
    }

    :deep(.table-toolbar__filters) {
        flex: 1 1 540px;
    }

    :deep(.table-toolbar__filters .search-text) {
        flex: 1 1 240px;
    }

    :deep(.table-toolbar__filters .dropdown-list) {
        flex: 1 1 150px;
    }

    .device-table-wrap {
        min-height: 440px;
        max-height: 800px;
    }
}

@media (max-width: 760px), (orientation: portrait) and (max-width: 900px) {
    .device-management-page {
        padding: 8px;
    }

    .device-view-tabs {
        margin-bottom: 10px;
    }

    :deep(.table-toolbar__filters .search-text),
    :deep(.table-toolbar__filters .dropdown-list) {
        flex: 1 1 100%;
        width: 100% !important;
    }

    .device-create-button {
        width: 100%;
    }
}
</style>
