from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .service import (
    generate_alarm_data,
    generate_last_7_days_data,
    generate_maintenance_data,
    generate_today_data,
    reset_data,
)


router = APIRouter(prefix="/api/simulator", tags=["simulator"])


@router.post("/generate-today")
def generate_today(db: Session = Depends(get_db)):
    return ok(generate_today_data(db))


@router.post("/generate-last-7-days")
def generate_last_7_days(db: Session = Depends(get_db)):
    return ok(generate_last_7_days_data(db))


@router.post("/generate-alarms")
def generate_alarms(db: Session = Depends(get_db)):
    return ok(generate_alarm_data(db))


@router.post("/generate-maintenance")
def generate_maintenance(db: Session = Depends(get_db)):
    return ok(generate_maintenance_data(db))


@router.post("/reset")
def reset(db: Session = Depends(get_db)):
    return ok(reset_data(db))
