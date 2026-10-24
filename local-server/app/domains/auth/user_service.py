from datetime import datetime

from sqlalchemy.orm import Session

from .models import User
from .repository import create_user as create_user_row
from .repository import delete_user as delete_user_row
from .repository import list_users as list_user_rows
from .repository import update_user as update_user_row


# 조건에 맞는 사용자 목록을 화면 응답으로 변환하고 전체 검색 건수를 함께 반환합니다.
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


# 사용자를 생성하고 비밀번호를 제외한 화면용 정보를 반환합니다.
def create_user(db: Session, payload: dict) -> dict:
    return _user_out(create_user_row(db, payload))


# 사용자를 수정하고 화면용 정보를 반환하며 대상이 없으면 None을 반환합니다.
def update_user(db: Session, user_id: int, payload: dict) -> dict | None:
    user = update_user_row(db, user_id, payload)
    if user is None:
        return None
    return _user_out(user)


# 사용자 삭제 결과를 반환하며 커밋은 저장소에서 처리합니다.
def delete_user(db: Session, user_id: int) -> bool:
    return delete_user_row(db, user_id)


# 일시를 초 단위 표시 문자열로 변환하며 값이 없으면 빈 문자열을 반환합니다.
def _format_datetime(value: datetime | None) -> str:
    if value is None:
        return ""
    return value.strftime("%Y-%m-%d %H:%M:%S")


# 사용자에서 비밀번호를 제외하고 날짜 필드를 화면용 문자열로 변환합니다.
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
