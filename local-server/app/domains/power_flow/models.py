from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from ...core.database import Base


class PowerFlowLayout(Base):
    __tablename__ = "power_flow_layouts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, default="기본 전력 흐름")
    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    canvas_width: Mapped[int] = mapped_column(Integer, nullable=False, default=1280)
    canvas_height: Mapped[int] = mapped_column(Integer, nullable=False, default=720)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class PowerFlowLayoutNode(Base):
    __tablename__ = "power_flow_layout_nodes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    layout_id: Mapped[int] = mapped_column(ForeignKey("power_flow_layouts.id"), nullable=False)
    client_id: Mapped[str] = mapped_column(String(80), nullable=False)
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"), nullable=False)
    x: Mapped[float] = mapped_column(Float, nullable=False)
    y: Mapped[float] = mapped_column(Float, nullable=False)
    width: Mapped[float] = mapped_column(Float, nullable=False, default=190)
    height: Mapped[float] = mapped_column(Float, nullable=False, default=104)


class PowerFlowJunction(Base):
    __tablename__ = "power_flow_junctions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    layout_id: Mapped[int] = mapped_column(ForeignKey("power_flow_layouts.id"), nullable=False)
    client_id: Mapped[str] = mapped_column(String(80), nullable=False)
    x: Mapped[float] = mapped_column(Float, nullable=False)
    y: Mapped[float] = mapped_column(Float, nullable=False)


class PowerFlowWire(Base):
    __tablename__ = "power_flow_wires"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    layout_id: Mapped[int] = mapped_column(ForeignKey("power_flow_layouts.id"), nullable=False)
    client_id: Mapped[str] = mapped_column(String(80), nullable=False)
    source_type: Mapped[str] = mapped_column(String(20), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(80), nullable=False)
    source_anchor: Mapped[str] = mapped_column(String(20), nullable=False, default="RIGHT")
    target_type: Mapped[str] = mapped_column(String(20), nullable=False)
    target_ref: Mapped[str] = mapped_column(String(80), nullable=False)
    target_anchor: Mapped[str] = mapped_column(String(20), nullable=False, default="LEFT")
    direction: Mapped[str] = mapped_column(String(20), nullable=False, default="FORWARD")
    metric_key: Mapped[str | None] = mapped_column(String(80))
    is_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    route_points_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
