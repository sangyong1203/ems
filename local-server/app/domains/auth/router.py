from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .dependencies import require_admin
from .models import User
from .schemas import LoginBody, PasswordChangeBody, TokenReissueBody
from .service import change_user_password, get_current_user, login_user, logout_user, reissue_tokens


# 토큰과 계정 응답이 브라우저나 프록시 캐시에 저장되지 않도록 합니다.
def disable_auth_cache(response: Response) -> None:
    response.headers['Cache-Control'] = 'no-store'


router = APIRouter(prefix='/api/auth', tags=['solar-auth'], dependencies=[Depends(disable_auth_cache)])  # 공개 인증 API와 인증 후 계정 API


# 비밀번호를 검증하여 관리자 세션을 발급합니다.
@router.post('/login')
def login(body: LoginBody, db: Session = Depends(get_db)):
    return login_user(db, body)


# 인증된 관리자 본인의 실제 사용자 정보를 반환합니다.
@router.get('/me')
def me(user: User = Depends(require_admin)):
    return ok(get_current_user(user))


# 유효한 갱신 토큰을 새 토큰 쌍으로 교체합니다.
@router.post('/reissue')
def reissue(body: TokenReissueBody, db: Session = Depends(get_db)):
    return reissue_tokens(db, body.refreshToken)


# 액세스 토큰이 만료되어도 갱신 토큰으로 해당 로그인 세션을 폐기할 수 있습니다.
@router.post('/logout')
def logout(body: TokenReissueBody, db: Session = Depends(get_db)):
    return logout_user(db, body.refreshToken)


# 현재 비밀번호를 확인하고 변경한 뒤 모든 세션을 폐기합니다.
@router.post('/password/change')
def change_password(body: PasswordChangeBody, user: User = Depends(require_admin), db: Session = Depends(get_db)):
    return change_user_password(db, user, body)


# 메일 전송 연동 전까지 비인증 비밀번호 재설정을 명시적으로 비활성화합니다.
@router.post('/password/reset')
@router.put('/password/reset')
def password_reset_disabled():
    raise HTTPException(status_code=403, detail='Email password reset is unavailable. Contact your administrator.')
