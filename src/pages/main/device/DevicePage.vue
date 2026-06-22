<template>
    <PageBody>
        <SearchBox :on-search="searchData" extra>
            <SearchText
                v-model="searchParams.keyword"
                label="Keyword"
                placeholder="Name, IP, location"
                width="360px"
                label-width="80px"
            />
            <DropdownList
                v-model="searchParams.status"
                label="Status"
                placeholder="All statuses"
                width="270px"
                label-width="64px"
                clearable
                :list="statusOptions"
                option-label="label"
                option-value="value"
            />
            <template #extra>
                <DropdownList
                    v-model="searchParams.model"
                    label="Model"
                    placeholder="All models"
                    width="280px"
                    label-width="64px"
                    clearable
                    :list="modelOptions"
                    option-label="label"
                    option-value="value"
                />
                <DropdownList
                    v-model="searchParams.detectionEnabled"
                    label="Detection"
                    placeholder="All"
                    width="240px"
                    label-width="88px"
                    clearable
                    :list="enabledOptions"
                    option-label="label"
                    option-value="value"
                />
                <DropdownList
                    v-model="searchParams.aiAnalysisEnabled"
                    label="AI Analysis"
                    placeholder="All"
                    width="250px"
                    label-width="96px"
                    clearable
                    :list="enabledOptions"
                    option-label="label"
                    option-value="value"
                />
            </template>
        </SearchBox>

        <ContentBlock>
            <OperationBox title="Total Cameras" :total="addComma(totalCount)">
                <el-button type="primary" @click="openCreateDialog">Add Camera</el-button>
            </OperationBox>

            <el-table
                v-loading="isTableLoading"
                :data="tableData"
                border
                stripe
                height="100%"
                :empty-text="isTableLoading ? '' : 'No Data'"
                @row-click="openEditDialog"
            >
                <el-table-column prop="name" label="Camera Name" min-width="180" />
                <el-table-column prop="ipAddress" label="IP Address" width="150" />
                <el-table-column prop="location" label="Location" min-width="170" />
                <el-table-column prop="model" label="Model" min-width="150" />
                <el-table-column label="Resolution" width="130">
                    <template #default="{ row }">{{ row.resolutionWidth }}x{{ row.resolutionHeight }}</template>
                </el-table-column>
                <el-table-column prop="fps" label="FPS" width="80" align="right" />
                <el-table-column prop="status" label="Status" width="130">
                    <template #default="{ row }">
                        <CommonTag :label="row.status" :variant="row.status" />
                    </template>
                </el-table-column>
                <el-table-column label="Detection" width="120" align="center">
                    <template #default="{ row }">
                        <CommonTag
                            :label="row.objectDetectionEnabled ? 'Enabled' : 'Disabled'"
                            :variant="row.objectDetectionEnabled ? 'Active' : 'Inactive'"
                        />
                    </template>
                </el-table-column>
                <el-table-column label="AI Analysis" width="130" align="center">
                    <template #default="{ row }">
                        <CommonTag
                            :label="row.aiAnalysisEnabled ? 'Enabled' : 'Disabled'"
                            :variant="row.aiAnalysisEnabled ? 'Active' : 'Inactive'"
                        />
                    </template>
                </el-table-column>
                <el-table-column label="Targets" width="100" align="right">
                    <template #default="{ row }">{{ row.detectionTargets.length }}</template>
                </el-table-column>
                <el-table-column prop="lastSeenAt" label="Last Seen" width="180" />
                <el-table-column label="Actions" width="170" align="center" fixed="right">
                    <template #default="{ row }">
                        <div class="table-actions">
                            <el-button link @click.stop="openEditDialog(row)">
                                <el-icon color="#e76dff" size="large"><Edit /></el-icon>
                            </el-button>
                            <el-button link @click.stop="openControlDialog(row)">
                                <el-icon color="#15e0b7" size="large"><Operation /></el-icon>
                            </el-button>
                            <el-button link @click.stop="deleteDevice(row)">
                                <el-icon color="gray" size="large"><Delete /></el-icon>
                            </el-button>
                        </div>
                    </template>
                </el-table-column>
            </el-table>

            <Pagination
                :total-row="totalCount"
                :page="searchParams.pageNumber"
                :row-size="searchParams.pageSize"
                @current-change="changePage"
                @size-change="changePageSize"
            />
        </ContentBlock>

        <DeviceFormDialog v-model="isFormDialogOpen" :device="editingDevice" @save="saveDevice" />
        <DeviceControlDialog
            v-model="isControlDialogOpen"
            :device="controlDevice"
            @save="saveDeviceSettings"
            @command="sendDeviceCommand"
        />
    </PageBody>
</template>

<script lang="ts" setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { Delete, Edit, Operation } from '@element-plus/icons-vue'
import { ElMessageBox } from 'element-plus'
import { Message, Notification } from '@/shared/composables/useFeedback'
import { addComma, isSuccessResponse } from '@/shared/utils'
import DeviceControlDialog from './components/DeviceControlDialog.vue'
import DeviceFormDialog from './components/DeviceFormDialog.vue'
import deviceApi from './service/device.api.ts'
import type {
    DeviceCommand,
    DeviceItem,
    DeviceSaveParams,
    DeviceSearchParams,
    DeviceSettingParams,
    DeviceStatus,
} from './service/device.types.ts'

const tableData = ref<DeviceItem[]>([])
const totalCount = ref(0)
const isTableLoading = ref(false)
const isFormDialogOpen = ref(false)
const isControlDialogOpen = ref(false)
const editingDevice = ref<DeviceItem | null>(null)
const controlDevice = ref<DeviceItem | null>(null)

const statusOptions: Array<{ label: DeviceStatus; value: DeviceStatus }> = [
    { label: 'Online', value: 'Online' },
    { label: 'Offline', value: 'Offline' },
    { label: 'Error', value: 'Error' },
    { label: 'Maintenance', value: 'Maintenance' },
]

const enabledOptions = [
    { label: 'Enabled', value: 'Y' },
    { label: 'Disabled', value: 'N' },
]

const modelOptions = computed(() => {
    const models = [...new Set(tableData.value.map(item => item.model).filter(Boolean))]
    return models.map(model => ({ label: model, value: model }))
})

const searchParams = reactive<DeviceSearchParams>({
    keyword: '',
    status: '',
    model: '',
    detectionEnabled: '',
    aiAnalysisEnabled: '',
    pageNumber: 1,
    pageSize: 10,
})

onMounted(async () => {
    await getList()
})

const searchData = async () => {
    searchParams.pageNumber = 1
    await getList()
}

const changePage = async (page: number) => {
    searchParams.pageNumber = page
    await getList()
}

const changePageSize = async (pageSize: number) => {
    searchParams.pageNumber = 1
    searchParams.pageSize = pageSize
    await getList()
}

const getList = async () => {
    isTableLoading.value = true
    try {
        const res = await deviceApi.getList(searchParams)
        if (!isSuccessResponse(res.result)) {
            tableData.value = []
            totalCount.value = 0
            Message.warning(res.resultMessage || 'Failed to load cameras.')
            return
        }

        tableData.value = res.data.list
        totalCount.value = res.data.totalCount
    } catch {
        tableData.value = []
        totalCount.value = 0
        Message.error('Failed to load cameras.')
    } finally {
        isTableLoading.value = false
    }
}

const openCreateDialog = () => {
    editingDevice.value = null
    isFormDialogOpen.value = true
}

const openEditDialog = (row: DeviceItem) => {
    editingDevice.value = row
    isFormDialogOpen.value = true
}

const openControlDialog = (row: DeviceItem) => {
    controlDevice.value = row
    isControlDialogOpen.value = true
}

const saveDevice = async (params: DeviceSaveParams) => {
    try {
        if (editingDevice.value?.id) {
            await deviceApi.updateDevice(editingDevice.value.id, params)
            Message.success('Camera updated.')
        } else {
            await deviceApi.createDevice(params)
            Message.success('Camera added.')
        }
        isFormDialogOpen.value = false
        await getList()
    } catch {
        Message.error('Failed to save camera.')
    }
}

const saveDeviceSettings = async (params: DeviceSettingParams) => {
    if (!controlDevice.value) return
    try {
        await deviceApi.updateSettings(controlDevice.value.id, params)
        Message.success('Camera settings updated.')
        isControlDialogOpen.value = false
        await getList()
    } catch {
        Message.error('Failed to update camera settings.')
    }
}

const sendDeviceCommand = async (command: DeviceCommand) => {
    if (!controlDevice.value) return
    try {
        const res = await deviceApi.sendCommand(controlDevice.value.id, { command })
        if (!isSuccessResponse(res.result)) {
            Message.warning(res.resultMessage || 'Command failed.')
            return
        }
        Notification.success(`${command.replace(/_/g, ' ')} command accepted.`)
        await getList()
    } catch {
        Message.error('Failed to send camera command.')
    }
}

const deleteDevice = async (row: DeviceItem) => {
    try {
        await ElMessageBox.confirm(`Delete ${row.name}?`, 'Confirm', {
            confirmButtonText: 'Delete',
            cancelButtonText: 'Cancel',
            type: 'warning',
        })
        await deviceApi.deleteDevice(row.id)
        Notification.success('Camera deleted.')
        await getList()
    } catch (error) {
        if (error !== 'cancel') {
            Message.error('Failed to delete camera.')
        }
    }
}
</script>
