# FastAPI 앱과 개발용 CORS, 시작 시 DB 초기화 및 API 라우터를 등록합니다.
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.router import api_router
from .core.config import APP_NAME
from .core.database import SessionLocal
from .db.init_db import create_tables, seed_database


app = FastAPI(title=APP_NAME)  # 로컬 API 애플리케이션
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 서버 시작 시 테이블과 시드 데이터를 준비하고 초기화용 DB 세션을 닫습니다.
@app.on_event("startup")
def startup_event():
    create_tables()
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()


app.include_router(api_router)
