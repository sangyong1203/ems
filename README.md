# Solar Vue Framework

Solar 관리 화면을 위한 Vue 3 기반 프론트엔드 프로젝트입니다. Vite, TypeScript, Vue Router, Pinia, Element Plus, SCSS를 사용합니다.

## 개발 환경

- Node.js 22.x 권장
- npm 10.x 이상 권장
- 백엔드 API 서버 필요

## 주요 기술

- Vue 3
- TypeScript
- Vite
- Vue Router
- Pinia
- Element Plus
- SCSS
- Axios
- ECharts
- dayjs

## 설치 및 실행

### 프론트 실행

```bash
npm install
npm run dev
```

npm 스크립트:
```bash
npm run dev          # 개발 서버 실행
npm run build        # 프로덕션 빌드
npm run preview      # 빌드 결과 미리보기
npm run type-check   # TypeScript 타입 검사
npm run lint         # ESLint 자동 수정
npm run format       # src 디렉터리 Prettier 포맷
```

### local server 실행 

```bash
cd local-server
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 기본 로그인 계정:

- ID: admin
- Password: 1111

### Docker Linux 배포

Docker Desktop을 실행한 뒤 Linux amd64 배포 패키지를 생성한후 Linux 서버에 복사해서 배포한다.

Linux 서버에는 Docker Engine과 Docker Compose plugin만 설치하면 된다. Node.js와 Python은 별도로 설치하지 않는다.

상세 배포 방법은 `deploy/README.md`를 참고한다.

#### Linux 배포 패키지 생성

Docker 실행후 프로젝트 루트에서 아래 명령을 실행하여 생성한다.

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\package-docker-linux.ps1
```

일반적인 Intel 또는 AMD 기반 Linux 서버는 `amd64` 패키지를 사용한다.

생성 파일:

```text
release/solar-ems-linux-amd64-deploy.zip
```

ZIP 내부 구성:

```text
solar-ems-images-linux-amd64.tar
compose.deploy.yaml
README.md
```
---

## Frontend Folder Structure Guide

이 프로젝트는 Vue 3 기반의 관리자/관제 시스템을 기준으로 한다.

폴더 구조의 목적은 처음부터 복잡하게 나누는 것이 아니라, 프로젝트가 커졌을 때도 **파일 위치를 예측하기 쉽고, 수정 범위가 명확한 구조**를 만드는 것이다.

핵심 원칙은 다음과 같다.

```text
화면은 pages/에 둔다.
공통 UI, 공통 로직, 공통 타입, Utils 등은 shared/에 둔다.
여러 화면에 쓰는 UI뿐 아니라 로직도 포함한 기능 덩어리는 features/에 둔다.
API 통신 공통 계층은 src/http/에 둔다.
메뉴별 api.ts, types.ts, mapper.ts, store.ts, constants.ts는 해당 메뉴의 service/에 둔다.
화면 기능 로직 분리 필요시 composables/로 분리한다.
전역 상태는 stores/에 둔다.
```

> 참고: 일반적인 대형 프로젝트에서는 공통 통신 계층을 `services/http/`로 분리하기도 한다.  
> 이 프로젝트에서는 기존 구조에 맞춰 `src/http/index.ts`의 `fetchApi()`를 공통 통신 계층으로 사용한다.

---

## 프로젝트 구조 

### 기본 구조

```text
src/
 ├─ main.ts                         // Vue 앱 진입점. 앱 생성, router, Pinia, 전역 스타일 등록
 ├─ App.vue                         // 최상위 루트 컴포넌트. 일반적으로 RouterView만 배치
 │
 ├─ http/                           // API 공통 통신 계층. fetchApi, 에러 처리, 공통 타입 관리
 │   ├─ index.ts                    // fetchApi 생성 및 HTTP 요청 공통 함수
 │   ├─ handleError.ts              // 공통 API 에러 처리 로직
 │   └─ type.ts                     // APIResponse, PayloadModel 등 HTTP 공통 타입
 │
 ├─ router/                         // Vue Router 설정
 │   ├─ index.ts                    // Router 생성 및 guard
 │   └─ routes.ts                   // 라우트 목록 정의
 │
 ├─ layouts/                        // 화면 전체 골격을 구성하는 레이아웃 컴포넌트
 │   ├─ MainLayout.vue              // 메인 화면 전체 골격 레이아웃. 로그인 후 메인 화면.
 │   ├─ AuthLayout.vue              // 로그인/인증 화면 레이아웃
 │   └─ EmptyLayout.vue             // 별도 레이아웃이 거의 없는 화면용 레이아웃
 │
 ├─ services/                       // 여러 메뉴에서 사용하는 공통 service
 │   ├─ file.service.ts             // 인증 이미지, 파일 등 공통 파일 API
 │   ├─ websocket.service.ts        // WebSocket 연결, 해제, 송수신 공통 service
 │   ├─ category.service.ts         // 카테고리 목록, 공통 분류 데이터 API/service
 │   └─ {feature}.service.ts        // 기능 단위 공통 API/service
 │
 ├─ features/                       // 여러 화면에 쓰는 UI뿐 아니라 로직도 포함한 기능 덩어리
 │   └─ powerFlow/                  // 전력 흐름 기능 (예시 폴더)
 │       ├─ components/             // 전력 흐름 전용 UI 컴포넌트
 │       └─ service/                // 전력 흐름 전용 타입, 계산, 유틸
 │
 ├─ pages/                          // 실제 라우트 화면
 │   ├─ login/                      // 로그인 화면 영역
 │   │   └─ LoginPage.vue           // 로그인 페이지 컴포넌트
 │   │
 │   └─ main/                       // 로그인 후 메인 메뉴 화면 영역 (아래는 메뉴 별 예시 폴더)
 │       ├─ dashboard/              // 대시보드 메뉴
 │       ├─ device/                 // 장비 관리 메뉴
 │       ├─ alarm/                  // 알람 관리 메뉴
 │       ├─ report/                 // 리포트 메뉴
 │       ├─ user/                   // 사용자 관리 메뉴
 │       └─ setting/                // 설정 메뉴
 │
 ├─ stores/                         // 전역 Pinia store
 │   ├─ app.store.ts                // 앱 전역 설정, 전역 UI 상태, 언어 설정, 테마 설정 등 
 │   ├─ menu.store.ts               // 메뉴 설정 등
 │   └─ auth.store.ts               // 인증 상태. 로그인 사용자, 토큰 등
 │
 ├─ shared/                         // 여러 메뉴에서 재사용하는 공통 코드 영역
 │   ├─ components/                 // 공통 UI 컴포넌트
 │   │   ├─ layout/                 // 페이지 내부의 공통 배치 구조를 담당하는 컴포넌트
 │   │   ├─ widget/                 // SearchText, DropdownList 등 재사용 위젯 컴포넌트
 │   │   ├─ dialog/                 // BaseDialog, ConfirmDialog 등 공통 다이얼로그 컴포넌트
 │   │   ├─ custom/                 // 이 프로젝트에서만 공통으로 사용할 커스텀 컴포넌트
 │   │   └─ index.ts                // 컴포넌트 자동 import 하려면 여기에 등록 
 │   │
 │   ├─ composables/                // .vue에서 사용하는 상태 기반 공통 기능 로직. usePagination, useDialog 등
 │   ├─ utils/                      // Vue와 무관한 상태가 없는 순수 함수. 날짜, 숫자, 파일 처리 등
 │   ├─ constants/                  // 공통 상수. 상태 코드, 옵션값 등
 │   ├─ mappers/                    // 여러 메뉴에서 반복되는 공통 데이터 변환 함수
 │   └─ types/                      // 공통 타입. SelectOption, TableColumn 등
 │
 └─ assets/                         // 정적 리소스
     ├─ images/                     // 이미지 파일
     ├─ icons/                      // 아이콘 파일
     ├─ fonts/                      // 폰트 파일
     └─ styles/                     // 전역 스타일
         ├─ reset.scss              // 브라우저 기본 스타일 초기화
         ├─ main.scss               // 스타일 엔트리. reset, theme, global, override를 모아서 import
         ├─ global.scss             // html, body, #app, 공통 class 등 전역 스타일
         ├─ style-theme.scss        // CSS 변수 기반 색상, 테마, 다크모드 설정
         ├─ element-plus.scss       // UI library 전역 override
         └─ font.scss               // 폰트
```

이 구조는 처음에는 단순하게 시작할 수 있고, 나중에 기능이 많아져도 자연스럽게 확장할 수 있다.

---

### `pages/`는 실제 화면을 관리한다

`pages/` 안의 각 폴더는 하나의 메뉴 또는 기능 화면 단위다.

예:
```text
pages/
 ├─ login/                          // 로그인/인증 화면
 └─ main/                           // 로그인 후 메인 화면
     ├─ dashboard/                  // 대시보드
     ├─ device/                     // 장비 관리
     ├─ alarm/                      // 알람 관리
     ├─ report/                     // 리포트
     ├─ user/                       // 사용자 관리
     └─ setting/                    // 설정
```

---

### 메뉴 별 폴더의 기본 구조

```text
pages/main/{menu}/
 ├─ {Menu}Page.vue                  // 메뉴 진입 화면. 라우터로 진입할 수 있음.  
 ├─ {Menu + Role}Page.vue           // 기타 기능 화면. 라우터로 진입할 수 있음. 
 ├─ components/                     // UI 컴포넌트, UI 조각. 라우터로 진입할 수 없음.
 ├─ composables/                    // .vue에서 내부 공통으로 사용되거나 분리된 화면 기능 로직
 └─ service/                        // 메뉴 데이터 계층
     ├─ {menu}.api.ts               // API 호출
     ├─ {menu}.types.ts             // Request/Response/UI 타입
     ├─ {menu}.mapper.ts            // request/response 변환
     ├─ {menu}.store.ts             // 공유/유지 필요한 상태
     ├─ {menu}.utils.ts             // 내부 공통으로 사용하는 순수 util 함수.
     └─ {menu}.constants.ts         // 상수 정의
```

예를 들어 `device` 메뉴는 아래처럼 구성한다.

```text
pages/main/device/
 ├─ DevicePage.vue                  
 ├─ components/                     
 │   ├─ DeviceSearchForm.vue        // 검색 조건 UI
 │   ├─ DeviceTable.vue             // 장비 목록 테이블
 │   └─ DeviceDetailPanel.vue       // 장비 상세 패널
 │
 ├─ composables/                    
 │   ├─ useDeviceSearch.ts          // 검색 조건, 목록 조회, loading
 │   ├─ useDeviceDialog.ts          // 팝업 열기/닫기 상태
 │   └─ useDeviceRealtime.ts        // 실시간 데이터 연결
 │
 └─ service/                        
     ├─ device.api.ts               
     ├─ device.types.ts             
     ├─ device.mapper.ts            
     └─ device.store.ts             
```

다만 모든 파일을 만들 필요는 없다. 간단한 화면은 아래 정도로도 충분하다.

```text
예시:
pages/main/device/
 ├─ DevicePage.vue                  // 해당 페이지 진입 화면
 ├─ DeviceDetailPage.vue            // 상세 페이지 화면
 ├─ components/                     // 해당 메뉴 컴포넌트, UI 조각, dialog 등
 └─ service/                        // 데이터 계층
     ├─ device.api.ts               // API 호출
     └─ device.types.ts             // 타입 정의
```

그리고 필요해질 때 하나씩 추가한다.

```text
composables/              → .vue의 로직 부분을 분리 필요 시 
device.mapper.ts          → 데이터 변환이 필요할 때, 특히 request, response 데이터 변환 필요 시 
device.store.ts           → 상태 공유나 유지가 필요할 때
device.constants.ts       → 전용 상수가 많아지고 해당 메뉴 폴더 공통으로 사용할 때
device.utils.ts           → 메뉴 내에 여러 컴포넌트에서 공통으로 사용되는 함수가 필요할 때
```

이 구조는 “필요할 때 확장하는 방식”으로 사용한다.

---

### `XxxPage.vue`의 역할

`XxxPage.vue`는 화면 전체를 조립하는 파일이다.

여기에 모든 로직을 몰아넣기보다는, 하위 컴포넌트와 composable을 연결하는 역할에 집중한다.

```text
XxxPage.vue
→ 화면 조립
→ 컴포넌트 배치
→ 이벤트 연결
→ composable 호출
→ 초기 조회 실행
```

예시:

```vue
<script setup lang="ts">
import { onMounted } from 'vue'
import DeviceSearchForm from './components/DeviceSearchForm.vue'
import DeviceTable from './components/DeviceTable.vue'
import DeviceDetailPanel from './components/DeviceDetailPanel.vue'
import { useDeviceSearch } from './composables/useDeviceSearch'
import { useDeviceDialog } from './composables/useDeviceDialog'

const {
  searchForm,
  rows,
  loading,
  searchDevices,
  resetSearchForm,
} = useDeviceSearch()

const {
  dialogVisible,
  selectedDeviceId,
  openDialog,
  closeDialog,
} = useDeviceDialog()

onMounted(() => {
  searchDevices()
})
</script>

<template>
  <section class="device-page">
    <DeviceSearchForm
      v-model="searchForm"
      @search="searchDevices"
      @reset="resetSearchForm"
    />

    <DeviceTable
      :rows="rows"
      :loading="loading"
      @row-click="openDialog"
    />

    <DeviceDetailPanel
      v-model="dialogVisible"
      :device-id="selectedDeviceId"
      @close="closeDialog"
    />
  </section>
</template>
```

이렇게 하면 `XxxPage.vue`는 화면 흐름을 이해하기 쉬운 상태로 유지된다.

---

### `{menu}/components/`는 메뉴 전용 UI 조각이다

`pages/main/{menu}/components/`에는 `{menu}` 해당 메뉴에서만 사용하는 컴포넌트를 둔다.

```text
예시:
pages/main/device/components/
 ├─ DeviceSearchForm.vue            // 장비 검색 조건 UI
 ├─ DeviceTable.vue                 // 장비 목록 테이블
 ├─ DeviceDetailPanel.vue           // 장비 상세 패널
 ├─ DeviceEditDialog.vue            // 장비 상세 패널
 └─ DeviceSearchText.vue            // 장비 메뉴 전용 검색 텍스트
```

기준은 단순하다.

```text
해당 메뉴에서만 쓴다
→ pages/main/device/components/

여러 메뉴에서 반복해서 쓴다면
→ shared/components/
```
---

### `composables/`는 `.vue`의 로직을 기능 단위로 분리한 것이다

`composables/`는 쉽게 말하면 `.vue` 파일의 `<script setup>`에 있던 기능 로직을 분리한 것이다.

예전에는 `DevicePage.vue` 안에 이런 코드가 모두 들어갈 수 있다.

```ts
const searchForm = ref(...)
const rows = ref([])
const loading = ref(false)

async function searchDevices() {}
function resetSearchForm() {}

const dialogVisible = ref(false)
function openDialog() {}
function closeDialog() {}
```

이렇게 검색, 테이블, 팝업, 상세, 실시간 로직이 한 파일에 섞이면 `Page.vue`가 점점 커지고 가독성이 낮아지고 코드가 복잡해진다. 그래서 기능별로 나누면 이런 문제들을 해결할 수 있다.

```text
useDeviceSearch.ts
→ 검색 조건, 목록 데이터, loading, 조회, 초기화

useDeviceDialog.ts
→ 팝업 열기/닫기, 선택된 장비 ID

useDeviceRealtime.ts
→ 실시간 데이터 연결, 수신 처리
```

예시:

```ts
// pages/main/device/composables/useDeviceSearch.ts

import { ref } from 'vue'
import { getDeviceList } from '../service/device.api'
import { mapDeviceItemToRow } from '../service/device.mapper'
import type { DeviceRow, DeviceSearchForm } from '../service/device.types'

export function useDeviceSearch() {
  const searchForm = ref<DeviceSearchForm>({
    keyword: '',
    status: 'ALL',
  })

  const rows = ref<DeviceRow[]>([])
  const loading = ref(false)

  async function searchDevices() {
    loading.value = true

    try {
      const res = await getDeviceList(searchForm.value)
      rows.value = res.data.items.map(mapDeviceItemToRow)
    } finally {
      loading.value = false
    }
  }

  function resetSearchForm() {
    searchForm.value = {
      keyword: '',
      status: 'ALL',
    }
  }

  return {
    searchForm,
    rows,
    loading,
    searchDevices,
    resetSearchForm,
  }
}
```

composable이 모든 로직을 넣는 곳은 아니다.

```text
기능 단위로 화면 상태와 화면 동작
→ composables/

순수 API 호출
→ service/*.api.ts

데이터 변환
→ service/*.mapper.ts

Pinia store 정의
→ service/*.store.ts 또는 stores/
```

---

### `service/`는 해당 메뉴의 데이터 계층이다

메뉴 내부의 `service/` 폴더는 해당 메뉴의 API, types, mapper, store, constants를 관리한다.

```text
pages/main/device/service/
 ├─ device.api.ts                   // 장비 API 호출
 ├─ device.types.ts                 // 장비 타입 정의
 ├─ device.mapper.ts                // 장비 데이터 변환
 ├─ device.constants.ts             // 장비 데이터 상수
 └─ device.store.ts                 // 장비 메뉴 공유/유지 상태
```

이 폴더는 해당 메뉴의 데이터 관련 코드를 모아두는 영역이다.

---

### `device.api.ts`는 API 호출만 담당한다

`device.api.ts`에는 백엔드 API 호출 함수, request params, response data를 작성한다. 

여기에는 Vue의 `ref`, `computed`, `loading` 같은 화면 상태를 넣지 않는다.

주요 역할:
```text
device.api.ts
→ 서버에 요청을 보낸다.
→ 응답을 받아온다.
→ 화면 상태는 관리하지 않는다.
```

예:
```ts
// pages/main/device/service/device.api.ts

import { fetchApi } from '@/http'
import type { PayloadModel } from '@/http/type'
import type {
  DeviceListRequest,
  DeviceListResponse,
} from './device.types'

export async function getDeviceList(params: DeviceListRequest): Promise<DeviceListResponse> {
  const payload: PayloadModel = { query: params }
  return await fetchApi().get('/devices', { payload })
}

```

---

### `device.types.ts`는 Request, Response, UI 타입을 정의한다

`device.types.ts`에는 해당 메뉴에서 사용하는 타입을 모은다.

```ts
// pages/main/device/service/device.types.ts

export type DeviceListRequest = {
  keyword?: string
  stat_code?: string
  start_date?: string
  end_date?: string
}
export type DeviceListResponse = APIResponse<{
  items: DeviceItem[]
  total: number
}>
export type DeviceItem = {
  device_id: string
  device_name: string
  stat_code: 'RUN' | 'ERR' | 'STP'
  created_at: string
}
export type DeviceSearchForm = {
  keyword: string
  status: 'ALL' | 'RUNNING' | 'ERROR' | 'STOPPED'
  dateRange?: [string, string] | null
}
export type DeviceRow = {
  id: string
  name: string
  status: 'RUNNING' | 'ERROR' | 'STOPPED'
  statusLabel: string
  createdAtText: string
}
```

타입은 목적에 따라 나누는 것이 좋다.

```text
Request
→ 서버에 보내는 요청 타입

Response
→ 서버에서 받은 원본 응답 타입

Form
→ 화면 입력 폼 타입

Row
→ 테이블 표시용 타입

Option
→ select, radio 등에 쓰는 옵션 타입
```

---

### `mapper`는 서버 데이터와 화면 데이터를 변환한다

mapper는 쉽게 말하면 다음 역할을 한다.

```text
서버에서 받은 데이터 구조를 화면에서 쓰는 구조로 바꾸는 함수

화면 Form 데이터를 서버 요청 형식으로 바꾸는 함수
```

즉 mapper는 두 방향이 있다.

```text
Response Mapper
서버 응답 → 화면 데이터

Request Mapper
화면 데이터 → 서버 요청 데이터
```

예시:

```ts
// pages/main/device/service/device.mapper.ts

import type {
  DeviceItem,
  DeviceRow,
  DeviceSearchForm,
  DeviceListRequest,
} from './device.types'

export function mapDeviceSearchFormToRequest(
  form: DeviceSearchForm,
): DeviceListRequest {
  return {
    keyword: form.keyword || undefined,
    stat_code: mapStatusToCode(form.status),
    start_date: form.dateRange?.[0],
    end_date: form.dateRange?.[1],
  }
}

export function mapDeviceItemToRow(item: DeviceItem): DeviceRow {
  return {
    id: item.device_id,
    name: item.device_name,
    status: mapStatusCodeToStatus(item.stat_code),
    statusLabel: mapStatusCodeToLabel(item.stat_code),
    createdAtText: formatDateTime(item.created_at),
  }
}

function mapStatusToCode(
  status: DeviceSearchForm['status'],
): DeviceListRequest['stat_code'] {
  const statusMap = {
    ALL: undefined,
    RUNNING: 'RUN',
    ERROR: 'ERR',
    STOPPED: 'STP',
  } as const

  return statusMap[status]
}

function mapStatusCodeToStatus(
  statusCode: DeviceItem['stat_code'],
): DeviceRow['status'] {
  const statusMap = {
    RUN: 'RUNNING',
    ERR: 'ERROR',
    STP: 'STOPPED',
  } as const

  return statusMap[statusCode]
}

function mapStatusCodeToLabel(statusCode: DeviceItem['stat_code']): string {
  const statusLabelMap = {
    RUN: '운전',
    ERR: '오류',
    STP: '정지',
  } as const

  return statusLabelMap[statusCode]
}

function formatDateTime(value: string): string {
  return value.replace('T', ' ').slice(0, 16)
}
```

사용 예:

```ts
const params = mapDeviceSearchFormToRequest(searchForm.value)

const res = await getDeviceList(params)

rows.value = res.data.items.map(mapDeviceItemToRow)
```

`items.map(mapDeviceItemToRow)`는 아래 코드와 같은 의미다.

```ts
rows.value = res.data.items.map((item) => {
  return mapDeviceItemToRow(item)
})
```

mapper를 쓰면 컴포넌트가 서버 필드명이나 코드값을 직접 몰라도 된다.

```text
서버 필드:
device_id
device_name
stat_code
created_at

화면 필드:
id
name
status
statusLabel
createdAtText
```

---

### mapper를 만드는 기준

모든 API에 mapper가 필요한 것은 아니다.

서버 응답과 화면 구조가 거의 같으면 그대로 써도 된다.

```ts
rows.value = response.items
```

하지만 아래 상황이면 mapper를 만드는 것이 좋다.

```text
API 필드명과 화면 필드명이 다를 때
코드값을 화면 라벨로 바꿔야 할 때
Y/N 값을 boolean으로 바꿔야 할 때
날짜를 요청/응답 날짜 형식으로 바꿔야 할 때
서버 응답을 테이블 row로 바꿔야 할 때
서버 응답을 차트 series로 바꿔야 할 때
서버 응답 변경 영향을 줄이고 싶을 때
```

예를 들어 서버가 `device_nm`을 `device_name`으로 바꿔도, mapper만 수정하면 화면 코드는 그대로 둘 수 있다.

---

### `xxx.store.ts`는 공유하거나 유지해야 하는 상태만 관리한다

Pinia store는 `useXxx()` 형태라서 composable처럼 보일 수 있지만, 역할이 다르다.

```text
composables/
→ 화면 로직 분리

store
→ 상태 저장소
```

따라서 Pinia store 파일을 `composables/` 안에 두지 않는다.

추천 위치는 두 가지다.

```text
전역 store
→ src/stores/

메뉴 전용 store
→ pages/main/{menu}/service/{menu}.store.ts
```

예시:

```ts
// pages/main/device/service/device.store.ts

import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import type { DeviceRow } from './device.types'

export const useDeviceStore = defineStore('device', () => {
  const selectedDeviceId = ref<string | null>(null)
  const selectedDevice = ref<DeviceRow | null>(null)
  const deviceRows = ref<DeviceRow[]>([])

  const hasSelectedDevice = computed(() => {
    return selectedDeviceId.value !== null
  })

  function setDeviceRows(rows: DeviceRow[]) {
    deviceRows.value = rows
  }

  function selectDevice(device: DeviceRow) {
    selectedDeviceId.value = device.id
    selectedDevice.value = device
  }

  function clearSelectedDevice() {
    selectedDeviceId.value = null
    selectedDevice.value = null
  }

  return {
    selectedDeviceId,
    selectedDevice,
    deviceRows,

    hasSelectedDevice,

    setDeviceRows,
    selectDevice,
    clearSelectedDevice,
  }
})
```

store에 넣을 것:

```text
여러 컴포넌트가 같이 보는 상태
페이지 이동 후에도 유지해야 하는 상태
실시간 상태
메뉴 단위 캐시 데이터
공통 코드 캐시
```

store에 넣지 않는 것:

```text
해당 화면에서만 쓰는 loading
해당 페이지에서만 쓰는 데이터나 상태
단순 팝업 visible 상태
간단한 API 호출 
해당 화면에서만 쓰는 데이터 변환 함수 등. 필요시 mapper에 분리
```
이런 값은 `.vue`에서 관리하면 충분하다.

---

### `src/http/`는 공통 통신 계층이다

공통 API 클라이언트인 `fetchApi()`를 `src/http/index.ts`에  둔다.

공통 통신 코드와 업무 API 역할을 아래처럼 구분한다.

```text
src/http/
→ axios/fetch 공통 통신 계층

pages/{menu}/service/*.api.ts
→ 실제 메뉴 API 호출 함수

services/{feature}.service.ts
→ 여러 메뉴에서 쓰는 공통 API/service
```

예시:

```text
http/
 ├─ index.ts                     // fetchApi 공통 클라이언트
 ├─ handleError.ts               // 공통 에러 처리
 └─ type.ts                      // API 공통 타입
```

`src/http`가 담당하는 것:

```text
baseURL
timeout
Authorization token
request interceptor
response interceptor
401 인증 만료 처리
공통 에러 처리
응답 unwrap
PayloadModel 정의
```

즉, `src/http/`는 실제 업무 API가 아니라 API 요청을 보내기 위한 공통 도구다.

---

### `src/services` 공통 service

여러 메뉴에서 사용하는 공통 API는 특정 메뉴 폴더 안에 두지 않는다.

예를 들어 아래 데이터는 여러 메뉴에서 사용할 가능성이 높다.

```text
공통 코드
카테고리 목록
권한 목록
장비 타입 목록
```

이런 API는 전역 `services/` 아래에 둔다.

```text
services/
 ├─ file.service.ts                 // 인증 이미지, 파일 등 공통 파일 API
 ├─ websocket.service.ts            // WebSocket 연결, 해제, 송수신 공통 service
 ├─ category.service.ts             // 카테고리성 공통 API
 └─ commonCode.service.ts           // 공통 코드 API
```

기본은 `기능.service.ts` 형태로 작성한다.
타입, mapper, 상수까지 커져서 한 파일이 읽기 어려워질 때만 `services/{feature}/` 폴더로 분리한다.

`websocket.service.ts`는 연결, 해제, 송신, 수신 callback 등록처럼 통신 자체만 담당한다.
화면별 메시지 해석과 UI 반영은 각 page, composable, store에서 처리한다.

---

### `shared`는 여러 메뉴에서 재사용되는 코드다

`shared/`는 공통 components, composables, utils, constants, types를 두는 영역이다.

```text
shared/
 ├─ components/                     // 공통 UI 컴포넌트
 │   ├─ layout/                     // 페이지 내부 배치 컴포넌트
 │   ├─ widget/                     // 공통 위젯 컴포넌트
 │   └─ dialog/                     // 공통 다이얼로그 컴포넌트
 ├─ composables/                    // 공통 Vue 로직
 ├─ utils/                          // 공통 순수 함수
 ├─ constants/                      // 공통 상수
└─ types/                          // 공통 타입
```

### `shared/components`

여러 메뉴에서 재사용하는 UI 컴포넌트, 즉 UI 조각을 둔다.

```text
shared/components/
 ├─ layout/                         // 페이지 내부 배치용 컴포넌트
 │   ├─ PageHeader.vue              // 페이지 상단 제목/액션 영역
 │   ├─ PageBody.vue                // 페이지 본문 래퍼
 │   └─ PageSection.vue             // 페이지 내부 섹션 영역
 │
 ├─ widget/                         // 재사용 가능한 화면 위젯
 │   ├─ BaseImage.vue               // 공통 이미지 컴포넌트
 │   ├─ DropdownList.vue            // 공통 드롭다운 리스트
 │   ├─ BaseSearchForm.vue          // 공통 검색 폼
 │   └─ SearchText.vue              // 공통 검색 텍스트
 │
 └─ dialog/                         // 공통 다이얼로그 컴포넌트
     ├─ BaseDialog.vue              // 기본 다이얼로그
     └─ ConfirmDialog.vue           // 확인/취소 다이얼로그
```

### `shared/composables`

여러 메뉴에서 재사용하는 Vue 기능 로직을 둔다.

```text
usePagination.ts
useDialog.ts
useProgress.ts
useResizeObserver.ts
useCategoryOptions.ts
```

### `shared/utils`

Vue와 관계없는 순수 함수를 둔다.
index.ts 파일 한곳에 모아 둔다. 함수가 많아서 역할 별 분리 필요 시 아래처럼 분리 작성후 index.ts에서 export 한다.
```text
index.ts  

date.util.ts
number.util.ts
file.util.ts
validation.util.ts
```

예:

```ts
export function formatNumber(value: number): string {
  return value.toLocaleString()
}
```

`utils`와 `composables`의 차이:

```text
utils
→ ref, computed 같은 Vue 기능을 사용하지 않는 순수 함수

composables
→ ref, computed, watch 등 Vue 기능을 사용하는 화면 로직
```

### `shared/constants`

여러 메뉴에서 사용하는 상수를 둔다. 상수 타입도 아래처럼 같이 정의해야 한다.

```ts
export const DEVICE_STATUS = {
  NORMAL: 'NORMAL',
  WARNING: 'WARNING',
  ERROR: 'ERROR',
  STOPPED: 'STOPPED',
} as const

export type DeviceStatus = keyof typeof DEVICE_STATUS
```

### `shared/types`

여러 화면에서 사용하는 공통 타입을 둔다.

```ts
export interface SelectOption<T = string> {
  label: string
  value: T
}
```

---

### `features`는 여러 화면에서 쓰는 기능 덩어리, UI만 있는 게 아니라 로직과 구조를 같이 가짐.
```text
아래 조건을 만족 면 features에 둔다. 
1. 여러 페이지에서 사용된다
2. UI뿐 아니라 로직, 상태 도 있다
3. 기능 자체가 독립적으로 설명 가능하다 
4. 상태 관리가 있다 (옵션)
5. 타입, 상수, 유틸이 같이 필요하다 (옵션)
6. API 호출 또는 데이터 매핑이 있다 (옵션)
```

### `layouts`는 컴포넌트지만 별도 분리한다

`layout`도 Vue 컴포넌트는 맞다. 하지만 일반적인 `components`와 역할이 다르다.

```text
components
→ 버튼, 테이블, 카드, 검색폼, 다이얼로그 같은 UI 조각

layouts
→ 페이지 전체의 공통 골격
```

예를 들어 `MainLayout.vue`는 아래처럼 화면 전체 구조를 담당한다.

```vue
<template>
  <div class="main-layout">
    <AppHeader />

    <div class="main-layout__body">
      <AppSidebar />

      <main class="main-layout__content">
        <RouterView />
      </main>
    </div>
  </div>
</template>
```

그래서 화면 전체 구조를 담당하는 layout은 보통 별도 폴더에 둔다.

```text
layouts/
 ├─ MainLayout.vue                  // 로그인 후 메인 레이아웃
 ├─ AuthLayout.vue                  // 로그인/인증 레이아웃
 └─ EmptyLayout.vue                 // 단독 화면용 빈 레이아웃
```

---

### `assets`는 정적 리소스다

`assets/`에는 이미지, 아이콘, 폰트, 전역 스타일을 둔다.

```text
assets/
 ├─ images/                      // 이미지
 ├─ icons/                       // 아이콘
 ├─ fonts/                       // 폰트
 └─ styles/                      // 전역 스타일
      ├─ reset.scss              // 브라우저 기본 스타일 초기화
      ├─ main.scss               // 스타일 엔트리. reset, theme, global, override를 모아서 import
      ├─ global.scss             // html, body, #app, 공통 class 등 전역 스타일
      ├─ style-theme.scss        // CSS 변수 기반 색상, 테마, 다크모드 설정
      ├─ element-plus.scss       // UI library 전역 override
      └─ font.scss               // 폰트
```

```text
assets/styles/
→ 전역 스타일, reset,  폰트 스타일, 스타일 테마
```

---

## 구조 판단 기준

### API는 어디에 두는가?

```text
특정 메뉴 전용 API
→ pages/main/{menu}/service/{menu}.api.ts

여러 메뉴에서 사용하는 API
→ services/{features}.service.ts

axios, fetch 공통 설정
→ src/http/
```

### 타입은 어디에 두는가?

```text
특정 메뉴 타입
→ pages/main/{menu}/service/{menu}.types.ts

여러 메뉴에서 쓰는 공통 타입
→ shared/types/
```

### mapper는 어디에 두는가?

```text

메뉴 내부 데이터 변환
→ pages/main/{menu}/service/{menu}.mapper.ts

여러 메뉴에서 반복되는 범용 데이터 변환
→ shared/mappers/

```

### store는 어디에 두는가?

```text
전역 상태
→ stores/

메뉴 전용 공유 상태
→ pages/main/{menu}/service/{menu}.store.ts

단순 화면 상태
→ .vue 또는 composables/
```

### composable은 어디에 두는가?

```text
해당 메뉴 화면 기능 로직
→ pages/main/{menu}/composables/

여러 메뉴에서 재사용되는 로직
→ shared/composables/
```

### component는 어디에 두는가?

```text
특정 메뉴에서만 사용
→ pages/main/{menu}/components/

여러 메뉴에서 재사용
→ shared/components/

예를 들어 `DeviceTable.vue`이 장비 관리 화면에만 쓰이면 메뉴 내부에 둔다.

하지만 `BaseImage.vue`, `BaseDialog.vue`, `SearchText.vue`처럼 여러 메뉴에서 공통으로 쓸 수 있는 컴포넌트는 `shared/components/`로 이동한다.
```

---

## 프로젝트 크기별 구조 차이

### 중소형 프로젝트

중소형에서는 너무 많이 나누지 않는다.

```text
pages/main/device/
 ├─ DevicePage.vue                  // 진입 페이지
 ├─ components/                     // 메뉴 전용 UI 컴포넌트
 └─ service/                        // 데이터 계층
     ├─ device.api.ts               // API 호출
     └─ device.types.ts             // 타입 정의
```

화면 로직은 `.vue` 파일에 작성하고, 기능 로직 분리 필요하거나 공통 로직 처리가 필요할 때 `composables/`로 분리한다. `mapper`, `store`, `constants`, `utils`는 필요할 때 추가한다.

```text
service/
 ├─ device.api.ts
 ├─ device.types.ts
 ├─ device.mapper.ts      // 필요할 때 추가
 ├─ device.constants.ts   // 필요할 때 추가
 ├─ device.utils.ts       // 필요할 때 추가
 └─ device.store.ts       // 필요할 때 추가
```

### 대형 프로젝트

대형 프로젝트에서는 기능이 많아지기 때문에 메뉴 내부를 더 나눈다.

```text
pages/main/device/
 ├─ DevicePage.vue
 ├─ components/
 │   ├─ DeviceSearchForm.vue
 │   ├─ DeviceTable.vue
 │   ├─ DeviceDetailPanel.vue
 │   └─ DeviceSearchText.vue
 │
 ├─ composables/
 │   ├─ useDeviceSearch.ts
 │   ├─ useDeviceDialog.ts
 │   └─ useDeviceRealtime.ts
 │
 └─ service/
     ├─ device.api.ts
     ├─ device.types.ts
     ├─ device.mapper.ts
     ├─ device.store.ts 
     ├─ device.utils.ts 
     └─ device.constants.ts
```

하지만 대형 구조를 처음부터 강제로 만들 필요는 없다.

기준:
```text
처음에는 단순하게 만든다.
코드가 복잡해지는 순간 분리한다.
```

---


## 핵심 정리

이 구조에서 가장 중요한 것은 폴더 이름이 아니라 역할이다.

```text
Page.vue
→ 화면 조립

components/
→ UI 조각

composables/
→ 화면 기능 로직 분리

api.ts
→ API 호출

types.ts
→ 타입 정의

mapper.ts
→ request/response 데이터 변환

store.ts
→ 공유하거나 유지해야 하는 상태

src/http/
→ 공통 통신 계층

services/
→ 여러 메뉴에서 사용하는 공통 API/service

shared/
→ 여러 메뉴에서 재사용하는 코드

assets/
→ 이미지, 아이콘, 폰트, 전역 스타일
```

최종적으로 이 프로젝트는 아래 원칙을 따른다.

```text
1. 메뉴 전용 코드는 메뉴 폴더 안에 둔다.
2. 여러 메뉴에서 반복되면 shared/로 올린다.
3. API와 화면 로직을 섞지 않는다.
4. 데이터 변환은 mapper로 분리한다.
5. store에는 공유/유지 상태와 그 상태를 변경하는 처리 로직만 둔다.
6. composables는 .vue의 화면 로직을 기능 단위로 분리한 것이다.
7. 처음부터 모든 폴더를 만들지 않는다. 필요할 때만 확장한다.
```

이 방식이면 중소형 프로젝트에서는 단순하게 시작할 수 있고, 나중에 프로젝트가 커지거나 화면과 API가 많아져도 구조를 무리 없이 확장할 수 있다.

---
## 코딩 규칙 및 가이드 

### 파일명 명명 규칙

- Vue 컴포넌트 파일명은 `PascalCase.vue`를 사용한다.
- 일반 TypeScript 파일명은 `camelCase.ts`를 사용한다.
- `*.api.ts`, `*.types.ts`, `*.mapper.ts`, `*.store.ts` 등 역할 파일은 `camelCase.role.ts` 형식을 사용한다.
  - 예: `device.api.ts`, `device.types.ts`, `device.mapper.ts`, `device.store.ts`
- service 파일명은 `camelCase.service.ts` 형식을 사용한다.
- composable 파일명은 `useXxx.ts` 형식을 사용한다.

### 변수/함수/타입 명명 규칙

- Pinia store 함수명은 `useXxxStore` 형식을 사용한다.
- 타입과 interface는 `PascalCase`를 사용한다.
- 변수와 함수는 `camelCase`를 사용한다.
- 상수는 `UPPER_SNAKE_CASE` 또는 `as const` 객체를 사용한다.

---

### `*.api.ts` 코드 작성 규칙

API 호출은 `src/http/index.ts`의 `fetchApi()`를 사용한다.

`*.api.ts`는 API 호출 함수 정의만 담당한다. 각 API 함수는 request type과 response type을 명시해야 한다. 화면 상태, 테이블 데이터, 로딩 상태, 메시지 처리 등은 페이지 컴포넌트 또는 composable에서 관리한다.

```ts
import { fetchApi } from '@/http'
import type { PayloadModel } from '@/http/type'
import type { ExampleListRequest, ExampleListResponse } from './types'

export default {
  async getList(params: ExampleListRequest): Promise<ExampleListResponse> {
    const payload: PayloadModel = { query: params }
    return fetchApi().get('/system/examples', { payload })
  },
}
```

요청 데이터는 HTTP 메서드에 따라 `PayloadModel`의 필드를 사용한다.

| 필드 | 용도 |
| --- | --- |
| `query` | GET query parameter |
| `body` | POST, PUT request body |
| `pathVariables` | URL path variable 치환 |

---

### 타입 작성 규칙

`*.types.ts`는 API input/output 타입과 화면에서 사용하는 데이터 모델 타입을 정의한다. 
Response type은 `APIResponse<T>` 타입을 이용해서 정의한다.

```ts
import type { APIResponse } from '@/http/type'

export type ExampleItem = {
  id: number
  name: string
  createdAt: string
}

export type ExampleListRequest = {
  keyword: string
  pageNumber: number
  pageSize: number
}

export type ExampleListResponse = APIResponse<{
  list: ExampleItem[]
  totalCount: number
}>
```
---

### 화면 내부 API 응답 처리 방식

네트워크 에러, 서버 장애, 인증 만료 같은 공통 HTTP/system error는 `src/http/handleError.ts`에서 공통 처리한다. 
각 페이지에서는 이런 공통 에러를 기본적으로 `try/catch`로 중복 처리하지 않는다.
각 페이지에서는 HTTP 요청이 정상 완료된 뒤 받은 `APIResponse`의 `result` 값을 기준으로 업무 성공/실패를 판단한다.

단, 특정 화면에서 별도 복구 처리, 후처리, fallback UI 처리가 필요한 경우에는 개별 try/catch를 사용할 수 있다.

기본 응답 형식:

```ts
type APIResponse<T = any> = {
    result: string
    resultMessage: string
    data: T
}
```

처리 방식:

```ts
import { isSuccessResponse } from '@/shared/utils'

const saveData = async () => {
    const res = await exampleApi.save(payload)

    if (!isSuccessResponse(res.result)) {
        Message.warning(res.resultMessage || 'Failed to save data.')
        return
    }

    await getList()
    Message.success('Saved.')
    closeDialog()
}
```

정리:

- HTTP/system error: `src/http/handleError.ts`에서 공통 처리
- business result error: 화면 또는 기능 단위에서 `isSuccessResponse(res.result)`로 판단
- 성공일 때만 목록 재조회, 성공 메시지, 다이얼로그 닫기 처리
- 실패일 때는 `res.resultMessage`를 우선 사용하고, 없으면 기능별 기본 메시지를 사용
- `isSuccessResponse`는 `src/shared/utils/api.util.ts`에 둔다
- `SUCCESS`, `success`처럼 대소문자가 섞일 수 있으므로 `isSuccessResponse` 내부에서 대문자로 정규화한다


---

### 공통 컴포넌트를 전역 컴포넌트 등록 방식

이 프로젝트는 Vite 설정을 통해 공통 컴포넌트를 전역 컴포넌트로 자동 등록한다.
공통 컴포넌트를 `shared/components/index.ts`에서 export하면 `.vue` 파일에서 별도 import 없이 직접 사용할 수 있다.

예:

```ts
export { default as SearchBox } from './widget/SearchBox.vue'
```
```vue
<SearchBox />
<BaseDialog />
<PageHeader title="장비 관리" />
```

주의:
shared/components/index.ts에서 export하지 않은 컴포넌트는 자동 등록 대상이 아니므로, 직접 import해서 사용해야 한다.

---

### 스타일 규칙

- 전역 컬러와 디자인 토큰은 `src/assets/styles/style-theme.scss`에 정의한다.
- 공통 컴포넌트의 색상은 가능하면 style-theme에서 제어한다.
- 화면 단위 스타일은 해당 `.vue` 파일의 `<style scoped>`에 둔다.
- Element Plus 기본 색상이 시스템 테마와 맞지 않으면 `main.scss` 또는 별도 Element Plus override 파일에서 전역 override를 정의한다.

---

### 라우터

- 전체 route는 `src/router/routes.ts`에 정의합니다.
- router 생성과 guard는 `src/router/index.ts`에서 관리합니다.


## 컴포넌트 설명

### el-table에 `multiple` 속성을 통해 멀티/싱글 체크 사용 방식

<el-table>에 `multiple` 속성 추가 여부와 `getTableSelection`함수 사용에 따라 다중 선택 여부를 제어할 수 있다.

`multiple` 속성을 추가하면 다중 선택 모드로 동작하며, 전체 선택 체크박스가 표시된다.  
`multiple` 속성이 없으면 단일 선택 모드로 동작하며, 전체 선택 체크박스가 표시되지 않는다.

선택값 처리는 `shared/utils`의 `getTableSelection(tableRef, val)` 함수를 사용한다.  
`getTableSelection()`은 `multiple` 속성 유무에 따라 다중 선택 또는 단일 선택 결과를 반환한다.

> 참고: `multiple`은 Element Plus 기본 속성이 아니라, 이 프로젝트에서 커스텀 처리한 속성이다.

예:
```vue
<el-table multiple @selection-change="getChecked"></el-table>
```
```ts
import { getTableSelection } from '@/shared/utils'
const tableRef: any = ref(null)
const getChecked = (val: any) => {
    const selected = getTableSelection(tableRef, val)
    console.log('Selected items', selected)
}
```

### AppIcon 컴포넌트
공통 아이콘은 `AppIcon` 컴포넌트를 사용한다. 아이콘 svg 파일은 `src/assets/icons/`에 두고, `src/shared/constants/appIcons.ts`의 `AppIcons`에 등록한다.

등록된 아이콘은 `.vue` 파일에서 별도 import 없이 아이콘 이름만 전달해서 사용한다.

```vue
<AppIcon name="IconUserMng" />
<AppIcon name="IconUserMng" color="var(--primary-color)" />
<AppIcon :name="item.icon" class="menu-icon" />
```

새 아이콘 추가 예시:

```ts
import IconUserMng from '@/assets/icons/IconUserMng.svg'

export const AppIcons = {
    IconUserMng,
} as const
```

### SearchBox 컴포넌트
목록의 검색 조건은 <SearchBox> 컴포넌트를 사용한다. 기타 검색 조건을 아래 줄에 추가하려면, <SearchBox> 태그에 'extra' 속성을 추가하고 `<template #extra></template>` 안에 작성 한다.

예:
```vue
<SearchBox :on-search="getList" extra>
    <SearchText label="검색" v-model="searchParams.searchValue">
        <DropdownList
            v-model="searchParams.searchKey"
            placeholder="Select"
            :list="searchTypes"
            option-label="label"
            option-value="searchKey"
        />
    </SearchText>
    <template #extra>
        <DropdownList
            label="Role"
            v-model="searchParams.roleCode"
            placeholder="Select role"
            :list="roleList"
            option-label="roleName"
            option-value="roleCode"
            @onChange="selectRole"
        />
    </template>
</SearchBox>
```
