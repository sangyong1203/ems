from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from ...core.database import Base


# 장비 또는 장비 미지정 지표의 최신 계측값
class TelemetryLatest(Base):
    __tablename__ = "telemetry_latest"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # 최신 계측 ID
    device_id: Mapped[int | None] = mapped_column(ForeignKey("devices.id"))  # 연결 장비 ID; None이면 특정 장비를 지정하지 않음
    metric_key: Mapped[str] = mapped_column(String(80), nullable=False)  # 계측 지표 키
    metric_value: Mapped[float] = mapped_column(Float, nullable=False)  # 계측값; 단위는 unit 기준
    unit: Mapped[str | None] = mapped_column(String(20))  # 계측 단위
    measured_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # 계측 시각


# 장비 또는 장비 미지정 지표의 시계열 이력
class TelemetryHistory(Base):
    __tablename__ = "telemetry_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # 계측 이력 ID
    device_id: Mapped[int | None] = mapped_column(ForeignKey("devices.id"))  # 연결 장비 ID; None이면 특정 장비를 지정하지 않음
    metric_key: Mapped[str] = mapped_column(String(80), nullable=False)  # 계측 지표 키
    metric_value: Mapped[float] = mapped_column(Float, nullable=False)  # 계측값; 단위는 unit 기준
    unit: Mapped[str | None] = mapped_column(String(20))  # 계측 단위
    measured_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # 계측 시각


# 사업장 단위 최신 계측값
class SiteTelemetryLatest(Base):
    __tablename__ = "site_telemetry_latest"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # 사업장 최신 계측 ID
    metric_key: Mapped[str] = mapped_column(String(80), nullable=False)  # 계측 지표 키
    metric_value: Mapped[float] = mapped_column(Float, nullable=False)  # 계측값; 단위는 unit 기준
    unit: Mapped[str | None] = mapped_column(String(20))  # 계측 단위
    measured_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # 계측 시각


# 사업장 단위 계측 이력
class SiteTelemetryHistory(Base):
    __tablename__ = "site_telemetry_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # 사업장 계측 이력 ID
    metric_key: Mapped[str] = mapped_column(String(80), nullable=False)  # 계측 지표 키
    metric_value: Mapped[float] = mapped_column(Float, nullable=False)  # 계측값; 단위는 unit 기준
    unit: Mapped[str | None] = mapped_column(String(20))  # 계측 단위
    measured_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # 계측 시각


# ESS 시스템별 최신 계측값
class EssSystemTelemetryLatest(Base):
    __tablename__ = "ess_system_telemetry_latest"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # ESS 최신 계측 ID
    ess_system_id: Mapped[int] = mapped_column(ForeignKey("ess_systems.id"), nullable=False)  # 연결 ESS 시스템 ID
    metric_key: Mapped[str] = mapped_column(String(80), nullable=False)  # 계측 지표 키
    metric_value: Mapped[float] = mapped_column(Float, nullable=False)  # 계측값; 단위는 unit 기준
    unit: Mapped[str | None] = mapped_column(String(20))  # 계측 단위
    measured_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # 계측 시각


# ESS 시스템별 계측 이력
class EssSystemTelemetryHistory(Base):
    __tablename__ = "ess_system_telemetry_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # ESS 계측 이력 ID
    ess_system_id: Mapped[int] = mapped_column(ForeignKey("ess_systems.id"), nullable=False)  # 연결 ESS 시스템 ID
    metric_key: Mapped[str] = mapped_column(String(80), nullable=False)  # 계측 지표 키
    metric_value: Mapped[float] = mapped_column(Float, nullable=False)  # 계측값; 단위는 unit 기준
    unit: Mapped[str | None] = mapped_column(String(20))  # 계측 단위
    measured_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # 계측 시각
