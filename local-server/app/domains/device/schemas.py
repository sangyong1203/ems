from pydantic import BaseModel, ConfigDict, Field

from ...shared.schemas import OrmModel
from ..pv_string.schemas import PvStringLinkOut, PvStringLinkSaveBody


# 장비 상세와 인버터 스트링 연결 응답
class DeviceOut(OrmModel):
    id: int  # 장비 ID
    device_type: str  # 장비 종류
    name: str  # 표시 이름
    manufacturer: str | None  # 제조사
    model_name: str | None  # 장비 모델명
    serial_number: str | None  # 장비 일련번호
    capacity: float | None  # 정격 용량; 단위는 capacity_unit 기준
    capacity_unit: str | None  # 정격 용량의 단위
    install_location: str | None  # 설치 위치
    install_date: str | None  # 설치일
    communication_type: str | None  # 통신 방식
    ip_address: str | None  # 장비 통신 IP 주소
    port: int | None  # 장비 통신 포트
    slave_id: int | None  # 통신 대상 슬레이브 ID
    protocol: str | None  # 통신 프로토콜
    status: str  # 장비 또는 설비 운전 상태
    is_active: bool  # 장비 또는 설비의 활성 여부
    warranty_start_date: str | None  # 보증 시작일
    warranty_end_date: str | None  # 보증 종료일
    vendor_name: str | None  # 공급 업체명
    vendor_contact: str | None  # 공급 업체 연락처
    memo: str | None  # 추가 메모
    image_path: str | None  # 장비 이미지 경로
    pv_string_links: list[PvStringLinkOut] = Field(default_factory=list)  # 인버터의 스트링 연결 목록


# 장비 등록·수정 및 스트링 연결 교체 요청
class DeviceSaveBody(BaseModel):
    model_config = ConfigDict(protected_namespaces=())  # model_ 접두사 필드 사용 허용

    device_type: str  # 장비 종류
    name: str  # 표시 이름
    manufacturer: str | None = None  # 제조사
    model_name: str | None = None  # 장비 모델명
    serial_number: str | None = None  # 장비 일련번호
    capacity: float | None = None  # 정격 용량; 단위는 capacity_unit 기준
    capacity_unit: str | None = None  # 정격 용량의 단위
    install_location: str | None = None  # 설치 위치
    install_date: str | None = None  # 설치일
    communication_type: str | None = None  # 통신 방식
    ip_address: str | None = None  # 장비 통신 IP 주소
    port: int | None = None  # 장비 통신 포트
    slave_id: int | None = None  # 통신 대상 슬레이브 ID
    protocol: str | None = None  # 통신 프로토콜
    status: str = "NORMAL"  # 장비 또는 설비 운전 상태
    is_active: bool = True  # 장비 또는 설비의 활성 여부
    warranty_start_date: str | None = None  # 보증 시작일
    warranty_end_date: str | None = None  # 보증 종료일
    vendor_name: str | None = None  # 공급 업체명
    vendor_contact: str | None = None  # 공급 업체 연락처
    memo: str | None = None  # 추가 메모
    image_path: str | None = None  # 장비 이미지 경로
    pv_string_links: list[PvStringLinkSaveBody] = Field(default_factory=list)  # 인버터의 스트링 연결 목록
