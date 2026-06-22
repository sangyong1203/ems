from sqlalchemy.orm import Session

from .models import ProjectConfig


def get_project_config(db: Session) -> ProjectConfig | None:
    return db.query(ProjectConfig).first()


def update_project_config(db: Session, payload: dict) -> ProjectConfig | None:
    project = get_project_config(db)
    if project is None:
        return None
    for key, value in payload.items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return project
