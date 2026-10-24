from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from ...core.database import Base


# 장비 알림과 확인·해결 이력
class Alarm(Base):
    __tablename__ = "alarms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # 알림 ID
    device_id: Mapped[int | None] = mapped_column(ForeignKey("devices.id"))  # 연결 장비 ID; None이면 특정 장비를 지정하지 않음
    severity: Mapped[str] = mapped_column(String(40), nullable=False)  # 알림 심각도
    alarm_type: Mapped[str] = mapped_column(String(80), nullable=False)  # 알림 유형
    message: Mapped[str] = mapped_column(String(255), nullable=False)  # 알림 메시지
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="OPEN")  # 알림 처리 상태 (OPEN / ACKED / RESOLVED)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # 알림 발생 시각
    acknowledged_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))  # 알림 확인 시각; 미확인 시 None
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))  # 알림 해결 시각; 미해결 시 None
