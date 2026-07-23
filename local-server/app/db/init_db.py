from datetime import datetime

from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

from .base import Base, Device, EssSystem, EssSystemBatteryRack, InverterPvStringLink, ProjectConfig, PvString, User
from ..core.database import engine
from ..domains.simulator.generator import generate_today


def _build_inverter(index: int) -> Device:
    return Device(
        device_type="INVERTER",
        name=f"Inverter #{index}",
        manufacturer="Sungrow",
        model_name="SG100CX",
        serial_number=f"INV-2026-{index:03d}",
        capacity=100,
        capacity_unit="kW",
        install_location=f"PV Yard A-{index}",
        install_date="2026-05-01",
        communication_type="Ethernet",
        ip_address=f"192.168.10.{20 + index}",
        port=502,
        slave_id=index,
        protocol="Modbus TCP",
        status="NORMAL",
        vendor_name="Solar EPC",
    )


def _ensure_inverter_devices(db: Session) -> None:
    existing_serials = {
        serial_number
        for (serial_number,) in db.query(Device.serial_number).filter(Device.device_type == "INVERTER").all()
    }
    missing_inverters = [
        _build_inverter(index)
        for index in range(1, 16)
        if f"INV-2026-{index:03d}" not in existing_serials
    ]

    if missing_inverters:
        db.add_all(missing_inverters)


def _ensure_ac_panel_device(db: Session) -> None:
    exists = db.query(Device).filter(Device.device_type == "AC_PANEL").first()
    if exists:
        return
    db.add(
        Device(
            device_type="AC_PANEL",
            name="AC Distribution Panel #1",
            manufacturer="LS Electric",
            model_name="AC-PANEL-500",
            serial_number="ACP-2026-001",
            capacity=500,
            capacity_unit="kW",
            install_location="Main Electrical Room",
            install_date="2026-05-01",
            status="NORMAL",
            vendor_name="Solar EPC",
        )
    )


def _ensure_ess_battery_device(db: Session) -> None:
    exists = db.query(Device).filter(Device.device_type == "ESS_BATTERY").first()
    if exists:
        return
    db.add(
        Device(
            device_type="ESS_BATTERY",
            name="Battery Bank #1",
            manufacturer="LG Energy Solution",
            model_name="ESS-RACK-1000",
            serial_number="BAT-2026-001",
            capacity=1000,
            capacity_unit="kWh",
            install_location="ESS Room",
            install_date="2026-05-01",
            status="NORMAL",
            vendor_name="Solar EPC",
        )
    )


def _normalize_battery_bank_names(db: Session) -> None:
    batteries = db.query(Device).filter(Device.device_type == "ESS_BATTERY").all()
    for battery in batteries:
        if battery.name and battery.name.startswith("ESS Battery"):
            battery.name = battery.name.replace("ESS Battery", "Battery Bank", 1)


def _ensure_pv_strings(db: Session) -> None:
    if db.query(PvString).count() > 0:
        return

    strings = [
        PvString(
            name=f"PV String #{index}",
            panel_count=18,
            panel_capacity_kw=0.55,
            rated_capacity_kw=9.9,
            install_location=f"PV Yard A-{index}",
            status="NORMAL",
            is_active=True,
        )
        for index in range(1, 21)
    ]
    db.add_all(strings)
    db.flush()

    inverter = db.query(Device).filter(Device.device_type == "INVERTER").order_by(Device.name.asc()).first()
    if inverter:
        for index, pv_string in enumerate(strings[:4], start=1):
            db.add(
                InverterPvStringLink(
                    inverter_device_id=inverter.id,
                    pv_string_id=pv_string.id,
                    mppt_no=1 if index <= 2 else 2,
                    channel_no=index if index <= 2 else index - 2,
                )
            )


def _ensure_ess_systems(db: Session) -> None:
    if db.query(EssSystem).count() > 0:
        return

    pcs = db.query(Device).filter(Device.device_type == "PCS").order_by(Device.id.asc()).first()
    bms = db.query(Device).filter(Device.device_type == "BMS").order_by(Device.id.asc()).first()
    battery = db.query(Device).filter(Device.device_type == "ESS_BATTERY").order_by(Device.id.asc()).first()

    db.add(
        EssSystem(
            name="ESS System #1",
            code="ESS-SYS-001",
            capacity_kwh=float(battery.capacity or 1000) if battery else 1000,
            pcs_device_id=pcs.id if pcs else None,
            bms_device_id=bms.id if bms else None,
            battery_device_id=battery.id if battery else None,
            status="NORMAL",
            is_active=True,
            install_location=battery.install_location if battery else "ESS Room",
        )
    )


def _ensure_battery_racks(db: Session) -> None:
    db.flush()
    system = db.query(EssSystem).order_by(EssSystem.id.asc()).first()
    if system is None:
        return

    existing_links = {
        link.rack_no
        for link in db.query(EssSystemBatteryRack).filter(EssSystemBatteryRack.ess_system_id == system.id).all()
    }
    rack_specs = [
        (1, "NORMAL"),
        (2, "NORMAL"),
        (3, "WARNING"),
        (4, "NORMAL"),
    ]

    for rack_no, status in rack_specs:
        serial_number = f"RACK-2026-{rack_no:03d}"
        rack = db.query(Device).filter(Device.serial_number == serial_number).first()
        if rack is None:
            rack = Device(
                device_type="BATTERY_RACK",
                name=f"Rack #{rack_no}",
                manufacturer="LG Energy Solution",
                model_name="ESS-RACK-250",
                serial_number=serial_number,
                capacity=250,
                capacity_unit="kWh",
                install_location=f"ESS Room Rack-{rack_no}",
                communication_type="CAN",
                slave_id=rack_no,
                protocol="CANopen",
                status=status,
                is_active=True,
            )
            db.add(rack)
            db.flush()

        if rack_no not in existing_links:
            db.add(
                EssSystemBatteryRack(
                    ess_system_id=system.id,
                    rack_device_id=rack.id,
                    rack_no=rack_no,
                    display_order=rack_no,
                )
            )


def _ensure_seed_users(db: Session) -> None:
    seed_users = [
        {
            "username": "admin",
            "password_hash": "1111",
            "name": "System Administrator",
            "email": "admin@Solar.local",
            "department": "Platform",
            "role": "Platform Admin",
            "status": "Active",
            "last_login_at": datetime(2026, 5, 22, 9, 10, 0),
            "created_at": datetime(2026, 5, 1, 10, 0, 0),
        },
        {
            "username": "operator@Solar.local",
            "password_hash": "1111",
            "name": "Operations Manager",
            "email": "operator@Solar.local",
            "department": "Operations",
            "role": "Operator",
            "status": "Active",
            "last_login_at": datetime(2026, 5, 21, 18, 24, 0),
            "created_at": datetime(2026, 5, 3, 14, 20, 0),
        },
        {
            "username": "viewer@Solar.local",
            "password_hash": "1111",
            "name": "Security Viewer",
            "email": "viewer@Solar.local",
            "department": "Security",
            "role": "Viewer",
            "status": "Inactive",
            "last_login_at": datetime(2026, 5, 18, 11, 5, 0),
            "created_at": datetime(2026, 5, 5, 9, 35, 0),
        },
    ]

    for item in seed_users:
        user = db.query(User).filter(User.username == item["username"]).first()
        if user is None:
            db.add(User(**item))
            continue

        for key, value in item.items():
            if key == "password_hash":
                continue
            if not getattr(user, key, None):
                setattr(user, key, value)


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)
    user_columns = {column["name"] for column in inspect(engine).get_columns("users")}
    user_column_defs = {
        "name": "VARCHAR(80) NOT NULL DEFAULT ''",
        "email": "VARCHAR(120) NOT NULL DEFAULT ''",
        "department": "VARCHAR(80) NOT NULL DEFAULT ''",
        "status": "VARCHAR(40) NOT NULL DEFAULT 'Active'",
        "last_login_at": "DATETIME",
    }
    with engine.begin() as connection:
        for column, definition in user_column_defs.items():
            if column not in user_columns:
                connection.execute(text(f"ALTER TABLE users ADD COLUMN {column} {definition}"))
        connection.execute(text("UPDATE users SET role = 'Platform Admin' WHERE role = 'admin'"))
        connection.execute(text("UPDATE users SET name = 'System Administrator' WHERE username = 'admin' AND name = ''"))
        connection.execute(text("UPDATE users SET email = 'admin@Solar.local' WHERE username = 'admin' AND email = ''"))
        connection.execute(text("UPDATE users SET department = 'Platform' WHERE username = 'admin' AND department = ''"))

    device_columns = {column["name"] for column in inspect(engine).get_columns("devices")}
    if "is_active" not in device_columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE devices ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT 1"))
    if "image_path" not in device_columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE devices ADD COLUMN image_path VARCHAR(255)"))

    project_columns = {column["name"] for column in inspect(engine).get_columns("project_config")}
    refresh_interval_columns = [
        "dashboard_refresh_interval",
        "solar_refresh_interval",
        "ess_refresh_interval",
        "power_flow_refresh_interval",
        "trend_refresh_interval",
    ]
    with engine.begin() as connection:
        for column in refresh_interval_columns:
            if column not in project_columns:
                connection.execute(text(f"ALTER TABLE project_config ADD COLUMN {column} INTEGER NOT NULL DEFAULT 5000"))
                connection.execute(text(f"UPDATE project_config SET {column} = data_refresh_interval"))


def seed_database(db: Session) -> None:
    _ensure_seed_users(db)

    if db.query(ProjectConfig).count() == 0:
        db.add(
            ProjectConfig(
                project_name="산업단지 태양광 ESS 구축사업",
                site_name="김제 스마트팩토리 태양광 ESS",
                location="전북 김제시",
                customer_name="김제 스마트팩토리",
                contractor_name="Solar EPC",
                solar_capacity_kw=500,
                ess_capacity_kwh=1000,
                system_name="Solar ESS EMS",
                data_refresh_interval=5000,
            )
        )

    if db.query(Device).count() == 0:
        devices = [
            *[_build_inverter(index) for index in range(1, 16)],
            Device(
                device_type="PCS",
                name="PCS #1",
                manufacturer="Hyosung",
                model_name="PCS-500",
                serial_number="PCS-2026-001",
                capacity=500,
                capacity_unit="kW",
                install_location="ESS Room",
                communication_type="Ethernet",
                ip_address="192.168.20.10",
                port=502,
                slave_id=11,
                protocol="Modbus TCP",
                status="NORMAL",
            ),
            Device(
                device_type="ESS_BATTERY",
                name="Battery Bank #1",
                manufacturer="LG Energy Solution",
                model_name="ESS-RACK-1000",
                serial_number="BAT-2026-001",
                capacity=1000,
                capacity_unit="kWh",
                install_location="ESS Room",
                install_date="2026-05-01",
                status="NORMAL",
            ),
            Device(
                device_type="BMS",
                name="BMS #1",
                manufacturer="LG Energy Solution",
                model_name="BMS-MASTER",
                serial_number="BMS-2026-001",
                capacity=1000,
                capacity_unit="kWh",
                install_location="ESS Room",
                communication_type="Ethernet",
                ip_address="192.168.20.20",
                port=502,
                slave_id=21,
                protocol="Modbus TCP",
                status="NORMAL",
            ),
            Device(
                device_type="GRID_METER",
                name="Grid Meter #1",
                manufacturer="Schneider",
                model_name="PM5350",
                serial_number="MTR-GRID-001",
                install_location="Main Panel",
                communication_type="RS485",
                slave_id=31,
                protocol="Modbus RTU",
                status="NORMAL",
            ),
            Device(
                device_type="LOAD_METER",
                name="Load Meter #1",
                manufacturer="Schneider",
                model_name="PM5350",
                serial_number="MTR-LOAD-001",
                install_location="Load Panel",
                communication_type="RS485",
                slave_id=32,
                protocol="Modbus RTU",
                status="NORMAL",
            ),
            Device(
                device_type="WEATHER_SENSOR",
                name="Weather Sensor #1",
                manufacturer="Hukseflux",
                model_name="SR30",
                serial_number="WTH-2026-001",
                install_location="PV Yard",
                communication_type="RS485",
                slave_id=41,
                protocol="Modbus RTU",
                status="NORMAL",
            ),
        ]
        db.add_all(devices)
        db.flush()
    else:
        _ensure_inverter_devices(db)

    _ensure_ac_panel_device(db)
    _ensure_ess_battery_device(db)
    _normalize_battery_bank_names(db)
    _ensure_pv_strings(db)
    _ensure_ess_systems(db)
    _ensure_battery_racks(db)

    db.commit()

    if db.query(ProjectConfig).count() and db.query(Device).count():
        generate_today(db)
