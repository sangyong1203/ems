<template>
    <section class="settings-page">
        <GlassPanel class="settings-panel" title="시스템 설정" subtitle="운영 환경과 가상 데이터를 관리합니다.">
            <el-tabs v-model="activeTab" class="settings-tabs">
                <el-tab-pane label="프로젝트 정보" name="project">
                    <ProjectSettingsTab :form="form" :saving="saving" @save="saveProject" />
                </el-tab-pane>

                <el-tab-pane label="설비 정보" name="equipment">
                    <EquipmentSettingsTab
                        :device-counts="deviceCounts"
                        :active-device-counts="activeDeviceCounts"
                        :capacity-summary="capacitySummary"
                    />
                </el-tab-pane>

                <el-tab-pane label="모니터링 설정" name="monitoring">
                    <MonitoringSettingsTab :form="form" :saving="saving" @save="saveProject" />
                </el-tab-pane>

                <el-tab-pane label="가상 데이터" name="simulator">
                    <SimulatorSettingsTab />
                </el-tab-pane>
            </el-tabs>
        </GlassPanel>
    </section>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { GlassPanel } from '@/components'
import { Message } from '@/composables/useFeedback'
import { isSuccessResponse } from '@/utils'
import EquipmentSettingsTab from './components/EquipmentSettingsTab.vue'
import MonitoringSettingsTab from './components/MonitoringSettingsTab.vue'
import ProjectSettingsTab from './components/ProjectSettingsTab.vue'
import SimulatorSettingsTab from './components/SimulatorSettingsTab.vue'
import settingsApi from './service/settings.api'
import type {
    DeviceCounts,
    EquipmentCapacities,
    ProjectConfig,
    ProjectConfigSavePayload,
} from './service/settings.types'

const activeTab = ref('project') // 활성 탭 (project / equipment / monitoring / simulator)
const saving = ref(false) // 저장 처리 중 상태
const deviceCounts = ref<DeviceCounts>({ // 전체 설비 종류별 수량
    INVERTER: 0,
    PCS: 0,
    ESS_BATTERY: 0,
    BATTERY_RACK: 0,
    BMS: 0,
    AC_PANEL: 0,
    METER: 0,
})
const activeDeviceCounts = ref<DeviceCounts>({ // 활성 운영 중인 설비 종류별 수량
    INVERTER: 0,
    PCS: 0,
    ESS_BATTERY: 0,
    BATTERY_RACK: 0,
    BMS: 0,
    AC_PANEL: 0,
    METER: 0,
})
const capacitySummary = ref<EquipmentCapacities>({ // 설비 용량 집계 (설치/운영 용량)
    solarInstalledKw: 0,
    solarOperatingKw: 0,
    essInstalledKwh: 0,
    essOperatingKwh: 0,
})
const form = reactive<ProjectConfigSavePayload>({ // 프로젝트 및 모니터링 설정 폼 데이터
    project_name: '',
    site_name: '',
    location: null,
    customer_name: null,
    contractor_name: null,
    solar_capacity_kw: 0,
    ess_capacity_kwh: 0,
    system_name: '',
    background_image_path: null,
    logo_image_path: null,
    data_refresh_interval: 10000,
    dashboard_refresh_interval: 10000,
    solar_refresh_interval: 10000,
    ess_refresh_interval: 10000,
    power_flow_refresh_interval: 10000,
    trend_refresh_interval: 10000,
})

// syncProject 조회된 프로젝트 설정 데이터 폼 및 상태 동기화
const syncProject = (data: ProjectConfig) => {
    const { device_counts, active_device_counts, equipment_capacities, id: _id, ...project } = data
    Object.assign(form, project)
    deviceCounts.value = device_counts
    activeDeviceCounts.value = active_device_counts
    capacitySummary.value = equipment_capacities
}

// getProject 프로젝트 기본 설정 및 설비 집계 조회
const getProject = async () => {
    const res = await settingsApi.getProject()
    if (isSuccessResponse(res.result)) {
        syncProject(res.data)
    }
}

// saveProject 프로젝트 및 모니터링 설정 저장
const saveProject = async () => {
    saving.value = true
    try {
        const res = await settingsApi.saveProject({ ...form })
        if (isSuccessResponse(res.result)) {
            syncProject(res.data)
            Message.success('설정을 저장했습니다.')
        }
    } finally {
        saving.value = false
    }
}

// onMounted 초기 프로젝트 설정 데이터 로드
onMounted(() => {
    getProject()
})
</script>

<style scoped lang="scss">
.settings-page {
    width: 100%;
    height: 100%;
    padding: 0 12px 20px;
}

.settings-panel {
    height: 100%;
}
</style>
