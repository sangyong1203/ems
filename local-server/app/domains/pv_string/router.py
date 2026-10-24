from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .schemas import PvStringSaveBody
from .service import (
    add_pv_string,
    get_pv_string_detail,
    get_pv_string_list,
    remove_pv_string,
    save_pv_string,
)


router = APIRouter(prefix="/api/pv-strings", tags=["pv-strings"])  # 이 도메인의 API 경로와 문서 태그


# 상태·검색어·연결 여부를 서비스에 전달하여 스트링 목록을 반환합니다.
@router.get("")
def pv_strings(
    status: str = Query(default=""),
    keyword: str = Query(default=""),
    connection: str = Query(default=""),
    db: Session = Depends(get_db),
):
    return ok(get_pv_string_list(db, status=status, keyword=keyword, connection=connection))


# 스트링 ID에 해당하는 연결 포함 상세를 반환합니다.
@router.get("/{pv_string_id}")
def pv_string_detail(pv_string_id: int, db: Session = Depends(get_db)):
    return ok(get_pv_string_detail(db, pv_string_id))


# 스트링 등록 본문을 서비스에 전달합니다.
@router.post("")
def create_pv_string(body: PvStringSaveBody, db: Session = Depends(get_db)):
    return ok(add_pv_string(db, body))


# 스트링 ID와 수정 본문을 서비스에 전달합니다.
@router.put("/{pv_string_id}")
def update_pv_string(pv_string_id: int, body: PvStringSaveBody, db: Session = Depends(get_db)):
    return ok(save_pv_string(db, pv_string_id, body))


# 스트링과 관련 연결의 삭제 결과를 반환합니다.
@router.delete("/{pv_string_id}")
def delete_pv_string(pv_string_id: int, db: Session = Depends(get_db)):
    return ok(remove_pv_string(db, pv_string_id))
