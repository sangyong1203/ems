from datetime import datetime

from ...shared.schemas import OrmModel


# 알림 상세와 선택적인 장비·정비 연결 응답
class AlarmOut(OrmModel):
    id: int  # 알림 ID
    device_id: int | None  # 연결 장비 ID; None이면 특정 장비를 지정하지 않음
    severity: str  # 알림 심각도
    alarm_type: str  # 알림 유형
    message: str  # 알림 메시지
    status: str  # 알림 처리 상태 (OPEN / ACKED / RESOLVED)
    occurred_at: datetime  # 알림 발생 시각
    acknowledged_at: datetime | None  # 알림 확인 시각; 미확인 시 None
    resolved_at: datetime | None  # 알림 해결 시각; 미해결 시 None
    device_name: str | None = None  # 연결 장비 이름
    device_type: str | None = None  # 장비 종류
    maintenance_id: int | None = None  # 연결 정비 기록 ID
    maintenance_status: str | None = None  # 연결 정비의 처리 상태
    maintenance_title: str | None = None  # 연결 정비의 제목
    maintenance_date: str | None = None  # 정비일
