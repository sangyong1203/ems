from sqlalchemy import DateTime, Float, Integer, String, func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ...core.database import Base


# 사업장 일별 에너지·알림·정비 집계
class DailyReport(Base):
    __tablename__ = "daily_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # 사업장 일일 리포트 ID
    report_date: Mapped[str] = mapped_column(String(20), nullable=False)  # 집계 기준일
    generation_kwh: Mapped[float] = mapped_column(Float, nullable=False, default=0)  # 일일 또는 조회 기간의 발전 에너지 (kWh)
    ess_charge_kwh: Mapped[float] = mapped_column(Float, nullable=False, default=0)  # ESS 충전 에너지 (kWh)
    ess_discharge_kwh: Mapped[float] = mapped_column(Float, nullable=False, default=0)  # ESS 방전 에너지 (kWh)
    grid_export_kwh: Mapped[float] = mapped_column(Float, nullable=False, default=0)  # 계통 송전 에너지 (kWh)
    grid_import_kwh: Mapped[float] = mapped_column(Float, nullable=False, default=0)  # 계통 수전 에너지 (kWh)
    alarm_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)  # 알림 건수
    maintenance_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)  # 정비 건수
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # 생성 시각


# ESS 시스템별 일일 에너지·SOC 집계
class EssDailyReport(Base):
    __tablename__ = "ess_daily_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # ESS 일일 리포트 ID
    ess_system_id: Mapped[int] = mapped_column(ForeignKey("ess_systems.id"), nullable=False)  # 연결 ESS 시스템 ID
    report_date: Mapped[str] = mapped_column(String(20), nullable=False)  # 집계 기준일
    ess_charge_kwh: Mapped[float] = mapped_column(Float, nullable=False, default=0)  # ESS 충전 에너지 (kWh)
    ess_discharge_kwh: Mapped[float] = mapped_column(Float, nullable=False, default=0)  # ESS 방전 에너지 (kWh)
    total_throughput_kwh: Mapped[float] = mapped_column(Float, nullable=False, default=0)  # 충전량과 방전량을 합한 총 처리 에너지 (kWh)
    net_energy_kwh: Mapped[float] = mapped_column(Float, nullable=False, default=0)  # 충전량에서 방전량을 뺀 순 에너지 (kWh)
    avg_soc: Mapped[float] = mapped_column(Float, nullable=False, default=0)  # 일일 평균 충전율 (%)
    min_soc: Mapped[float] = mapped_column(Float, nullable=False, default=0)  # 일일 최저 충전율 (%)
    max_soc: Mapped[float] = mapped_column(Float, nullable=False, default=0)  # 일일 최고 충전율 (%)
    alarm_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)  # 알림 건수
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # 생성 시각
