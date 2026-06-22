from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .service import get_ess_overview, get_ess_system_overview, get_ess_systems


router = APIRouter(prefix="/api/ess", tags=["ess"])


@router.get("/overview")
def ess_overview(db: Session = Depends(get_db)):
    return ok(get_ess_overview(db))


@router.get("/systems")
def ess_systems(db: Session = Depends(get_db)):
    return ok(get_ess_systems(db))


@router.get("/systems/{system_id}/overview")
def ess_system_overview(system_id: int, db: Session = Depends(get_db)):
    return ok(get_ess_system_overview(db, system_id))
