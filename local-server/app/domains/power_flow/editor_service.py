from sqlalchemy.orm import Session

from .repository import get_editor_data, save_editor_data
from .schemas import PowerFlowLayoutSaveBody


def get_power_flow_editor_data(db: Session) -> dict:
    return get_editor_data(db)


def save_power_flow_editor_data(db: Session, body: PowerFlowLayoutSaveBody) -> dict:
    return save_editor_data(db, body.model_dump())
