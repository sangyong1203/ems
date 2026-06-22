from sqlalchemy import DateTime, Float, Integer, String, func
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
