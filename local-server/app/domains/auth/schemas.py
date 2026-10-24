from pydantic import BaseModel


# 로그인 요청
class LoginBody(BaseModel):
    username: str  # 로그인에 사용하는 사용자 ID
    password: str  # 입력 비밀번호


# 로컬 비밀번호 변경 요청 형식
class PasswordChangeBody(BaseModel):
    newPassword: str  # 변경 요청 비밀번호
    verificationToken: str | None = None  # 검증 토큰; 로컬 처리에서는 검증하지 않음
    isAdmin: str | None = None  # 관리자 구분 입력; 로컬 처리에서는 사용하지 않음


# 로컬 비밀번호 재설정 요청 형식
class PasswordResetRequestBody(BaseModel):
    email: str  # 이메일 주소
    requestType: str | None = None  # 재설정 요청 구분; 로컬 처리에서는 사용하지 않음
    isAdmin: str | None = None  # 관리자 구분 입력; 로컬 처리에서는 사용하지 않음


# 로컬 비밀번호 재설정 저장 형식
class PasswordResetBody(BaseModel):
    password: str  # 입력 비밀번호
    requestType: str | None = None  # 재설정 요청 구분; 로컬 처리에서는 사용하지 않음
    isAdmin: str | None = None  # 관리자 구분 입력; 로컬 처리에서는 사용하지 않음
    verificationToken: str | None = None  # 검증 토큰; 로컬 처리에서는 검증하지 않음


# 로컬 토큰 재발급 요청 형식
class TokenReissueBody(BaseModel):
    refreshToken: str | None = None  # 갱신 토큰; 로컬 재발급에서는 검증하지 않음
    isAdmin: str | None = None  # 관리자 구분 입력; 로컬 처리에서는 사용하지 않음


# 사용자 등록·수정 요청
class UserSaveBody(BaseModel):
    name: str  # 사용자 이름
    email: str  # 이메일 주소
    department: str  # 소속 부서
    role: str  # 사용자 역할
    status: str  # 사용자 활성 상태 (Active / Inactive)
