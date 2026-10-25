from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from ...core.database import Base


# 사용자 계정과 로그인 이력
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # 사용자 ID
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)  # 로그인에 사용하는 사용자 ID
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)  # Argon2id 비밀번호 해시
    name: Mapped[str] = mapped_column(String(80), nullable=False, default="")  # 사용자 이름
    email: Mapped[str] = mapped_column(String(120), nullable=False, default="")  # 이메일 주소
    department: Mapped[str] = mapped_column(String(80), nullable=False, default="")  # 소속 부서
    role: Mapped[str] = mapped_column(String(40), nullable=False, default="Operator")  # 사용자 역할
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="Active")  # 사용자 활성 상태 (Active / Inactive / Locked)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))  # 마지막 로그인 시각
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # 생성 시각


# 사용자별 로그인 세션; 만료 시각은 UTC 기준으로 저장
class AuthSession(Base):
    __tablename__ = 'auth_sessions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # 로그인 세션 ID
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False, index=True)  # 인증된 사용자 ID
    access_token_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)  # 액세스 토큰 해시
    refresh_token_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)  # 갱신 토큰 해시
    previous_refresh_token_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)  # 직전 갱신 토큰; 동시 로그아웃의 폐기 확인에만 사용
    access_expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)  # 액세스 만료 시각 (UTC)
    refresh_expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)  # 세션 절대 만료 시각 (UTC); 갱신 시 연장하지 않음
    revoked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)  # 폐기 여부
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)  # 로그인 시각 (UTC)
