
Solar ESS EMS MVP 기획 문서를 기준으로 FastAPI 백엔드 MVP 골격을 생성하세요.

목표:
- project root 하위에 local-server/ 폴더를 생성한다.
- FastAPI + SQLite + SQLAlchemy + Pydantic 기반 백엔드 구조를 만든다.
- 실제 장비 연동은 하지 않는다.
- Virtual Data Generator 기반의 샘플 데이터를 사용한다.
- 프론트엔드가 호출할 수 있는 REST API 기본 구조를 만든다.

기술 스택:
- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- Uvicorn

생성할 구조:
local-server/
  requirements.txt
  app/
    main.py
    core/
      config.py
      database.py
    models/
      user.py
      project_config.py
      device.py
      telemetry.py
      alarm.py
      maintenance.py
      report.py
    schemas/
      common.py
      auth.py
      project.py
      device.py
      telemetry.py
      alarm.py
      maintenance.py
      report.py
    routers/
      auth.py
      project.py
      dashboard.py
      devices.py
      telemetry.py
      alarms.py
      maintenance.py
      reports.py
      simulator.py
    services/
      dashboard_service.py
      telemetry_service.py
      simulator_service.py
    repositories/
      device_repository.py
      telemetry_repository.py
      alarm_repository.py
      maintenance_repository.py
      report_repository.py
    simulator/
      generator.py
    seed.py

이번 작업 범위:
1. FastAPI 앱 실행 가능하게 구성
2. SQLite 연결 구성
3. SQLAlchemy Base/session 구성
4. 주요 모델 정의
   - users
   - project_config
   - devices
   - telemetry_latest
   - telemetry_history
   - alarms
   - maintenance_records
   - maintenance_parts
   - daily_reports
5. 기본 seed 데이터 생성
   - admin / 1111
   - 샘플 프로젝트 현장
   - Inverter 5대
   - PCS 1대
   - BMS 1식
   - Grid Meter 1대
   - Load Meter 1대
   - Weather Sensor 1식
6. 최소 API 구현
   - POST /api/auth/login
   - GET /api/project
   - GET /api/devices
   - GET /api/dashboard/summary
   - GET /api/dashboard/power-flow
   - POST /api/simulator/generate-today
   - POST /api/simulator/reset
7. CORS 설정
   - Vue 개발 서버에서 호출 가능하게 허용
8. local-server/README.md 작성
   - 설치 방법
   - 실행 방법
   - 기본 계정
   - API 확인 방법

중요 규칙:
- 백엔드는 local-server/ 안에서만 작업하세요.
- 실제 Modbus, MQTT, 장비 제어, SMS, PDF/Excel 출력은 구현하지 마세요.
- 우선 실행 가능한 백엔드 골격과 샘플 API를 만드는 것이 목표입니다.