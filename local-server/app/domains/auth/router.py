from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .schemas import LoginBody, PasswordChangeBody, PasswordResetBody, PasswordResetRequestBody, TokenReissueBody
from .service import build_password_reset_response, get_current_user, login_user


router = APIRouter(prefix="/api/auth", tags=["solar-auth"])  # 이 도메인의 API 경로와 문서 태그


# 로그인 정보를 검증하는 서비스의 성공 또는 업무 실패 응답을 그대로 반환합니다.
@router.post("/login")
def login(body: LoginBody, db: Session = Depends(get_db)):
    return login_user(db, body)


# 로컬 개발용 고정 관리자 정보를 공통 성공 응답으로 반환합니다.
@router.get("/me")
def me():
    return ok(get_current_user())


# 입력 토큰을 검증하지 않고 로컬용 고정 액세스·갱신 토큰을 반환합니다.
@router.post("/reissue")
def reissue(_: TokenReissueBody):
    return ok(
        {
            "accessToken": "solar-ems-local-access-token",
            "refreshToken": "solar-ems-local-refresh-token",
        }
    )


# 요청 본문을 받되 실제 비밀번호 변경 없이 고정 검증 토큰을 반환합니다.
@router.post("/password/change")
def change_password(_: PasswordChangeBody):
    return build_password_reset_response()


# 재설정 요청을 받되 메일 발송 없이 고정 검증 토큰을 반환합니다.
@router.post("/password/reset")
def request_password_reset(_: PasswordResetRequestBody):
    return build_password_reset_response()


# 재설정 본문을 받되 실제 비밀번호 저장 없이 고정 검증 토큰을 반환합니다.
@router.put("/password/reset")
def reset_password(_: PasswordResetBody):
    return build_password_reset_response()
