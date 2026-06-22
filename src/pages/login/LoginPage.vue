<template>
    <div class="layout-login">
        <div class="login-block fade-in">
            <div class="login-block-content">
                <div class="login-header">
                    <!-- <logoMark class="logo-mark"></logoMark> -->
                    <p class="login-header-content">Solar ESS</p>
                    <p>Energy Management System</p>
                </div>
                <div class="devide-line"></div>
                <div class="login">
                    <el-form ref="formRef" :model="loginForm" :rules="rules" :show-message="false" autocomplete="off">
                        <input class="login-autofill-blocker" type="text" name="username" autocomplete="username" />
                        <input
                            class="login-autofill-blocker"
                            type="password"
                            name="password"
                            autocomplete="current-password"
                        />
                        <el-form-item prop="loginId" style="margin-bottom: 24px">
                            <el-input
                                v-model="loginForm.loginId"
                                :placeholder="'User ID'"
                                autocomplete="off"
                                :readonly="isLoginIdReadonly"
                                name="login-id"
                                autocapitalize="off"
                                autocorrect="off"
                                spellcheck="false"
                                @focus="isLoginIdReadonly = false"
                                @mousedown="isLoginIdReadonly = false"
                                @input="message = ''"
                            >
                                <template #prefix>
                                    <!-- <IconLoginUser></IconLoginUser> -->
                                    <el-icon><User /></el-icon>
                                </template>
                            </el-input>
                        </el-form-item>
                        <el-form-item prop="password">
                            <el-input
                                v-model="loginForm.password"
                                :placeholder="'Password'"
                                type="password"
                                show-password
                                autocomplete="new-password"
                                :readonly="isPasswordReadonly"
                                name="login-password"
                                class="custom-pw-input"
                                @focus="isPasswordReadonly = false"
                                @mousedown="isPasswordReadonly = false"
                                @input="message = ''"
                                @keyup.enter="login()"
                            >
                                <template #prefix>
                                    <!-- <IconLoginPassword></IconLoginPassword> -->
                                    <el-icon><Lock /></el-icon>
                                </template>
                            </el-input>
                        </el-form-item>

                        <div style="position: relative; margin-top: 12px">
                            <el-text v-model="message" type="warning" size="large" class="WarningMessage">{{
                                message
                            }}</el-text>

                            <el-button type="primary" size="large" class="login-btn" @click="login()">
                                <div style="position: relative">
                                    <el-icon v-show="isLoading" class="loading-icon icon-spin"><Loading /></el-icon>
                                    {{ 'Sign In' }}
                                </div>
                            </el-button>
                        </div>
                    </el-form>
                </div>
                <div class="find-password">
                    <p>
                        <a @click="passwordReset" style="cursor: pointer">Forgot password?</a>
                    </p>
                </div>
            </div>
        </div>
    </div>
    <PasswordResetDialog ref="PasswordResetDialogRef"></PasswordResetDialog>
</template>

<script lang="ts" setup>
import { ref, onMounted, reactive } from 'vue'
import type { FormRules, FormInstance } from 'element-plus'
import { ElNotification } from 'element-plus'
import { useRouter } from 'vue-router'
import PasswordResetDialog from './PasswordResetDialog.vue'
import loginApi from './service/login.api.ts'
import { useMenuStore } from '@/stores/menu.store'
import { useNavStore } from '@/stores/nav.store'
import { useAuthStore } from '@/stores/auth.store'
import type { RoleLevel } from '@/stores/auth.store'

const router = useRouter()
const formRef = ref<FormInstance | null>(null)
const menuStore = useMenuStore()
const navStore = useNavStore()
const authStore = useAuthStore()
const loginForm = reactive({
    loginId: '',
    password: '',
    isSaveId: false,
})
const rules: FormRules = {
    loginId: [
        {
            validator: (rule: any, value: any, callback: any) => {
                if (!String(value ?? '').trim()) {
                    callback(new Error('Please enter your email address.'))
                } else {
                    callback()
                }
            },
            trigger: 'blur',
        },
    ],
    password: [
        {
            validator: (rule: any, value: any, callback: any) => {
                if (!String(value ?? '').trim()) {
                    callback(new Error('Please enter your password.'))
                } else {
                    callback()
                }
            },
            trigger: 'blur',
        },
    ],
}

onMounted(async () => {})

const message = ref('')
const isLoading = ref(false)
const isLoginIdReadonly = ref(true)
const isPasswordReadonly = ref(true)

const normalizeRoleLevel = (value?: string): RoleLevel => {
    if (value === 'PLATFORM_ADMIN' || value === 'USER') return value
    return 'PLATFORM_ADMIN'
}

const completeLogin = async (signinData: any, loginId: string) => {
    authStore.setTokens({
        accessToken: signinData.accessToken,
        refreshToken: signinData.refreshToken,
        verificationToken: signinData.verificationToken,
    })

    const userInfoResponse = await loginApi.getUserInfo()
    const userInfo = userInfoResponse.data ?? {}
    const landingPage = signinData.landingPage || userInfo.landingPage || '/dashboard'
    const userLevel = normalizeRoleLevel(userInfo.userLevel)

    navStore.init()
    menuStore.init()
    menuStore.setTempMenu(userLevel)
    authStore.setSession({
        tokens: {
            accessToken: signinData.accessToken,
            refreshToken: signinData.refreshToken,
            verificationToken: signinData.verificationToken,
        },
        user: {
            loginId: userInfo.email || loginId,
            name: userInfo.krName || userInfo.name || '',
            userLevel,
            email: userInfo.email || loginId,
            landingPage,
        },
    })

    router.push({ path: landingPage })
}

const login = () => {
    if (isLoading.value) return
    if (!formRef.value) return
    try {
        formRef.value.validate(async (valid: boolean, invalidFields?: Record<string, Array<{ message?: string }>>) => {
            if (valid) {
                const loginId = loginForm.loginId.trim()
                const password = loginForm.password.trim()
                loginForm.loginId = loginId
                loginForm.password = password

                const params = {
                    username: loginId,
                    password: password,
                }
                isLoading.value = true
                ElNotification.closeAll()
                try {
                    const res = await loginApi.signin(params)
                    if (res.result == 'SUCCESS') {
                        await completeLogin(res.data ?? {}, loginId)
                    } else if (res.result == 'PASSWORD_INCORRECT') {
                        message.value = 'The password does not match. Please try again.'
                    } else if (res.result == 'INVALID_INPUT_PARAMETERS') {
                        message.value = 'No matching user information found. Please check your input and try again.'
                    } else {
                        message.value = res.resultMessage || 'Login failed.'
                    }
                } catch (err: any) {
                    console.log('login error', err)
                    const errorData = err?.data ?? err?.response?.data ?? err
                    const result = errorData?.result
                    if (result == 'INVALID_INPUT_PARAMETERS' || result == 'DOMAIN_NOT_ALLOWED') {
                        message.value = 'No matching user information found. Please check your input and try again.'
                    } else if (result == 'PASSWORD_INCORRECT') {
                        message.value = 'The password does not match. Please try again.'
                    } else {
                        message.value = errorData?.resultMessage || 'Login failed.'
                    }
                } finally {
                    isLoading.value = false
                }
            } else {
                const firstErrorMessage = invalidFields ? Object.values(invalidFields)[0]?.[0]?.message : ''
                message.value = firstErrorMessage || 'Please check your ID and password.'
            }
        })
    } catch (error) {
        console.log('login', error)
    }
}
const PasswordResetDialogRef: any = ref(null)
const passwordReset = () => {
    PasswordResetDialogRef.value?.openDialog()
}
</script>

<style lang="scss" scoped>
.layout-login {
    --primary-color: #b446d2;
    --glass-border-color: rgba(180, 70, 210, 0.4);
    --input-border-color: rgba(72, 24, 98, 0.82);
    --input-hover-border-color: rgba(98, 35, 132, 0.92);
    --input-text-color: #dedede;
    --placeholder-color: #bebebe;
    --icon-color: #c9d1d9;
    --button-text-color: #bebebe;

    position: relative;
    display: flex;
    justify-content: center;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background:
        linear-gradient(120deg, rgba(234, 220, 190, 0.28), rgba(8, 18, 32, 0.58)),
        url('@/assets/images/login-bg-image.png') center / cover no-repeat;

    &::before,
    &::after {
        content: '';
        position: absolute;
        pointer-events: none;
    }

    &::before {
        inset: -24px;
        background: url('@/assets/images/login-bg-image.png') center / cover no-repeat;
        filter: blur(10px) saturate(0.95);
        opacity: 0.72;
        transform: scale(1.02);
    }

    &::after {
        inset: 0;
        background: radial-gradient(circle at 58% 35%, rgba(255, 255, 255, 0.18), transparent 26%),
            radial-gradient(circle at 30% 72%, rgba(42, 15, 66, 0.38), transparent 38%), rgba(4, 9, 17, 0.32);
    }

    :deep(input:-webkit-autofill),
    :deep(input:-webkit-autofill:hover),
    :deep(input:-webkit-autofill:focus),
    :deep(input:-webkit-autofill:active) {
        -webkit-box-shadow: 0 0 0 1000px rgba(88, 18, 117, 0.22) inset !important;
        -webkit-text-fill-color: var(--input-text-color) !important;
        transition: background-color 9999s ease-in-out 0s;
    }
}

.login-autofill-blocker {
    position: absolute;
    top: 0;
    left: 0;
    width: 1px;
    height: 1px;
    opacity: 0;
    pointer-events: none;
}

.login-block {
    position: relative;
    z-index: 1;
    display: flex;
    flex: 1;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: auto;
    height: 100%;
    padding: 2.5%;
}

.login-block-content {
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 28px;
    width: 586px;
    min-height: 568px;
    padding: 48px 40px 40px;
    overflow: hidden;
    border: 1px solid var(--glass-border-color);
    border-radius: 28px;
    box-shadow:
        0 28px 90px rgba(0, 0, 0, 0.34),
        0 0 60px rgba(126, 47, 135, 0.24),
        inset 0 1px 0 rgba(255, 255, 255, 0.34),
        inset 0 -1px 0 rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(22px) saturate(1.25);
    -webkit-backdrop-filter: blur(22px) saturate(1.25);

    &::before,
    &::after {
        content: '';
        position: absolute;
    }

    &::before {
        inset: 0;
        background: linear-gradient(25deg, rgba(255, 255, 255, 0.22), transparent 42%),
            radial-gradient(circle at -5% 0%, rgba(140, 129, 243, 0.22), transparent 22%);
    }
}
.devide-line {
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(241, 180, 247, 0.52), transparent);
}

.login-header,
.login,
.find-password {
    position: relative;
    z-index: 1;
}

.login-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    width: 100%;

    p:not(.login-header-content) {
        color: rgba(255, 255, 255, 0.76);
        text-shadow: 0 1px 12px rgba(0, 0, 0, 0.24);
        font-size: 24px;
        font-weight: 400;
    }
}

.login-header-content {
    width: 100%;
    color: rgba(255, 255, 255, 0.92);
    font-size: 70px;
    font-weight: lighter;
    text-align: center;
    text-shadow: 0 2px 18px rgba(0, 0, 0, 0.3);
}

.login {
    width: 100%;
    margin-right: auto;
    margin-left: auto;

    :deep(.el-form-item) {
        margin-bottom: 8px;
    }

    :deep(.el-form-item__error) {
        color: var(--icon-color);
        font-size: 16px;
    }

    :deep(.el-form-item.is-error .el-input__validateIcon) {
        color: var(--icon-color);
    }

    :deep(.el-form-item.is-error .el-input__wrapper),
    :deep(.el-form-item.is-error .el-input__wrapper.is-focus) {
        box-shadow: 0 0 0 1px var(--el-color-danger) inset !important;
    }

    :deep(.el-input) {
        --el-input-border-radius: 100px;
        height: 64px;
    }

    :deep(.el-input__wrapper) {
        padding: 20px;
        font-size: 20px;
        background: rgba(30, 21, 56, 0.36) !important;
        border: 1px solid var(--input-border-color);
        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, 0.08),
            0 10px 24px rgba(0, 0, 0, 0.12) !important;
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
    }

    :deep(.el-input__wrapper:hover) {
        background: rgba(42, 25, 72, 0.44) !important;
        border-color: var(--input-hover-border-color);
    }

    :deep(.el-input__wrapper.is-focus) {
        background: rgba(42, 25, 72, 0.5) !important;
        // border-color: var(--primary-color);
        box-shadow: 0 0 0 1px var(--primary-color) inset !important;
    }

    :deep(.el-input__inner) {
        height: 45px;
        color: var(--input-text-color) !important;
        -webkit-text-fill-color: var(--input-text-color);
    }

    :deep(.el-input__inner::placeholder),
    :deep(input::placeholder) {
        color: var(--placeholder-color) !important;
        font-weight: lighter;
        -webkit-text-fill-color: var(--placeholder-color) !important;
        opacity: 1;
    }

    :deep(.el-input__prefix-inner),
    :deep(.el-input__suffix-inner) {
        align-items: center;
        height: 100%;
        color: var(--icon-color);
    }

    :deep(.el-input__prefix) {
        left: 22px;
    }

    :deep(.el-input__prefix-inner > .el-icon) {
        width: 18px;
        height: 18px;
        margin-top: 1px;
        font-size: 18px;
    }
}

.custom-pw-input :deep(.el-input__password) {
    font-size: 20px;
}

.login-btn {
    width: 100%;
    height: 64px !important;
    margin-top: 40px;
    color: var(--button-text-color) !important;
    font-size: 20px;
    font-weight: lighter;
    background: rgba(18, 2, 37, 0.58);
    border: 1px solid var(--glass-border-color);
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.12),
        0 14px 28px rgba(0, 0, 0, 0.18);

    &:hover {
        background: rgba(43, 16, 70, 0.68);
    }

    &:focus,
    &:focus-visible {
        outline: none;
        border-color: var(--glass-border-color);
        box-shadow:
            0 0 0 1px var(--glass-border-color),
            inset 0 1px 0 rgba(255, 255, 255, 0.12),
            0 14px 28px rgba(0, 0, 0, 0.18);
    }
}
.loading-icon {
    position: absolute;
    left: -24px;
    top: 2px;
}

.WarningMessage {
    position: absolute;
    top: -5px;
    left: 50%;
    display: block;
    width: max-content;
    max-width: 580px;
    color: var(--text-color--red);
    text-align: center;
    transform: translateX(-50%);
}

.find-password {
    display: flex;
    justify-content: center;
    width: 504px;

    p {
        width: 280px;
        color: var(--input-text-color);
        font-size: 15px;
        line-height: 24px;
        text-align: center;
    }

    a {
        color: var(--primary-color);
        text-decoration: underline;
    }
}

.fade-in {
    animation: glassEnter 520ms ease-out both;
}

.fade-in .login-header,
.fade-in .login,
.fade-in .find-password {
    animation: contentFadeIn 620ms ease-out 80ms both;
}

@keyframes glassEnter {
    from {
        transform: translateY(30px);
    }

    to {
        transform: translateY(0);
    }
}

@keyframes contentFadeIn {
    from {
        opacity: 0;
        transform: translateY(18px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@media (max-width: 1024px) {
    .login-block {
        width: 100%;
        height: 100%;
    }
}
</style>
