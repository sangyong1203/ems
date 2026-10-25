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
            <el-form-item :label="editingUser ? 'New password' : 'Initial password'" prop="password">
                <el-input
                    v-model="form.password"
                    type="password"
                    show-password
                    autocomplete="new-password"
                    :maxlength="128"
                    :placeholder="editingUser ? 'Leave blank to keep the password' : 'Enter 8–128 characters'"
                />
            </el-form-item>
            <el-form-item label="Department" prop="department">
                <el-input v-model="form.department" placeholder="Enter department" />
            </el-form-item>
            <p class="user-role-guide">Only Platform Admin accounts can sign in.</p>
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
import { BaseDialog } from '@/components'
import { REG_EXPS } from '@/utils'
import type { UserItem, UserRole, UserSaveParams, UserStatus } from '../service/userManagement.types'

type SelectOption<T extends string> = {
    label: T
    value: T
}

const props = defineProps<{
    modelValue: boolean // 모달 표시 여부
    editingUser: UserItem | null // 수정 대상 사용자 정보 (신규 등록 시 null)
}>()

const emit = defineEmits<{
    'update:modelValue': [value: boolean] // 모달 표시 상태 업데이트
    submit: [payload: UserSaveParams] // 사용자 저장 이벤트
    cancel: [] // 취소 이벤트
}>()

const formRef = ref<FormInstance | null>(null) // 엘리먼트 폼 인스턴스
const form = reactive<UserSaveParams>({ // 사용자 입력 폼 데이터
    name: '',
    email: '',
    department: '',
    role: 'Platform Admin',
    password: '',
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

const rules: FormRules = { // 폼 유효성 검사 규칙
    password: [{
        validator: (_rule, value: string | undefined, callback) => {
            if (!value && props.editingUser) {
                callback()
                return
            }
            if (!value || value.length < 8 || value.length > 128) {
                callback(new Error('Enter an initial password of 8–128 characters.'))
                return
            }
            callback()
        },
        trigger: 'blur',
    }],
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

// resetForm 폼 입력값 기본값 초기화
const resetForm = () => {
    form.name = ''
    form.email = ''
    form.department = ''
    form.role = 'Platform Admin'
    form.password = ''
    form.status = 'Active'
}

// watch(props) 모달 열릴 때 사용자 데이터 바인딩 및 유효성 검사 초기화
watch(
    () => [props.modelValue, props.editingUser] as const,
    async ([isOpen, user]) => {
        if (!isOpen) return

        form.password = ''
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

// clearValidate 폼 유효성 검증 오류 메시지 제거
const clearValidate = () => {
    formRef.value?.clearValidate()
}

// handleSave 폼 유효성 검증 후 사용자 저장 전달
const handleSave = async () => {
    const isValid = await formRef.value?.validate().catch(() => false)
    if (!isValid) return

    const { password, ...user } = form
    emit('submit', { ...user, ...(password ? { password } : {}) })
}

defineExpose({ clearValidate })
</script>
