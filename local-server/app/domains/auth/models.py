from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from ...core.database import Base


# 사용자 계정과 로그인 이력
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # 사용자 ID
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)  # 로그인에 사용하는 사용자 ID
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)  # 로컬 서버에서 입력 비밀번호와 직접 비교하는 저장값
    name: Mapped[str] = mapped_column(String(80), nullable=False, default="")  # 사용자 이름
    email: Mapped[str] = mapped_column(String(120), nullable=False, default="")  # 이메일 주소
    department: Mapped[str] = mapped_column(String(80), nullable=False, default="")  # 소속 부서
    role: Mapped[str] = mapped_column(String(40), nullable=False, default="Operator")  # 사용자 역할
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="Active")  # 사용자 활성 상태 (Active / Inactive)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))  # 마지막 로그인 시각
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # 생성 시각
