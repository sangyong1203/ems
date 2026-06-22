# Solar/ESS EMS MVP 개발 기획 문서

## 1. 프로젝트 개요

### 1.1 프로젝트명

**Solar ESS EMS MVP**

### 1.2 프로젝트 목적

본 프로젝트는 태양광/ESS 구축 프로젝트에 포함하여 발주처에 납품할 수 있는 **단일 현장용 설치형 EMS**를 개발하는 것을 목표로 한다.

초기 MVP는 실제 인버터, PCS, BMS, 계량기, 기상센서 등과 직접 연동하지 않는다. 대신 **가상 데이터 기반**으로 태양광 발전량, ESS 상태, 전력 흐름, 장비 상태, 알림, 정비 이력, 리포트 기능을 구현한다.

향후 실제 프로젝트 수주 시에는 가상 데이터 생성 모듈을 실제 장비 데이터 수집 모듈로 교체하거나 확장하여 현장별 납품형 시스템으로 발전시킨다.

---

## 2. 제품 유형

**EPC 납품형 단일 현장 Solar/ESS EMS**

본 시스템은 하나의 태양광/ESS 구축 현장에 설치되어 발주처가 현장 설비 상태를 확인하고, 기본 운전 현황과 장비/정비 이력을 관리할 수 있도록 하는 설치형 시스템이다.

---

## 3. 주요 고객

### 3.1 1차 고객

**태양광/ESS EPC 업체**

EPC 업체가 태양광/ESS 구축 프로젝트에 포함하여 발주처에 제공할 수 있는 관제·관리 시스템으로 사용한다.

### 3.2 2차 고객

**EPC + O&M 유지보수 겸업 업체**

시공 후 일정 기간 유지보수까지 담당하는 업체가 장비 상태, 알림, 정비 이력, 기본 리포트를 관리하는 용도로 사용할 수 있다.

### 3.3 3차 고객

**발전사업자 또는 산업단지/공장 발주처**

태양광/ESS 설비를 도입한 현장에서 자체적으로 현장 상태를 확인하는 용도로 사용할 수 있다.

---

## 4. 핵심 포지셔닝

본 시스템의 핵심 포지션은 다음과 같다.

> 태양광/ESS 구축 프로젝트에 포함하여 납품 가능한 단일 현장 설치형 EMS MVP

핵심 가치는 다음과 같다.

```text
1. 발주처 검수용 대시보드 제공
2. 태양광/ESS 설비 상태 시각화
3. 전력 흐름 확인
4. 장비 정보 관리
5. 장애/알림 이력 관리
6. 태양광/ESS 정비 이력 관리
7. 리포트 기반 운전 현황 확인
8. 향후 실제 장비 연동 가능 구조
```

---

## 5. MVP 개발 범위

### 5.1 포함 기능

```text
1. 로그인
2. 현장 대시보드
3. 태양광 상태 확인
4. ESS 상태 확인
5. 전력 흐름 확인
6. 트렌드 차트 확인
7. 장비 관리
8. 정비 관리
9. 알림 이력 관리
10. 운전 리포트
11. 가상 데이터 생성
12. 시스템 설정
```

### 5.2 제외 기능

MVP에서는 아래 기능을 제외한다.

```text
1. 실제 Modbus TCP/RTU 연동
2. 실제 MQTT 연동
3. 실제 PCS/BMS 제어
4. 실제 계량기 연동
5. 실제 SMP/REC 자동 수집
6. VPP/전력중개사업자 연계
7. 복잡한 사용자 권한 관리
8. 카카오/SMS 실시간 알림
9. PDF/Excel 자동 출력
10. 부품 재고 관리
11. 정비 사진/첨부파일 업로드
12. 장비 제어 명령 전송
13. 수익 정산 자동화
```

단, 향후 확장 가능하도록 데이터 구조와 폴더 구조는 유연하게 설계한다.

---

## 6. 주요 기술 스택

| 영역 | 기술 |
|---|---|
| Frontend | Vue 3 |
| Build Tool | Vite |
| Language | TypeScript |
| UI Framework | Element Plus |
| Chart | Apache ECharts |
| Backend | FastAPI |
| Database | SQLite |
| ORM | SQLAlchemy |
| Schema Validation | Pydantic |
| API 방식 | REST API |
| 데이터 갱신 | 5초~10초 Polling |
| 인증 | MVP 단순 로그인 또는 Mock Auth |
| 배포 | 로컬 실행 기준, 추후 Docker 가능 |

---

## 7. 시스템 구조

### 7.1 MVP 구조

```text
[Vue 3 + Element Plus Frontend]
              ↓
          REST API
              ↓
       [FastAPI Backend]
              ↓
        [SQLite Database]
              ↑
   [Virtual Data Generator]
```

### 7.2 향후 실제 장비 연동 구조

```text
[Inverter / PCS / BMS / Meter / Sensor]
              ↓
       Modbus TCP/RTU, MQTT, HTTP API
              ↓
        [Device Collector]
              ↓
       [FastAPI Backend]
              ↓
        [Database]
              ↓
        [Vue EMS Dashboard]
```
### 장비 및 데이터 설명 (Inverter / PCS / BMS / Meter / Sensor)
### Inverter, 인버터
태양광 패널에서 만든 DC 전기를 AC 전기로 바꿔주는 장비입니다.

태양광 패널은 직류, 즉 DC 전기를 만듭니다.
하지만 일반 전력망, 공장, 건물 부하는 보통 교류, 즉 AC 전기를 사용합니다.
```text
태양광 패널 DC 전기
→ 인버터
→ AC 전기
→ 부하 또는 계통
```
#### EMS에서 수집하는 데이터
```text
현재 발전 출력 kW
금일 발전량 kWh
누적 발전량 kWh
DC 전압
DC 전류
AC 전압
AC 전류
주파수
인버터 상태
오류코드
통신 상태

```
### PCS, Power Conversion System
ESS 배터리와 전력망/부하 사이에서 전력을 변환하고 충전·방전을 담당하는 장비입니다.

ESS 배터리는 DC 전기를 저장합니다.
하지만 계통이나 부하는 AC를 사용합니다.
PCS는 배터리를 충전할 때는 AC를 DC로 바꾸고, 방전할 때는 DC를 AC로 바꿉니다. 엄밀히 말하면 PCS도 인버터 기능을 포함하지만, ESS에서는 보통 PCS라고 부릅니다

```text
충전 시:
계통/태양광 AC
→ PCS
→ DC
→ 배터리 충전

방전 시:
배터리 DC
→ PCS
→ AC
→ 부하/계통 공급
```

#### EMS에서 수집하는 데이터
```text
충전 전력 kW
방전 전력 kW
PCS 운전 상태
AC 전압
AC 전류
주파수
오류코드
운전 모드
통신 상태
```

### BMS, Battery Management System
ESS 배터리를 안전하게 관리하는 시스템입니다.
ESS 안전과 관련해서 가장 중요한 장비가 BMS입니다.

배터리는 과충전, 과방전, 과열, 셀 전압 불균형이 생기면 위험합니다.
BMS는 배터리 상태를 계속 감시하고 보호합니다.

```text
배터리 셀 상태 감시
배터리 온도 감시
SOC(State of Charge) 계산
SOH(State of Health) 계산
과충전/과방전 보호
셀 밸런싱
경고/차단 신호 발생
```
#### EMS에서 수집하는 데이터
```text
SOC %
SOH %
배터리 전압
배터리 전류
최대 셀 전압
최소 셀 전압
셀 전압 편차
최대 온도
최소 온도
BMS 경고 상태
배터리 랙 상태
```
### Meter, 계량기
전기가 얼마나 흐르는지 측정하는 장비입니다.
전력 흐름 화면에서 Meter 데이터가 중요합니다.

EMS에서는 실제 발전량, 부하 사용량, 계통 송전량, 계통 수전량을 알기 위해 계량기 데이터가 필요합니다.
```text
태양광 발전량 측정
부하 사용량 측정
계통으로 보낸 전력 측정
계통에서 받은 전력 측정
ESS 충전/방전량 측정
```
#### EMS에서 수집하는 데이터
```text
현재 전력 kW
누적 전력량 kWh
전압
전류
역률
주파수
송전량
수전량
```

### Sensor, 센서
현장 환경이나 설비 주변 상태를 측정하는 장비입니다.

태양광/ESS에서는 보통 기상센서와 온도센서가 중요합니다.
```text
왜 필요한가?

발전량 낮음 + 일사량 낮음
→ 날씨 영향 가능성 높음

발전량 낮음 + 일사량 정상
→ 인버터/패널/접속반 문제 가능성 높음
```
#### EMS에서 수집하는 데이터
```text
일사량 W/m²
외기 온도 ℃
모듈 온도 ℃
풍속 m/s
습도 %
ESS실 온도
화재 감지 상태
```
### 전체 관계도
```text
태양광 패널
   ↓ DC
Inverter
   ↓ AC
부하 / 계통

ESS 배터리
   ↓ DC
BMS가 배터리 상태 감시
   ↓
PCS가 충전/방전 전력 변환
   ↓ AC
부하 / 계통

Meter
→ 발전량, 부하, 송전, 수전 측정

Sensor
→ 일사량, 온도, 풍속, ESS실 환경 측정
```
#### EMS 화면과 연결하면
| 장비       | 주로 보이는 화면            |
| -------- | -------------------- |
| Inverter | 태양광 화면, 장비 관리, 알림 이력 |
| PCS      | ESS 화면, 전력 흐름, 장비 관리 |
| BMS      | ESS 화면, 알림 이력, 정비 관리 |
| Meter    | 전력 흐름, 리포트           |
| Sensor   | 태양광, ESS, 트렌드, 알림 이력 |


MVP에서는 `Virtual Data Generator`가 장비 데이터 역할을 수행한다.  
향후에는 `Virtual Data Generator`를 `Modbus Collector`, `MQTT Collector`, `Device API Collector` 등으로 대체할 수 있어야 한다.
```text
용어 설명:
Modbus Collector는 산업 현장의 다양한 센서, PLC, 모터 등 각종 제어 기기에서 Modbus 프로토콜을 사용해 기기 상태와 가동 데이터를 수집(Collecting)하고 저장·전달하는 소프트웨어 및 하드웨어 시스템입니다.
```
---

## 8. 단일 현장 기준 기본 정보

MVP는 하나의 프로젝트 현장만 관리한다.

### 8.1 예시 현장

```text
프로젝트명: 산업단지 태양광 ESS 구축사업
현장명: 김제 스마트팩토리 태양광 ESS
고객사: 샘플에너지 주식회사
시공사: 샘플 EPC
위치: 전라북도 김제시
태양광 용량: 500kW
ESS 용량: 1,000kWh
인버터: 5대
PCS: 1대
BMS: 1식
계량기: 2대
기상센서: 1식
```

---

## 9. 메뉴 구성

최종 메뉴는 아래와 같이 구성한다.

```text
대시보드
태양광
ESS
전력 흐름
트렌드
장비 관리
정비 관리
알림 이력
운전 리포트
설정
```

로그인 화면은 사이드바 메뉴에 포함하지 않는다.

---

## 10. 화면별 기능 정의

### 10.1 로그인

#### 목적

EMS 시스템 접속을 위한 기본 로그인 화면이다.

#### 주요 기능

```text
- ID 입력
- Password 입력
- 로그인 버튼
- 임시 관리자 계정 사용
```

#### MVP 계정 예시

```text
admin / admin1234
```

#### 인증 범위

MVP에서는 Mock 로그인 또는 단순 토큰 인증으로 구현한다.  
JWT, refresh token, 권한별 메뉴 제어는 후속 단계에서 검토한다.

---

### 10.2 대시보드

#### 목적

단일 현장의 태양광/ESS 전체 운전 상태를 한눈에 확인한다.  
가장 중요한 데모 화면이다.

#### 표시 항목

```text
- 프로젝트명
- 현장명
- 태양광 설비 용량
- ESS 설비 용량
- 현재 운전 상태
- 최근 갱신 시간
- 현재 태양광 발전 출력
- 금일 발전량
- 누적 발전량
- ESS SOC
- ESS 충전/방전 상태
- ESS 충전/방전 전력
- PCS 상태
- BMS 상태
- 인버터 정상/장애 수
- 현재 부하 사용량
- 계통 송전/수전 전력
- 최근 알림
- 최근 정비 일정
```

#### 핵심 역할

대시보드는 EPC 업체가 발주처에게 가장 먼저 보여줄 수 있는 대표 데모 화면이다.  
따라서 시각적 완성도와 핵심 상태값의 가독성이 중요하다.

---

### 10.3 태양광

#### 목적

태양광 인버터 및 발전 상태를 상세 확인한다.

#### 표시 항목

```text
- 전체 태양광 현재 출력
- 금일 발전량
- 누적 발전량
- 인버터별 출력
- DC 전압
- DC 전류
- AC 전압
- AC 전류
- 주파수
- 인버터 상태
- 오류코드
- 최근 수신 시간
```

#### 인버터 상태 예시

```text
정상
출력저하
과전압
저전압
통신장애
정지
```

---

### 10.4 ESS

#### 목적

ESS, PCS, BMS 상태를 상세 확인한다.

#### 표시 항목

```text
- ESS SOC
- ESS SOH
- 충전 전력
- 방전 전력
- 배터리 전압
- 배터리 전류
- 배터리 온도
- PCS 상태
- BMS 상태
- 운전 모드
- 최대 셀 전압
- 최소 셀 전압
- 최대 온도
- 최소 온도
```

#### ESS 운전 모드

```text
자동
수동
충전
방전
대기
장애
```

---

### 10.5 전력 흐름

#### 목적

태양광, ESS, 부하, 계통 간 전력 흐름을 시각적으로 보여준다.

#### 표시 항목

```text
- 태양광 발전 전력
- ESS 충전 전력
- ESS 방전 전력
- 부하 소비 전력
- 계통 송전 전력
- 계통 수전 전력
```

#### 전력 흐름 예시

```text
태양광 발전: 382kW
부하 사용: 260kW
ESS 충전: 120kW
계통 송전: 2kW
```

#### MVP 구현 방향

복잡한 SVG 애니메이션보다는 아래 정도의 구조를 우선 구현한다.

```text
태양광 카드
ESS 카드
부하 카드
계통 카드
화살표 라인
현재 kW 표시
충전/방전/송전/수전 상태 색상 표시
```
#### EMS(에너지 관리 시스템)의 우선순위 로직
태양광-ESS 연계 시스템에서 EMS는 보통 아래와 같은 우선순위 알고리즘으로 전력 흐름을 제어합니다.
1순위 (자체 소비): PV 전력으로 공장·빌딩 내부의 부하(소비처)를 먼저 커버합니다.
2순위 (ESS 충전): 남는 PV 전력으로 ESS를 충전합니다.
3순위 (PV 직접 송전): ESS가 꽉 차면(SOC 100%), 남는 PV 전력을 계통으로 직접 보냅니다.
4순위 (ESS 밤간 송전): 야간이나 전력 피크 타임에 ESS 전력을 계통으로 보냅니다. 이 부분은 기능은 활성/비활성을 설정할 수 있다.
---

### 10.6 트렌드

#### 목적

시간대별 주요 데이터를 차트로 확인한다.

#### 차트 항목

```text
- 태양광 발전 출력 차트
- ESS SOC 차트
- ESS 충전/방전 차트
- 배터리 온도 차트
- 계통 송수전 차트
- 부하 사용량 차트
```

#### 필터

```text
- 오늘
- 최근 7일
- 최근 30일
- 사용자 지정 기간
- 데이터 항목 선택
```

#### 개발 우선순위

트렌드 화면은 필요하지만, 대시보드/태양광/ESS/전력 흐름/장비 관리/알림 이력보다 우선순위는 낮다.

---

### 10.7 장비 관리

#### 목적

현장에 설치된 장비 정보를 등록, 수정, 조회한다.

#### 장비 유형

```text
태양광 인버터
PCS
BMS
계량기
기상센서
접속반
부하 계측기
계통 계측기
```

#### 장비 목록 컬럼

```text
- 장비 유형
- 장비명
- 제조사
- 모델명
- 시리얼 번호
- 정격용량
- 설치 위치
- 통신 방식
- 상태
- 최근 수신 시간
- 관리 버튼
```

#### 장비 등록/수정 항목

```text
기본 정보
- 장비 유형
- 장비명
- 제조사
- 모델명
- 시리얼 번호
- 정격 용량
- 설치 위치
- 설치일

통신 정보
- 통신 방식
- IP 주소
- Port
- Slave ID
- Protocol

보증/관리 정보
- 보증 시작일
- 보증 종료일
- 담당 업체
- 담당자 연락처
- 메모
```
```text
용어 설명:
Slave ID는 주로 산업용 Modbus 프로토콜에서 데이터를 주고받을 때 여러 기기 중 "통신할 특정 기기를 지목하기 위한 고유 식별 번호(주소)"를 말한다.
```
---

### 10.8 정비 관리

#### 목적

태양광/ESS 장비의 정기점검, 장애점검, 수리, 부품교체 이력을 관리한다.

#### MVP 범위

MVP에서는 정비 업무관리 시스템 수준까지 확장하지 않고, **정비 이력 관리 중심**으로 구현한다.

#### 정비 유형

```text
정기점검
장애점검
수리
부품교체
청소
성능점검
배터리점검
통신점검
기타
```

#### 정비 상태

```text
예정
진행중
완료
보류
취소
```

#### 정비 이력 목록 컬럼

```text
- 정비일
- 장비명
- 장비 유형
- 정비 유형
- 정비 제목
- 정비 상태
- 담당자
- 다음 점검일
- 관리 버튼
```

#### MVP 정비 등록 항목

```text
- 정비 대상 장비
- 정비 유형
- 정비 제목
- 정비 내용
- 조치 내용
- 정비 상태
- 정비일
- 다음 점검 예정일
- 담당자
- 비고
```

#### 후속 단계로 미루는 항목

```text
- 교체 부품 상세
- 정비 비용 분석
- 첨부파일/사진 업로드
- 부품 재고
- 정비 업체별 비용 분석
```

---

### 10.9 알림 이력

#### 목적

장비 장애, 통신 장애, ESS 경고 등 이벤트를 확인하고 처리한다.

#### 알림 유형

```text
인버터 장애
통신 장애
발전량 저하
ESS 과온
SOC 낮음
PCS 장애
BMS 경고
계량기 오류
데이터 수신 지연
```

#### 알림 등급

```text
정보
주의
심각
```

#### 처리 상태

```text
미확인
확인
처리중
완료
```

#### 주요 기능

```text
- 알림 목록 조회
- 알림 상세 확인
- 알림 확인 처리
- 알림 완료 처리
- 알림에서 정비 등록
```

#### 알림 → 정비 등록 자동 입력 항목

알림에서 정비 등록을 생성할 때 아래 값을 자동 입력한다.

```text
- 장비명
- 알림 유형
- 알림 메시지
- 발생 시간
- 정비 유형: 장애점검
- 정비 제목: 알림 메시지 기반 자동 생성
```

---

### 10.10 운전 리포트

#### 목적

단일 현장의 운전 현황, 발전량, ESS 충방전, 알림, 정비 이력을 요약해서 보여준다.

#### 리포트 성격

운전 리포트는 운영 보고서보다는 **검수/데모용 운전 현황 요약** 성격으로 구성한다.

#### MVP 리포트 항목

```text
- 운전 상태 요약
- 장비 정상/장애 요약
- 일간 발전량
- 월간 발전량
- ESS 충전량
- ESS 방전량
- 계통 송전량
- 계통 수전량
- 알림 발생 건수
- 심각 알림 건수
- 정비 건수
- 완료된 정비
- 미완료 정비
- 주요 장비 상태
```

#### 제외 기능

MVP에서는 PDF/Excel 출력은 제외하고 화면 조회까지만 구현한다.

---

### 10.11 설정

#### 목적

프로젝트 현장 정보, 설비 정보, UI 설정, 가상 데이터 생성 기능을 관리한다.

#### 설정 영역

```text
1. 프로젝트 정보
2. 설비 정보
3. UI 설정
4. 가상 데이터 관리
```

#### 프로젝트 정보

```text
- 프로젝트명
- 현장명
- 고객사명
- 시공사명
- 위치
```

#### 설비 정보

```text
- 태양광 설비 용량
- ESS 용량
- 인버터 수
- PCS 수
- BMS 수
- 계량기 수
```

#### UI 설정

```text
- 시스템 이름
- 로고 이미지 경로
- 배경 이미지 경로
- 데이터 갱신 주기
```

#### 가상 데이터 관리

```text
- 오늘 데이터 생성
- 최근 7일 데이터 생성
- 알림 데이터 생성
- 정비 데이터 생성
- 전체 데이터 초기화
```

---

## 11. 가상 데이터 설계

### 11.1 가상 데이터 목적

실제 장비 연동 전에도 EMS 화면을 검증하고 EPC 업체에게 데모를 보여줄 수 있어야 한다.

### 11.2 생성 데이터

```text
- 태양광 발전량
- 인버터별 출력
- ESS SOC/SOH
- ESS 충전/방전 전력
- PCS/BMS 상태
- 계통 송수전
- 부하 사용량
- 배터리 온도
- 알림 이벤트
- 정비 이력
```

### 11.3 태양광 발전량 패턴

태양광 데이터는 실제처럼 보여야 한다.

```text
밤: 0kW
아침: 천천히 증가
정오: 최대 출력 근처
오후: 점진적 감소
저녁: 0kW
```

예시:

```text
06:00  20kW
08:00  120kW
10:00  330kW
12:00  480kW
14:00  420kW
16:00  180kW
18:00  30kW
20:00  0kW
```

### 11.4 ESS 데이터 패턴

ESS 데이터는 태양광 발전과 연동되어야 한다.

```text
오전: 대기 또는 충전 시작
낮: 태양광 발전량 증가 → ESS 충전
오후: SOC 증가
저녁: 방전
밤: 대기
```

예시:

```text
09:00 SOC 35%, 충전 시작
12:00 SOC 62%, 충전 중
15:00 SOC 88%, 충전 제한
18:00 SOC 82%, 방전 시작
21:00 SOC 48%, 방전 종료
```

### 11.5 전력 흐름 계산 예시

#### 충전 상황

```text
태양광 발전량 = 382kW
부하 사용량 = 260kW
ESS 충전량 = 120kW
계통 송전량 = 2kW
```

계산식:

```text
계통 송전 = 태양광 발전 - 부하 사용 - ESS 충전
```

#### 방전 상황

```text
부하 사용량 = 300kW
태양광 발전량 = 80kW
ESS 방전량 = 180kW
계통 수전량 = 40kW
```

계산식:

```text
계통 수전 = 부하 사용 - 태양광 발전 - ESS 방전
```

### 11.6 알림 데이터 예시

```text
- 인버터 #2 통신 장애
- PCS 과전압 경고
- BMS 배터리 온도 상승
- 발전량 예상 대비 40% 저하
- ESS SOC 20% 이하
- 계량기 데이터 수신 지연
```

### 11.7 정비 데이터 예시

```text
정비 유형: 장애점검
장비: 인버터 #2
증상: 출력 0kW 지속
원인: DC 입력 퓨즈 단선
조치: 퓨즈 교체
정비 후 상태: 정상
```

```text
정비 유형: 배터리점검
장비: BMS #1
증상: 특정 셀 전압 편차 증가
원인: 셀 밸런싱 필요
조치: BMS 밸런싱 수행
정비 후 상태: 정상 감시
```

---

## 12. 데이터베이스 설계 초안

SQLite 기준 MVP 테이블은 다음과 같다.

```text
users
project_config
devices
telemetry_latest
telemetry_history
alarms
maintenance_records
maintenance_parts
daily_reports
```

### 12.1 users

```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  role TEXT NOT NULL DEFAULT 'admin',
  created_at TEXT NOT NULL
);
```

### 12.2 project_config

```sql
CREATE TABLE project_config (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  project_name TEXT NOT NULL,
  site_name TEXT NOT NULL,
  location TEXT,
  customer_name TEXT,
  contractor_name TEXT,
  solar_capacity_kw REAL NOT NULL,
  ess_capacity_kwh REAL NOT NULL,
  system_name TEXT DEFAULT 'Solar ESS EMS',
  background_image_path TEXT,
  logo_image_path TEXT,
  data_refresh_interval INTEGER DEFAULT 5000,
  dashboard_refresh_interval INTEGER DEFAULT 5000,
  solar_refresh_interval INTEGER DEFAULT 5000,
  ess_refresh_interval INTEGER DEFAULT 5000,
  power_flow_refresh_interval INTEGER DEFAULT 5000,
  trend_refresh_interval INTEGER DEFAULT 5000,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
```

### 12.3 devices

```sql
CREATE TABLE devices (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  device_type TEXT NOT NULL,
  name TEXT NOT NULL,
  manufacturer TEXT,
  model_name TEXT,
  serial_number TEXT,
  capacity REAL,
  capacity_unit TEXT,
  install_location TEXT,
  install_date TEXT,
  communication_type TEXT,
  ip_address TEXT,
  port INTEGER,
  slave_id INTEGER,
  protocol TEXT,
  status TEXT NOT NULL DEFAULT 'NORMAL',
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  warranty_start_date TEXT,
  warranty_end_date TEXT,
  vendor_name TEXT,
  vendor_contact TEXT,
  memo TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
```

### 12.4 telemetry_latest

```sql
CREATE TABLE telemetry_latest (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  device_id INTEGER,
  metric_key TEXT NOT NULL,
  metric_value REAL NOT NULL,
  unit TEXT,
  measured_at TEXT NOT NULL,
  FOREIGN KEY (device_id) REFERENCES devices(id)
);
```

### 12.5 telemetry_history

```sql
CREATE TABLE telemetry_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  device_id INTEGER,
  metric_key TEXT NOT NULL,
  metric_value REAL NOT NULL,
  unit TEXT,
  measured_at TEXT NOT NULL,
  FOREIGN KEY (device_id) REFERENCES devices(id)
);
```

### 12.6 alarms

```sql
CREATE TABLE alarms (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  device_id INTEGER,
  severity TEXT NOT NULL,
  alarm_type TEXT NOT NULL,
  message TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'OPEN',
  occurred_at TEXT NOT NULL,
  acknowledged_at TEXT,
  resolved_at TEXT,
  FOREIGN KEY (device_id) REFERENCES devices(id)
);
```

### 12.7 maintenance_records

```sql
CREATE TABLE maintenance_records (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  device_id INTEGER,
  alarm_id INTEGER,
  maintenance_type TEXT NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  cause TEXT,
  action_taken TEXT,
  before_status TEXT,
  after_status TEXT,
  status TEXT NOT NULL DEFAULT 'SCHEDULED',
  maintenance_date TEXT,
  next_maintenance_date TEXT,
  manager_name TEXT,
  contractor_name TEXT,
  cost REAL DEFAULT 0,
  memo TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (device_id) REFERENCES devices(id),
  FOREIGN KEY (alarm_id) REFERENCES alarms(id)
);
```

#### MVP 주의

`maintenance_records` 테이블에는 향후 확장을 고려해 `cause`, `before_status`, `after_status`, `cost`, `contractor_name` 등을 둘 수 있다.  
다만 MVP 화면에서는 모든 항목을 반드시 노출하지 않아도 된다.

### 12.8 maintenance_parts

```sql
CREATE TABLE maintenance_parts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  maintenance_id INTEGER NOT NULL,
  part_name TEXT NOT NULL,
  quantity INTEGER NOT NULL DEFAULT 1,
  unit_price REAL DEFAULT 0,
  memo TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY (maintenance_id) REFERENCES maintenance_records(id)
);
```

#### MVP 주의

`maintenance_parts`는 후속 확장을 위한 테이블이다.  
MVP 화면에서는 부품 재고 및 부품 상세 관리는 제외한다.

### 12.9 daily_reports

```sql
CREATE TABLE daily_reports (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  report_date TEXT NOT NULL,
  generation_kwh REAL NOT NULL DEFAULT 0,
  ess_charge_kwh REAL NOT NULL DEFAULT 0,
  ess_discharge_kwh REAL NOT NULL DEFAULT 0,
  grid_export_kwh REAL NOT NULL DEFAULT 0,
  grid_import_kwh REAL NOT NULL DEFAULT 0,
  alarm_count INTEGER NOT NULL DEFAULT 0,
  maintenance_count INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL
);
```

---

## 13. 구현 API 명세

### 13.1 Auth

```text
POST /api/auth/login
GET  /api/auth/me
```

### 13.2 Project

```text
GET /api/project
PUT /api/project
```

### 13.3 Dashboard

```text
GET /api/dashboard/summary
GET /api/dashboard/power-flow
GET /api/dashboard/recent-alarms
GET /api/dashboard/recent-maintenance
```

### 13.4 Devices

```text
GET    /api/devices
GET    /api/devices/{device_id}
POST   /api/devices
PUT    /api/devices/{device_id}
DELETE /api/devices/{device_id}
```

장비 목록 API는 다음 검색 조건을 지원한다.

```text
deviceType
status
keyword
```

`keyword`는 장비명, 제조사, 모델명, 시리얼 번호, 설치 위치를 대상으로 대소문자 구분 없이 부분 일치 검색한다.

### 13.5 Solar / ESS / Power Flow / Trend

```text
GET /api/solar/overview
GET /api/ess/overview
GET /api/power-flow/overview
GET /api/trend/overview
```

각 overview API는 화면 데이터와 해당 화면의 `refreshInterval`을 함께 반환한다.

### 13.6 Telemetry

```text
GET /api/telemetry/latest
GET /api/telemetry/history
GET /api/telemetry/power-flow
```

### 13.7 Alarms

```text
GET  /api/alarms
GET  /api/alarms/{alarm_id}
PUT  /api/alarms/{alarm_id}/ack
PUT  /api/alarms/{alarm_id}/resolve
POST /api/alarms/{alarm_id}/maintenance
```

알림 목록 API는 검색어, 장비, 등급, 알림 유형, 상태, 기간 필터를 지원한다.

### 13.8 Maintenance

```text
GET    /api/maintenance
GET    /api/maintenance/{maintenance_id}
POST   /api/maintenance
PUT    /api/maintenance/{maintenance_id}
DELETE /api/maintenance/{maintenance_id}
```

정비 목록 API는 검색어, 장비, 정비 유형, 상태, 기간 필터를 지원한다.

### 13.9 Reports

```text
GET /api/reports/daily
GET /api/reports/summary
GET /api/reports/statistics
```

### 13.10 Simulator

```text
POST /api/simulator/generate-today
POST /api/simulator/generate-last-7-days
POST /api/simulator/generate-alarms
POST /api/simulator/generate-maintenance
POST /api/simulator/reset
```

---

## 14. 현재 MVP 구현 기준 명세

이 절은 초기 기획 이후 구현 과정에서 구체화된 기능과 데이터 규칙을 정리한다.
앞 절의 초기 설명과 내용이 다른 경우 이 절의 내용을 현재 MVP 기준으로 적용한다.

### 14.1 메뉴별 주요 기능

| 메뉴 | 주요 기능 |
|---|---|
| 대시보드 | 태양광 발전, ESS SOC 및 충방전, 부하, 미처리 알림, 인버터 상태, 최근 알림, 정비 일정 요약 |
| 태양광 | 현재 발전량, 설비 대비 출력, 일일 및 누적 발전량, 인버터별 출력과 상태, 인버터 정상 비율 |
| ESS | SOC, SOH, 충방전 전력, 일일 충방전량, 배터리 전압·전류·온도, PCS/BMS 상태 |
| 전력 흐름 | 태양광, ESS, 부하, 계통 간 실시간 전력 이동량과 계통 송수전 상태 |
| 트렌드 | 태양광 출력, ESS 충방전, ESS SOC, 계통 송수전, 부하, 배터리 온도 추이 |
| 장비 관리 | 장비 검색·필터, 등록·수정·삭제, 운영 활성화 전환, 통신 및 보증 정보 관리 |
| 정비 관리 | 정비 검색·필터, 등록·수정·삭제, 정비 상태 관리, 알림 기반 정비 연결 |
| 알림 이력 | 알림 검색·필터, 확인 처리, 연결 정비 등록, 정비 진행 상태 확인 |
| 운전 리포트 | 기간별 에너지 집계, 운전 요약, 부하·발전·ESS·계통·알림 통계 차트 |
| 설정 | 프로젝트 정보, 설비 집계, 화면별 모니터링 주기, 가상 데이터 생성 및 초기화 |

### 14.2 전력 흐름 제어 정책

태양광-ESS 연계 시스템의 전력 배분 우선순위는 다음과 같다.

```text
1순위: PV 발전 전력을 내부 부하에 우선 공급
2순위: 잔여 PV 전력으로 ESS 충전
3순위: ESS 충전 이후 잔여 PV 전력을 계통으로 송전
4순위: 부하 부족분을 ESS 방전으로 공급
5순위: PV 및 ESS로 충족하지 못한 부하를 계통 수전으로 공급
```

ESS 전력을 계통으로 직접 송전하는 기능은 정책 옵션으로 구분한다.
현재 MVP에서는 `essGridExportEnabled = false`로 비활성화되어 있으며, 향후 운영 정책 설정으로 확장한다.

#### 전력 흐름 계산

```text
PV → 부하   = min(PV 발전량, 부하 사용량)
PV → ESS    = min(ESS 충전량, PV 잔여량)
PV → 계통   = PV 잔여량
ESS → 부하  = min(ESS 방전량, 부하 부족량)
ESS → 계통  = ESS 방전 잔여량, 단 정책 활성화 시에만 허용
계통 → 부하 = PV 및 ESS 공급 이후 남은 부하 부족량
계통 송전   = PV → 계통 + ESS → 계통
```

### 14.3 장비 활성화와 설비 용량

장비의 물리적 설치 여부와 EMS 운영 포함 여부를 구분하기 위해 `devices.is_active`를 사용한다.

```text
설치 용량: 등록된 전체 장비의 정격 용량 합계
운영 가능 용량: is_active = true인 장비의 정격 용량 합계
```

현재 집계 기준은 다음과 같다.

| 구분 | 집계 대상 | 단위 |
|---|---|---|
| 태양광 설치 용량 | 전체 인버터 | kW |
| 태양광 운영 가능 용량 | 활성 인버터 | kW |
| ESS 설치 용량 | 전체 BMS | kWh |
| ESS 운영 가능 용량 | 활성 BMS | kWh |

장비 관리 화면에서 각 장비의 운영 활성화 여부를 직접 변경할 수 있다.

### 14.4 주요 계측 데이터

실시간 값은 `telemetry_latest`, 이력 값은 `telemetry_history`에 저장한다.
두 테이블은 공통적으로 `device_id`, `metric_key`, `metric_value`, `unit`, `measured_at`을 사용한다.

| metric_key | 설명 | 단위 |
|---|---|---|
| `solar_power_kw` | 태양광 현재 발전 출력 | kW |
| `solar_today_kwh` | 태양광 금일 누적 발전량 | kWh |
| `solar_total_kwh` | 태양광 전체 누적 발전량 | kWh |
| `inverter_power_kw` | 인버터별 현재 출력 | kW |
| `load_power_kw` | 현재 부하 전력 | kW |
| `grid_export_kw` | 계통 송전 전력 | kW |
| `grid_import_kw` | 계통 수전 전력 | kW |
| `ess_soc` | ESS 충전 상태 | % |
| `ess_soh` | ESS 건강 상태 | % |
| `ess_charge_kw` | ESS 충전 전력 | kW |
| `ess_discharge_kw` | ESS 방전 전력 | kW |
| `battery_voltage_v` | 배터리 전압 | V |
| `battery_current_a` | 배터리 전류 | A |
| `battery_temperature_c` | 배터리 온도 | ℃ |
| `ambient_temperature_c` | 외기온 | ℃ |
| `pv_module_temperature_c` | 태양광 모듈 온도 | ℃ |
| `inverter_temperature_c` | 인버터 온도 | ℃ |

### 14.5 알림과 정비 연결

알림에서 정비 등록을 실행하면 `maintenance_records.alarm_id`로 정비 이력이 연결된다.
이미 연결 정비가 있으면 중복 생성하지 않고 기존 정비를 반환한다.

알림 화면의 조치 상태는 알림 상태와 연결 정비 상태를 함께 사용하여 계산한다.

| 조건 | 화면 표시 |
|---|---|
| 알림 `OPEN` | 미확인 |
| 알림 `ACKED` + 연결 정비 없음 | 확인됨 |
| 연결 정비 `SCHEDULED` | 정비등록 |
| 연결 정비 `IN_PROGRESS` | 조치중 |
| 연결 정비 `COMPLETED` | 조치완료 |
| 연결 정비 `HOLD` | 보류 |
| 연결 정비 `CANCELED` | 취소 |

알림 이력은 장애 발생과 확인 여부를 관리하고, 실제 조치 완료 처리는 정비 관리에서 수행한다.

### 14.6 모니터링 데이터 갱신 주기

모니터링 주기는 프로젝트 설정에서 화면별로 관리한다.

| 필드 | 적용 화면 |
|---|---|
| `dashboard_refresh_interval` | 대시보드 |
| `solar_refresh_interval` | 태양광 |
| `ess_refresh_interval` | ESS |
| `power_flow_refresh_interval` | 전력 흐름 |
| `trend_refresh_interval` | 트렌드 |

선택 가능한 주기는 3초, 5초, 10초, 30초, 1분, 5분, 10분이다.
기존 `data_refresh_interval`은 하위 호환을 위해 유지한다.

### 14.7 운전 통계 리포트

운전 리포트는 일일 조회와 기간 조회를 지원한다.

#### 기간 집계 항목

```text
태양광 발전량
ESS 충전량
ESS 방전량
계통 송전량
계통 수전량
총 부하량
알림 건수
정비 건수
```

#### 통계 차트

| 차트 | 표시 데이터 |
|---|---|
| 부하 통계 | 총 부하, 태양광 공급량, 계통 공급량, ESS 공급량 |
| 태양광 발전량 통계 | 태양광 발전량, 외기온 |
| ESS 충방전 통계 | 충전량, 방전량, SOC |
| 계통 송수전 통계 | 송전량, 수전량 |
| 에너지 자립률 추이 | 태양광 공급량 / 총 부하량 |
| 일별 알림 통계 | 날짜별 알림 발생 건수 |
| 알림 등급 분포 | 심각, 주의, 정보 등급별 알림 건수 |

### 14.8 가상 데이터 생성 범위

현재 MVP는 실제 장비 연동 대신 가상 데이터 생성기를 사용한다.

```text
오늘 데이터 생성
최근 7일 데이터 생성
알림 데이터 생성
정비 데이터 생성
전체 가상 데이터 초기화
```

가상 데이터 생성기는 향후 Modbus TCP/RTU, MQTT 또는 장비별 API 수집 모듈로 교체할 수 있도록 분리한다.

### 14.9 후속 개발 항목

현재 MVP 이후 우선 검토할 항목은 다음과 같다.

```text
1. 실제 인버터, PCS, BMS, 계량기, 센서 연동
2. ESS 계통 직접 송전 정책 설정 및 운전 스케줄
3. 사용자 권한별 메뉴와 기능 제어
4. 알림 외부 발송 연동
5. PDF/Excel 리포트 출력
6. 장비별 통신 장애 감시와 수집 품질 관리
7. 정비 비용, 부품 재고, 첨부 파일 관리
```

---
