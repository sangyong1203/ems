from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from ...core.database import Base


class PvString(Base):
    __tablename__ = "pv_strings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    panel_count: Mapped[int | None] = mapped_column(Integer)
    panel_capacity_kw: Mapped[float | None] = mapped_column(Float)
    rated_capacity_kw: Mapped[float | None] = mapped_column(Float)
    install_location: Mapped[str | None] = mapped_column(String(160))
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="NORMAL")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    memo: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class InverterPvStringLink(Base):
    __tablename__ = "inverter_pv_string_links"
    __table_args__ = (UniqueConstraint("pv_string_id", name="uq_inverter_pv_string_links_pv_string_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    inverter_device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"), nullable=False)
    pv_string_id: Mapped[int] = mapped_column(ForeignKey("pv_strings.id"), nullable=False)
    mppt_no: Mapped[int | None] = mapped_column(Integer)
    channel_no: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
