import json

from sqlalchemy import func
from sqlalchemy.orm import Session

from .models import PowerFlowJunction, PowerFlowLayout, PowerFlowLayoutNode, PowerFlowWire
from ..device.models import Device
from ..ess.models import EssSystem, EssSystemBatteryRack
from ..pv_string.models import InverterPvStringLink, PvString
from ..telemetry.models import TelemetryLatest
from ..telemetry.repository import latest_site_map


def _get_default_layout(db: Session) -> PowerFlowLayout:
    layout = db.query(PowerFlowLayout).filter(PowerFlowLayout.is_default.is_(True)).first()
    if layout is None:
        layout = PowerFlowLayout()
        db.add(layout)
        db.commit()
        db.refresh(layout)
    return layout


def _choose_anchor(source_node: PowerFlowLayoutNode, target_node: PowerFlowLayoutNode) -> tuple[str, str]:
    delta_x = (target_node.x + target_node.width / 2) - (source_node.x + source_node.width / 2)
    delta_y = (target_node.y + target_node.height / 2) - (source_node.y + source_node.height / 2)
    if abs(delta_x) >= abs(delta_y):
        return ("RIGHT", "LEFT") if delta_x >= 0 else ("LEFT", "RIGHT")
    return ("BOTTOM", "TOP") if delta_y >= 0 else ("TOP", "BOTTOM")


def _has_existing_wire(
    wires: list[PowerFlowWire],
    source_node_id: str,
    target_node_id: str,
) -> bool:
    for wire in wires:
        if wire.source_type != "NODE" or wire.target_type != "NODE":
            continue
        if {wire.source_ref, wire.target_ref} == {source_node_id, target_node_id}:
            return True
    return False


def _ensure_battery_rack_wires(
    db: Session,
    layout_id: int,
    nodes: list[PowerFlowLayoutNode],
    wires: list[PowerFlowWire],
    devices: list[Device],
) -> bool:
    if not nodes:
        return False

    node_by_device_id = {node.device_id: node for node in nodes}
    device_by_id = {device.id: device for device in devices}
    battery_nodes = {
        device_id: node
        for device_id, node in node_by_device_id.items()
        if device_by_id.get(device_id) and device_by_id[device_id].device_type == "ESS_BATTERY"
    }
    rack_nodes = {
        device_id: node
        for device_id, node in node_by_device_id.items()
        if device_by_id.get(device_id) and device_by_id[device_id].device_type == "BATTERY_RACK"
    }

    if not battery_nodes or not rack_nodes:
        return False

    systems = db.query(EssSystem).filter(EssSystem.battery_device_id.is_not(None)).all()
    rack_links = (
        db.query(EssSystemBatteryRack)
        .order_by(EssSystemBatteryRack.ess_system_id.asc(), EssSystemBatteryRack.display_order.asc())
        .all()
    )
    rack_links_by_system: dict[int, list[EssSystemBatteryRack]] = {}
    for link in rack_links:
        rack_links_by_system.setdefault(link.ess_system_id, []).append(link)

    created = False
    for system in systems:
        battery_device_id = system.battery_device_id
        if battery_device_id is None or battery_device_id not in battery_nodes:
            continue

        battery_node = battery_nodes[battery_device_id]
        for link in rack_links_by_system.get(system.id, []):
            rack_node = rack_nodes.get(link.rack_device_id)
            if rack_node is None:
                continue
            if _has_existing_wire(wires, rack_node.client_id, battery_node.client_id):
                continue

            source_anchor, target_anchor = _choose_anchor(rack_node, battery_node)
            auto_wire = PowerFlowWire(
                layout_id=layout_id,
                client_id=f"auto-rack-link-{link.rack_device_id}-{battery_device_id}",
                source_type="NODE",
                source_ref=rack_node.client_id,
                source_anchor=source_anchor,
                target_type="NODE",
                target_ref=battery_node.client_id,
                target_anchor=target_anchor,
                direction="BIDIRECTIONAL",
                metric_key="battery_rack_current_a",
                is_enabled=True,
                route_points_json="[]",
            )
            db.add(auto_wire)
            wires.append(auto_wire)
            created = True

    return created


def get_editor_data(db: Session) -> dict:
    layout = _get_default_layout(db)
    devices = db.query(Device).order_by(Device.device_type.asc(), Device.name.asc()).all()
    nodes = db.query(PowerFlowLayoutNode).filter(PowerFlowLayoutNode.layout_id == layout.id).all()
    junctions = db.query(PowerFlowJunction).filter(PowerFlowJunction.layout_id == layout.id).all()
    wires = db.query(PowerFlowWire).filter(PowerFlowWire.layout_id == layout.id).all()
    telemetry = latest_site_map(db)
    telemetry_rows = db.query(TelemetryLatest).all()
    telemetry_by_device = {(item.device_id, item.metric_key): item for item in telemetry_rows}
    device_telemetry: dict[str, dict[str, float]] = {}
    for item in sorted(telemetry_rows, key=lambda row: row.measured_at):
        if item.device_id is None:
            continue
        device_telemetry.setdefault(str(item.device_id), {})[item.metric_key] = float(item.metric_value)
    module_counts = {
        inverter_id: int(module_count or 0)
        for inverter_id, module_count in (
            db.query(InverterPvStringLink.inverter_device_id, func.sum(PvString.panel_count))
            .join(PvString, PvString.id == InverterPvStringLink.pv_string_id)
            .group_by(InverterPvStringLink.inverter_device_id)
            .all()
        )
    }
    metric_units = {
        "inverter_power_kw": "kW",
        "ess_soc": "%",
        "ess_soc_avg": "%",
        "battery_rack_soc": "%",
        "grid_export_kw": "kW",
        "grid_import_kw": "kW",
        "load_power_kw": "kW",
        "ambient_temperature_c": "℃",
    }

    def device_metric(device: Device) -> tuple[float | None, str | None]:
        if device.device_type == "AC_PANEL":
            return None, None

        metric_keys = {
            "INVERTER": ["inverter_power_kw"],
            "PCS": ["ess_charge_kw", "ess_discharge_kw"],
            "ESS_BATTERY": ["ess_soc", "ess_soc_avg"],
            "BATTERY_RACK": ["battery_rack_soc"],
            "BMS": ["ess_soc"],
            "GRID_METER": ["grid_export_kw", "grid_import_kw"],
            "LOAD_METER": ["load_power_kw"],
            "WEATHER_SENSOR": ["ambient_temperature_c"],
            "SENSOR": ["ambient_temperature_c"],
        }.get(device.device_type, [])
        for metric_key in metric_keys:
            metric = telemetry_by_device.get((device.id, metric_key)) or telemetry.get(metric_key)
            if metric is not None and float(metric.metric_value) != 0:
                return float(metric.metric_value), metric.unit or metric_units.get(metric_key)
        if device.capacity is not None:
            return float(device.capacity), device.capacity_unit
        return None, None

    return {
        "layout": {
            "id": layout.id,
            "name": layout.name,
            "canvas_width": layout.canvas_width,
            "canvas_height": layout.canvas_height,
            "nodes": [
                {
                    "client_id": item.client_id,
                    "device_id": item.device_id,
                    "x": item.x,
                    "y": item.y,
                    "width": item.width,
                    "height": item.height,
                }
                for item in nodes
            ],
            "junctions": [{"client_id": item.client_id, "x": item.x, "y": item.y} for item in junctions],
            "wires": [
                {
                    "client_id": item.client_id,
                    "source_type": item.source_type,
                    "source_ref": item.source_ref,
                    "source_anchor": item.source_anchor,
                    "target_type": item.target_type,
                    "target_ref": item.target_ref,
                    "target_anchor": item.target_anchor,
                    "direction": item.direction,
                    "metric_key": item.metric_key,
                    "is_enabled": item.is_enabled,
                    "route_points": json.loads(item.route_points_json or "[]"),
                }
                for item in wires
            ],
        },
        "devices": [
            {
                "id": item.id,
                "device_type": item.device_type,
                "name": item.name,
                "status": item.status,
                "is_active": item.is_active,
                "image_path": item.image_path,
                "display_value": device_metric(item)[0],
                "display_unit": device_metric(item)[1],
                "module_count": module_counts.get(item.id) if item.device_type == "INVERTER" else None,
            }
            for item in devices
        ],
        "telemetry": {key: float(value.metric_value) for key, value in telemetry.items()},
        "device_telemetry": device_telemetry,
    }


def save_editor_data(db: Session, payload: dict) -> dict:
    layout = _get_default_layout(db)
    layout.canvas_width = payload["canvas_width"]
    layout.canvas_height = payload["canvas_height"]

    db.query(PowerFlowWire).filter(PowerFlowWire.layout_id == layout.id).delete()
    db.query(PowerFlowJunction).filter(PowerFlowJunction.layout_id == layout.id).delete()
    db.query(PowerFlowLayoutNode).filter(PowerFlowLayoutNode.layout_id == layout.id).delete()

    db.add_all([PowerFlowLayoutNode(layout_id=layout.id, **item) for item in payload["nodes"]])
    db.add_all([PowerFlowJunction(layout_id=layout.id, **item) for item in payload["junctions"]])
    db.add_all(
        [
            PowerFlowWire(
                layout_id=layout.id,
                client_id=item["client_id"],
                source_type=item["source_type"],
                source_ref=item["source_ref"],
                source_anchor=item["source_anchor"],
                target_type=item["target_type"],
                target_ref=item["target_ref"],
                target_anchor=item["target_anchor"],
                direction=item["direction"],
                metric_key=item["metric_key"],
                is_enabled=item["is_enabled"],
                route_points_json=json.dumps(item["route_points"]),
            )
            for item in payload["wires"]
        ],
    )
    db.flush()
    devices = db.query(Device).order_by(Device.device_type.asc(), Device.name.asc()).all()
    nodes = db.query(PowerFlowLayoutNode).filter(PowerFlowLayoutNode.layout_id == layout.id).all()
    wires = db.query(PowerFlowWire).filter(PowerFlowWire.layout_id == layout.id).all()
    _ensure_battery_rack_wires(db, layout.id, nodes, wires, devices)
    db.commit()
    return get_editor_data(db)
