# 모든 ORM 모델을 가져와 Base.metadata에 테이블을 등록합니다.
from ..core.database import Base
from ..domains.alarm.models import Alarm
from ..domains.auth.models import AuthSession, User
from ..domains.device.models import Device
from ..domains.ess.models import EssSystem, EssSystemBatteryRack
from ..domains.maintenance.models import MaintenancePart, MaintenanceRecord
from ..domains.power_flow.models import PowerFlowJunction, PowerFlowLayout, PowerFlowLayoutNode, PowerFlowWire
from ..domains.project.models import ProjectConfig
from ..domains.pv_string.models import InverterPvStringLink, PvString
from ..domains.report.models import DailyReport, EssDailyReport
from ..domains.telemetry.models import (
    EssSystemTelemetryHistory,
    EssSystemTelemetryLatest,
    SiteTelemetryHistory,
    SiteTelemetryLatest,
    TelemetryHistory,
    TelemetryLatest,
)

__all__ = [  # 모델 등록 모듈이 외부에 제공하는 이름 목록
    "Alarm",
    "AuthSession",
    "Base",
    "DailyReport",
    "Device",
    "EssDailyReport",
    "EssSystem",
    "EssSystemBatteryRack",
    "EssSystemTelemetryHistory",
    "EssSystemTelemetryLatest",
    "InverterPvStringLink",
    "MaintenancePart",
    "MaintenanceRecord",
    "PowerFlowJunction",
    "PowerFlowLayout",
    "PowerFlowLayoutNode",
    "PowerFlowWire",
    "ProjectConfig",
    "PvString",
    "SiteTelemetryHistory",
    "SiteTelemetryLatest",
    "TelemetryHistory",
    "TelemetryLatest",
    "User",
]
