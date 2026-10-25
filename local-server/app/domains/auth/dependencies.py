from datetime import datetime, timezone

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from ...core.database import get_db
from .models import AuthSession, User
from .security import hash_token


bearer = HTTPBearer(auto_error=False)  # 누락·잘못된 인증 방식도 일관된 401로 응답


# UTC 시각을 SQLite DateTime과 비교 가능한 형태로 반환합니다.
def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


# 액세스 토큰과 세션 만료·폐기·사용자 활성 상태를 매 요청마다 확인합니다.
def get_authenticated_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
) -> User:
    unauthorized = HTTPException(status_code=401, detail='Authentication required or session expired.', headers={'WWW-Authenticate': 'Bearer'})
    if credentials is None:
        raise unauthorized
    session = db.query(AuthSession).filter(
        AuthSession.access_token_hash == hash_token(credentials.credentials),
        AuthSession.revoked.is_(False),
        AuthSession.access_expires_at > utc_now(),
        AuthSession.refresh_expires_at > utc_now(),
    ).first()
    if session is None:
        raise unauthorized
    user = db.get(User, session.user_id)
    if user is None or user.status != 'Active':
        raise unauthorized
    return user


# 관리자 전용 정책을 적용하며 프론트에서 전달하는 역할·관리자 플래그는 신뢰하지 않습니다.
def require_admin(user: User = Depends(get_authenticated_user)) -> User:
    if user.role != 'Platform Admin':
        raise HTTPException(status_code=403, detail='Administrator access required.')
    return user
