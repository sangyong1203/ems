<template>
    <BaseDialog
        :model-value="isShowDialog"
        :title="'Password reset'"
        width="450"
        height="35%"
        :buttonTypes="['Close', 'Reset']"
        @on-close="onClose"
        @on-reset="onReset"
    >
        <p class="msg">
            We will send a password reset link to the address registered with your account. <br />
            Please enter your Email to proceed.
        </p>

        <el-form ref="ruleFormRef" :model="ruleForm" :rules="rules" require-asterisk-position="right" @submit.prevent>
            <el-form-item label="E-mail" prop="email">
                <el-input v-model="ruleForm.email" maxlength="36" />
            </el-form-item>
        </el-form>
    </BaseDialog>
</template>

<script lang="ts" setup>
import { BaseDialog } from '@/shared/components'
import type { FormRules, FormInstance } from 'element-plus'
import { ref, reactive } from 'vue'
import loginApi from '@/pages/login/service/login.api'
import { Notification } from '@/shared/composables/useFeedback'

const emits = defineEmits(['refresh'])

const isShowDialog = ref(false)

const onClose = () => {
    isShowDialog.value = false
    ruleFormRef.value?.clearValidate()
    emits('refresh')
}

const onReset = async () => {
    const valid = await ruleFormRef.value?.validate()
    if (valid) {
        const params = {
            email: ruleForm.email,
            requestType: 'PWDRESET',
            isAdmin: 'Y',
        }

        loginApi
            .requestPasswordReset(params)
            .then(res => {
                if (res.result.toLowerCase() == 'success') {
                    Notification.success(
                        'A password reset email has been sent to the address associated with your account. Click the link in the email to securely create a new password.',
                    )
                    isShowDialog.value = false
                } else {
                    Notification.error(
                        res.resultMessage || 'An error occurred while changing the password. Please try again.',
                    )
                }
            })
            .catch(() => {
                Notification.error('An error occurred while changing the password. Please try again.')
            })
    }
}

const openDialog = async () => {
    isShowDialog.value = true
    ruleForm.email = ''
    ruleFormRef.value?.clearValidate()
}
defineExpose({ openDialog })

const ruleFormRef = ref<FormInstance>()
const ruleForm = reactive({
    email: '',
})
const rules = reactive<FormRules>({
    email: [
        { required: true, message: 'Please enter your email address.', trigger: [] },
        {
            type: 'email',
            message: 'Please enter a valid email address.',
            trigger: [],
        },
    ],
})
</script>

<style scoped>
.msg {
    margin-bottom: 30px;
}
</style>
