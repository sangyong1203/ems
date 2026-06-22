from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .service import get_trend_overview


router = APIRouter(prefix="/api/trend", tags=["trend"])


@router.get("/overview")
def trend_overview(db: Session = Depends(get_db)):
    return ok(get_trend_overview(db))
