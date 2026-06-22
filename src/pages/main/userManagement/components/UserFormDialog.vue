<template>
    <BaseDialog
        :model-value="modelValue"
        :title="editingUser ? 'Edit User' : 'Add User'"
        width="560px"
        :button-types="['Cancel', 'Save']"
        @update:model-value="emit('update:modelValue', $event)"
        @on-cancel="emit('cancel')"
        @on-save="handleSave"
    >
        <el-form ref="formRef" :model="form" :rules="rules" label-width="120px" label-position="left">
            <el-form-item label="Name" prop="name">
                <el-input v-model="form.name" placeholder="Enter name" />
            </el-form-item>
            <el-form-item label="Email" prop="email">
                <el-input v-model="form.email" placeholder="Enter email" />
            </el-form-item>
            <el-form-item label="Department" prop="department">
                <el-input v-model="form.department" placeholder="Enter department" />
            </el-form-item>
            <el-form-item label="Role" prop="role">
                <el-select v-model="form.role" placeholder="Select role" style="width: 100%">
                    <el-option v-for="item in roleOptions" :key="item.value" :label="item.label" :value="item.value" />
                </el-select>
            </el-form-item>
            <el-form-item label="Status" prop="status">
                <el-select v-model="form.status" placeholder="Select status" style="width: 100%">
                    <el-option
                        v-for="item in statusOptions"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    />
                </el-select>
            </el-form-item>
        </el-form>
    </BaseDialog>
</template>

<script lang="ts" setup>
import { nextTick, reactive, ref, watch } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { BaseDialog } from '@/shared/components'
import { REG_EXPS } from '@/shared/utils'
import type { UserItem, UserRole, UserSaveParams, UserStatus } from '../service/userManagement.types'

type SelectOption<T extends string> = {
    label: T
    value: T
}

const props = defineProps<{
    modelValue: boolean
    editingUser: UserItem | null
}>()

const emit = defineEmits<{
    'update:modelValue': [value: boolean]
    submit: [payload: UserSaveParams]
    cancel: []
}>()

const formRef = ref<FormInstance | null>(null)
const form = reactive<UserSaveParams>({
    name: '',
    email: '',
    department: '',
    role: 'Operator',
    status: 'Active',
})

const roleOptions: Array<SelectOption<UserRole>> = [
    { label: 'Platform Admin', value: 'Platform Admin' },
    { label: 'Operator', value: 'Operator' },
    { label: 'Viewer', value: 'Viewer' },
]

const statusOptions: Array<SelectOption<UserStatus>> = [
    { label: 'Active', value: 'Active' },
    { label: 'Inactive', value: 'Inactive' },
    { label: 'Locked', value: 'Locked' },
]

const rules: FormRules = {
    name: [{ required: true, message: 'Please enter a name.', trigger: 'blur' }],
    email: [
        { required: true, message: 'Please enter an email.', trigger: 'blur' },
        {
            validator: (_rule, value, callback) => {
                if (!REG_EXPS.EMAIL.test(String(value ?? ''))) {
                    callback(new Error('Please enter a valid email.'))
                    return
                }
                callback()
            },
            trigger: 'blur',
        },
    ],
    department: [{ required: true, message: 'Please enter a department.', trigger: 'blur' }],
    role: [{ required: true, message: 'Please select a role.', trigger: 'change' }],
    status: [{ required: true, message: 'Please select a status.', trigger: 'change' }],
}

const resetForm = () => {
    form.name = ''
    form.email = ''
    form.department = ''
    form.role = 'Operator'
    form.status = 'Active'
}

watch(
    () => [props.modelValue, props.editingUser] as const,
    async ([isOpen, user]) => {
        if (!isOpen) return

        if (user) {
            form.name = user.name
            form.email = user.email
            form.department = user.department
            form.role = user.role
            form.status = user.status
        } else {
            resetForm()
        }

        await nextTick()
        clearValidate()
    },
    { immediate: true },
)

const clearValidate = () => {
    formRef.value?.clearValidate()
}

const handleSave = async () => {
    const isValid = await formRef.value?.validate().catch(() => false)
    if (!isValid) return

    emit('submit', { ...form })
}

defineExpose({ clearValidate })
</script>
