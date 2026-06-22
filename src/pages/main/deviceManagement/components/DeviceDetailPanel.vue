<template>
    <div class="device-side">
        <GlassPanel
            class="device-detail-panel"
            title="장비 상세"
            :subtitle="device ? deviceTypeLabel(device.device_type) : '목록에서 장비를 선택하세요'"
            :value="device ? statusLabel(device.status) : '-'"
        >
            <template v-if="device">
                <div class="device-detail-head">
                    <div class="device-detail-head__info">
                        <strong>{{ device.name }}</strong>
                        <span>{{ device.manufacturer || '-' }} / {{ device.model_name || '-' }}</span>
                    </div>
                </div>

                <div class="device-detail-scroll">
                    <div class="device-detail-section">
                        <h3>기본 정보</h3>
                        <dl class="device-detail-list">
                            <div>
                                <dt>시리얼 번호</dt>
                                <dd>{{ device.serial_number || '-' }}</dd>
                            </div>
                            <div>
                                <dt>{{ capacityDetailLabel }}</dt>
                                <dd>{{ capacityText(device) }}</dd>
                            </div>
                            <div>
                                <dt>운영 여부</dt>
                                <dd>{{ device.is_active ? '활성' : '비활성' }}</dd>
                            </div>
                            <div>
                                <dt>설치 위치</dt>
                                <dd>{{ device.install_location || '-' }}</dd>
                            </div>
                            <div>
                                <dt>설치일</dt>
                                <dd>{{ device.install_date || '-' }}</dd>
                            </div>
                        </dl>
                    </div>

                    <div class="device-detail-section">
                        <h3>통신 정보</h3>
                        <dl class="device-detail-list">
                            <div>
                                <dt>통신 방식</dt>
                                <dd>{{ device.communication_type || '-' }}</dd>
                            </div>
                            <div>
                                <dt>IP / Port</dt>
                                <dd>{{ ipPortText }}</dd>
                            </div>
                            <div>
                                <dt>Slave ID</dt>
                                <dd>{{ device.slave_id ?? '-' }}</dd>
                            </div>
                            <div>
                                <dt>Protocol</dt>
                                <dd>{{ device.protocol || '-' }}</dd>
                            </div>
                        </dl>
                    </div>

                    <div class="device-detail-section">
                        <h3>보증/관리</h3>
                        <dl class="device-detail-list">
                            <div>
                                <dt>보증 기간</dt>
                                <dd>{{ warrantyText }}</dd>
                            </div>
                            <div>
                                <dt>관리 업체</dt>
                                <dd>{{ device.vendor_name || '-' }}</dd>
                            </div>
                            <div>
                                <dt>연락처</dt>
                                <dd>{{ device.vendor_contact || '-' }}</dd>
                            </div>
                            <div>
                                <dt>메모</dt>
                                <dd>{{ device.memo || '-' }}</dd>
                            </div>
                        </dl>
                    </div>

                    <div v-if="device.device_type === 'INVERTER'" class="device-detail-section">
                        <h3>연결 태양광 스트링</h3>
                        <div v-if="device.pv_string_links.length" class="device-string-list">
                            <article v-for="link in device.pv_string_links" :key="link.pv_string_id">
                                <strong>{{ link.pv_string_name || `PV String #${link.pv_string_id}` }}</strong>
                                <span>MPPT {{ link.mppt_no ?? '-' }} / CH {{ link.channel_no ?? '-' }}</span>
                            </article>
                        </div>
                        <p v-else class="device-empty-text device-empty-text--inline">연결된 스트링이 없습니다.</p>
                    </div>
                </div>
            </template>
            <p v-else class="device-empty-text">선택된 장비가 없습니다.</p>
        </GlassPanel>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { GlassPanel } from '@/shared/components'
import type { DeviceItem } from '../service/deviceManagement.types'

const props = defineProps<{
    device: DeviceItem | null
}>()

const ipPortText = computed(() => {
    if (!props.device?.ip_address) {
        return '-'
    }
    return props.device.port ? `${props.device.ip_address}:${props.device.port}` : props.device.ip_address
})

const warrantyText = computed(() => {
    if (!props.device?.warranty_start_date && !props.device?.warranty_end_date) {
        return '-'
    }
    return `${props.device.warranty_start_date || '-'} ~ ${props.device.warranty_end_date || '-'}`
})

const capacityDetailLabel = computed(() => (props.device?.device_type === 'SENSOR' ? '측정 범위' : '정격 용량'))

const deviceTypeLabel = (value: string) => {
    const labels: Record<string, string> = {
        INVERTER: '인버터',
        PCS: 'PCS',
        ESS_BATTERY: 'ESS Battery',
        BMS: 'BMS',
        AC_PANEL: 'AC 배전반',
        METER: '계량기',
        SENSOR: '센서',
        ETC: '기타',
    }
    return labels[value] || value || '-'
}

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

const capacityText = (device: DeviceItem) => {
    if (device.capacity === null || device.capacity === undefined) {
        return '-'
    }
    return `${Number(device.capacity).toLocaleString(undefined, { maximumFractionDigits: 1 })} ${device.capacity_unit || ''}`.trim()
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

.device-empty-text--inline {
    margin: 0;
}

.device-string-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.device-string-list article {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    padding: 10px 12px;
    border: 1px solid rgba(21, 224, 183, 0.22);
    border-radius: 6px;
    background: rgba(21, 224, 183, 0.06);
}

.device-string-list strong {
    font-size: 13px;
}

.device-string-list span {
    color: var(--text-color--secondary);
    font-size: 12px;
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

    .device-detail-list div,
    .device-string-list article {
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
