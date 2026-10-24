from fastapi import HTTPException
from sqlalchemy.orm import Session

from .repository import create_pv_string, delete_pv_string, get_pv_string, list_pv_strings, update_pv_string
from .schemas import PvStringOut, PvStringSaveBody


# 조회된 스트링을 응답 스키마로 변환하고 목록과 건수를 반환합니다.
def get_pv_string_list(db: Session, status: str = "", keyword: str = "", connection: str = "") -> dict:
    items = list_pv_strings(db, status=status, keyword=keyword, connection=connection)
    return {"list": [_pv_string_out(item) for item in items], "totalCount": len(items)}


# 스트링 상세를 반환하며 없으면 404 오류를 발생시킵니다.
def get_pv_string_detail(db: Session, pv_string_id: int) -> dict:
    item = get_pv_string(db, pv_string_id)
    if item is None:
        raise HTTPException(status_code=404, detail="PV string not found")
    return _pv_string_out(item)


# 등록 본문을 저장하고 스트링 응답으로 변환합니다.
def add_pv_string(db: Session, body: PvStringSaveBody) -> dict:
    item = create_pv_string(db, body.model_dump())
    return _pv_string_out(item)


# 스트링을 수정하고 응답으로 변환하며 없으면 404 오류를 발생시킵니다.
def save_pv_string(db: Session, pv_string_id: int, body: PvStringSaveBody) -> dict:
    item = update_pv_string(db, pv_string_id, body.model_dump())
    if item is None:
        raise HTTPException(status_code=404, detail="PV string not found")
    return _pv_string_out(item)


# 스트링과 연결을 삭제하며 대상이 없으면 404 오류를 발생시킵니다.
def remove_pv_string(db: Session, pv_string_id: int) -> dict:
    if not delete_pv_string(db, pv_string_id):
        raise HTTPException(status_code=404, detail="PV string not found")
    return {"deleted": True}


# 스트링 사전을 응답 스키마로 검증하여 직렬화합니다.
def _pv_string_out(item: dict) -> dict:
    return PvStringOut.model_validate(item).model_dump()
