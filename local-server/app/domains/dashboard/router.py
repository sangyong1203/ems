from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .service import (
    get_dashboard_summary,
    get_power_flow,
    get_recent_alarm_ids,
    get_recent_maintenance_ids,
)


router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    return ok(get_dashboard_summary(db))


@router.get("/power-flow")
def power_flow(db: Session = Depends(get_db)):
    return ok(get_power_flow(db))


@router.get("/recent-alarms")
def dashboard_recent_alarms(db: Session = Depends(get_db)):
    return ok(get_recent_alarm_ids(db))


@router.get("/recent-maintenance")
def dashboard_recent_maintenance(db: Session = Depends(get_db)):
    return ok(get_recent_maintenance_ids(db))
