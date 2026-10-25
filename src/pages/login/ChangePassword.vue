<template>
    <BaseDialog
        v-model="visible"
        title="Change password"
        width="500px"
        :button-types="['Cancel', 'Save']"
        @on-cancel="visible = false"
        @on-save="handleSave"
    >
        <el-form class="change-password-form" label-position="top" @submit.prevent="handleSave">
            <el-form-item label="Current password">
                <el-input v-model="form.currentPassword" type="password" show-password autocomplete="current-password" :maxlength="128" />
            </el-form-item>
            <el-form-item label="New password (8–128 characters)">
                <el-input v-model="form.newPassword" type="password" show-password autocomplete="new-password" :maxlength="128" />
            </el-form-item>
            <el-form-item label="Confirm new password">
                <el-input v-model="form.confirmPassword" type="password" show-password autocomplete="new-password" :maxlength="128" />
            </el-form-item>
            <p class="change-password-message" role="alert">{{ validationMessage }}</p>
        </el-form>
    </BaseDialog>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { BaseDialog } from '@/components'
import { Notification } from '@/composables/useFeedback'
import { useAuthStore } from '@/stores/auth.store'
import { useMenuStore } from '@/stores/menu.store'
import { useNavStore } from '@/stores/nav.store'
import loginApi from './service/login.api'

const visible = ref(false) // 비밀번호 변경 창 표시 여부
const saving = ref(false) // 중복 변경 요청 방지
const validationMessage = ref('') // 입력 및 처리 오류 안내
const form = reactive({ currentPassword: '', newPassword: '', confirmPassword: '' }) // 비밀번호 입력
const router = useRouter() // 변경 후 로그인 화면으로 이동
const authStore = useAuthStore() // 폐기된 인증 상태 제거

// 창을 열 때 이전 비밀번호와 오류 메시지를 비웁니다.
const openDialog = () => {
    Object.assign(form, { currentPassword: '', newPassword: '', confirmPassword: '' })
    validationMessage.value = ''
    visible.value = true
}

// 현재 비밀번호를 재확인하여 변경하고 폐기된 세션으로 요청하지 않도록 로그인 화면으로 이동합니다.
const handleSave = async () => {
    if (saving.value) return
    if (!form.currentPassword || form.newPassword.length < 8 || form.newPassword.length > 128) {
        validationMessage.value = 'Enter your current password and a new password of 8–128 characters.'
        return
    }
    if (form.newPassword !== form.confirmPassword) {
        validationMessage.value = 'The new passwords do not match.'
        return
    }
    saving.value = true
    try {
        const response = await loginApi.changePassword({ currentPassword: form.currentPassword, newPassword: form.newPassword })
        if (response.result !== 'SUCCESS') {
            validationMessage.value = response.resultMessage
            return
        }
        visible.value = false
        Object.assign(form, { currentPassword: '', newPassword: '', confirmPassword: '' })
        authStore.clearSession()
        useMenuStore().init()
        useNavStore().init()
        Notification.success('Password changed. Please sign in again.')
        await router.replace('/login')
    } catch {
        validationMessage.value = 'Password change failed. Check your current password and try again.'
    } finally {
        saving.value = false
    }
}

defineExpose({ openDialog })
</script>
