from sqlalchemy import DateTime, Float, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from ...core.database import Base


class ProjectConfig(Base):
    __tablename__ = "project_config"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_name: Mapped[str] = mapped_column(String(160), nullable=False)
    site_name: Mapped[str] = mapped_column(String(160), nullable=False)
    location: Mapped[str | None] = mapped_column(String(255))
    customer_name: Mapped[str | None] = mapped_column(String(160))
    contractor_name: Mapped[str | None] = mapped_column(String(160))
    solar_capacity_kw: Mapped[float] = mapped_column(Float, nullable=False)
    ess_capacity_kwh: Mapped[float] = mapped_column(Float, nullable=False)
    system_name: Mapped[str] = mapped_column(String(120), default="Solar ESS EMS")
    background_image_path: Mapped[str | None] = mapped_column(String(255))
    logo_image_path: Mapped[str | None] = mapped_column(String(255))
    data_refresh_interval: Mapped[int] = mapped_column(Integer, default=5000)
    dashboard_refresh_interval: Mapped[int] = mapped_column(Integer, default=5000)
    solar_refresh_interval: Mapped[int] = mapped_column(Integer, default=5000)
    ess_refresh_interval: Mapped[int] = mapped_column(Integer, default=5000)
    power_flow_refresh_interval: Mapped[int] = mapped_column(Integer, default=5000)
    trend_refresh_interval: Mapped[int] = mapped_column(Integer, default=5000)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
