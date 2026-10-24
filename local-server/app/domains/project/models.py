from sqlalchemy import DateTime, Float, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from ...core.database import Base


# 프로젝트 정보와 화면별 갱신 주기
class ProjectConfig(Base):
    __tablename__ = "project_config"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # 프로젝트 설정 ID
    project_name: Mapped[str] = mapped_column(String(160), nullable=False)  # 프로젝트명
    site_name: Mapped[str] = mapped_column(String(160), nullable=False)  # 사업장명
    location: Mapped[str | None] = mapped_column(String(255))  # 사업장 위치
    customer_name: Mapped[str | None] = mapped_column(String(160))  # 고객명
    contractor_name: Mapped[str | None] = mapped_column(String(160))  # 시공 또는 정비 업체명
    solar_capacity_kw: Mapped[float] = mapped_column(Float, nullable=False)  # 설정된 태양광 용량 (kW)
    ess_capacity_kwh: Mapped[float] = mapped_column(Float, nullable=False)  # 설정된 ESS 에너지 용량 (kWh)
    system_name: Mapped[str] = mapped_column(String(120), default="Solar ESS EMS")  # 화면에 표시할 시스템명
    background_image_path: Mapped[str | None] = mapped_column(String(255))  # 배경 이미지 경로
    logo_image_path: Mapped[str | None] = mapped_column(String(255))  # 로고 이미지 경로
    data_refresh_interval: Mapped[int] = mapped_column(Integer, default=5000)  # 기본 데이터 갱신 주기 (밀리초)
    dashboard_refresh_interval: Mapped[int] = mapped_column(Integer, default=5000)  # 대시보드 갱신 주기 (밀리초)
    solar_refresh_interval: Mapped[int] = mapped_column(Integer, default=5000)  # 태양광 화면 갱신 주기 (밀리초)
    ess_refresh_interval: Mapped[int] = mapped_column(Integer, default=5000)  # ESS 화면 갱신 주기 (밀리초)
    power_flow_refresh_interval: Mapped[int] = mapped_column(Integer, default=5000)  # 전력 흐름 화면 갱신 주기 (밀리초)
    trend_refresh_interval: Mapped[int] = mapped_column(Integer, default=5000)  # 트렌드 화면 갱신 주기 (밀리초)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # 생성 시각
    updated_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )  # 마지막 수정 시각
