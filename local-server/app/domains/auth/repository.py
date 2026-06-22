from sqlalchemy import or_
from sqlalchemy.orm import Session

from .models import User


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def list_users(
    db: Session,
    *,
    keyword: str = "",
    role: str = "",
    status: str = "",
    page_number: int = 1,
    page_size: int = 10,
) -> tuple[list[User], int]:
    query = db.query(User).order_by(User.id.asc())
    normalized_keyword = keyword.strip()

    if normalized_keyword:
        keyword_pattern = f"%{normalized_keyword}%"
        query = query.filter(
            or_(
                User.name.ilike(keyword_pattern),
                User.email.ilike(keyword_pattern),
                User.department.ilike(keyword_pattern),
                User.username.ilike(keyword_pattern),
            )
        )
    if role:
        query = query.filter(User.role == role)
    if status:
        query = query.filter(User.status == status)

    total_count = query.count()
    if page_number > 0 and page_size > 0:
        query = query.offset((page_number - 1) * page_size).limit(page_size)
    return query.all(), total_count


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, payload: dict) -> User:
    user = User(
        username=payload["email"],
        password_hash="1111",
        name=payload["name"],
        email=payload["email"],
        department=payload["department"],
        role=payload["role"],
        status=payload["status"],
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user_id: int, payload: dict) -> User | None:
    user = get_user(db, user_id)
    if user is None:
        return None

    user.username = payload["email"]
    user.name = payload["name"]
    user.email = payload["email"]
    user.department = payload["department"]
    user.role = payload["role"]
    user.status = payload["status"]
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> bool:
    user = get_user(db, user_id)
    if user is None:
        return False
    db.delete(user)
    db.commit()
    return True
