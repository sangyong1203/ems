from pydantic import BaseModel

from ...shared.schemas import OrmModel


# 정비 상세와 선택적인 연결 장비 응답
class MaintenanceOut(OrmModel):
    id: int  # 정비 기록 ID
    device_id: int | None  # 연결 장비 ID; None이면 특정 장비를 지정하지 않음
    alarm_id: int | None  # 연결 알림 ID; 연결이 없으면 None
    maintenance_type: str  # 정비 유형
    title: str  # 제목
    description: str | None  # 상세 설명
    action_taken: str | None  # 수행한 조치
    status: str  # 정비 처리 상태
    maintenance_date: str | None  # 정비일
    next_maintenance_date: str | None  # 다음 정비 예정일
    manager_name: str | None  # 정비 담당자명
    cause: str | None = None  # 문제 원인
    before_status: str | None = None  # 정비 전 상태
    after_status: str | None = None  # 정비 후 상태
    contractor_name: str | None = None  # 시공 또는 정비 업체명
    cost: float | None = None  # 정비 비용
    memo: str | None = None  # 추가 메모
    device_name: str | None = None  # 연결 장비 이름
    device_type: str | None = None  # 장비 종류


# 정비 등록·수정 요청
class MaintenanceSaveBody(BaseModel):
    device_id: int | None = None  # 연결 장비 ID; None이면 특정 장비를 지정하지 않음
    alarm_id: int | None = None  # 연결 알림 ID; 연결이 없으면 None
    maintenance_type: str  # 정비 유형
    title: str  # 제목
    description: str | None = None  # 상세 설명
    cause: str | None = None  # 문제 원인
    action_taken: str | None = None  # 수행한 조치
    before_status: str | None = None  # 정비 전 상태
    after_status: str | None = None  # 정비 후 상태
    status: str = "SCHEDULED"  # 정비 처리 상태
    maintenance_date: str | None = None  # 정비일
    next_maintenance_date: str | None = None  # 다음 정비 예정일
    manager_name: str | None = None  # 정비 담당자명
    contractor_name: str | None = None  # 시공 또는 정비 업체명
    cost: float | None = None  # 정비 비용
    memo: str | None = None  # 추가 메모
