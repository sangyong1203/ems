from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .schemas import UserSaveBody
from .user_service import create_user, delete_user, list_users, update_user


router = APIRouter(prefix="/api/users", tags=["users"])  # 이 도메인의 API 경로와 문서 태그


# 검색·페이지 조건을 서비스에 전달하고 목록과 전체 건수를 성공 응답으로 반환합니다.
@router.get("")
def get_users(
    keyword: str = Query(default=""),
    role: str = Query(default=""),
    status: str = Query(default=""),
    pageNumber: int = Query(default=1),
    pageSize: int = Query(default=10),
    db: Session = Depends(get_db),
):
    items, total_count = list_users(
        db,
        keyword=keyword,
        role=role,
        status=status,
        page_number=pageNumber,
        page_size=pageSize,
    )
    return ok({"list": items, "totalCount": total_count})


# 사용자 등록 본문을 사전으로 변환하여 저장하고 생성된 사용자 정보를 반환합니다.
@router.post("")
def add_user(body: UserSaveBody, db: Session = Depends(get_db)):
    return ok(create_user(db, body.model_dump()))


# 사용자 정보를 수정하며 대상이 없으면 404로 응답합니다.
@router.put("/{user_id}")
def save_user(user_id: int, body: UserSaveBody, db: Session = Depends(get_db)):
    item = update_user(db, user_id, body.model_dump())
    if item is None:
        raise HTTPException(status_code=404, detail="User not found")
    return ok(item)


# 사용자를 삭제하며 대상이 없으면 404로 응답합니다.
@router.delete("/{user_id}")
def remove_user(user_id: int, db: Session = Depends(get_db)):
    if not delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return ok({"result": "SUCCESS"})
