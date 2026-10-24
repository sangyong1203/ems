from ...shared.schemas import OrmModel


# 사업장 일일 리포트 응답
class DailyReportOut(OrmModel):
    id: int  # 사업장 일일 리포트 ID
    report_date: str  # 집계 기준일
    generation_kwh: float  # 일일 또는 조회 기간의 발전 에너지 (kWh)
    ess_charge_kwh: float  # ESS 충전 에너지 (kWh)
    ess_discharge_kwh: float  # ESS 방전 에너지 (kWh)
    grid_export_kwh: float  # 계통 송전 에너지 (kWh)
    grid_import_kwh: float  # 계통 수전 에너지 (kWh)
    alarm_count: int  # 알림 건수
    maintenance_count: int  # 정비 건수


# 조회 기간의 일일 리포트 합계 응답
class ReportSummaryOut(OrmModel):
    date_from: str  # 조회 시작일
    date_to: str  # 조회 종료일
    day_count: int  # 조회 기간에 포함된 리포트 수
    generation_kwh: float  # 일일 또는 조회 기간의 발전 에너지 (kWh)
    ess_charge_kwh: float  # ESS 충전 에너지 (kWh)
    ess_discharge_kwh: float  # ESS 방전 에너지 (kWh)
    grid_export_kwh: float  # 계통 송전 에너지 (kWh)
    grid_import_kwh: float  # 계통 수전 에너지 (kWh)
    alarm_count: int  # 알림 건수
    maintenance_count: int  # 정비 건수


# 리포트 통계의 일별 시계열 항목
class ReportStatisticsPointOut(OrmModel):
    date: str  # 일별 시계열 기준일
    generation_kwh: float  # 일일 또는 조회 기간의 발전 에너지 (kWh)
    temperature_c: float  # 최신 외기 온도에 가상 편차를 적용한 값 (℃)
    ess_charge_kwh: float  # ESS 충전 에너지 (kWh)
    ess_discharge_kwh: float  # ESS 방전 에너지 (kWh)
    ess_soc: float  # 최신 SOC에 가상 편차를 적용한 충전율 (%)
    grid_export_kwh: float  # 계통 송전 에너지 (kWh)
    grid_import_kwh: float  # 계통 수전 에너지 (kWh)
    load_total_kwh: float  # 에너지 수지로 계산한 총 부하 (kWh)
    load_solar_kwh: float  # 태양광으로 공급한 부하 에너지 (kWh)
    load_grid_kwh: float  # 계통으로 공급한 부하 에너지 (kWh)
    load_ess_kwh: float  # ESS로 공급한 부하 에너지 (kWh)
    self_reliance_rate: float  # 총 부하 중 태양광 공급량의 비율 (%)
    alarm_count: int  # 알림 건수


# 심각도별 알림 건수 응답
class AlarmSeverityDistributionOut(OrmModel):
    severity: str  # 알림 심각도
    count: int  # 분포 항목에 해당하는 알림 수


# 장비별 알림 건수 응답
class AlarmDeviceDistributionOut(OrmModel):
    device_name: str  # 연결 장비 이름
    count: int  # 분포 항목에 해당하는 알림 수


# 리포트 기간 합계·시계열·알림 분포 응답
class ReportStatisticsOut(OrmModel):
    summary: ReportSummaryOut  # 기간 합계
    series: list[ReportStatisticsPointOut]  # 일별 통계 시계열
    alarm_severity_distribution: list[AlarmSeverityDistributionOut]  # 심각도별 알림 분포
    alarm_by_device: list[AlarmDeviceDistributionOut]  # 장비별 알림 분포; 현재 통계 서비스는 빈 목록 반환
