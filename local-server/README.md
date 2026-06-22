# Solar ESS EMS Local Server

Solar ESS EMS MVP용 로컬 FastAPI 서버입니다.

이 서버는 프론트엔드 개발과 MVP 기능 검증을 위한 로컬 API 서버이며, 현재는 SQLite와 가상 데이터를 사용합니다. 실제 Modbus, MQTT, PCS, BMS, 계량기, 센서, SMS, 파일 export 시스템과는 연결하지 않습니다.

---

## 개발 환경

- Python 3.12 권장
- FastAPI
- SQLAlchemy 2.x
- SQLite
- Uvicorn

의존성은 `requirements.txt`에서 관리합니다.

---

## 설치 및 실행

### Windows PowerShell

```powershell
cd local-server
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Linux / WSL

```bash
cd local-server
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

서버 실행 후 API 문서는 아래 주소에서 확인할 수 있습니다.

```text
http://127.0.0.1:8000/docs
```

SQLite 파일은 최초 실행 시 아래 경로에 생성됩니다.

```text
local-server/solar_ems.db
```

---

## 기본 계정

```text
ID: admin
Password: 1111
```

---

## 프로젝트 구조

```text
local-server/
 ├─ requirements.txt                 # Python dependency 목록
 ├─ README.md                        # local server 개발 가이드
 ├─ solar_ems.db                     # SQLite DB 파일. 실행 시 생성되며 commit 금지
 │
 └─ app/
     ├─ main.py                      # FastAPI 앱 생성, CORS 설정, startup 처리, router 등록
     │
     ├─ api/
     │   └─ router.py                # 모든 domain router를 한 곳에서 등록
     │
     ├─ core/
     │   ├─ config.py                # APP_NAME, DATABASE_URL 등 환경 설정
     │   ├─ database.py              # SQLAlchemy engine, SessionLocal, Base, get_db
     │   └─ responses.py             # 공통 응답 helper
     │
     ├─ db/
     │   ├─ base.py                  # SQLAlchemy metadata 등록용 모델 import
     │   └─ init_db.py               # 테이블 생성, 컬럼 보정, seed 데이터 생성
     │
     ├─ shared/
     │   └─ schemas.py               # 여러 domain에서 쓰는 Pydantic 공통 base schema
     │
     └─ domains/
         ├─ auth/                    # 로그인, 사용자 관리
         ├─ project/                 # 프로젝트/설비 설정
         ├─ device/                  # 장비 관리
         ├─ pv_string/               # 태양광 PV string 관리
         ├─ telemetry/               # 최신/이력 계측 데이터
         ├─ dashboard/               # 대시보드 요약
         ├─ solar/                   # 태양광 화면 데이터
         ├─ ess/                     # ESS 시스템 목록, 선택 ESS 상세 모니터링 데이터
         ├─ power_flow/              # 전력 흐름도 및 편집 데이터
         ├─ alarm/                   # 알림 이력
         ├─ maintenance/             # 정비 관리
         ├─ report/                  # 운전 리포트
         ├─ trend/                   # 트렌드 화면 데이터
         └─ simulator/               # 가상 데이터 생성/reset
```

---

## 폴더 역할

### `app/main.py`

FastAPI 앱의 진입점입니다.

담당 역할:

- FastAPI 앱 생성
- CORS 설정
- startup 시 DB table 생성 및 seed 실행
- `api_router` 등록

비즈니스 로직은 `main.py`에 작성하지 않습니다.

---

### `app/api/router.py`

전체 API router를 등록하는 파일입니다.

각 domain의 `router.py`에서 router를 export하고, `api/router.py`에서 include합니다.

```python
from ..domains.device.router import router as devices_router

api_router.include_router(devices_router)
```

규칙:

- API 등록 위치는 `api/router.py` 한 곳으로 통일합니다.
- domain 내부 router는 자기 prefix만 책임집니다.
- legacy route는 유지하지 않습니다.

---

### `app/core/`

서버 전역 기반 코드입니다.

```text
core/
 ├─ config.py       # 환경 설정
 ├─ database.py     # DB 연결, Session, Base
 └─ responses.py    # 공통 응답 형식
```

여기에는 특정 업무 도메인 로직을 넣지 않습니다.

---

### `app/db/`

DB 초기화와 SQLAlchemy 모델 등록을 담당합니다.

```text
db/
 ├─ base.py          # 모든 domain model import. Base.metadata 등록 목적
 └─ init_db.py       # create_tables, seed_database
```

`db/base.py`는 모델을 직접 사용하기 위한 파일이라기보다, SQLAlchemy가 모든 테이블 metadata를 알 수 있도록 domain model을 모아 import하는 파일입니다.

새 model 파일을 추가하면 반드시 `db/base.py`에 import해야 `Base.metadata.create_all()`에서 테이블이 생성됩니다.

---

### `app/shared/`

여러 domain에서 재사용하는 공통 코드입니다.

현재는 Pydantic 공통 base schema를 관리합니다.

```python
class OrmModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())
```

특정 domain에만 필요한 schema, util, 상수는 `shared/`에 두지 않습니다.

---

### `app/domains/ess/`

ESS 화면의 시스템 목록과 선택된 ESS 시스템의 상세 모니터링 데이터를 제공합니다.

현재 ESS는 단일 설비 가정이 아니라 여러 ESS 시스템을 선택할 수 있는 구조로 관리합니다.

주요 책임:

- `ess_systems` 테이블 기반 ESS 시스템 목록 제공
- ESS별 PCS, BMS, Battery 장비 연결 정보 제공
- 선택 ESS의 SOC, SOH, 충전/방전 전력, 온도, 상태 요약 제공
- 선택 ESS 장비 기준 telemetry 조회, 장비별 데이터가 없으면 기존 공통 telemetry로 fallback

주요 API:

```text
GET /api/ess/systems
GET /api/ess/systems/{system_id}/overview
GET /api/ess/overview
```

`/api/ess/overview`는 기존 프론트 호환용으로 첫 번째 ESS 시스템의 overview를 반환합니다.

---

## Domain 구조

기본 domain 구조는 아래를 따릅니다.

```text
domains/{domain}/
 ├─ router.py          # FastAPI endpoint 정의
 ├─ service.py         # 업무 로직, 응답 조립, 예외 처리
 ├─ repository.py      # DB query, insert, update, delete
 ├─ models.py          # SQLAlchemy model
 ├─ schemas.py         # Pydantic request/response schema
 └─ __init__.py
```

모든 domain이 모든 파일을 반드시 가질 필요는 없습니다.

예:

- 단순 조회 domain은 `models.py`, `repository.py` 없이 `router.py`, `service.py`만 가질 수 있습니다.
- DB 테이블이 필요한 domain은 `models.py`, `repository.py`를 둡니다.
- 요청/응답 타입이 필요한 domain은 `schemas.py`를 둡니다.

---

## Layer 역할

### `router.py`

HTTP endpoint만 정의합니다.

담당 역할:

- URL prefix
- HTTP method
- Query/path/body parameter
- `Depends(get_db)`
- service 호출
- 공통 응답 wrapper 적용

예:

```python
router = APIRouter(prefix="/api/devices", tags=["devices"])


@router.get("")
def devices(
    deviceType: str = Query(default=""),
    status: str = Query(default=""),
    keyword: str = Query(default=""),
    db: Session = Depends(get_db),
):
    return ok(get_device_list(db, device_type=deviceType, status=status, keyword=keyword))
```

규칙:

- router에 복잡한 비즈니스 로직을 넣지 않습니다.
- DB query를 router에서 직접 작성하지 않습니다.
- 프론트에서 쓰는 query 이름은 기존 API 계약을 고려해 유지합니다.

---

### `service.py`

업무 로직을 담당합니다.

담당 역할:

- repository 호출 조합
- request body를 저장 가능한 payload로 변환
- response dict 조립
- 존재하지 않는 데이터에 대한 `HTTPException`
- 여러 repository를 묶는 workflow 처리

예:

```python
def get_device_detail(db: Session, device_id: int) -> dict:
    device = get_device(db, device_id)
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return _device_out(device, db)
```

규칙:

- DB query 자체는 repository에 둡니다.
- 화면 응답용 데이터 조립은 service에서 처리합니다.
- 여러 domain의 데이터를 조합해야 할 때는 service에서 조합합니다.

---

### `repository.py`

DB 접근만 담당합니다.

담당 역할:

- SQLAlchemy query
- create/update/delete
- filter/order/join
- commit/refresh 처리

예:

```python
def get_device(db: Session, device_id: int) -> Device | None:
    return db.query(Device).filter(Device.id == device_id).first()
```

규칙:

- HTTP 응답 형식은 repository에서 만들지 않습니다.
- `ok()`를 repository에서 호출하지 않습니다.
- 화면 표시용 문자열 조립은 service에서 처리합니다.
- DB transaction 처리는 현재 단순 MVP 기준으로 repository에서 commit합니다.

---

### `models.py`

SQLAlchemy ORM model을 정의합니다.

규칙:

- SQLAlchemy 2.x 스타일 `Mapped`, `mapped_column`을 사용합니다.
- DateTime 컬럼은 `datetime` 타입을 사용합니다.
- 새 model을 추가하면 `app/db/base.py`에 import합니다.
- 테이블명은 복수형 또는 기존 DB naming을 따릅니다.

예:

```python
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from ...core.database import Base


class Example(Base):
    __tablename__ = "examples"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
```

---

### `schemas.py`

Pydantic request/response schema를 정의합니다.

규칙:

- Request body는 `XxxBody` 또는 `XxxSaveBody` 형식을 사용합니다.
- Response schema는 `XxxOut` 형식을 사용합니다.
- ORM model에서 바로 변환할 schema는 `OrmModel`을 상속합니다.

예:

```python
from ...shared.schemas import OrmModel


class DeviceOut(OrmModel):
    id: int
    name: str
    device_type: str
```

---

## API 응답 규칙

기본 응답 형식은 `core/responses.py`의 `ok()`를 사용합니다.

```python
def ok(data, result_message: str = "SUCCESS"):
    return {"result": "SUCCESS", "resultMessage": result_message, "data": data}
```

응답 예:

```json
{
  "result": "SUCCESS",
  "resultMessage": "SUCCESS",
  "data": {
    "list": [],
    "totalCount": 0
  }
}
```

규칙:

- 정상 응답은 가능하면 `ok(data)`로 감쌉니다.
- 업무 실패를 HTTP error로 볼 수 있으면 `HTTPException`을 사용합니다.
- 프론트는 `result === "SUCCESS"` 기준으로 업무 성공 여부를 판단합니다.

---

## DB 및 Seed 규칙

### DB 연결

DB 연결 정보는 `core/config.py`의 `DATABASE_URL`을 사용합니다.

기본값:

```text
sqlite:///local-server/solar_ems.db
```

환경변수로 대체할 수 있습니다.

```bash
DATABASE_URL=sqlite:///custom.db uvicorn app.main:app
```

### 초기화 흐름

서버 startup 시 `main.py`에서 아래 순서로 실행됩니다.

```text
create_tables()
seed_database(db)
```

`create_tables()`:

- `Base.metadata.create_all()` 실행
- MVP 중간 변경을 위한 일부 컬럼 보정

`seed_database()`:

- 기본 admin 계정 생성
- 프로젝트 설정 생성
- 기본 장비 생성
- PV string 생성
- 오늘의 가상 telemetry, alarm, maintenance, report 생성

### 주의

- `solar_ems.db`는 commit하지 않습니다.
- seed 데이터는 로컬 개발용입니다.
- 실제 운영 DB migration 도구는 아직 적용하지 않았습니다.
- 테이블 컬럼 변경이 많아지면 Alembic 같은 migration 도구 도입을 검토합니다.

---

## 가상 데이터

`domains/simulator/`는 화면 개발용 데이터를 생성합니다.

```text
simulator/
 ├─ generator.py      # 시간대별 PV, ESS, 계통, 알람, 리포트 데이터 생성
 ├─ service.py        # reset/generate workflow
 └─ router.py         # simulator API
```

주요 API:

```text
POST /api/simulator/generate-today
POST /api/simulator/reset
```

---

## 새 Domain 추가 가이드

예를 들어 `energy_policy` domain을 추가할 경우:

```text
domains/energy_policy/
 ├─ router.py
 ├─ service.py
 ├─ repository.py
 ├─ models.py
 ├─ schemas.py
 └─ __init__.py
```

작업 순서:

1. `models.py`에 SQLAlchemy model 작성
2. `schemas.py`에 request/response schema 작성
3. `repository.py`에 DB query 작성
4. `service.py`에 업무 로직 작성
5. `router.py`에 endpoint 작성
6. `db/base.py`에 model import 추가
7. `api/router.py`에 router include 추가
8. `python -m compileall app` 또는 서버 import로 확인

---

## 코딩 규칙

### 파일명

- Python 파일은 `snake_case.py`를 사용합니다.
- domain 폴더명도 `snake_case`를 사용합니다.
- 일반적인 domain 파일명은 아래를 우선 사용합니다.

```text
router.py
service.py
repository.py
models.py
schemas.py
```

특수 목적 파일은 역할이 드러나게 작성합니다.

```text
editor_router.py
editor_service.py
equipment_repository.py
user_service.py
```

---

### 함수명

- Python 함수는 `snake_case`를 사용합니다.
- 조회 함수는 `get_`, `list_`, `count_`, `find_`를 우선 사용합니다.
- 생성/수정/삭제 함수는 `create_`, `update_`, `delete_`, `remove_`, `save_`를 사용합니다.

예:

```python
def list_devices(...):
def get_device(...):
def create_device(...):
def update_device(...):
def delete_device(...):
```

---

### Import 규칙

- domain 내부 참조는 상대 import를 사용합니다.
- 다른 domain model/repository가 필요하면 명시적으로 import합니다.
- `app.models` 같은 중앙 re-export 레이어는 사용하지 않습니다.
- 공통 DB Base는 `core.database.Base`에서 정의하고, 모델 등록은 `db/base.py`에서 처리합니다.

예:

```python
from .models import Device
from ..pv_string.repository import replace_inverter_links
from ...core.database import get_db
```

---

### Type Hint 규칙

- 함수 인자와 반환 타입은 가능한 명시합니다.
- SQLAlchemy model 날짜 컬럼은 `datetime`을 사용합니다.
- Pydantic response schema와 model 타입이 맞도록 관리합니다.

예:

```python
def get_device(db: Session, device_id: int) -> Device | None:
    ...


def get_device_list(db: Session, device_type: str = "", status: str = "", keyword: str = "") -> dict:
    ...
```

---

### Error 처리 규칙

- 존재하지 않는 resource는 service에서 `HTTPException(status_code=404)`를 발생시킵니다.
- repository는 가능하면 `None` 또는 `False`를 반환하고, HTTP 판단은 service에서 합니다.
- router는 복잡한 error 판단을 하지 않습니다.

---

## 검증 명령

### Python compile 확인

```powershell
python -m compileall local-server\app
```

또는 `local-server` 폴더 안에서는:

```powershell
python -m compileall app
```

### FastAPI app import 확인

프로젝트 루트에서:

```powershell
$env:PYTHONPATH='local-server'
python -c "from app.main import app; print(len(app.routes))"
```

### route 확인

```powershell
$env:PYTHONPATH='local-server'
python -c "from app.main import app; print([route.path for route in app.routes])"
```

---

## Commit 금지 파일

아래 파일/폴더는 commit하지 않습니다.

```text
local-server/.venv/
local-server/__pycache__/
local-server/app/**/__pycache__/
local-server/solar_ems.db
```

---

## 핵심 정리

```text
main.py
→ 앱 생성과 startup만 담당

api/router.py
→ 전체 router 등록만 담당

core/
→ 서버 전역 기반 코드

db/
→ 모델 등록, DB 초기화, seed

domains/{domain}/router.py
→ HTTP endpoint

domains/{domain}/service.py
→ 업무 로직과 응답 조립

domains/{domain}/repository.py
→ DB 접근

domains/{domain}/models.py
→ SQLAlchemy model

domains/{domain}/schemas.py
→ Pydantic schema

shared/
→ 여러 domain에서 재사용하는 공통 코드
```

기본 원칙:

```text
1. API endpoint는 router에 둔다.
2. 업무 판단은 service에 둔다.
3. DB query는 repository에 둔다.
4. DB table model은 models.py에 둔다.
5. request/response 타입은 schemas.py에 둔다.
6. 새 model은 db/base.py에 등록한다.
7. 새 router는 api/router.py에 등록한다.
8. legacy API는 다시 만들지 않는다.
```
