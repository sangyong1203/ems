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


router = APIRouter(prefix="/api/pv-strings", tags=["pv-strings"])


@router.get("")
def pv_strings(
    status: str = Query(default=""),
    keyword: str = Query(default=""),
    connection: str = Query(default=""),
    db: Session = Depends(get_db),
):
    return ok(get_pv_string_list(db, status=status, keyword=keyword, connection=connection))


@router.get("/{pv_string_id}")
def pv_string_detail(pv_string_id: int, db: Session = Depends(get_db)):
    return ok(get_pv_string_detail(db, pv_string_id))


@router.post("")
def create_pv_string(body: PvStringSaveBody, db: Session = Depends(get_db)):
    return ok(add_pv_string(db, body))


@router.put("/{pv_string_id}")
def update_pv_string(pv_string_id: int, body: PvStringSaveBody, db: Session = Depends(get_db)):
    return ok(save_pv_string(db, pv_string_id, body))


@router.delete("/{pv_string_id}")
def delete_pv_string(pv_string_id: int, db: Session = Depends(get_db)):
    return ok(remove_pv_string(db, pv_string_id))
