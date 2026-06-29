from sqlalchemy import DateTime, Float, Integer, String, func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ...core.database import Base


class DailyReport(Base):
    __tablename__ = "daily_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    report_date: Mapped[str] = mapped_column(String(20), nullable=False)
    generation_kwh: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    ess_charge_kwh: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    ess_discharge_kwh: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    grid_export_kwh: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    grid_import_kwh: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    alarm_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    maintenance_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class EssDailyReport(Base):
    __tablename__ = "ess_daily_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ess_system_id: Mapped[int] = mapped_column(ForeignKey("ess_systems.id"), nullable=False)
    report_date: Mapped[str] = mapped_column(String(20), nullable=False)
    ess_charge_kwh: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    ess_discharge_kwh: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    total_throughput_kwh: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    net_energy_kwh: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    avg_soc: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    min_soc: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    max_soc: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    alarm_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
