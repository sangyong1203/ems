from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from ...core.database import Base


class TelemetryLatest(Base):
    __tablename__ = "telemetry_latest"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    device_id: Mapped[int | None] = mapped_column(ForeignKey("devices.id"))
    metric_key: Mapped[str] = mapped_column(String(80), nullable=False)
    metric_value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str | None] = mapped_column(String(20))
    measured_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class TelemetryHistory(Base):
    __tablename__ = "telemetry_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    device_id: Mapped[int | None] = mapped_column(ForeignKey("devices.id"))
    metric_key: Mapped[str] = mapped_column(String(80), nullable=False)
    metric_value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str | None] = mapped_column(String(20))
    measured_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class SiteTelemetryLatest(Base):
    __tablename__ = "site_telemetry_latest"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    metric_key: Mapped[str] = mapped_column(String(80), nullable=False)
    metric_value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str | None] = mapped_column(String(20))
    measured_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class SiteTelemetryHistory(Base):
    __tablename__ = "site_telemetry_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    metric_key: Mapped[str] = mapped_column(String(80), nullable=False)
    metric_value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str | None] = mapped_column(String(20))
    measured_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class EssSystemTelemetryLatest(Base):
    __tablename__ = "ess_system_telemetry_latest"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ess_system_id: Mapped[int] = mapped_column(ForeignKey("ess_systems.id"), nullable=False)
    metric_key: Mapped[str] = mapped_column(String(80), nullable=False)
    metric_value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str | None] = mapped_column(String(20))
    measured_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class EssSystemTelemetryHistory(Base):
    __tablename__ = "ess_system_telemetry_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ess_system_id: Mapped[int] = mapped_column(ForeignKey("ess_systems.id"), nullable=False)
    metric_key: Mapped[str] = mapped_column(String(80), nullable=False)
    metric_value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str | None] = mapped_column(String(20))
    measured_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
