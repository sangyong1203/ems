from pydantic import BaseModel

from ...shared.schemas import OrmModel


# 프로젝트 설정과 장비 수·용량 집계 응답
class ProjectConfigOut(OrmModel):
    id: int  # 프로젝트 설정 ID
    project_name: str  # 프로젝트명
    site_name: str  # 사업장명
    location: str | None  # 사업장 위치
    customer_name: str | None  # 고객명
    contractor_name: str | None  # 시공 또는 정비 업체명
    solar_capacity_kw: float  # 설정된 태양광 용량 (kW)
    ess_capacity_kwh: float  # 설정된 ESS 에너지 용량 (kWh)
    system_name: str  # 화면에 표시할 시스템명
    background_image_path: str | None  # 배경 이미지 경로
    logo_image_path: str | None  # 로고 이미지 경로
    data_refresh_interval: int  # 기본 데이터 갱신 주기 (밀리초)
    dashboard_refresh_interval: int  # 대시보드 갱신 주기 (밀리초)
    solar_refresh_interval: int  # 태양광 화면 갱신 주기 (밀리초)
    ess_refresh_interval: int  # ESS 화면 갱신 주기 (밀리초)
    power_flow_refresh_interval: int  # 전력 흐름 화면 갱신 주기 (밀리초)
    trend_refresh_interval: int  # 트렌드 화면 갱신 주기 (밀리초)
    device_counts: dict[str, int]  # 종류별 전체 장비 수
    active_device_counts: dict[str, int]  # 종류별 활성 장비 수
    equipment_capacities: dict[str, float]  # 태양광·ESS의 설치 및 운전 용량 집계


# 프로젝트 설정과 갱신 주기 수정 요청
class ProjectConfigSaveBody(BaseModel):
    project_name: str  # 프로젝트명
    site_name: str  # 사업장명
    location: str | None = None  # 사업장 위치
    customer_name: str | None = None  # 고객명
    contractor_name: str | None = None  # 시공 또는 정비 업체명
    solar_capacity_kw: float  # 설정된 태양광 용량 (kW)
    ess_capacity_kwh: float  # 설정된 ESS 에너지 용량 (kWh)
    system_name: str  # 화면에 표시할 시스템명
    background_image_path: str | None = None  # 배경 이미지 경로
    logo_image_path: str | None = None  # 로고 이미지 경로
    data_refresh_interval: int  # 기본 데이터 갱신 주기 (밀리초)
    dashboard_refresh_interval: int  # 대시보드 갱신 주기 (밀리초)
    solar_refresh_interval: int  # 태양광 화면 갱신 주기 (밀리초)
    ess_refresh_interval: int  # ESS 화면 갱신 주기 (밀리초)
    power_flow_refresh_interval: int  # 전력 흐름 화면 갱신 주기 (밀리초)
    trend_refresh_interval: int  # 트렌드 화면 갱신 주기 (밀리초)
