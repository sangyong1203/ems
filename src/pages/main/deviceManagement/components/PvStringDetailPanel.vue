<template>
    <div class="device-side">
        <GlassPanel
            class="device-detail-panel"
            title="태양광 스트링 상세"
            :subtitle="pvString ? connectionText : '목록에서 스트링을 선택하세요'"
            :value="pvString ? statusLabel(pvString.status) : '-'"
        >
            <template v-if="pvString">
                <div class="device-detail-head">
                    <div class="device-detail-head__info">
                        <strong>{{ pvString.name }}</strong>
                        <span>{{ pvString.install_location || '-' }}</span>
                    </div>
                </div>

                <div class="device-detail-scroll">
                    <div class="device-detail-section">
                        <h3>기본 정보</h3>
                        <dl class="device-detail-list">
                            <div>
                                <dt>패널 수량</dt>
                                <dd>{{ pvString.panel_count ?? '-' }}</dd>
                            </div>
                            <div>
                                <dt>패널 정격</dt>
                                <dd>{{ numberText(pvString.panel_capacity_kw, 'kW') }}</dd>
                            </div>
                            <div>
                                <dt>스트링 정격</dt>
                                <dd>{{ numberText(pvString.rated_capacity_kw, 'kW') }}</dd>
                            </div>
                            <div>
                                <dt>운영 여부</dt>
                                <dd>{{ pvString.is_active ? '활성' : '비활성' }}</dd>
                            </div>
                        </dl>
                    </div>

                    <div class="device-detail-section">
                        <h3>연결 정보</h3>
                        <dl class="device-detail-list">
                            <div>
                                <dt>연결 인버터</dt>
                                <dd>{{ pvString.inverter_name || '미연결' }}</dd>
                            </div>
                            <div>
                                <dt>MPPT 번호</dt>
                                <dd>{{ pvString.mppt_no ?? '-' }}</dd>
                            </div>
                            <div>
                                <dt>채널 번호</dt>
                                <dd>{{ pvString.channel_no ?? '-' }}</dd>
                            </div>
                        </dl>
                    </div>

                    <div class="device-detail-section">
                        <h3>관리 정보</h3>
                        <dl class="device-detail-list">
                            <div>
                                <dt>메모</dt>
                                <dd>{{ pvString.memo || '-' }}</dd>
                            </div>
                        </dl>
                    </div>
                </div>
            </template>
            <p v-else class="device-empty-text">선택된 스트링이 없습니다.</p>
        </GlassPanel>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { GlassPanel } from '@/shared/components'
import type { PvStringItem } from '../service/deviceManagement.types'

const props = defineProps<{
    pvString: PvStringItem | null
}>()

const connectionText = computed(() => (props.pvString?.inverter_name ? '인버터 연결' : '미연결'))

const statusLabel = (value: string) => {
    const labels: Record<string, string> = {
        NORMAL: '정상',
        WARNING: '주의',
        FAULT: '장애',
        MAINTENANCE: '점검',
        UNKNOWN: '미확인',
    }
    return labels[value] || value || '-'
}

const numberText = (value: number | null, unit: string) => {
    if (value === null || value === undefined) {
        return '-'
    }
    return `${Number(value).toLocaleString(undefined, { maximumFractionDigits: 2 })} ${unit}`
}
</script>

<style scoped lang="scss">
.device-side {
    flex: 0 0 32%;
    display: flex;
    min-width: 0;
    min-height: 0;
}

.device-detail-panel {
    flex: 1 1 auto;
}

.device-detail-head {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 14px;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--border-color);
}

.device-detail-head__info {
    display: flex;
    flex-direction: row;
    align-items: baseline;
    justify-content: space-between;
    gap: 6px;
    width: 100%;
}

.device-detail-head strong {
    font-size: 24px;
    line-height: 28px;
}

.device-detail-head span {
    color: var(--text-color--secondary);
    font-size: 13px;
}

.device-detail-scroll {
    min-height: 0;
    overflow-y: auto;
    padding-right: 16px;
    margin-right: -12px;
}

.device-detail-scroll::-webkit-scrollbar {
    width: 6px;
}

.device-detail-scroll::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.04);
    border-radius: 999px;
}

.device-detail-scroll::-webkit-scrollbar-thumb {
    background: rgba(231, 109, 255, 0.38);
    border-radius: 999px;
}

.device-detail-section {
    padding: 16px 0 0;
}

.device-detail-section h3 {
    margin: 0 0 12px;
    font-size: 14px;
}

.device-detail-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin: 0;
}

.device-detail-list div {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border-color);
}

.device-detail-list dt,
.device-detail-list dd {
    margin: 0;
}

.device-detail-list dt {
    flex: 0 0 96px;
    color: var(--text-color--secondary);
    font-size: 13px;
}

.device-detail-list dd {
    min-width: 0;
    color: #ffffff;
    font-size: 13px;
    font-weight: 700;
    text-align: right;
    word-break: break-word;
}

.device-empty-text {
    margin: auto;
    color: var(--text-color--secondary);
    font-size: 14px;
}

@media (max-width: 1180px), (orientation: portrait) {
    .device-side {
        flex: 0 0 auto;
        width: 100%;
        min-height: 360px;
    }

    .device-detail-head__info {
        align-items: flex-start;
        flex-direction: column;
    }

    .device-detail-scroll {
        max-height: none;
    }
}

@media (max-width: 760px), (orientation: portrait) and (max-width: 900px) {
    .device-side {
        min-height: 320px;
    }

    .device-detail-head strong {
        font-size: 22px;
        line-height: 28px;
    }

    .device-detail-list div {
        align-items: flex-start;
        flex-direction: column;
        gap: 6px;
    }

    .device-detail-list dt {
        flex: 0 0 auto;
    }

    .device-detail-list dd {
        width: 100%;
        text-align: left;
    }
}
</style>
