from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .service import get_latest_telemetry, get_telemetry_history, get_telemetry_power_flow


router = APIRouter(prefix="/api/telemetry", tags=["telemetry"])


@router.get("/latest")
def latest(db: Session = Depends(get_db)):
    return ok(get_latest_telemetry(db))


@router.get("/history")
def history(metricKey: str = Query(default="solar_power_kw"), limit: int = Query(default=48), db: Session = Depends(get_db)):
    return ok(get_telemetry_history(db, metricKey, limit))


@router.get("/power-flow")
def telemetry_power_flow(db: Session = Depends(get_db)):
    return ok(get_telemetry_power_flow(db))
