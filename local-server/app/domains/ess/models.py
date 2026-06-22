from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ...core.database import Base


class EssSystem(Base):
    __tablename__ = "ess_systems"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    code: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    capacity_kwh: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    pcs_device_id: Mapped[int | None] = mapped_column(ForeignKey("devices.id"))
    bms_device_id: Mapped[int | None] = mapped_column(ForeignKey("devices.id"))
    battery_device_id: Mapped[int | None] = mapped_column(ForeignKey("devices.id"))
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="NORMAL")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    install_location: Mapped[str | None] = mapped_column(String(160))
    memo: Mapped[str | None] = mapped_column(Text)
