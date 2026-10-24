from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from ...core.database import Base


# 태양광 스트링 구성과 정격 용량
class PvString(Base):
    __tablename__ = "pv_strings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # 스트링 ID
    name: Mapped[str] = mapped_column(String(120), nullable=False)  # 표시 이름
    panel_count: Mapped[int | None] = mapped_column(Integer)  # 스트링에 구성된 모듈 수
    panel_capacity_kw: Mapped[float | None] = mapped_column(Float)  # 모듈 한 장의 정격 용량 (kW)
    rated_capacity_kw: Mapped[float | None] = mapped_column(Float)  # 스트링 정격 용량 (kW)
    install_location: Mapped[str | None] = mapped_column(String(160))  # 설치 위치
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="NORMAL")  # 장비 또는 설비 운전 상태
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)  # 장비 또는 설비의 활성 여부
    memo: Mapped[str | None] = mapped_column(Text)  # 추가 메모
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # 생성 시각
    updated_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )  # 마지막 수정 시각


# 스트링당 하나의 인버터에 연결하는 MPPT·채널 정보
class InverterPvStringLink(Base):
    __tablename__ = "inverter_pv_string_links"
    __table_args__ = (UniqueConstraint("pv_string_id", name="uq_inverter_pv_string_links_pv_string_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # 인버터와 스트링의 연결 ID
    inverter_device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"), nullable=False)  # 연결 인버터 장비 ID
    pv_string_id: Mapped[int] = mapped_column(ForeignKey("pv_strings.id"), nullable=False)  # 연결 스트링 ID
    mppt_no: Mapped[int | None] = mapped_column(Integer)  # 인버터 MPPT 번호
    channel_no: Mapped[int | None] = mapped_column(Integer)  # MPPT 내 연결 채널 번호
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # 생성 시각
