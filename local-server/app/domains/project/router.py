from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .schemas import ProjectConfigSaveBody
from .service import get_project_config, save_project_config


router = APIRouter(prefix="/api/project", tags=["project"])  # 이 도메인의 API 경로와 문서 태그


# 프로젝트 설정과 장비 집계를 공통 성공 응답으로 반환합니다.
@router.get("")
def get_project(db: Session = Depends(get_db)):
    return ok(get_project_config(db))


# 프로젝트 설정 수정 본문을 저장 서비스에 전달합니다.
@router.put("")
def save_project(body: ProjectConfigSaveBody, db: Session = Depends(get_db)):
    return ok(save_project_config(db, body))
