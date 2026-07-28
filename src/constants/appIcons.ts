import IconAlarmHistory from '@/assets/icons/IconAlarmHistory.svg'
import IconAcPanel from '@/assets/icons/IconAcPanel.svg'
import IconDashboard from '@/assets/icons/IconDashboard.svg'
import IconDeviceManagement from '@/assets/icons/IconDeviceManagement.svg'
import IconEss from '@/assets/icons/IconEss.svg'
import IconMaintenance from '@/assets/icons/IconMaintenance.svg'
import IconOperationReport from '@/assets/icons/IconOperationReport.svg'
import IconPowerFlow from '@/assets/icons/IconPowerFlow.svg'
import IconSetting from '@/assets/icons/IconSetting.svg'
import IconSolar from '@/assets/icons/IconSolar.svg'
import IconTrend from '@/assets/icons/IconTrend.svg'
import IconEnergyLoad from '@/assets/icons/IconEnergyLoad.svg'
import IconBatteryCharging from '@/assets/icons/IconBatteryCharging.svg'
import IconElectricGrid from '@/assets/icons/IconElectricGrid.svg'
import IconInverter from '@/assets/icons/IconInverter.svg'
import IconPcs from '@/assets/icons/IconPcs.svg'
import IconBms from '@/assets/icons/IconBms.svg'
import IconMeter from '@/assets/icons/IconMeter.svg'
import IconSensor from '@/assets/icons/IconSensor.svg'
import IconDevice from '@/assets/icons/IconDevice.svg'
import IconAlignHorizontal from '@/assets/icons/IconAlignHorizontal.svg'
import IconAlignVertical from '@/assets/icons/IconAlignVertical.svg'
import IconDistributeHorizontal from '@/assets/icons/IconDistributeHorizontal.svg'
import IconDistributeVertical from '@/assets/icons/IconDistributeVertical.svg'

export const AppIcons = {
    IconAlarmHistory,
    IconAcPanel,
    IconDashboard,
    IconDeviceManagement,
    IconEss,
    IconMaintenance,
    IconOperationReport,
    IconPowerFlow,
    IconSetting,
    IconSolar,
    IconTrend,
    IconEnergyLoad,
    IconBatteryCharging,
    IconElectricGrid,
    IconInverter,
    IconPcs,
    IconBms,
    IconMeter,
    IconSensor,
    IconDevice,
    IconAlignHorizontal,
    IconAlignVertical,
    IconDistributeHorizontal,
    IconDistributeVertical
} as const

export type AppIconName = keyof typeof AppIcons
