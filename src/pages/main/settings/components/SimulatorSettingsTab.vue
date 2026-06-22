<template>
    <div class="simulator-list">
        <article v-for="action in simulatorActions" :key="action.key" class="simulator-action">
            <div>
                <h3>{{ action.title }}</h3>
                <p>{{ action.description }}</p>
            </div>
            <el-button
                :type="action.danger ? 'danger' : 'primary'"
                :plain="action.danger"
                :loading="runningAction === action.key"
                @click="runSimulatorAction(action.key)"
            >
                {{ action.buttonLabel }}
            </el-button>
        </article>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessageBox } from 'element-plus'
import { Message } from '@/shared/composables/useFeedback'
import { isSuccessResponse } from '@/shared/utils'
import settingsApi from '../service/settings.api'

type SimulatorActionKey = 'today' | 'last7Days' | 'alarms' | 'maintenance' | 'reset'

type SimulatorAction = {
    key: SimulatorActionKey
    title: string
    description: string
    buttonLabel: string
    danger?: boolean
}

const runningAction = ref<SimulatorActionKey | null>(null)

const simulatorActions: SimulatorAction[] = [
    {
        key: 'today',
        title: '오늘 데이터 생성',
        description: '오늘 시간대별 telemetry와 일일 집계를 다시 생성합니다.',
        buttonLabel: '생성',
    },
    {
        key: 'last7Days',
        title: '최근 7일 데이터 생성',
        description: '통계 리포트 확인용 최근 7일 데이터를 생성합니다.',
        buttonLabel: '생성',
    },
    {
        key: 'alarms',
        title: '알림 데이터 생성',
        description: '알림 이력 확인용 샘플 알림을 다시 생성합니다.',
        buttonLabel: '생성',
    },
    {
        key: 'maintenance',
        title: '정비 데이터 생성',
        description: '정비 관리 확인용 샘플 정비 일정을 다시 생성합니다.',
        buttonLabel: '생성',
    },
    {
        key: 'reset',
        title: '전체 데이터 초기화',
        description: 'telemetry, 리포트, 알림, 정비 데이터를 모두 삭제합니다.',
        buttonLabel: '초기화',
        danger: true,
    },
]

const resetSimulator = async () => {
    try {
        await ElMessageBox.confirm('가상 데이터를 모두 초기화하시겠습니까?', '전체 데이터 초기화', {
            confirmButtonText: '초기화',
            cancelButtonText: '취소',
            type: 'warning',
        })
    } catch {
        return
    }

    return await settingsApi.resetSimulator()
}

const runSimulatorAction = async (action: SimulatorActionKey) => {
    runningAction.value = action
    try {
        const request = {
            today: settingsApi.generateToday,
            last7Days: settingsApi.generateLast7Days,
            alarms: settingsApi.generateAlarms,
            maintenance: settingsApi.generateMaintenance,
            reset: resetSimulator,
        }[action]
        const res = await request()
        if (res && isSuccessResponse(res.result)) {
            Message.success(action === 'reset' ? '가상 데이터를 초기화했습니다.' : '가상 데이터를 생성했습니다.')
        }
    } finally {
        runningAction.value = null
    }
}
</script>

<style scoped lang="scss">
.simulator-list {
    display: flex;
    max-width: 980px;
    flex-direction: column;
    gap: 10px;
}

.simulator-action {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 18px;
    min-height: 76px;
    padding: 15px 18px;
    border: 1px solid rgb(255 255 255 / 10%);
    border-radius: 6px;
    background: rgb(255 255 255 / 4%);
}

.simulator-action h3 {
    margin: 0 0 8px;
    font-size: 16px;
}

.simulator-action p {
    margin: 0;
    color: var(--text-color--secondary);
    font-size: 13px;
}

@media (max-width: 760px) {
    .simulator-action {
        align-items: flex-start;
        flex-direction: column;
    }
}
</style>
