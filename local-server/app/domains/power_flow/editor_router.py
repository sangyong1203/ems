from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .schemas import PowerFlowLayoutSaveBody
from .editor_service import get_power_flow_editor_data, save_power_flow_editor_data


router = APIRouter(prefix="/api/power-flow/editor", tags=["power-flow-editor"])


@router.get("")
def editor_data(db: Session = Depends(get_db)):
    return ok(get_power_flow_editor_data(db))


@router.put("")
def save_editor(body: PowerFlowLayoutSaveBody, db: Session = Depends(get_db)):
    return ok(save_power_flow_editor_data(db, body))
