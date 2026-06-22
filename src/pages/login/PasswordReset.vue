<template>
    <div class="wrapper">
        <div class="header">
            <div>Admin Portal</div>
        </div>

        <div class="instruction">
            <p>Please set your new password following the rules below:</p>
        </div>

        <div class="guideline">
            <ul>
                <li>
                    Please write in 8 to 12 characters using a mixture of English letters, numbers and special
                    characters (!@#$%^&*)
                </li>
                <li>Do not include email address.</li>
                <li>The same character cannot be repeated more than 3 times.</li>
                <li>You cannot use more than 3 consecutive digits</li>
            </ul>
        </div>

        <div class="input-form">
            <el-form label-width="auto" label-position="left" require-asterisk-position="right">
                <el-form-item label="New Password" prop="newPassword">
                    <el-input
                        v-model="formData.newPassword"
                        maxlength="12"
                        type="password"
                        placeholder="Input password"
                    />
                </el-form-item>
                <el-form-item label="New Password confirm" prop="newPasswordConfirm">
                    <el-input
                        v-model="formData.newPasswordConfirm"
                        maxlength="12"
                        type="password"
                        placeholder="New Password confirm"
                    />
                </el-form-item>
            </el-form>
            <div class="validationMsg">{{ validationMsg }}</div>
        </div>

        <div class="btn-container">
            <el-button @click="handleCancel">Cancel</el-button>
            <el-button type="primary" @click="handleSave">Save</el-button>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, reactive } from 'vue'
import type { ChangePassword } from './service/login.types'
import { useRouter, useRoute } from 'vue-router'
import { onMounted } from 'vue'
import loginApi from '@/pages/login/service/login.api'
import { Notification } from '@/shared/composables/useFeedback'

const router = useRouter()
const route = useRoute()

const formData = reactive<ChangePassword>({
    newPassword: '',
    newPasswordConfirm: '',
})

const validationMsg = ref('')

const handleSave = async () => {
    if (!formData.newPassword) {
        validationMsg.value = 'Please enter a new password.'
        return
    }

    if (!formData.newPasswordConfirm) {
        validationMsg.value = 'Please enter your password verification number.'
        return
    }

    if (formData.newPassword !== formData.newPasswordConfirm) {
        validationMsg.value = 'The new password and confirmation do not match.'
        return
    }

    const passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,12}$/
    if (!passwordPattern.test(formData.newPassword)) {
        validationMsg.value =
            'Please check your password again. Passwords must be 8-12 characters mixed with alphabetic characters, numbers, and special characters (!@#$%&*^).'
        return
    }

    const repeatCharPattern = /(.)\1\1/
    if (repeatCharPattern.test(formData.newPassword)) {
        validationMsg.value =
            'Please check your password again. You cannot repeat the same character more than 3 times.'
        return
    }

    const consecutiveCharPattern = /012|123|234|345|456|567|678|789|890|987|876|765|654|543|432|321|210/
    if (consecutiveCharPattern.test(formData.newPassword)) {
        validationMsg.value =
            'Please check your password again. You cannot repeat consecutive numbers more than 3 times.'
        return
    }

    if (verificationToken.value) {
        loginApi
            .resetPassword({
                password: formData.newPassword,
                requestType: 'PWDRESET',
                isAdmin: 'Y',
                verificationToken: verificationToken.value,
            })
            .then(res => {
                if (res.result.toLowerCase() == 'success') {
                    Notification.success(
                        'Your password has been reset. Please enter a new password to complete the process.',
                    )
                    router.push({ name: 'login' })
                } else {
                    validationMsg.value =
                        res.resultMessage || 'An error occurred while changing the password. Please try again.'
                }
            })
            .catch(err => {
                console.log(err)
                validationMsg.value =
                    err.resultMessage || 'An error occurred while changing the password. Please try again.'
            })
    }
}

const handleCancel = () => {
    router.push({ name: 'login' })
}

const verificationToken = ref('')
onMounted(() => {
    // console.log(route.params.verificationToken)
    verificationToken.value = route.params.verificationToken as string
})
</script>

<style scoped>
.wrapper {
    width: 920px;
    margin: 0 auto;

    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    padding: 40px;

    .header {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 840px;
        height: 144px;
        gap: 16px;

        div:first-child {
            width: 270px;
            margin: 0 auto;
        }

        div:last-child {
            font-weight: 400;
            font-style: Light;
            font-size: 32px;
        }
    }

    .instruction {
        p {
            margin: 16px 8px;
            width: 840px;
            height: 15px;
            font-weight: 400;
            font-style: Regular;
            font-size: 15px;
            line-height: 100%;
            letter-spacing: 0%;
            text-align: center;
            vertical-align: middle;
            color: #ff383c;
        }
    }

    .guideline {
        width: 840px;
        height: 160px;
        padding: 20px;
        background-color: #f7f6f9;
        margin: 16px 8px;
        border-radius: 8px;

        ul {
            li {
                width: 800px;
                font-weight: 400;
                font-size: 16px;
                line-height: 160%;
                letter-spacing: -3%;
                color: #3e2576;
            }
        }
    }

    .input-form {
        width: 840px;
        height: 179px;
        gap: 20px;
        border-top-width: 2px;
        padding-top: 20px;
        padding-bottom: 20px;

        :deep(.el-form-item__label) {
            font-weight: 600;
            font-style: Bold;
            font-size: 18px;
            line-height: 20px;
            letter-spacing: 0%;
        }

        :deep(.el-input__wrapper) {
            border: none !important;
            box-shadow: none !important;
        }

        :deep(.el-input__inner) {
            width: 613px;
            height: 36px;
            min-width: 180px;
            border-radius: 999px;
            padding-top: 4px;
            padding-right: 8px;
            padding-bottom: 4px;
            padding-left: 20px;
            background-color: #f4f4f4;
            border: none;
        }

        .validationMsg {
            margin: 16px 8px;
            font-weight: 400;
            font-size: 15px;
            text-align: center;
            vertical-align: middle;
            color: #ff383c;
        }
    }

    .btn-container {
        display: flex;
        justify-content: center;
        gap: 4px;
    }
}
</style>
