from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from ...core.database import Base


# 설비 장비와 통신·설치 정보
class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # 장비 ID
    device_type: Mapped[str] = mapped_column(String(40), nullable=False)  # 장비 종류
    name: Mapped[str] = mapped_column(String(120), nullable=False)  # 표시 이름
    manufacturer: Mapped[str | None] = mapped_column(String(120))  # 제조사
    model_name: Mapped[str | None] = mapped_column(String(120))  # 장비 모델명
    serial_number: Mapped[str | None] = mapped_column(String(120))  # 장비 일련번호
    capacity: Mapped[float | None] = mapped_column(Float)  # 정격 용량; 단위는 capacity_unit 기준
    capacity_unit: Mapped[str | None] = mapped_column(String(20))  # 정격 용량의 단위
    install_location: Mapped[str | None] = mapped_column(String(160))  # 설치 위치
    install_date: Mapped[str | None] = mapped_column(String(20))  # 설치일
    communication_type: Mapped[str | None] = mapped_column(String(40))  # 통신 방식
    ip_address: Mapped[str | None] = mapped_column(String(80))  # 장비 통신 IP 주소
    port: Mapped[int | None] = mapped_column(Integer)  # 장비 통신 포트
    slave_id: Mapped[int | None] = mapped_column(Integer)  # 통신 대상 슬레이브 ID
    protocol: Mapped[str | None] = mapped_column(String(40))  # 통신 프로토콜
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="NORMAL")  # 장비 또는 설비 운전 상태
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)  # 장비 또는 설비의 활성 여부
    warranty_start_date: Mapped[str | None] = mapped_column(String(20))  # 보증 시작일
    warranty_end_date: Mapped[str | None] = mapped_column(String(20))  # 보증 종료일
    vendor_name: Mapped[str | None] = mapped_column(String(120))  # 공급 업체명
    vendor_contact: Mapped[str | None] = mapped_column(String(120))  # 공급 업체 연락처
    memo: Mapped[str | None] = mapped_column(Text)  # 추가 메모
    image_path: Mapped[str | None] = mapped_column(String(255))  # 장비 이미지 경로
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # 생성 시각
    updated_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )  # 마지막 수정 시각
