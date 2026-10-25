<template>
    <BaseDialog v-model="visible" title="Password reset" width="450px" :button-types="['Close']" @on-close="visible = false">
        <p class="password-reset-unavailable">Email password reset is unavailable. Please contact your administrator.</p>
    </BaseDialog>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { BaseDialog } from '@/components'

const visible = ref(false) // 비밀번호 재설정 안내 표시 여부

// 메일 연동 전에는 재설정 요청 대신 관리자 문의 안내만 표시합니다.
const openDialog = () => {
    visible.value = true
}

defineExpose({ openDialog })
</script>
