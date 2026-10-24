# SQLite 엔진과 요청별 SQLAlchemy 세션을 관리합니다.
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from .config import DATABASE_URL


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # SQLite 연결 엔진; 스레드 간 연결 사용 허용
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # 자동 커밋·자동 flush를 끈 요청별 세션 팩터리


# 모든 ORM 모델이 테이블 메타데이터를 공유하는 선언형 기본 클래스
class Base(DeclarativeBase):
    pass


# 요청에 사용할 DB 세션을 제공하고, 처리 성공 여부와 관계없이 종료 시 닫습니다.
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()  # 현재 요청에서 사용할 독립 세션
    try:
        yield db
    finally:
        db.close()
