from fastapi import HTTPException
from sqlalchemy.orm import Session

from .repository import (
    create_maintenance,
    delete_maintenance,
    get_maintenance,
    get_maintenance_with_device,
    list_maintenance,
    update_maintenance,
)
from .schemas import MaintenanceOut, MaintenanceSaveBody


# 정비 검색 결과에 장비 정보를 합쳐 목록과 검색 건수를 반환합니다.
def get_maintenance_list(
    db: Session,
    keyword: str = "",
    device_id: int | None = None,
    maintenance_type: str = "",
    status: str = "",
    date_from: str = "",
    date_to: str = "",
) -> dict:
    items = list_maintenance(
        db,
        keyword=keyword,
        device_id=device_id,
        maintenance_type=maintenance_type,
        status=status,
        date_from=date_from,
        date_to=date_to,
    )
    return {"list": [_maintenance_to_dict(item, device) for item, device in items], "totalCount": len(items)}


# 장비를 포함한 정비 상세를 반환하며 없으면 404 오류를 발생시킵니다.
def get_maintenance_detail(db: Session, maintenance_id: int) -> dict:
    result = get_maintenance_with_device(db, maintenance_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    item, device = result
    return _maintenance_to_dict(item, device)


# 정비 등록 본문을 저장한 뒤 연결 장비를 포함한 상세를 다시 조회합니다.
def add_maintenance(db: Session, body: MaintenanceSaveBody) -> dict:
    item = create_maintenance(db, body.model_dump())
    return get_maintenance_detail(db, item.id)


# 정비 수정 후 상세를 다시 조회하며 없으면 404 오류를 발생시킵니다.
def save_maintenance(db: Session, maintenance_id: int, body: MaintenanceSaveBody) -> dict:
    item = update_maintenance(db=db, maintenance_id=maintenance_id, payload=body.model_dump())
    if item is None:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    return get_maintenance_detail(db, item.id)


# 정비를 삭제하며 없으면 404 오류를 발생시킵니다.
def remove_maintenance(db: Session, maintenance_id: int) -> dict:
    if not delete_maintenance(db, maintenance_id):
        raise HTTPException(status_code=404, detail="Maintenance not found")
    return {"deleted": True}


# 정비 응답에 연결 장비의 이름과 종류를 추가합니다.
def _maintenance_to_dict(item, device=None) -> dict:
    data = MaintenanceOut.model_validate(item).model_dump()
    data["device_name"] = device.name if device else None
    data["device_type"] = device.device_type if device else None
    return data
