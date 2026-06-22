from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .service import get_power_flow_overview


router = APIRouter(prefix="/api/power-flow", tags=["power-flow"])


@router.get("/overview")
def power_flow_overview(db: Session = Depends(get_db)):
    return ok(get_power_flow_overview(db))
