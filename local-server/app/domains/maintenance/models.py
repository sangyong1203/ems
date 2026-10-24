from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from ...core.database import Base


# 장비 정비 기록과 조치 정보
class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # 정비 기록 ID
    device_id: Mapped[int | None] = mapped_column(ForeignKey("devices.id"))  # 연결 장비 ID; None이면 특정 장비를 지정하지 않음
    alarm_id: Mapped[int | None] = mapped_column(ForeignKey("alarms.id"))  # 연결 알림 ID; 연결이 없으면 None
    maintenance_type: Mapped[str] = mapped_column(String(60), nullable=False)  # 정비 유형
    title: Mapped[str] = mapped_column(String(180), nullable=False)  # 제목
    description: Mapped[str | None] = mapped_column(Text)  # 상세 설명
    cause: Mapped[str | None] = mapped_column(Text)  # 문제 원인
    action_taken: Mapped[str | None] = mapped_column(Text)  # 수행한 조치
    before_status: Mapped[str | None] = mapped_column(String(40))  # 정비 전 상태
    after_status: Mapped[str | None] = mapped_column(String(40))  # 정비 후 상태
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="SCHEDULED")  # 정비 처리 상태
    maintenance_date: Mapped[str | None] = mapped_column(String(20))  # 정비일
    next_maintenance_date: Mapped[str | None] = mapped_column(String(20))  # 다음 정비 예정일
    manager_name: Mapped[str | None] = mapped_column(String(80))  # 정비 담당자명
    contractor_name: Mapped[str | None] = mapped_column(String(120))  # 시공 또는 정비 업체명
    cost: Mapped[float] = mapped_column(Float, default=0)  # 정비 비용
    memo: Mapped[str | None] = mapped_column(Text)  # 추가 메모
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # 생성 시각
    updated_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )  # 마지막 수정 시각


# 정비 기록에 연결된 사용 부품
class MaintenancePart(Base):
    __tablename__ = "maintenance_parts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # 정비 부품 ID
    maintenance_id: Mapped[int] = mapped_column(ForeignKey("maintenance_records.id"), nullable=False)  # 연결 정비 기록 ID
    part_name: Mapped[str] = mapped_column(String(120), nullable=False)  # 사용 부품명
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)  # 사용 부품 수량
    unit_price: Mapped[float] = mapped_column(Float, default=0)  # 부품 단가
    memo: Mapped[str | None] = mapped_column(Text)  # 추가 메모
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # 생성 시각
