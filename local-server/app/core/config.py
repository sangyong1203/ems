# 환경변수와 서버 파일 위치를 기준으로 로컬 서버 설정을 구성합니다.
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]  # local-server 디렉터리의 절대 경로
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'solar_ems.db'}")  # 환경변수 우선; 생략 시 local-server의 SQLite 파일 사용
APP_NAME = "Solar ESS EMS Local API"  # API 문서에 표시할 서버 이름
