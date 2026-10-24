from sqlalchemy.orm import Session

from .generator import (
    generate_last_7_days,
    generate_sample_alarms,
    generate_sample_maintenance,
    generate_today,
    reset_operational_data,
)


# 계측과 오늘 리포트·샘플 알림 및 정비의 재생성을 위임합니다.
def generate_today_data(db: Session) -> dict:
    return generate_today(db)


# 오늘 데이터와 최근 7일 리포트의 재생성을 위임합니다.
def generate_last_7_days_data(db: Session) -> dict:
    return generate_last_7_days(db)


# 기존 알림을 샘플 알림으로 교체하는 작업을 위임합니다.
def generate_alarm_data(db: Session) -> dict:
    return generate_sample_alarms(db)


# 기존 정비 기록을 샘플 정비로 교체하는 작업을 위임합니다.
def generate_maintenance_data(db: Session) -> dict:
    return generate_sample_maintenance(db)


# 운전 데이터를 삭제하고 초기화 완료 결과를 반환합니다.
def reset_data(db: Session) -> dict:
    reset_operational_data(db)
    return {"reset": True}
