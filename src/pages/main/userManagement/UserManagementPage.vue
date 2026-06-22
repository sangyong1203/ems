<template>
    <PageBody>
        <SearchBox :on-search="searchData">
            <SearchText
                v-model="searchParams.keyword"
                label="Keyword"
                placeholder="Name, email, department"
                width="360px"
                label-width="80px"
            />
            <DropdownList
                v-model="searchParams.role"
                label="Role"
                placeholder="All roles"
                width="260px"
                label-width="56px"
                clearable
                :list="roleOptions"
                option-label="label"
                option-value="value"
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
        </SearchBox>

        <ContentBlock>
            <OperationBox title="Total Users" :total="addComma(totalCount)">
                <el-button type="primary" @click="openCreateDialog">Add User</el-button>
            </OperationBox>

            <el-table :data="tableData" border stripe height="100%" :empty-text="'No Data'" @row-click="openEditDialog">
                <el-table-column prop="name" label="Name" min-width="150" />
                <el-table-column prop="email" label="Email" min-width="220" />
                <el-table-column prop="department" label="Department" min-width="190" />
                <el-table-column prop="role" label="Role" width="150" />
                <el-table-column prop="status" label="Status" width="120">
                    <template #default="{ row }">
                        <CommonTag :label="row.status" :variant="row.status" />
                    </template>
                </el-table-column>
                <el-table-column prop="lastLoginAt" label="Last Login" width="180" />
                <el-table-column prop="createdAt" label="Created" width="180" />
                <el-table-column label="Actions" width="140" align="center">
                    <template #default="{ row }">
                        <div class="table-actions">
                            <el-button link @click.stop="openEditDialog(row)"
                                ><el-icon color="#e76dff" size="large"><Edit /></el-icon
                            ></el-button>
                            <el-button link @click.stop="confirmDeleteUser(row)"
                                ><el-icon color="gray" size="large"><Delete /></el-icon
                            ></el-button>
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

        <UserFormDialog v-model="isDialogOpen" :editing-user="editingUser" @cancel="closeDialog" @submit="saveUser" />
    </PageBody>
</template>

<script lang="ts" setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessageBox } from 'element-plus'
import {
    CommonTag,
    ContentBlock,
    DropdownList,
    OperationBox,
    PageBody,
    Pagination,
    SearchBox,
    SearchText,
} from '@/shared/components'
import { Message, Notification } from '@/shared/composables/useFeedback'
import { addComma, isSuccessResponse } from '@/shared/utils'
import UserFormDialog from './components/UserFormDialog.vue'
import userManagementApi from './service/userManagement.api.ts'
import type { RequestParams, UserItem, UserRole, UserSaveParams, UserStatus } from './service/userManagement.types.ts'

const tableData = ref<UserItem[]>([])
const totalCount = ref(0)
const isDialogOpen = ref(false)
const editingUser = ref<UserItem | null>(null)

const roleOptions: Array<{ label: UserRole; value: UserRole }> = [
    { label: 'Platform Admin', value: 'Platform Admin' },
    { label: 'Operator', value: 'Operator' },
    { label: 'Viewer', value: 'Viewer' },
]

const statusOptions: Array<{ label: UserStatus; value: UserStatus }> = [
    { label: 'Active', value: 'Active' },
    { label: 'Inactive', value: 'Inactive' },
    { label: 'Locked', value: 'Locked' },
]

const searchParams = reactive<RequestParams>({
    keyword: '',
    role: '',
    status: '',
    pageNumber: 1,
    pageSize: 10,
})

onMounted(async () => {
    await searchData()
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
    try {
        const res = await userManagementApi.getList(searchParams)

        if (!isSuccessResponse(res.result)) {
            tableData.value = []
            totalCount.value = 0
            Message.warning(res.resultMessage || 'Failed to load users.')
            return
        }

        tableData.value = res.data.list
        totalCount.value = res.data.totalCount
    } catch {
        tableData.value = []
        totalCount.value = 0
        Message.error('Failed to load users.')
    }
}

const openCreateDialog = () => {
    editingUser.value = null
    isDialogOpen.value = true
}

const openEditDialog = (row: UserItem) => {
    editingUser.value = row
    isDialogOpen.value = true
}

const closeDialog = () => {
    isDialogOpen.value = false
}

const saveUser = async (payload: UserSaveParams) => {
    const res = editingUser.value?.id
        ? await userManagementApi.updateUser(editingUser.value.id, payload)
        : await userManagementApi.createUser(payload)

    if (!isSuccessResponse(res.result)) {
        Message.warning(res.resultMessage || 'Failed to save user.')
        return
    }

    await searchData()
    Message.success(editingUser.value ? 'User updated.' : 'User added.')
    closeDialog()
}

const confirmDeleteUser = async (row: UserItem) => {
    try {
        await ElMessageBox.confirm(`Delete ${row.name}?`, 'Confirm', {
            confirmButtonText: 'Delete',
            cancelButtonText: 'Cancel',
            type: 'warning',
        })
        await deleteUser(row)
    } catch (error) {
        if (error !== 'cancel' && error !== 'close') {
            Message.error('Failed to delete user.')
        }
    }
}

const deleteUser = async (row: UserItem) => {
    const res = await userManagementApi.deleteUser(row.id)
    if (!isSuccessResponse(res.result)) {
        Message.warning(res.resultMessage || 'Failed to delete user.')
        return
    }

    await searchData()
    Notification.success('User deleted.')
}
</script>
