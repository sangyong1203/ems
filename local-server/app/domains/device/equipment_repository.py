from sqlalchemy.orm import Session

from .models import Device


# 장비 종류와 단위가 일치하는 용량을 합산하며 단위는 대소문자를 구분하지 않습니다.
def _capacity_sum(devices: list[Device], device_type: str, capacity_unit: str) -> float:
    return round(
        sum(
            float(device.capacity or 0)
            for device in devices
            if device.device_type == device_type and (device.capacity_unit or "").lower() == capacity_unit.lower()
        ),
        1,
    )


# 전체·활성 장비의 종류별 수와 태양광·ESS 설치 및 운전 용량을 집계합니다.
def get_equipment_summary(db: Session) -> dict:
    devices = db.query(Device).all()
    active_devices = [device for device in devices if device.is_active]

    return {
        "deviceCounts": {
            "INVERTER": len([device for device in devices if device.device_type == "INVERTER"]),
            "PCS": len([device for device in devices if device.device_type == "PCS"]),
            "ESS_BATTERY": len([device for device in devices if device.device_type == "ESS_BATTERY"]),
            "BATTERY_RACK": len([device for device in devices if device.device_type == "BATTERY_RACK"]),
            "BMS": len([device for device in devices if device.device_type == "BMS"]),
            "AC_PANEL": len([device for device in devices if device.device_type == "AC_PANEL"]),
            "METER": len([device for device in devices if device.device_type in ("GRID_METER", "LOAD_METER")]),
        },
        "activeDeviceCounts": {
            "INVERTER": len([device for device in active_devices if device.device_type == "INVERTER"]),
            "PCS": len([device for device in active_devices if device.device_type == "PCS"]),
            "ESS_BATTERY": len([device for device in active_devices if device.device_type == "ESS_BATTERY"]),
            "BATTERY_RACK": len([device for device in active_devices if device.device_type == "BATTERY_RACK"]),
            "BMS": len([device for device in active_devices if device.device_type == "BMS"]),
            "AC_PANEL": len([device for device in active_devices if device.device_type == "AC_PANEL"]),
            "METER": len(
                [device for device in active_devices if device.device_type in ("GRID_METER", "LOAD_METER")]
            ),
        },
        "capacities": {
            "solarInstalledKw": _capacity_sum(devices, "INVERTER", "kW"),
            "solarOperatingKw": _capacity_sum(active_devices, "INVERTER", "kW"),
            "essInstalledKwh": _capacity_sum(devices, "ESS_BATTERY", "kWh"),
            "essOperatingKwh": _capacity_sum(active_devices, "ESS_BATTERY", "kWh"),
        },
    }
