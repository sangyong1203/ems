from fastapi import HTTPException
from sqlalchemy.orm import Session

from .repository import create_pv_string, delete_pv_string, get_pv_string, list_pv_strings, update_pv_string
from .schemas import PvStringOut, PvStringSaveBody


def get_pv_string_list(db: Session, status: str = "", keyword: str = "", connection: str = "") -> dict:
    items = list_pv_strings(db, status=status, keyword=keyword, connection=connection)
    return {"list": [_pv_string_out(item) for item in items], "totalCount": len(items)}


def get_pv_string_detail(db: Session, pv_string_id: int) -> dict:
    item = get_pv_string(db, pv_string_id)
    if item is None:
        raise HTTPException(status_code=404, detail="PV string not found")
    return _pv_string_out(item)


def add_pv_string(db: Session, body: PvStringSaveBody) -> dict:
    item = create_pv_string(db, body.model_dump())
    return _pv_string_out(item)


def save_pv_string(db: Session, pv_string_id: int, body: PvStringSaveBody) -> dict:
    item = update_pv_string(db, pv_string_id, body.model_dump())
    if item is None:
        raise HTTPException(status_code=404, detail="PV string not found")
    return _pv_string_out(item)


def remove_pv_string(db: Session, pv_string_id: int) -> dict:
    if not delete_pv_string(db, pv_string_id):
        raise HTTPException(status_code=404, detail="PV string not found")
    return {"deleted": True}


def _pv_string_out(item: dict) -> dict:
    return PvStringOut.model_validate(item).model_dump()
