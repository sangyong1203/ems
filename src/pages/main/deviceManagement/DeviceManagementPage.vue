<template>
    <section class="device-management-page">
        <MetricCardRow :items="kpiItems" />

        <div class="device-management-content">
            <GlassPanel class="device-panel device-panel--list" title="관리 목록" :value="activeTabValue">
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

                <div class="device-toolbar">
                    <div v-if="activeTab === 'devices'" class="device-toolbar__filters">
                        <SearchText
                            v-model="searchParams.keyword"
                            placeholder="장비명, 모델명, 위치 검색"
                            width="240px"
                            showSuffixIcon
                            @on-enter="getDevices"
                        />
                        <DropdownList
                            v-model="searchParams.deviceType"
                            placeholder="장비 유형"
                            width="150px"
                            :list="deviceTypeFilterOptions"
                            option-label="label"
                            option-value="value"
                            @on-change="getDevices"
                        />
                        <DropdownList
                            v-model="searchParams.status"
                            placeholder="상태"
                            width="150px"
                            :list="statusFilterOptions"
                            option-label="label"
                            option-value="value"
                            @on-change="getDevices"
                        />
                    </div>
                    <div v-else class="device-toolbar__filters">
                        <SearchText
                            v-model="pvStringSearchParams.keyword"
                            placeholder="스트링명, 위치, 인버터 검색"
                            width="240px"
                            showSuffixIcon
                            @on-enter="getPvStrings"
                        />
                        <DropdownList
                            v-model="pvStringSearchParams.status"
                            placeholder="상태"
                            width="150px"
                            :list="statusFilterOptions"
                            option-label="label"
                            option-value="value"
                            @on-change="getPvStrings"
                        />
                        <DropdownList
                            v-model="pvStringSearchParams.connection"
                            placeholder="연결 상태"
                            width="150px"
                            :list="connectionFilterOptions"
                            option-label="label"
                            option-value="value"
                            @on-change="getPvStrings"
                        />
                    </div>
                    <div class="device-toolbar__actions">
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
                    </div>
                </div>

                <div v-if="activeTab === 'devices'" class="device-table-wrap">
                    <el-table
                        class="device-table"
                        :data="devices"
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
                            <template #default="{ row }">{{ capacityText(row) }}</template>
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
                                    @change="toggleDeviceActive(row)"
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
                                <TableRowActions @edit="openEditDialog(row)" @delete="deleteDevice(row)" />
                            </template>
                        </el-table-column>
                    </el-table>
                </div>

                <div v-else class="device-table-wrap">
                    <el-table
                        class="device-table"
                        :data="pvStrings"
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
                                <TableRowActions @edit="openEditPvStringDialog(row)" @delete="deletePvString(row)" />
                            </template>
                        </el-table-column>
                    </el-table>
                </div>
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
import { DropdownList, GlassPanel, MetricCardRow, SearchText, StatusBadge, TableRowActions } from '@/shared/components'
import { Message } from '@/shared/composables/useFeedback'
import { isSuccessResponse } from '@/shared/utils'
import DeviceDetailPanel from './components/DeviceDetailPanel.vue'
import DeviceFormDialog from './components/DeviceFormDialog.vue'
import PvStringDetailPanel from './components/PvStringDetailPanel.vue'
import PvStringFormDialog from './components/PvStringFormDialog.vue'
import deviceManagementApi from './service/deviceManagement.api'
import type { DeviceItem, DeviceSaveParams, PvStringItem, PvStringSaveParams } from './service/deviceManagement.types'

const devices = ref<DeviceItem[]>([])
const pvStrings = ref<PvStringItem[]>([])
const allPvStrings = ref<PvStringItem[]>([])
const selectedDevice = ref<DeviceItem | null>(null)
const selectedPvString = ref<PvStringItem | null>(null)
const editingDevice = ref<DeviceItem | null>(null)
const editingPvString = ref<PvStringItem | null>(null)
const isFormDialogOpen = ref(false)
const isPvStringFormDialogOpen = ref(false)
const updatingActiveDeviceIds = ref(new Set<number>())
const activeTab = ref<'devices' | 'pvStrings'>('devices')

const searchParams = reactive({
    keyword: '',
    deviceType: '',
    status: '',
})

const pvStringSearchParams = reactive({
    keyword: '',
    status: '',
    connection: '',
})

const deviceTypeFilterOptions = [
    { label: '전체 유형', value: '' },
    { label: '인버터', value: 'INVERTER' },
    { label: 'PCS', value: 'PCS' },
    { label: 'ESS Battery', value: 'ESS_BATTERY' },
    { label: 'BMS', value: 'BMS' },
    { label: 'AC 배전반', value: 'AC_PANEL' },
    { label: '계량기', value: 'METER' },
    { label: '센서', value: 'SENSOR' },
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

const deviceTypeLabel = (value: string) => {
    const labels: Record<string, string> = {
        INVERTER: '인버터',
        PCS: 'PCS',
        ESS_BATTERY: 'ESS Battery',
        BMS: 'BMS',
        AC_PANEL: 'AC 배전반',
        METER: '계량기',
        SENSOR: '센서',
        ETC: '기타',
    }
    return labels[value] || value || '-'
}

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

const capacityText = (device: DeviceItem) => {
    if (device.capacity === null || device.capacity === undefined) {
        return '-'
    }
    return `${Number(device.capacity).toLocaleString(undefined, { maximumFractionDigits: 1 })} ${device.capacity_unit || ''}`.trim()
}

const selectDevice = (device: DeviceItem) => {
    selectedDevice.value = device
}

const selectPvString = (pvString: PvStringItem) => {
    selectedPvString.value = pvString
}

const getDevices = async () => {
    const res = await deviceManagementApi.getList(searchParams)
    if (isSuccessResponse(res.result)) {
        devices.value = res.data.list
        if (!devices.value.length) {
            selectedDevice.value = null
            return
        }
        const selectedId = selectedDevice.value?.id
        selectedDevice.value = devices.value.find(item => item.id === selectedId) ?? devices.value[0]
    }
}

const getPvStrings = async () => {
    const res = await deviceManagementApi.getPvStrings(pvStringSearchParams)
    if (isSuccessResponse(res.result)) {
        pvStrings.value = res.data.list
        if (!pvStrings.value.length) {
            selectedPvString.value = null
            return
        }
        const selectedId = selectedPvString.value?.id
        selectedPvString.value = pvStrings.value.find(item => item.id === selectedId) ?? pvStrings.value[0]
    }
}

const getAllPvStrings = async () => {
    const res = await deviceManagementApi.getPvStrings()
    if (isSuccessResponse(res.result)) {
        allPvStrings.value = res.data.list
    }
}

const openCreateDialog = () => {
    editingDevice.value = null
    getAllPvStrings()
    isFormDialogOpen.value = true
}

const openEditDialog = (device: DeviceItem) => {
    editingDevice.value = device
    getAllPvStrings()
    isFormDialogOpen.value = true
}

const openCreatePvStringDialog = () => {
    editingPvString.value = null
    isPvStringFormDialogOpen.value = true
}

const openEditPvStringDialog = (pvString: PvStringItem) => {
    editingPvString.value = pvString
    isPvStringFormDialogOpen.value = true
}

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

const numberText = (value: number | null, unit: string) => {
    if (value === null || value === undefined) {
        return '-'
    }
    return `${Number(value).toLocaleString(undefined, { maximumFractionDigits: 2 })} ${unit}`
}

watch(
    () => searchParams.keyword,
    (keyword, prevKeyword) => {
        if (prevKeyword && !keyword.trim()) {
            getDevices()
        }
    },
)

watch(
    () => pvStringSearchParams.keyword,
    (keyword, prevKeyword) => {
        if (prevKeyword && !keyword.trim()) {
            getPvStrings()
        }
    },
)

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

.device-toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    margin-bottom: 14px;
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

.device-toolbar__filters,
.device-toolbar__actions {
    display: flex;
    align-items: center;
    gap: 10px;
}

.device-toolbar__filters {
    flex-wrap: wrap;
    min-width: 0;
}

.device-toolbar__actions {
    flex: 0 0 auto;
}

.device-create-button {
    height: 32px;
    padding: 0 16px;
}

.device-table-wrap {
    flex: 1;
    min-height: 0;
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

    .device-toolbar {
        align-items: flex-start;
        flex-wrap: wrap;
    }

    .device-toolbar__filters {
        flex: 1 1 540px;
    }

    :deep(.device-toolbar__filters .search-text) {
        flex: 1 1 240px;
    }

    :deep(.device-toolbar__filters .dropdown-list) {
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

    .device-toolbar {
        gap: 10px;
    }

    .device-toolbar__filters,
    .device-toolbar__actions {
        width: 100%;
    }

    :deep(.device-toolbar__filters .search-text),
    :deep(.device-toolbar__filters .dropdown-list) {
        flex: 1 1 100%;
        width: 100% !important;
    }

    .device-create-button {
        width: 100%;
    }
}
</style>
