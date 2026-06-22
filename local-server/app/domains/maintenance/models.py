from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from ...core.database import Base


class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    device_id: Mapped[int | None] = mapped_column(ForeignKey("devices.id"))
    alarm_id: Mapped[int | None] = mapped_column(ForeignKey("alarms.id"))
    maintenance_type: Mapped[str] = mapped_column(String(60), nullable=False)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    cause: Mapped[str | None] = mapped_column(Text)
    action_taken: Mapped[str | None] = mapped_column(Text)
    before_status: Mapped[str | None] = mapped_column(String(40))
    after_status: Mapped[str | None] = mapped_column(String(40))
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="SCHEDULED")
    maintenance_date: Mapped[str | None] = mapped_column(String(20))
    next_maintenance_date: Mapped[str | None] = mapped_column(String(20))
    manager_name: Mapped[str | None] = mapped_column(String(80))
    contractor_name: Mapped[str | None] = mapped_column(String(120))
    cost: Mapped[float] = mapped_column(Float, default=0)
    memo: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class MaintenancePart(Base):
    __tablename__ = "maintenance_parts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    maintenance_id: Mapped[int] = mapped_column(ForeignKey("maintenance_records.id"), nullable=False)
    part_name: Mapped[str] = mapped_column(String(120), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    unit_price: Mapped[float] = mapped_column(Float, default=0)
    memo: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
