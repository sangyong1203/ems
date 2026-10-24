from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from ...core.database import Base


# 전력 흐름 기본 배치와 캔버스 크기
class PowerFlowLayout(Base):
    __tablename__ = "power_flow_layouts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # 전력 흐름 배치 ID
    name: Mapped[str] = mapped_column(String(120), nullable=False, default="기본 전력 흐름")  # 표시 이름
    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)  # 기본 배치 여부
    canvas_width: Mapped[int] = mapped_column(Integer, nullable=False, default=1280)  # 캔버스 너비 (px)
    canvas_height: Mapped[int] = mapped_column(Integer, nullable=False, default=720)  # 캔버스 높이 (px)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # 생성 시각
    updated_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )  # 마지막 수정 시각


# 장비에 연결된 전력 흐름 배치 노드
class PowerFlowLayoutNode(Base):
    __tablename__ = "power_flow_layout_nodes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # 장비 배치 노드 ID
    layout_id: Mapped[int] = mapped_column(ForeignKey("power_flow_layouts.id"), nullable=False)  # 소속 전력 흐름 배치 ID
    client_id: Mapped[str] = mapped_column(String(80), nullable=False)  # 클라이언트에서 배치 요소를 구분하는 ID
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"), nullable=False)  # 연결 장비 ID
    x: Mapped[float] = mapped_column(Float, nullable=False)  # 캔버스 기준 가로 좌표 (px)
    y: Mapped[float] = mapped_column(Float, nullable=False)  # 캔버스 기준 세로 좌표 (px)
    width: Mapped[float] = mapped_column(Float, nullable=False, default=190)  # 노드 너비 (px)
    height: Mapped[float] = mapped_column(Float, nullable=False, default=104)  # 노드 높이 (px)


# 전력 흐름 배선의 분기점
class PowerFlowJunction(Base):
    __tablename__ = "power_flow_junctions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # 배선 분기점 ID
    layout_id: Mapped[int] = mapped_column(ForeignKey("power_flow_layouts.id"), nullable=False)  # 소속 전력 흐름 배치 ID
    client_id: Mapped[str] = mapped_column(String(80), nullable=False)  # 클라이언트에서 배치 요소를 구분하는 ID
    x: Mapped[float] = mapped_column(Float, nullable=False)  # 캔버스 기준 가로 좌표 (px)
    y: Mapped[float] = mapped_column(Float, nullable=False)  # 캔버스 기준 세로 좌표 (px)


# 노드·분기점 사이 배선과 경유 좌표
class PowerFlowWire(Base):
    __tablename__ = "power_flow_wires"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # 배선 ID
    layout_id: Mapped[int] = mapped_column(ForeignKey("power_flow_layouts.id"), nullable=False)  # 소속 전력 흐름 배치 ID
    client_id: Mapped[str] = mapped_column(String(80), nullable=False)  # 클라이언트에서 배치 요소를 구분하는 ID
    source_type: Mapped[str] = mapped_column(String(20), nullable=False)  # 출발 요소 종류 (NODE 또는 JUNCTION)
    source_ref: Mapped[str] = mapped_column(String(80), nullable=False)  # 출발 요소의 client_id
    source_anchor: Mapped[str] = mapped_column(String(20), nullable=False, default="RIGHT")  # 출발 요소의 연결 위치
    target_type: Mapped[str] = mapped_column(String(20), nullable=False)  # 도착 요소 종류 (NODE 또는 JUNCTION)
    target_ref: Mapped[str] = mapped_column(String(80), nullable=False)  # 도착 요소의 client_id
    target_anchor: Mapped[str] = mapped_column(String(20), nullable=False, default="LEFT")  # 도착 요소의 연결 위치
    direction: Mapped[str] = mapped_column(String(20), nullable=False, default="FORWARD")  # 배선의 흐름 방향
    metric_key: Mapped[str | None] = mapped_column(String(80))  # 계측 지표 키
    is_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)  # 배선 활성 여부
    route_points_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")  # 배선 경유 좌표 목록을 직렬화한 JSON
