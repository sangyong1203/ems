from sqlalchemy.orm import Session

from .generator import (
    generate_last_7_days,
    generate_sample_alarms,
    generate_sample_maintenance,
    generate_today,
    reset_operational_data,
)


def generate_today_data(db: Session) -> dict:
    return generate_today(db)


def generate_last_7_days_data(db: Session) -> dict:
    return generate_last_7_days(db)


def generate_alarm_data(db: Session) -> dict:
    return generate_sample_alarms(db)


def generate_maintenance_data(db: Session) -> dict:
    return generate_sample_maintenance(db)


def reset_data(db: Session) -> dict:
    reset_operational_data(db)
    return {"reset": True}
