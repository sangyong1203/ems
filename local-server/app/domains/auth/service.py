from datetime import datetime

from sqlalchemy.orm import Session

from ...core.responses import ok
from .repository import get_user_by_username
from .schemas import LoginBody


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


def build_password_reset_response() -> dict:
    return ok({"verificationToken": "solar-ems-local-verification-token"})
