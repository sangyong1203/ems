from fastapi import HTTPException
from sqlalchemy.orm import Session

from .models import ProjectConfig
from ..device.equipment_repository import get_equipment_summary
from .repository import get_project_config as fetch_project_config
from .repository import update_project_config
from .schemas import ProjectConfigOut, ProjectConfigSaveBody


# 프로젝트 설정과 장비 집계를 반환하며 설정이 없으면 404 오류를 발생시킵니다.
def get_project_config(db: Session) -> dict:
    project = fetch_project_config(db)
    if project is None:
        raise HTTPException(status_code=404, detail="Project config not found")
    return _project_response(db, project)


# 프로젝트 설정을 저장하고 장비 집계를 포함한 응답을 반환하며 없으면 404 오류를 발생시킵니다.
def save_project_config(db: Session, body: ProjectConfigSaveBody) -> dict:
    project = update_project_config(db, body.model_dump())
    if project is None:
        raise HTTPException(status_code=404, detail="Project config not found")
    return _project_response(db, project)


# 프로젝트 설정에 전체·활성 장비 수와 용량 집계를 결합합니다.
def _project_response(db: Session, project: ProjectConfig) -> dict:
    equipment = get_equipment_summary(db)
    return ProjectConfigOut.model_validate(
        {
            **project.__dict__,
            "device_counts": equipment["deviceCounts"],
            "active_device_counts": equipment["activeDeviceCounts"],
            "equipment_capacities": equipment["capacities"],
        }
    ).model_dump()
