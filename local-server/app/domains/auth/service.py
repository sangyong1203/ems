from datetime import datetime

from sqlalchemy.orm import Session

from ...core.responses import ok
from .repository import get_user_by_username
from .schemas import LoginBody


# 저장된 비밀번호와 활성 상태를 확인하고 로그인 시각을 저장한 뒤 로컬용 고정 토큰을 반환합니다.
def login_user(db: Session, body: LoginBody) -> dict:
    user = get_user_by_username(db, body.username)
    if user is None or user.password_hash != body.password:
        return {"result": "LOGIN_FAILED", "resultMessage": "Invalid username or password.", "data": None}
    if user.status != "Active":
        return {"result": "LOGIN_FAILED", "resultMessage": "User is not active.", "data": None}

    user.last_login_at = datetime.now()
    db.commit()

    return ok(
        {
            "accessToken": "solar-ems-local-access-token",
            "refreshToken": "solar-ems-local-refresh-token",
            "verificationToken": "solar-ems-local-verification-token",
            "landingPage": "/dashboard",
            "user": {"id": user.id, "username": user.username, "role": user.role, "name": user.name},
        }
    )


# 토큰 검증 없이 로컬 개발용 고정 관리자 정보를 반환합니다.
def get_current_user() -> dict:
    return {
        "id": 1,
        "username": "admin",
        "email": "admin",
        "krName": "Admin",
        "name": "Admin",
        "role": "Platform Admin",
        "userLevel": "PLATFORM_ADMIN",
        "landingPage": "/dashboard",
    }


# 비밀번호를 변경하지 않고 로컬용 고정 검증 토큰을 성공 응답으로 반환합니다.
def build_password_reset_response() -> dict:
    return ok({"verificationToken": "solar-ems-local-verification-token"})
