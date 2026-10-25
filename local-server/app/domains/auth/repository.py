from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .models import AuthSession, User
from .security import hash_password


# 로그인 ID가 정확히 일치하는 사용자를 조회합니다.
def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


# 검색어·역할·상태로 사용자를 조회하며 양수 페이지 조건일 때만 페이징합니다.
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


# 사용자 ID로 단건 조회하며 없으면 None을 반환합니다.
def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


# 이메일을 로그인 ID로 사용하고 관리자가 입력한 초기 비밀번호를 해시화하여 저장합니다.
def create_user(db: Session, payload: dict) -> User:
    if not payload.get("password"):
        raise HTTPException(status_code=422, detail="Initial password is required.")
    user = User(
        username=payload["email"],
        password_hash=hash_password(payload["password"]),
        name=payload["name"],
        email=payload["email"],
        department=payload["department"],
        role=payload["role"],
        status=payload["status"],
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="A user with this login ID already exists.")
    db.refresh(user)
    return user


# 사용자 정보와 이메일 기반 로그인 ID를 갱신하고 커밋하며 없으면 None을 반환합니다.
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
    if payload.get("password"):
        user.password_hash = hash_password(payload["password"])
    db.query(AuthSession).filter(AuthSession.user_id == user.id).update({"revoked": True})
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="A user with this login ID already exists.")
    db.refresh(user)
    return user


# 사용자를 삭제하고 커밋하며 대상이 없으면 False를 반환합니다.
def delete_user(db: Session, user_id: int) -> bool:
    user = get_user(db, user_id)
    if user is None:
        return False
    db.query(AuthSession).filter(AuthSession.user_id == user.id).delete()
    db.delete(user)
    db.commit()
    return True
