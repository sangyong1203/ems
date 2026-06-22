import type {
    PowerFlowAnchor,
    PowerFlowDeviceItem,
    PowerFlowDeviceVisual,
    PowerFlowEndpoint,
    PowerFlowJunction,
    PowerFlowLayoutNode,
    PowerFlowPoint,
    PowerFlowWire,
    PowerFlowWireTone,
} from './powerFlow.types'

export const deviceVisual = (deviceType: string): PowerFlowDeviceVisual => {
    const visuals: Record<string, PowerFlowDeviceVisual> = {
        INVERTER: { icon: 'IconInverter', label: '인버터' },
        PCS: { icon: 'IconPcs', label: 'PCS' },
        ESS_BATTERY: { icon: 'IconEss', label: 'ESS Battery' },
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
        .filter(item => item.source_ref === endpoint.ref || item.target_ref === endpoint.ref)
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
                visitedJunctions,
            )
        })
}

const endpointDevicesForWire = (
    wire: PowerFlowWire,
    nodes: PowerFlowLayoutNode[],
    wires: PowerFlowWire[],
    devices: PowerFlowDeviceItem[],
) => {
    const items = [
        ...connectedDevicesForEndpoint({ type: wire.source_type, ref: wire.source_ref }, nodes, wires, devices),
        ...connectedDevicesForEndpoint({ type: wire.target_type, ref: wire.target_ref }, nodes, wires, devices),
    ]

    return Array.from(new Map(items.map(device => [device.id, device])).values())
}

export const wireCurrentActive = (wire: PowerFlowWire, telemetry: Record<string, number>) => {
    if (!wire.is_enabled || !wire.metric_key) {
        return false
    }
    return Number(telemetry[wire.metric_key] ?? 0) > 0
}

export const createClientId = (prefix: string) => `${prefix}-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`
