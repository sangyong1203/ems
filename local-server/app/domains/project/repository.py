from sqlalchemy.orm import Session

from .models import ProjectConfig


# 첫 프로젝트 설정을 조회하며 설정이 없으면 None을 반환합니다.
def get_project_config(db: Session) -> ProjectConfig | None:
    return db.query(ProjectConfig).first()


# 기존 프로젝트의 전달된 필드를 갱신·커밋하며 설정이 없으면 None을 반환합니다.
def update_project_config(db: Session, payload: dict) -> ProjectConfig | None:
    project = get_project_config(db)
    if project is None:
        return None
    for key, value in payload.items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return project
