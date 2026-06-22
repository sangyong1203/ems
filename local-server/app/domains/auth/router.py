from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .schemas import LoginBody, PasswordChangeBody, PasswordResetBody, PasswordResetRequestBody, TokenReissueBody
from .service import build_password_reset_response, get_current_user, login_user


router = APIRouter(prefix="/api/auth", tags=["solar-auth"])


@router.post("/login")
def login(body: LoginBody, db: Session = Depends(get_db)):
    return login_user(db, body)


@router.get("/me")
def me():
    return ok(get_current_user())


@router.post("/reissue")
def reissue(_: TokenReissueBody):
    return ok(
        {
            "accessToken": "solar-ems-local-access-token",
            "refreshToken": "solar-ems-local-refresh-token",
        }
    )


@router.post("/password/change")
def change_password(_: PasswordChangeBody):
    return build_password_reset_response()


@router.post("/password/reset")
def request_password_reset(_: PasswordResetRequestBody):
    return build_password_reset_response()


@router.put("/password/reset")
def reset_password(_: PasswordResetBody):
    return build_password_reset_response()
