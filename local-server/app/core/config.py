# 환경변수와 서버 파일 위치를 기준으로 로컬 서버 설정을 구성합니다.
import os
import shlex
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]  # local-server 디렉터리의 절대 경로
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'solar_ems.db'}")  # 환경변수 우선; 생략 시 local-server의 SQLite 파일 사용
APP_NAME = "Solar ESS EMS Local API"  # API 문서에 표시할 서버 이름


# 환경변수를 우선 사용하고, 없으면 실행 위치와 관계없이 서버 전용 .env의 초기 비밀번호를 읽습니다.
def get_initial_admin_password() -> str:
    if "INITIAL_ADMIN_PASSWORD" in os.environ:
        return os.environ["INITIAL_ADMIN_PASSWORD"]

    env_path = BASE_DIR / ".env"  # 서버 전용 초기 관리자 설정 파일
    if not env_path.is_file():
        return ""

    password = ""  # 파일에서 마지막으로 지정한 초기 비밀번호
    for line in env_path.read_text(encoding="utf-8-sig").splitlines():
        key, separator, value = line.strip().removeprefix("export ").partition("=")
        if not separator or key.strip() != "INITIAL_ADMIN_PASSWORD":
            continue
        # 따옴표와 주석만 해석하며 환경변수 치환이나 명령 실행은 하지 않습니다.
        lexer = shlex.shlex(value, posix=True)
        lexer.whitespace_split = True
        lexer.commenters = "#"
        try:
            values = list(lexer)
        except ValueError:
            raise ValueError("Invalid quotes in local-server/.env INITIAL_ADMIN_PASSWORD.") from None
        if len(values) > 1:
            raise ValueError("Quote INITIAL_ADMIN_PASSWORD in local-server/.env when it contains spaces.")
        password = values[0] if values else ""
    return password
