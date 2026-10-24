from pydantic import BaseModel

from ...shared.schemas import OrmModel


# 인버터와 스트링의 연결 응답
class PvStringLinkOut(OrmModel):
    id: int  # 인버터와 스트링의 연결 ID
    inverter_device_id: int  # 연결 인버터 장비 ID
    pv_string_id: int  # 연결 스트링 ID
    mppt_no: int | None  # 인버터 MPPT 번호
    channel_no: int | None  # MPPT 내 연결 채널 번호
    pv_string_name: str | None = None  # 연결 스트링 이름
    inverter_name: str | None = None  # 연결 인버터 이름


# 장비 저장 시 전달할 스트링 연결 요청
class PvStringLinkSaveBody(BaseModel):
    pv_string_id: int  # 연결 스트링 ID
    mppt_no: int | None = None  # 인버터 MPPT 번호
    channel_no: int | None = None  # MPPT 내 연결 채널 번호


# 스트링 정보와 선택적인 인버터 연결 응답
class PvStringOut(OrmModel):
    id: int  # 스트링 ID
    name: str  # 표시 이름
    panel_count: int | None  # 스트링에 구성된 모듈 수
    panel_capacity_kw: float | None  # 모듈 한 장의 정격 용량 (kW)
    rated_capacity_kw: float | None  # 스트링 정격 용량 (kW)
    install_location: str | None  # 설치 위치
    status: str  # 장비 또는 설비 운전 상태
    is_active: bool  # 장비 또는 설비의 활성 여부
    memo: str | None  # 추가 메모
    inverter_device_id: int | None = None  # 연결 인버터 장비 ID
    inverter_name: str | None = None  # 연결 인버터 이름
    mppt_no: int | None = None  # 인버터 MPPT 번호
    channel_no: int | None = None  # MPPT 내 연결 채널 번호


# 스트링 등록·수정 요청
class PvStringSaveBody(BaseModel):
    name: str  # 표시 이름
    panel_count: int | None = None  # 스트링에 구성된 모듈 수
    panel_capacity_kw: float | None = None  # 모듈 한 장의 정격 용량 (kW)
    rated_capacity_kw: float | None = None  # 스트링 정격 용량 (kW)
    install_location: str | None = None  # 설치 위치
    status: str = "NORMAL"  # 장비 또는 설비 운전 상태
    is_active: bool = True  # 장비 또는 설비의 활성 여부
    memo: str | None = None  # 추가 메모
