<template>
    <el-row class="main-header">
        <el-col :span="14">
            <div class="header-left">
                <AppIcon v-if="icon" :name="icon" class="menu-icon"></AppIcon>
                <span class="title">
                    <span class="title-text">{{ title }}</span>
                </span>
            </div>
        </el-col>
        <el-col :span="10">
            <div class="header-right">
                <el-popover
                    v-model:visible="userPopoverVisible"
                    placement="bottom-end"
                    trigger="click"
                    :width="320"
                    @show="loadUserInfo"
                >
                    <template #reference>
                        <button
                            type="button"
                            class="header-user"
                            aria-label="사용자 상세 정보"
                            aria-haspopup="dialog"
                            :aria-expanded="userPopoverVisible"
                        >
                            <el-icon class="header-user-icon"><User /></el-icon>
                            <span class="header-user-name">{{ userName }}</span>
                            <el-icon class="header-user-arrow"><ArrowDown /></el-icon>
                        </button>
                    </template>
                    <section class="header-user-profile" aria-label="사용자 상세 정보" :aria-busy="userInfoLoading">
                        <h2 class="header-user-profile__title">사용자 정보</h2>
                        <p v-if="userInfoLoading" class="header-user-profile__message" role="status">조회 중...</p>
                        <div v-else-if="userInfoError" class="header-user-profile__error" role="alert">
                            <p>{{ userInfoError }}</p>
                            <el-button link type="primary" @click="loadUserInfo">다시 조회</el-button>
                        </div>
                        <dl v-else-if="userInfo" class="header-user-profile__details">
                            <dt>이름</dt>
                            <dd>{{ userInfo.name }}</dd>
                            <dt>사용자 ID</dt>
                            <dd>{{ userInfo.username }}</dd>
                            <dt>이메일</dt>
                            <dd>{{ userInfo.email }}</dd>
                            <dt>역할</dt>
                            <dd>{{ userInfo.role }}</dd>
                        </dl>
                        <div class="header-user-profile__actions">
                            <el-button class="change-password-button" @click="openChangePassword">Change password</el-button>
                        </div>
                    </section>
                </el-popover>
                <el-button type="primary" circle class="logout" @click="emit('logout')">
                    <el-icon><SwitchButton /></el-icon>
                </el-button>
            </div>
        </el-col>
    </el-row>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { ArrowDown, SwitchButton, User } from '@element-plus/icons-vue'
import loginApi from '@/pages/login/service/login.api'
import type { UserInfo } from '@/pages/login/service/login.types'

const userPopoverVisible = ref(false) // 사용자 상세 팝업 표시 여부
const userInfo = ref<UserInfo | null>(null) // 서버가 반환한 현재 사용자 상세 정보
const userInfoLoading = ref(false) // 사용자 상세 조회 중
const userInfoError = ref('') // 상세 조회 실패 안내

withDefaults(
    defineProps<{
        title?: string
        icon?: string
        userName?: string
    }>(),
    {
        title: '',
        icon: '',
        userName: 'User',
    },
)

const emit = defineEmits<{
    logout: []
    'change-password': []
}>()

// 팝업을 열 때마다 인증된 사용자 정보를 조회하여 최신 이름·이메일·역할을 표시합니다.
const loadUserInfo = async () => {
    if (userInfoLoading.value) return
    userInfoLoading.value = true
    userInfoError.value = ''
    userInfo.value = null
    try {
        const response = await loginApi.getUserInfo()
        if (response.result !== 'SUCCESS') {
            userInfoError.value = '사용자 정보를 불러오지 못했습니다.'
            return
        }
        userInfo.value = response.data
    } catch {
        userInfoError.value = '사용자 정보를 불러오지 못했습니다.'
    } finally {
        userInfoLoading.value = false
    }
}

// 사용자 팝업을 닫고 기존 비밀번호 변경 창을 엽니다.
const openChangePassword = () => {
    userPopoverVisible.value = false
    emit('change-password')
}
</script>

<style scoped lang="scss">
.main-header,
.main-header :deep(.el-col),
.header-left,
.header-right {
    height: 100%;
}

.header-left {
    display: flex;
    align-items: center;
}

.header-left .title {
    color: #fff;
    text-decoration-line: none;
    text-decoration: none;
    display: flex;
    align-items: center;
}

.header-left .title-text {
    font-size: 20px;
    line-height: 24px;
    white-space: nowrap;
    font-weight: 700;
    font-family: 'Pretendard', sans-serif;
    letter-spacing: 0;
    // color: var(--header-title-text-color);
}

.header-right {
    text-align: right;
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 4px;
}

.header-user {
    min-width: 0;
    max-width: 320px;
    height: 36px;
    padding: 0 14px;
    display: flex;
    align-items: center;
    gap: 8px;
    border: 1px solid var(--border-color);
    border-radius: 999px;
    background: var(--surface-control-color);
    color: var(--text-color--primary);
    cursor: pointer;
}

.header-user:hover,
.header-user:focus-visible {
    border-color: var(--accent-color);
}

.header-user:focus-visible {
    outline: 2px solid var(--accent-color);
    outline-offset: 2px;
}

.header-user-arrow {
    flex-shrink: 0;
    font-size: 12px;
    color: var(--text-color--secondary);
}

.header-user-profile {
    padding: 4px;
    color: var(--text-color--primary);
    text-align: left;
}

.header-user-profile__title {
    margin: 0 0 16px;
    font-size: 16px;
    font-weight: 700;
}

.header-user-profile__details {
    display: grid;
    grid-template-columns: 72px minmax(0, 1fr);
    gap: 12px;
    margin: 0;
    font-size: 13px;
    line-height: 1.5;
}

.header-user-profile__details dt,
.header-user-profile__message,
.header-user-profile__error {
    color: var(--text-color--secondary);
}

.header-user-profile__details dd {
    margin: 0;
    overflow-wrap: anywhere;
}

.header-user-profile__actions {
    margin-top: 16px;
    padding-top: 16px;
    border-top: 1px solid var(--border-color);
}

.header-user-profile__actions .change-password-button {
    width: 100%;
}

.header-user-icon {
    flex: 0 0 auto;
    width: 17px;
    height: 17px;
    color: var(--accent-color);
}

.header-user-icon svg {
    width: 17px;
    height: 17px;
}

.header-user-name {
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-size: 14px;
    font-weight: 500;
    letter-spacing: 0;
}

.logout {
    border: 1px solid var(--border-color);
    background-color: var(--surface-control-color);
    color: var(--text-color--white);
}

.logout:hover {
    background-color: var(--layout-menu-active-bg-color);
    border-color: var(--accent-color);
    color: var(--accent-color);
    cursor: pointer;
}

.logout .el-icon {
    width: 18px;
    height: 18px;
    transform: rotate(90deg);
}

.logout .el-icon svg {
    width: 18px;
    height: 18px;
}
.menu-icon {
    color: var(--primary-color) !important;
    width: 24px;
    height: 24px;
    margin-right: 8px;
}
</style>
