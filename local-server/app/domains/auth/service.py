from datetime import datetime, timedelta
from secrets import token_urlsafe

from fastapi import HTTPException
from sqlalchemy import or_, update
from sqlalchemy.orm import Session

from ...core.responses import ok
from .dependencies import utc_now
from .models import AuthSession, User
from .repository import get_user_by_username
from .schemas import LoginBody, PasswordChangeBody
from .security import DUMMY_PASSWORD_HASH, hash_password, hash_token, password_hasher, verify_password


ACCESS_LIFETIME = timedelta(hours=1)  # 액세스 토큰 유효기간
REFRESH_LIFETIME = timedelta(days=1)  # 로그인 시점부터 세션의 절대 유효기간


# 신규 세션을 발급하며 토큰 원문은 응답으로만 전달하고 DB에는 해시를 저장합니다.
def _create_session(db: Session, user: User) -> dict:
    now = utc_now()
    access_token, refresh_token = token_urlsafe(48), token_urlsafe(48)
    db.add(AuthSession(
        user_id=user.id,
        access_token_hash=hash_token(access_token),
        refresh_token_hash=hash_token(refresh_token),
        access_expires_at=now + ACCESS_LIFETIME,
        refresh_expires_at=now + REFRESH_LIFETIME,
        created_at=now,
        revoked=False,
    ))
    return {'accessToken': access_token, 'refreshToken': refresh_token}


# 비밀번호·활성 상태를 확인하고 관리자에게만 로그인 세션을 발급합니다.
def login_user(db: Session, body: LoginBody) -> dict:
    user = get_user_by_username(db, body.username.strip())
    valid_password = verify_password(user.password_hash if user else DUMMY_PASSWORD_HASH, body.password)
    if user is None or not valid_password or user.status != 'Active':
        return {'result': 'LOGIN_FAILED', 'resultMessage': 'Invalid username or password.', 'data': None}
    if user.role != 'Platform Admin':
        raise HTTPException(status_code=403, detail='Administrator access required.')
    if password_hasher.check_needs_rehash(user.password_hash):
        user.password_hash = hash_password(body.password)
    db.query(AuthSession).filter(AuthSession.refresh_expires_at <= utc_now()).delete(synchronize_session=False)
    user.last_login_at = datetime.now()
    tokens = _create_session(db, user)
    db.commit()
    return ok({**tokens, 'landingPage': '/dashboard', 'user': get_current_user(user)})


# 검증된 현재 사용자의 실제 정보를 프론트 인증 계약에 맞춰 반환합니다.
def get_current_user(user: User) -> dict:
    return {
        'id': user.id, 'username': user.username, 'email': user.email,
        'name': user.name, 'role': user.role, 'userLevel': 'PLATFORM_ADMIN', 'landingPage': '/dashboard',
    }


# 갱신 토큰을 한 번만 교체하며 만료·폐기된 세션이나 비관리자 계정은 재발급하지 않습니다.
def reissue_tokens(db: Session, refresh_token: str) -> dict:
    now = utc_now()
    old_hash = hash_token(refresh_token)
    session = db.query(AuthSession).filter(
        AuthSession.refresh_token_hash == old_hash,
        AuthSession.revoked.is_(False),
        AuthSession.refresh_expires_at > now,
    ).first()
    unauthorized = HTTPException(status_code=401, detail='Refresh token is invalid or expired.')
    if session is None:
        raise unauthorized
    user = db.get(User, session.user_id)
    if user is None or user.status != 'Active':
        raise unauthorized
    if user.role != 'Platform Admin':
        raise HTTPException(status_code=403, detail='Administrator access required.')
    access_token, new_refresh_token = token_urlsafe(48), token_urlsafe(48)
    result = db.execute(update(AuthSession).where(
        AuthSession.id == session.id,
        AuthSession.refresh_token_hash == old_hash,
        AuthSession.revoked.is_(False),
        AuthSession.refresh_expires_at > now,
    ).values(
        access_token_hash=hash_token(access_token),
        refresh_token_hash=hash_token(new_refresh_token),
        previous_refresh_token_hash=old_hash,
        access_expires_at=min(now + ACCESS_LIFETIME, session.refresh_expires_at),
    ).execution_options(synchronize_session=False))
    if result.rowcount != 1:
        db.rollback()
        raise unauthorized
    db.commit()
    return ok({'accessToken': access_token, 'refreshToken': new_refresh_token})


# 현재 또는 직전 갱신 토큰의 세션을 폐기하여 토큰 교체와 로그아웃이 겹쳐도 세션이 남지 않게 합니다.
def logout_user(db: Session, refresh_token: str) -> dict:
    token_hash = hash_token(refresh_token)
    db.query(AuthSession).filter(or_(
        AuthSession.refresh_token_hash == token_hash,
        AuthSession.previous_refresh_token_hash == token_hash,
    )).update({'revoked': True})
    db.commit()
    return ok({'loggedOut': True})


# 현재 비밀번호를 재확인하여 새 해시를 저장하고 해당 사용자의 모든 세션을 폐기합니다.
def change_user_password(db: Session, user: User, body: PasswordChangeBody) -> dict:
    if not verify_password(user.password_hash, body.currentPassword):
        raise HTTPException(status_code=400, detail='Current password is incorrect.')
    user.password_hash = hash_password(body.newPassword)
    db.query(AuthSession).filter(AuthSession.user_id == user.id).update({'revoked': True})
    db.commit()
    return ok({'changed': True})
