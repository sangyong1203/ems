from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


# 로그인 요청; 기존 계정 전환을 위해 로그인 비밀번호에는 신규 길이 정책을 강제하지 않음
class LoginBody(BaseModel):
    username: str = Field(min_length=1, max_length=80)  # 로그인 ID
    password: str = Field(min_length=1, max_length=128)  # 입력 비밀번호


# 인증된 사용자의 비밀번호 변경 요청
class PasswordChangeBody(BaseModel):
    model_config = ConfigDict(extra='forbid')  # 기존 검증 토큰·관리자 플래그 입력을 허용하지 않음
    currentPassword: str = Field(min_length=1, max_length=128)  # 현재 비밀번호 재확인
    newPassword: str = Field(min_length=8, max_length=128)  # 새 비밀번호


# 세션 재발급 또는 로그아웃 요청
class TokenReissueBody(BaseModel):
    model_config = ConfigDict(extra='forbid')
    refreshToken: str = Field(min_length=1, max_length=256)  # 서버가 발급한 갱신 토큰 원문; 유효성은 저장된 해시로 확인


# 사용자 등록·수정 요청; 비밀번호는 생성 시 필수이며 수정 시 생략하면 유지
class UserSaveBody(BaseModel):
    name: str = Field(min_length=1, max_length=80)  # 사용자 이름
    email: str = Field(min_length=1, max_length=80)  # 이메일과 로그인 ID
    department: str = Field(max_length=80)  # 소속 부서
    role: Literal['Platform Admin', 'Operator', 'Viewer']  # 현재 로그인은 관리자 역할만 허용
    status: Literal['Active', 'Inactive', 'Locked']  # 계정 상태
    password: str | None = Field(default=None, min_length=8, max_length=128)  # 신규 초기 비밀번호 또는 관리자 재설정값
