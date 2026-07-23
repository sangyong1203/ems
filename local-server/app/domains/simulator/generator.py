from datetime import datetime, timedelta
from math import sin, pi
from random import Random

from sqlalchemy import delete
from sqlalchemy.orm import Session

from ..alarm.models import Alarm
from ..device.models import Device
from ..ess.models import EssSystem, EssSystemBatteryRack
from ..maintenance.models import MaintenanceRecord
from ..report.models import DailyReport, EssDailyReport
from ..telemetry.models import (
    EssSystemTelemetryHistory,
    EssSystemTelemetryLatest,
    SiteTelemetryHistory,
    SiteTelemetryLatest,
    TelemetryHistory,
    TelemetryLatest,
)


METRIC_UNITS = {
    "solar_power_kw": "kW",
    "solar_today_kwh": "kWh",
    "solar_total_kwh": "kWh",
    "load_power_kw": "kW",
    "grid_export_kw": "kW",
    "grid_import_kw": "kW",
    "ess_soc": "%",
    "ess_soc_avg": "%",
    "ess_soh": "%",
    "ess_soh_avg": "%",
    "ess_charge_kw": "kW",
    "ess_discharge_kw": "kW",
    "battery_voltage_v": "V",
    "battery_current_a": "A",
    "battery_temperature_c": "℃",
    "battery_temperature_avg_c": "℃",
    "battery_rack_soc": "%",
    "battery_rack_soh": "%",
    "battery_rack_voltage_v": "V",
    "battery_rack_current_a": "A",
    "battery_rack_avg_temperature_c": "℃",
    "battery_rack_max_temperature_c": "℃",
    "ambient_temperature_c": "℃",
    "pv_module_temperature_c": "℃",
    "inverter_temperature_c": "℃",
    "inverter_power_kw": "kW",
}


def _solar_power_for_hour(hour: int) -> float:
    if hour < 6 or hour > 19:
        return 0
    daylight_ratio = (hour - 6) / 13
    return round(max(0, sin(daylight_ratio * pi)) * 500, 1)


def _upsert_latest(db: Session, device_id: int | None, metric_key: str, value: float, measured_at: datetime) -> None:
    latest = (
        db.query(TelemetryLatest)
        .filter(TelemetryLatest.device_id == device_id, TelemetryLatest.metric_key == metric_key)
        .first()
    )
    if latest is None:
        db.add(
            TelemetryLatest(
                device_id=device_id,
                metric_key=metric_key,
                metric_value=value,
                unit=METRIC_UNITS.get(metric_key),
                measured_at=measured_at,
            )
        )
        db.flush()
        return

    latest.metric_value = value
    latest.unit = METRIC_UNITS.get(metric_key)
    latest.measured_at = measured_at


def _upsert_site_latest(db: Session, metric_key: str, value: float, measured_at: datetime) -> None:
    latest = db.query(SiteTelemetryLatest).filter(SiteTelemetryLatest.metric_key == metric_key).first()
    if latest is None:
        db.add(
            SiteTelemetryLatest(
                metric_key=metric_key,
                metric_value=value,
                unit=METRIC_UNITS.get(metric_key),
                measured_at=measured_at,
            )
        )
        db.flush()
        return

    latest.metric_value = value
    latest.unit = METRIC_UNITS.get(metric_key)
    latest.measured_at = measured_at


def _upsert_system_latest(
    db: Session,
    ess_system_id: int,
    metric_key: str,
    value: float,
    measured_at: datetime,
) -> None:
    latest = (
        db.query(EssSystemTelemetryLatest)
        .filter(
            EssSystemTelemetryLatest.ess_system_id == ess_system_id,
            EssSystemTelemetryLatest.metric_key == metric_key,
        )
        .first()
    )
    if latest is None:
        db.add(
            EssSystemTelemetryLatest(
                ess_system_id=ess_system_id,
                metric_key=metric_key,
                metric_value=value,
                unit=METRIC_UNITS.get(metric_key),
                measured_at=measured_at,
            )
        )
        db.flush()
        return

    latest.metric_value = value
    latest.unit = METRIC_UNITS.get(metric_key)
    latest.measured_at = measured_at


def _metric_device_id(metric_key: str, pcs: Device | None, bms: Device | None) -> int | None:
    if metric_key in {"ess_charge_kw", "ess_discharge_kw"}:
        return pcs.id if pcs else None
    if metric_key.startswith("ess") or metric_key.startswith("battery"):
        return bms.id if bms else None
    return None


def reset_operational_data(db: Session) -> None:
    db.execute(delete(TelemetryLatest))
    db.execute(delete(TelemetryHistory))
    db.execute(delete(SiteTelemetryLatest))
    db.execute(delete(SiteTelemetryHistory))
    db.execute(delete(EssSystemTelemetryLatest))
    db.execute(delete(EssSystemTelemetryHistory))
    db.execute(delete(MaintenanceRecord))
    db.execute(delete(Alarm))
    db.execute(delete(DailyReport))
    db.execute(delete(EssDailyReport))
    db.commit()


def generate_today(db: Session) -> dict:
    now = datetime.now().replace(second=0, microsecond=0)
    today_start = now.replace(hour=0, minute=0)
    random = Random(today_start.strftime("%Y%m%d"))

    db.execute(delete(TelemetryLatest))
    db.execute(delete(TelemetryHistory))
    db.execute(delete(SiteTelemetryLatest))
    db.execute(delete(SiteTelemetryHistory))
    db.execute(delete(EssSystemTelemetryLatest))
    db.execute(delete(EssSystemTelemetryHistory))
    db.execute(delete(DailyReport).where(DailyReport.report_date == today_start.strftime("%Y-%m-%d")))
    db.execute(delete(EssDailyReport).where(EssDailyReport.report_date == today_start.strftime("%Y-%m-%d")))

    total_generation = 0.0
    total_charge = 0.0
    total_discharge = 0.0
    total_grid_export = 0.0
    total_grid_import = 0.0

    devices = db.query(Device).all()
    inverter_devices = [item for item in devices if item.device_type == "INVERTER"]
    active_inverter_count = len([item for item in inverter_devices if item.is_active])
    pcs = next((item for item in devices if item.device_type == "PCS"), None)
    bms = next((item for item in devices if item.device_type == "BMS"), None)
    ess_system = db.query(EssSystem).order_by(EssSystem.id.asc()).first()
    battery_racks = (
        db.query(Device)
        .join(EssSystemBatteryRack, EssSystemBatteryRack.rack_device_id == Device.id)
        .order_by(EssSystemBatteryRack.display_order.asc())
        .all()
    )
    soc_samples: list[float] = []

    for hour in range(24):
        measured_at = today_start + timedelta(hours=hour)
        solar_power = _solar_power_for_hour(hour)
        load_power = round(210 + random.uniform(-25, 55), 1)

        if 9 <= hour <= 16:
            ess_charge = round(min(max(solar_power - load_power, 0), 140), 1)
            ess_discharge = 0.0
        elif 18 <= hour <= 22:
            ess_charge = 0.0
            ess_discharge = round(random.uniform(70, 170), 1)
        else:
            ess_charge = 0.0
            ess_discharge = 0.0

        grid_export = round(max(solar_power - load_power - ess_charge, 0), 1)
        grid_import = round(max(load_power - solar_power - ess_discharge, 0), 1)
        soc = round(min(92, max(18, 62 + (hour - 12) * 1.8 + ess_charge * 0.06 - ess_discharge * 0.04)), 1)
        battery_temperature = round(26 + random.uniform(-2.5, 7.5), 1)
        ambient_temperature = round(18 + max(solar_power / 500, 0) * 10 + random.uniform(-1.5, 1.5), 1)
        pv_module_temperature = round(ambient_temperature + max(solar_power / 500, 0) * 18 + random.uniform(-1, 1), 1)
        inverter_temperature = round(ambient_temperature + max(solar_power / 500, 0) * 12 + random.uniform(-1, 1), 1)

        site_values = {
            "solar_power_kw": solar_power,
            "solar_today_kwh": round(total_generation + solar_power, 1),
            "solar_total_kwh": round(128420 + total_generation + solar_power, 1),
            "load_power_kw": load_power,
            "grid_export_kw": grid_export,
            "grid_import_kw": grid_import,
            "ess_charge_kw": ess_charge,
            "ess_discharge_kw": ess_discharge,
            "ess_soc_avg": soc,
            "ess_soh_avg": 96.4,
            "battery_temperature_avg_c": battery_temperature,
            "ambient_temperature_c": ambient_temperature,
            "pv_module_temperature_c": pv_module_temperature,
            "inverter_temperature_c": inverter_temperature,
        }
        system_values = {
            "ess_soc": soc,
            "ess_soh": 96.4,
            "ess_charge_kw": ess_charge,
            "ess_discharge_kw": ess_discharge,
            "battery_voltage_v": round(720 + soc * 1.6, 1),
            "battery_current_a": round((ess_charge - ess_discharge) * 1.35, 1),
            "battery_temperature_c": battery_temperature,
        }
        legacy_values = {**site_values, **system_values}

        for key, value in site_values.items():
            db.add(
                SiteTelemetryHistory(
                    metric_key=key,
                    metric_value=value,
                    unit=METRIC_UNITS.get(key),
                    measured_at=measured_at,
                )
            )
            if measured_at <= now:
                _upsert_site_latest(db, key, value, measured_at)

        if ess_system is not None:
            soc_samples.append(soc)
            for key, value in system_values.items():
                db.add(
                    EssSystemTelemetryHistory(
                        ess_system_id=ess_system.id,
                        metric_key=key,
                        metric_value=value,
                        unit=METRIC_UNITS.get(key),
                        measured_at=measured_at,
                    )
                )
                if measured_at <= now:
                    _upsert_system_latest(db, ess_system.id, key, value, measured_at)

        for key, value in legacy_values.items():
            device_id = _metric_device_id(key, pcs, bms)
            db.add(
                TelemetryHistory(
                    device_id=device_id,
                    metric_key=key,
                    metric_value=value,
                    unit=METRIC_UNITS.get(key),
                    measured_at=measured_at,
                )
            )
            if measured_at <= now:
                _upsert_latest(db, device_id, key, value, measured_at)

        for index, inverter in enumerate(inverter_devices):
            if not inverter.is_active:
                continue
            inverter_power = round((solar_power / max(active_inverter_count, 1)) * random.uniform(0.94, 1.04), 1)
            db.add(
                TelemetryHistory(
                    device_id=inverter.id,
                    metric_key="inverter_power_kw",
                    metric_value=inverter_power,
                    unit="kW",
                    measured_at=measured_at,
                )
            )
            if measured_at <= now:
                _upsert_latest(db, inverter.id, "inverter_power_kw", inverter_power, measured_at)
            if index == 1 and hour == 11:
                inverter.status = "WARNING"

        rack_soc_offsets = [0.2, -0.8, -1.8, 0.2]
        rack_voltage_offsets = [-0.3, -1.3, -3.3, 0.7]
        rack_current_offsets = [0.3, 1.3, -0.7, 0.3]
        rack_temperature_offsets = [-0.8, -0.4, 2.9, -0.6]
        rack_temperature_spreads = [1.3, 1.8, 3.7, 1.8]
        rack_current = (ess_discharge - ess_charge) * 1.35 / max(len(battery_racks), 1)
        battery_voltage_value = float(system_values["battery_voltage_v"])

        for index, rack in enumerate(battery_racks):
            offset_index = index % len(rack_soc_offsets)
            average_temperature = round(battery_temperature + rack_temperature_offsets[offset_index], 1)
            rack_values = {
                "battery_rack_soc": round(min(100, max(0, soc + rack_soc_offsets[offset_index])), 1),
                "battery_rack_soh": [96.5, 96.4, 96.1, 96.6][offset_index],
                "battery_rack_voltage_v": round(battery_voltage_value + rack_voltage_offsets[offset_index], 1),
                "battery_rack_current_a": (
                    round(rack_current + rack_current_offsets[offset_index], 1) if rack_current != 0 else 0
                ),
                "battery_rack_avg_temperature_c": average_temperature,
                "battery_rack_max_temperature_c": round(
                    average_temperature + rack_temperature_spreads[offset_index],
                    1,
                ),
            }
            for key, value in rack_values.items():
                db.add(
                    TelemetryHistory(
                        device_id=rack.id,
                        metric_key=key,
                        metric_value=value,
                        unit=METRIC_UNITS.get(key),
                        measured_at=measured_at,
                    )
                )
                if measured_at <= now:
                    _upsert_latest(db, rack.id, key, value, measured_at)

        total_generation += solar_power
        total_charge += ess_charge
        total_discharge += ess_discharge
        total_grid_export += grid_export
        total_grid_import += grid_import

    db.add(
        DailyReport(
            report_date=today_start.strftime("%Y-%m-%d"),
            generation_kwh=round(total_generation, 1),
            ess_charge_kwh=round(total_charge, 1),
            ess_discharge_kwh=round(total_discharge, 1),
            grid_export_kwh=round(total_grid_export, 1),
            grid_import_kwh=round(total_grid_import, 1),
            alarm_count=3,
            maintenance_count=2,
        )
    )
    if ess_system is not None:
        db.add(
            EssDailyReport(
                ess_system_id=ess_system.id,
                report_date=today_start.strftime("%Y-%m-%d"),
                ess_charge_kwh=round(total_charge, 1),
                ess_discharge_kwh=round(total_discharge, 1),
                total_throughput_kwh=round(total_charge + total_discharge, 1),
                net_energy_kwh=round(total_charge - total_discharge, 1),
                avg_soc=round(sum(soc_samples) / len(soc_samples), 1) if soc_samples else 0,
                min_soc=round(min(soc_samples), 1) if soc_samples else 0,
                max_soc=round(max(soc_samples), 1) if soc_samples else 0,
                alarm_count=3,
            )
        )

    _generate_sample_alarms(db)
    _generate_sample_maintenance(db)
    db.commit()
    return {"generatedAt": now.strftime("%Y-%m-%d %H:%M:%S")}


def generate_last_7_days(db: Session) -> dict:
    result = generate_today(db)
    today = datetime.now().date()
    latest = db.query(DailyReport).filter(DailyReport.report_date == today.isoformat()).first()
    if latest is None:
        return result

    for offset in range(1, 7):
        report_date = (today - timedelta(days=offset)).isoformat()
        factor = 0.88 + (offset % 4) * 0.05
        db.execute(delete(DailyReport).where(DailyReport.report_date == report_date))
        db.execute(delete(EssDailyReport).where(EssDailyReport.report_date == report_date))
        db.add(
            DailyReport(
                report_date=report_date,
                generation_kwh=round(latest.generation_kwh * factor, 1),
                ess_charge_kwh=round(latest.ess_charge_kwh * factor, 1),
                ess_discharge_kwh=round(latest.ess_discharge_kwh * (1.04 - offset * 0.02), 1),
                grid_export_kwh=round(latest.grid_export_kwh * factor, 1),
                grid_import_kwh=round(latest.grid_import_kwh * (1.08 - offset * 0.02), 1),
                alarm_count=offset % 4,
                maintenance_count=1 if offset in (2, 5) else 0,
            )
        )
        for system in db.query(EssSystem).all():
            ess_charge = round(latest.ess_charge_kwh * factor, 1)
            ess_discharge = round(latest.ess_discharge_kwh * (1.04 - offset * 0.02), 1)
            db.add(
                EssDailyReport(
                    ess_system_id=system.id,
                    report_date=report_date,
                    ess_charge_kwh=ess_charge,
                    ess_discharge_kwh=ess_discharge,
                    total_throughput_kwh=round(ess_charge + ess_discharge, 1),
                    net_energy_kwh=round(ess_charge - ess_discharge, 1),
                    avg_soc=round(max(0, min(100, 72 + ((offset % 5) - 2) * 1.7)), 1),
                    min_soc=round(max(0, min(100, 64 + ((offset % 4) - 2) * 1.5)), 1),
                    max_soc=round(max(0, min(100, 82 + ((offset % 4) - 1) * 1.2)), 1),
                    alarm_count=offset % 4,
                )
            )
    db.commit()
    return {"generatedAt": result["generatedAt"], "dayCount": 7}


def generate_sample_alarms(db: Session) -> dict:
    _generate_sample_alarms(db)
    db.commit()
    return {"generatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "alarmCount": 3}


def generate_sample_maintenance(db: Session) -> dict:
    _generate_sample_maintenance(db)
    db.commit()
    return {"generatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "maintenanceCount": 2}


def _generate_sample_alarms(db: Session) -> None:
    db.query(MaintenanceRecord).filter(MaintenanceRecord.alarm_id.isnot(None)).update(
        {MaintenanceRecord.alarm_id: None},
        synchronize_session=False,
    )
    db.execute(delete(Alarm))
    now = datetime.now().replace(second=0, microsecond=0)
    devices = db.query(Device).all()
    inverter = next((item for item in devices if item.device_type == "INVERTER"), None)
    pcs = next((item for item in devices if item.device_type == "PCS"), None)
    bms = next((item for item in devices if item.device_type == "BMS"), None)
    db.add_all(
        [
            Alarm(
                device_id=inverter.id if inverter else None,
                severity="WARNING",
                alarm_type="발전량 저하",
                message="인버터 #2 출력이 기준값보다 낮습니다.",
                status="OPEN",
                occurred_at=now - timedelta(hours=2),
            ),
            Alarm(
                device_id=pcs.id if pcs else None,
                severity="INFO",
                alarm_type="PCS 상태",
                message="PCS가 충전 모드로 전환되었습니다.",
                status="ACKED",
                occurred_at=now - timedelta(hours=4),
                acknowledged_at=now - timedelta(hours=3, minutes=50),
            ),
            Alarm(
                device_id=bms.id if bms else None,
                severity="CRITICAL",
                alarm_type="BMS 경고",
                message="배터리 온도가 주의 기준에 접근했습니다.",
                status="OPEN",
                occurred_at=now - timedelta(minutes=45),
            ),
        ]
    )


def _generate_sample_maintenance(db: Session) -> None:
    db.execute(delete(MaintenanceRecord))
    today = datetime.now().date()
    inverter = db.query(Device).filter(Device.device_type == "INVERTER").first()
    bms = db.query(Device).filter(Device.device_type == "BMS").first()
    db.add_all(
        [
            MaintenanceRecord(
                device_id=inverter.id if inverter else None,
                maintenance_type="정기점검",
                title="인버터 정기 점검",
                description="인버터 통신 상태와 출력 로그 확인",
                action_taken="단자 체결 상태 확인 및 통신 로그 점검",
                status="COMPLETED",
                maintenance_date=(today - timedelta(days=3)).isoformat(),
                next_maintenance_date=(today + timedelta(days=27)).isoformat(),
                manager_name="EMS 관리자",
            ),
            MaintenanceRecord(
                device_id=bms.id if bms else None,
                maintenance_type="배터리점검",
                title="BMS 셀 밸런싱 점검",
                description="셀 전압 편차 추이 확인",
                status="SCHEDULED",
                maintenance_date=(today + timedelta(days=7)).isoformat(),
                manager_name="O&M 담당자",
            ),
        ]
    )
