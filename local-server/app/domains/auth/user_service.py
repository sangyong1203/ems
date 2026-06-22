from datetime import datetime

from sqlalchemy.orm import Session

from .models import User
from .repository import create_user as create_user_row
from .repository import delete_user as delete_user_row
from .repository import list_users as list_user_rows
from .repository import update_user as update_user_row


def list_users(
    db: Session,
    *,
    keyword: str = "",
    role: str = "",
    status: str = "",
    page_number: int = 1,
    page_size: int = 10,
) -> tuple[list[dict], int]:
    items, total_count = list_user_rows(
        db,
        keyword=keyword,
        role=role,
        status=status,
        page_number=page_number,
        page_size=page_size,
    )
    return [_user_out(item) for item in items], total_count


def create_user(db: Session, payload: dict) -> dict:
    return _user_out(create_user_row(db, payload))


def update_user(db: Session, user_id: int, payload: dict) -> dict | None:
    user = update_user_row(db, user_id, payload)
    if user is None:
        return None
    return _user_out(user)


def delete_user(db: Session, user_id: int) -> bool:
    return delete_user_row(db, user_id)


def _format_datetime(value: datetime | None) -> str:
    if value is None:
        return ""
    return value.strftime("%Y-%m-%d %H:%M:%S")


def _user_out(user: User) -> dict:
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "department": user.department,
        "role": user.role,
        "status": user.status,
        "lastLoginAt": _format_datetime(user.last_login_at),
        "createdAt": _format_datetime(user.created_at),
    }
