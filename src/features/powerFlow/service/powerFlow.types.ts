import type { AppIconName } from '@/shared/constants/appIcons'

export type PowerFlowAnchor = 'TOP' | 'RIGHT' | 'BOTTOM' | 'LEFT'
export type PowerFlowEndpointType = 'NODE' | 'JUNCTION'
export type PowerFlowDirection = 'FORWARD' | 'REVERSE' | 'BIDIRECTIONAL'
export type PowerFlowWireTone = 'active' | 'inactive' | 'warning' | 'fault'

export type PowerFlowDeviceItem = {
    id: number
    device_type: string
    name: string
    status: string
    is_active: boolean
    image_path?: string | null
    display_value?: number | null
    display_unit?: string | null
    module_count?: number | null
}

export type PowerFlowLayoutNode = {
    client_id: string
    device_id: number
    x: number
    y: number
    width: number
    height: number
}

export type PowerFlowJunction = {
    client_id: string
    x: number
    y: number
}

export type PowerFlowRoutePoint = {
    x: number
    y: number
}

export type PowerFlowWire = {
    client_id: string
    source_type: PowerFlowEndpointType
    source_ref: string
    source_anchor: PowerFlowAnchor
    target_type: PowerFlowEndpointType
    target_ref: string
    target_anchor: PowerFlowAnchor
    direction: PowerFlowDirection
    metric_key?: string | null
    is_enabled: boolean
    route_points: PowerFlowRoutePoint[]
}

export type PowerFlowLayout = {
    id: number
    name: string
    canvas_width: number
    canvas_height: number
    nodes: PowerFlowLayoutNode[]
    junctions: PowerFlowJunction[]
    wires: PowerFlowWire[]
}

export type PowerFlowEditorData = {
    layout: PowerFlowLayout
    devices: PowerFlowDeviceItem[]
    telemetry: Record<string, number>
}

export type PowerFlowLayoutSaveBody = Omit<PowerFlowLayout, 'id' | 'name'>

export type PowerFlowEndpoint = {
    type: PowerFlowEndpointType
    ref: string
    anchor: PowerFlowAnchor
}

export type PowerFlowPoint = {
    x: number
    y: number
}

export type PowerFlowDeviceVisual = {
    icon: AppIconName
    label: string
}
