from sqlalchemy.orm import Session

from ..domains.device.models import Device
from ..domains.power_flow.models import PowerFlowLayout, PowerFlowLayoutNode, PowerFlowWire


POWER_FLOW_NODES = [
    ("node-1784786141015-dd80ts", "RACK-2026-001", 1185.5999857584634, 1290.7498728434248),
    ("node-1784786142275-wu7nye", "RACK-2026-003", 1643.0221998426648, 1290.7498728434248),
    ("node-1784786146763-lhcy9v", "RACK-2026-002", 1414.3110928005642, 1290.7498728434248),
    ("node-1784786148961-7u9xgp", "RACK-2026-004", 1871.7333068847656, 1290.7498728434248),
    ("node-1784786153542-hmbrvk", "ACP-2026-001", 1528.1555345323352, 794.8667805989583),
    ("node-1784786386506-oeybm1", "INV-2026-001", 976.5333014594186, 518.5333887736001),
    ("node-1784786409558-pwrlwa", "INV-2026-012", 645.0221574571397, 802.3200078328451),
    ("node-1784786411538-j1j6xu", "INV-2026-011", 645.0221574571397, 650.4266728719076),
    ("node-1784786414318-n8cskd", "INV-2026-010", 645.0221574571397, 498.53333791097),
    ("node-1784786415834-htjum5", "INV-2026-013", 645.0221574571397, 954.2133427937827),
    ("node-1784786417376-my5sds", "INV-2026-014", 645.0221574571397, 1106.1066777547203),
    ("node-1784786420881-39ngvy", "INV-2026-006", 976.5333014594186, 1060.7466451009116),
    ("node-1784786422125-nzpt39", "INV-2026-004", 976.5333014594186, 788.9067138671875),
    ("node-1784786432088-xr9gbk", "INV-2026-005", 976.5333014594186, 924.8266794840495),
    ("node-1784786445577-mfiol6", "INV-2026-003", 976.5333014594186, 652.9867482503255),
    ("node-1784786512559-hxbp62", "MTR-GRID-001", 2044.33344523112, 891.0000050862631),
    ("node-1784786514646-sqemaq", "MTR-LOAD-001", 2044.33344523112, 714.6665395100912),
    ("node-1784786528146-gjn6pa", "PCS-2026-001", 1528.1555345323352, 946.6666107177732),
    ("node-1784786545633-k0q9zh", "BAT-2026-001", 1528.1555345323352, 1108.4998524983725),
    ("node-1784786589568-sr1ysh", "BMS-2026-001", 1822.3333231608074, 1108.4998524983725),
]


POWER_FLOW_WIRES = [
    ("wire-1784786548527-vxqqg3", "node-1784786528146-gjn6pa", "BOTTOM", "node-1784786545633-k0q9zh", "TOP"),
    ("wire-1784786551439-p8dapk", "node-1784786153542-hmbrvk", "BOTTOM", "node-1784786528146-gjn6pa", "TOP"),
    ("wire-1784786556800-avljgm", "node-1784786141015-dd80ts", "TOP", "node-1784786545633-k0q9zh", "BOTTOM"),
    ("wire-1784786558322-w48458", "node-1784786146763-lhcy9v", "TOP", "node-1784786545633-k0q9zh", "BOTTOM"),
    ("wire-1784786560093-uheidx", "node-1784786142275-wu7nye", "TOP", "node-1784786545633-k0q9zh", "BOTTOM"),
    ("wire-1784786562816-8tg75y", "node-1784786148961-7u9xgp", "TOP", "node-1784786545633-k0q9zh", "BOTTOM"),
    ("wire-1784786592085-dulkj5", "node-1784786545633-k0q9zh", "RIGHT", "node-1784786589568-sr1ysh", "LEFT"),
    ("wire-1784786619735-rfmbqt", "node-1784786420881-39ngvy", "RIGHT", "node-1784786153542-hmbrvk", "LEFT"),
    ("wire-1784786622511-tw4scb", "node-1784786432088-xr9gbk", "RIGHT", "node-1784786153542-hmbrvk", "LEFT"),
    ("wire-1784786625014-mlhwpb", "node-1784786422125-nzpt39", "RIGHT", "node-1784786153542-hmbrvk", "LEFT"),
    ("wire-1784786630095-elfsez", "node-1784786445577-mfiol6", "RIGHT", "node-1784786153542-hmbrvk", "LEFT"),
    ("wire-1784786632768-rbe4h2", "node-1784786386506-oeybm1", "RIGHT", "node-1784786153542-hmbrvk", "LEFT"),
    ("wire-1784786635474-0dm1w8", "node-1784786414318-n8cskd", "RIGHT", "node-1784786153542-hmbrvk", "LEFT"),
    ("wire-1784786638083-56h8p9", "node-1784786411538-j1j6xu", "RIGHT", "node-1784786153542-hmbrvk", "LEFT"),
    ("wire-1784786641243-4fkz1i", "node-1784786409558-pwrlwa", "RIGHT", "node-1784786153542-hmbrvk", "LEFT"),
    ("wire-1784786645285-n19lo3", "node-1784786415834-htjum5", "RIGHT", "node-1784786153542-hmbrvk", "LEFT"),
    ("wire-1784786648251-e2b3n6", "node-1784786417376-my5sds", "RIGHT", "node-1784786153542-hmbrvk", "LEFT"),
    ("wire-1784786669712-a0kvy0", "node-1784786153542-hmbrvk", "RIGHT", "node-1784786512559-hxbp62", "LEFT"),
    ("wire-1784786672852-nd7x6n", "node-1784786153542-hmbrvk", "RIGHT", "node-1784786514646-sqemaq", "LEFT"),
]


def ensure_power_flow_layout(db: Session) -> None:
    if db.query(PowerFlowLayoutNode).count() > 0:
        return

    layout = db.query(PowerFlowLayout).filter(PowerFlowLayout.is_default.is_(True)).first()
    if layout is None:
        layout = PowerFlowLayout(
            name="기본 전력 흐름",
            is_default=True,
            canvas_width=1280,
            canvas_height=720,
        )
        db.add(layout)
        db.flush()
    else:
        layout.canvas_width = 1280
        layout.canvas_height = 720

    serial_numbers = [serial_number for _, serial_number, _, _ in POWER_FLOW_NODES]
    devices = db.query(Device).filter(Device.serial_number.in_(serial_numbers)).all()
    devices_by_serial = {device.serial_number: device for device in devices}
    missing_serials = sorted(set(serial_numbers) - set(devices_by_serial))
    if missing_serials:
        raise RuntimeError(f"Power-flow seed devices not found: {', '.join(missing_serials)}")

    db.add_all(
        [
            PowerFlowLayoutNode(
                layout_id=layout.id,
                client_id=client_id,
                device_id=devices_by_serial[serial_number].id,
                x=x,
                y=y,
                width=190,
                height=84,
            )
            for client_id, serial_number, x, y in POWER_FLOW_NODES
        ]
    )
    db.add_all(
        [
            PowerFlowWire(
                layout_id=layout.id,
                client_id=client_id,
                source_type="NODE",
                source_ref=source_ref,
                source_anchor=source_anchor,
                target_type="NODE",
                target_ref=target_ref,
                target_anchor=target_anchor,
                direction="FORWARD",
                metric_key=None,
                is_enabled=True,
                route_points_json="[]",
            )
            for client_id, source_ref, source_anchor, target_ref, target_anchor in POWER_FLOW_WIRES
        ]
    )
