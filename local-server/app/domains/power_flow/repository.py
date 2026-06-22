import json

from sqlalchemy import func
from sqlalchemy.orm import Session

from .models import PowerFlowJunction, PowerFlowLayout, PowerFlowLayoutNode, PowerFlowWire
from ..device.models import Device
from ..pv_string.models import InverterPvStringLink, PvString
from ..telemetry.models import TelemetryLatest
from ..telemetry.repository import latest_map


def _get_default_layout(db: Session) -> PowerFlowLayout:
    layout = db.query(PowerFlowLayout).filter(PowerFlowLayout.is_default.is_(True)).first()
    if layout is None:
        layout = PowerFlowLayout()
        db.add(layout)
        db.commit()
        db.refresh(layout)
    return layout


def get_editor_data(db: Session) -> dict:
    layout = _get_default_layout(db)
    devices = db.query(Device).order_by(Device.device_type.asc(), Device.name.asc()).all()
    nodes = db.query(PowerFlowLayoutNode).filter(PowerFlowLayoutNode.layout_id == layout.id).all()
    junctions = db.query(PowerFlowJunction).filter(PowerFlowJunction.layout_id == layout.id).all()
    wires = db.query(PowerFlowWire).filter(PowerFlowWire.layout_id == layout.id).all()
    telemetry = latest_map(db)
    telemetry_rows = db.query(TelemetryLatest).all()
    telemetry_by_device = {(item.device_id, item.metric_key): item for item in telemetry_rows}
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
        "grid_export_kw": "kW",
        "grid_import_kw": "kW",
        "load_power_kw": "kW",
        "ambient_temperature_c": "℃",
    }

    def device_metric(device: Device) -> tuple[float | None, str | None]:
        metric_keys = {
            "INVERTER": ["inverter_power_kw"],
            "PCS": ["ess_charge_kw", "ess_discharge_kw"],
            "ESS_BATTERY": ["ess_soc"],
            "BMS": ["ess_soc"],
            "AC_PANEL": ["load_power_kw", "grid_export_kw", "grid_import_kw"],
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
    db.commit()
    return get_editor_data(db)
