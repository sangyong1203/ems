from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .schemas import ProjectConfigSaveBody
from .service import get_project_config, save_project_config


router = APIRouter(prefix="/api/project", tags=["project"])


@router.get("")
def get_project(db: Session = Depends(get_db)):
    return ok(get_project_config(db))


@router.put("")
def save_project(body: ProjectConfigSaveBody, db: Session = Depends(get_db)):
    return ok(save_project_config(db, body))
