from sqlalchemy.orm import Session

from .repository import get_editor_data, save_editor_data
from .schemas import PowerFlowLayoutSaveBody


# 기본 전력 흐름 배치와 편집 화면에 필요한 장비·계측 정보를 반환합니다.
def get_power_flow_editor_data(db: Session) -> dict:
    return get_editor_data(db)


# 저장 본문을 중첩 사전으로 변환하여 배치를 전체 교체합니다.
def save_power_flow_editor_data(db: Session, body: PowerFlowLayoutSaveBody) -> dict:
    return save_editor_data(db, body.model_dump())
