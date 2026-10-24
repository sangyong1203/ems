from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .schemas import PowerFlowLayoutSaveBody
from .editor_service import get_power_flow_editor_data, save_power_flow_editor_data


router = APIRouter(prefix="/api/power-flow/editor", tags=["power-flow-editor"])  # 이 도메인의 API 경로와 문서 태그


# 배치와 장비·계측 정보를 포함한 편집 데이터를 반환합니다.
@router.get("")
def editor_data(db: Session = Depends(get_db)):
    return ok(get_power_flow_editor_data(db))


# 편집 배치 저장 본문을 전달하고 저장 후 편집 데이터를 반환합니다.
@router.put("")
def save_editor(body: PowerFlowLayoutSaveBody, db: Session = Depends(get_db)):
    return ok(save_power_flow_editor_data(db, body))
