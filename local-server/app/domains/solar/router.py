from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .service import get_solar_overview


router = APIRouter(prefix="/api/solar", tags=["solar"])


@router.get("/overview")
def solar_overview(db: Session = Depends(get_db)):
    return ok(get_solar_overview(db))
