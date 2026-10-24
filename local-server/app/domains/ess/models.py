from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ...core.database import Base


# PCS·BMS·배터리로 구성한 ESS 시스템
class EssSystem(Base):
    __tablename__ = "ess_systems"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # ESS 시스템 ID
    name: Mapped[str] = mapped_column(String(120), nullable=False)  # 표시 이름
    code: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)  # ESS 시스템 식별 코드
    capacity_kwh: Mapped[float] = mapped_column(Float, nullable=False, default=0)  # ESS 정격 에너지 용량 (kWh)
    pcs_device_id: Mapped[int | None] = mapped_column(ForeignKey("devices.id"))  # 연결 PCS 장비 ID
    bms_device_id: Mapped[int | None] = mapped_column(ForeignKey("devices.id"))  # 연결 BMS 장비 ID
    battery_device_id: Mapped[int | None] = mapped_column(ForeignKey("devices.id"))  # 연결 배터리 뱅크 장비 ID
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="NORMAL")  # 장비 또는 설비 운전 상태
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)  # 장비 또는 설비의 활성 여부
    install_location: Mapped[str | None] = mapped_column(String(160))  # 설치 위치
    memo: Mapped[str | None] = mapped_column(Text)  # 추가 메모


# ESS 시스템과 배터리 랙의 연결 및 표시 순서
class EssSystemBatteryRack(Base):
    __tablename__ = "ess_system_battery_racks"
    __table_args__ = (
        UniqueConstraint("ess_system_id", "rack_device_id", name="uq_ess_system_battery_rack_device"),
        UniqueConstraint("ess_system_id", "rack_no", name="uq_ess_system_battery_rack_no"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # ESS와 랙의 연결 ID
    ess_system_id: Mapped[int] = mapped_column(ForeignKey("ess_systems.id"), nullable=False)  # 연결 ESS 시스템 ID
    rack_device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"), nullable=False)  # 배터리 랙 장비 ID
    rack_no: Mapped[int] = mapped_column(Integer, nullable=False)  # ESS 시스템 내 랙 번호
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)  # 랙 표시 순서
