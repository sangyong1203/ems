from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .schemas import UserSaveBody
from .user_service import create_user, delete_user, list_users, update_user


router = APIRouter(prefix="/api/users", tags=["users"])


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


@router.post("")
def add_user(body: UserSaveBody, db: Session = Depends(get_db)):
    return ok(create_user(db, body.model_dump()))


@router.put("/{user_id}")
def save_user(user_id: int, body: UserSaveBody, db: Session = Depends(get_db)):
    item = update_user(db, user_id, body.model_dump())
    if item is None:
        raise HTTPException(status_code=404, detail="User not found")
    return ok(item)


@router.delete("/{user_id}")
def remove_user(user_id: int, db: Session = Depends(get_db)):
    if not delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return ok({"result": "SUCCESS"})
