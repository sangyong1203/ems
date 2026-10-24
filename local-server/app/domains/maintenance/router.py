from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .schemas import MaintenanceSaveBody
from .service import (
    add_maintenance,
    get_maintenance_detail,
    get_maintenance_list,
    remove_maintenance,
    save_maintenance,
)


router = APIRouter(prefix="/api/maintenance", tags=["maintenance"])  # 이 도메인의 API 경로와 문서 태그


# 정비 검색 조건의 쿼리 필드명을 서비스 인자로 매핑하여 목록을 반환합니다.
@router.get("")
def maintenance(
    keyword: str = Query(default=""),
    deviceId: int | None = Query(default=None),
    maintenanceType: str = Query(default=""),
    status: str = Query(default=""),
    dateFrom: str = Query(default=""),
    dateTo: str = Query(default=""),
    db: Session = Depends(get_db),
):
    return ok(
        get_maintenance_list(
            db,
            keyword=keyword,
            device_id=deviceId,
            maintenance_type=maintenanceType,
            status=status,
            date_from=dateFrom,
            date_to=dateTo,
        )
    )


# 정비 ID로 장비 포함 상세 조회를 요청합니다.
@router.get("/{maintenance_id}")
def maintenance_detail(maintenance_id: int, db: Session = Depends(get_db)):
    return ok(get_maintenance_detail(db, maintenance_id))


# 정비 등록 본문을 서비스에 전달합니다.
@router.post("")
def create_maintenance(body: MaintenanceSaveBody, db: Session = Depends(get_db)):
    return ok(add_maintenance(db, body))


# 정비 ID와 수정 본문을 서비스에 전달합니다.
@router.put("/{maintenance_id}")
def update_maintenance(maintenance_id: int, body: MaintenanceSaveBody, db: Session = Depends(get_db)):
    return ok(save_maintenance(db, maintenance_id, body))


# 정비 삭제를 요청하고 처리 결과를 반환합니다.
@router.delete("/{maintenance_id}")
def delete_maintenance(maintenance_id: int, db: Session = Depends(get_db)):
    return ok(remove_maintenance(db, maintenance_id))
