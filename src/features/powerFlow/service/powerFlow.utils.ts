import type {
    PowerFlowAnchor,
    PowerFlowDeviceItem,
    PowerFlowDeviceVisual,
    PowerFlowEndpoint,
    PowerFlowJunction,
    PowerFlowLayoutNode,
    PowerFlowPoint,
    PowerFlowWire,
    PowerFlowWireCurrentState,
    PowerFlowWireTone,
} from './powerFlow.types'

export const deviceVisual = (deviceType: string): PowerFlowDeviceVisual => {
    const visuals: Record<string, PowerFlowDeviceVisual> = {
        INVERTER: { icon: 'IconInverter', label: '인버터' },
        PCS: { icon: 'IconPcs', label: 'PCS' },
        ESS_BATTERY: { icon: 'IconEss', label: '배터리 뱅크' },
        BATTERY_RACK: { icon: 'IconEss', label: '배터리 랙' },
        BMS: { icon: 'IconBms', label: 'BMS' },
        AC_PANEL: { icon: 'IconAcPanel', label: 'AC 배전반' },
        GRID_METER: { icon: 'IconElectricGrid', label: '계통 계량기' },
        LOAD_METER: { icon: 'IconEnergyLoad', label: '부하 계량기' },
        WEATHER_SENSOR: { icon: 'IconSensor', label: '기상 센서' },
        SENSOR: { icon: 'IconSensor', label: '센서' },
    }
    return visuals[deviceType] ?? { icon: 'IconDevice', label: deviceType }
}

export const deviceStatusLabel = (device: PowerFlowDeviceItem) => {
    if (!device.is_active) {
        return '비활성'
    }
    const labels: Record<string, string> = {
        NORMAL: '정상',
        WARNING: '주의',
        FAULT: '장애',
    }
    return labels[device.status] ?? device.status
}

export const anchorPoint = (node: PowerFlowLayoutNode, anchor: PowerFlowAnchor): PowerFlowPoint => {
    if (anchor === 'TOP') {
        return { x: node.x + node.width / 2, y: node.y }
    }
    if (anchor === 'BOTTOM') {
        return { x: node.x + node.width / 2, y: node.y + node.height }
    }
    if (anchor === 'LEFT') {
        return { x: node.x, y: node.y + node.height / 2 }
    }
    return { x: node.x + node.width, y: node.y + node.height / 2 }
}

export const endpointPoint = (
    endpoint: PowerFlowEndpoint,
    nodes: PowerFlowLayoutNode[],
    junctions: PowerFlowJunction[],
): PowerFlowPoint | null => {
    if (endpoint.type === 'JUNCTION') {
        return junctions.find(item => item.client_id === endpoint.ref) ?? null
    }
    const node = nodes.find(item => item.client_id === endpoint.ref)
    return node ? anchorPoint(node, endpoint.anchor) : null
}

export const wirePath = (
    wire: PowerFlowWire,
    nodes: PowerFlowLayoutNode[],
    junctions: PowerFlowJunction[],
): string => {
    const source = endpointPoint(
        { type: wire.source_type, ref: wire.source_ref, anchor: wire.source_anchor },
        nodes,
        junctions,
    )
    const target = endpointPoint(
        { type: wire.target_type, ref: wire.target_ref, anchor: wire.target_anchor },
        nodes,
        junctions,
    )
    if (!source || !target) {
        return ''
    }
    const points = [source, ...wire.route_points, target]
    return points.map((point, index) => `${index ? 'L' : 'M'} ${point.x} ${point.y}`).join(' ')
}

export const wireTone = (
    wire: PowerFlowWire,
    nodes: PowerFlowLayoutNode[],
    wires: PowerFlowWire[],
    devices: PowerFlowDeviceItem[],
): PowerFlowWireTone => {
    const endpointDevices = endpointDevicesForWire(wire, nodes, wires, devices)
    if (!wire.is_enabled || endpointDevices.some(device => !device.is_active)) {
        return 'inactive'
    }
    return 'active'
}

const nodeDeviceForRef = (ref: string, nodes: PowerFlowLayoutNode[], devices: PowerFlowDeviceItem[]) => {
    const node = nodes.find(item => item.client_id === ref)
    if (!node) {
        return null
    }
    return devices.find(device => device.id === node.device_id) ?? null
}

const connectedDevicesForEndpoint = (
    endpoint: Pick<PowerFlowEndpoint, 'type' | 'ref'>,
    nodes: PowerFlowLayoutNode[],
    wires: PowerFlowWire[],
    devices: PowerFlowDeviceItem[],
    visitedJunctions = new Set<string>(),
    excludedWireId?: string,
): PowerFlowDeviceItem[] => {
    if (endpoint.type === 'NODE') {
        const device = nodeDeviceForRef(endpoint.ref, nodes, devices)
        return device ? [device] : []
    }
    if (visitedJunctions.has(endpoint.ref)) {
        return []
    }
    visitedJunctions.add(endpoint.ref)

    return wires
        .filter(
            item =>
                item.client_id !== excludedWireId &&
                (item.source_ref === endpoint.ref || item.target_ref === endpoint.ref),
        )
        .flatMap(item => {
            const isSource = item.source_ref === endpoint.ref
            return connectedDevicesForEndpoint(
                {
                    type: isSource ? item.target_type : item.source_type,
                    ref: isSource ? item.target_ref : item.source_ref,
                },
                nodes,
                wires,
                devices,
                new Set(visitedJunctions),
                excludedWireId,
            )
        })
}

const endpointDeviceSides = (
    wire: PowerFlowWire,
    nodes: PowerFlowLayoutNode[],
    wires: PowerFlowWire[],
    devices: PowerFlowDeviceItem[],
) => ({
    source: connectedDevicesForEndpoint(
        { type: wire.source_type, ref: wire.source_ref },
        nodes,
        wires,
        devices,
        new Set(),
        wire.client_id,
    ),
    target: connectedDevicesForEndpoint(
        { type: wire.target_type, ref: wire.target_ref },
        nodes,
        wires,
        devices,
        new Set(),
        wire.client_id,
    ),
})

const endpointDevicesForWire = (
    wire: PowerFlowWire,
    nodes: PowerFlowLayoutNode[],
    wires: PowerFlowWire[],
    devices: PowerFlowDeviceItem[],
) => {
    const sides = endpointDeviceSides(wire, nodes, wires, devices)
    const items = [...sides.source, ...sides.target]

    return Array.from(new Map(items.map(device => [device.id, device])).values())
}

const metricValue = (
    metricKey: string,
    relatedDevices: PowerFlowDeviceItem[],
    telemetry: Record<string, number>,
    deviceTelemetry: Record<string, Record<string, number>>,
) => {
    const deviceValues = relatedDevices.flatMap(device => {
        const value = deviceTelemetry[String(device.id)]?.[metricKey]
        return value == null ? [] : [Number(value)]
    })
    if (deviceValues.length > 0) {
        return Math.max(...deviceValues)
    }
    return Number(telemetry[metricKey] ?? 0)
}

const directionFromType = (
    sourceDevices: PowerFlowDeviceItem[],
    targetDevices: PowerFlowDeviceItem[],
    fromType: string,
) => {
    const sourceHasType = sourceDevices.some(device => device.device_type === fromType)
    const targetHasType = targetDevices.some(device => device.device_type === fromType)
    if (sourceHasType && !targetHasType) {
        return 'FORWARD' as const
    }
    if (targetHasType && !sourceHasType) {
        return 'REVERSE' as const
    }
    return null
}

const directionTowardType = (
    sourceDevices: PowerFlowDeviceItem[],
    targetDevices: PowerFlowDeviceItem[],
    toType: string,
) => {
    const sourceHasType = sourceDevices.some(device => device.device_type === toType)
    const targetHasType = targetDevices.some(device => device.device_type === toType)
    if (targetHasType && !sourceHasType) {
        return 'FORWARD' as const
    }
    if (sourceHasType && !targetHasType) {
        return 'REVERSE' as const
    }
    return null
}

const currentState = (
    power: number,
    direction: PowerFlowWireCurrentState['direction'] | null,
): PowerFlowWireCurrentState => ({
    active: power > 0 && direction !== null,
    direction: direction ?? 'FORWARD',
})

export const wireCurrentState = (
    wire: PowerFlowWire,
    nodes: PowerFlowLayoutNode[],
    wires: PowerFlowWire[],
    devices: PowerFlowDeviceItem[],
    telemetry: Record<string, number>,
    deviceTelemetry: Record<string, Record<string, number>> = {},
): PowerFlowWireCurrentState => {
    const inactiveState: PowerFlowWireCurrentState = { active: false, direction: 'FORWARD' }
    if (!wire.is_enabled) {
        return inactiveState
    }

    const sides = endpointDeviceSides(wire, nodes, wires, devices)
    const relatedDevices = [...sides.source, ...sides.target]
    const deviceTypes = new Set(relatedDevices.map(device => device.device_type))

    if (deviceTypes.has('BMS')) {
        return inactiveState
    }

    if (deviceTypes.has('INVERTER')) {
        const inverterDevices = relatedDevices.filter(device => device.device_type === 'INVERTER')
        return currentState(
            metricValue('inverter_power_kw', inverterDevices, telemetry, deviceTelemetry),
            directionFromType(sides.source, sides.target, 'INVERTER'),
        )
    }

    if (deviceTypes.has('GRID_METER')) {
        const exportPower = metricValue('grid_export_kw', [], telemetry, deviceTelemetry)
        const importPower = metricValue('grid_import_kw', [], telemetry, deviceTelemetry)
        if (exportPower > 0) {
            return currentState(exportPower, directionTowardType(sides.source, sides.target, 'GRID_METER'))
        }
        return currentState(importPower, directionFromType(sides.source, sides.target, 'GRID_METER'))
    }

    if (deviceTypes.has('LOAD_METER')) {
        return currentState(
            metricValue('load_power_kw', [], telemetry, deviceTelemetry),
            directionTowardType(sides.source, sides.target, 'LOAD_METER'),
        )
    }

    if (deviceTypes.has('PCS') && deviceTypes.has('ESS_BATTERY')) {
        const chargePower = metricValue('ess_charge_kw', relatedDevices, telemetry, deviceTelemetry)
        const dischargePower = metricValue('ess_discharge_kw', relatedDevices, telemetry, deviceTelemetry)
        return chargePower > 0
            ? currentState(chargePower, directionFromType(sides.source, sides.target, 'PCS'))
            : currentState(dischargePower, directionFromType(sides.source, sides.target, 'ESS_BATTERY'))
    }

    if (deviceTypes.has('BATTERY_RACK') && deviceTypes.has('ESS_BATTERY')) {
        const rackDevices = relatedDevices.filter(device => device.device_type === 'BATTERY_RACK')
        const rackCurrent = metricValue('battery_rack_current_a', rackDevices, telemetry, deviceTelemetry)
        if (rackCurrent > 0) {
            return currentState(rackCurrent, directionFromType(sides.source, sides.target, 'BATTERY_RACK'))
        }
        return currentState(
            Math.abs(rackCurrent),
            directionTowardType(sides.source, sides.target, 'BATTERY_RACK'),
        )
    }

    if (deviceTypes.has('PCS')) {
        const chargePower = metricValue('ess_charge_kw', relatedDevices, telemetry, deviceTelemetry)
        const dischargePower = metricValue('ess_discharge_kw', relatedDevices, telemetry, deviceTelemetry)
        return chargePower > 0
            ? currentState(chargePower, directionTowardType(sides.source, sides.target, 'PCS'))
            : currentState(dischargePower, directionFromType(sides.source, sides.target, 'PCS'))
    }

    return inactiveState
}

export const createClientId = (prefix: string) => `${prefix}-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`
