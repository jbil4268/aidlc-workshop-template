# Customer Frontend - Tech Stack Decisions

## Frontend Framework

### Decision: Vue.js 3
**Rationale**:
- 사용자 요구사항에서 명시됨
- 가벼운 러닝 커브
- Composition API로 로직 재사용 용이
- 반응형 시스템으로 상태 관리 간편

**Alternatives Considered**:
- React: 더 큰 생태계, 하지만 요구사항에서 Vue 지정
- Svelte: 더 작은 번들, 하지만 생태계 작음

---

## Build Tool

### Decision: Vite
**Rationale**:
- Vue 3 공식 권장 도구
- 빠른 HMR (Hot Module Replacement)
- 간단한 설정
- 최적화된 프로덕션 빌드

**Alternatives Considered**:
- Webpack: 더 많은 설정 필요
- Parcel: 간단하지만 Vue 지원 약함

---

## Styling

### Decision: Tailwind CSS
**Rationale**:
- 사용자 요구사항에서 명시됨
- Utility-first 접근으로 빠른 개발
- 반응형 디자인 쉬움
- 작은 프로덕션 번들 (PurgeCSS)

**Configuration**:
- JIT (Just-In-Time) 모드 사용
- 커스텀 색상 팔레트 정의
- 반응형 breakpoints 설정

**Alternatives Considered**:
- Bootstrap: 더 무거움, 커스터마이징 어려움
- Plain CSS: 개발 속도 느림

---

## State Management

### Decision: Vue Composition API (No Vuex/Pinia)
**Rationale**:
- 간단한 애플리케이션 (복잡한 상태 관리 불필요)
- Composition API의 `ref`, `reactive`로 충분
- SessionStorage로 세션 상태 관리
- 컴포넌트 간 props/events로 통신

**State Structure**:
```javascript
// Global state (SessionStorage)
- sessionToken
- tableNumber
- tableId

// Local state (Component)
- cart (MenuListPage)
- orders (OrderStatusPage)
- menus, categories (MenuListPage)
```

**Alternatives Considered**:
- Pinia: 오버엔지니어링
- Vuex: 레거시, Pinia로 대체됨

---

## HTTP Client

### Decision: Axios
**Rationale**:
- 간편한 API
- 인터셉터로 공통 헤더 설정 가능
- 에러 핸들링 용이
- 타임아웃 설정 가능

**Configuration**:
```javascript
axios.defaults.baseURL = 'http://localhost:8000'
axios.defaults.timeout = 10000
```

**Alternatives Considered**:
- Fetch API: 네이티브, 하지만 기능 부족
- Vue Resource: 더 이상 유지보수 안 됨

---

## Routing

### Decision: Vue Router 4
**Rationale**:
- Vue 3 공식 라우터
- SPA 네비게이션
- Route guards로 인증 체크
- History mode 사용

**Routes**:
```javascript
/scan   - QRScanPage
/menu   - MenuListPage (protected)
/order  - OrderPage (protected)
/status - OrderStatusPage (protected)
```

**Alternatives Considered**:
- No Router: 수동 라우팅 복잡함

---

## QR Code Scanner

### Decision: html5-qrcode
**Rationale**:
- 브라우저 네이티브 카메라 API 사용
- 간단한 API
- 모바일 지원 좋음
- 라이센스: MIT

**Usage**:
```javascript
import { Html5Qrcode } from 'html5-qrcode'
```

**Alternatives Considered**:
- qrcode-reader: 더 이상 유지보수 안 됨
- jsQR: 수동 카메라 처리 필요

---

## UI Components

### Decision: Custom Components (No UI Library)
**Rationale**:
- Tailwind CSS로 충분히 구현 가능
- 작은 번들 사이즈
- 완전한 커스터마이징

**Component Library**:
- Button
- Card
- Modal
- Input
- Badge
- Spinner

**Alternatives Considered**:
- Vuetify: 너무 무거움
- Element Plus: Material Design 불필요
- Headless UI: 스타일링 여전히 필요

---

## Icons

### Decision: Heroicons
**Rationale**:
- Tailwind CSS 제작사에서 만듦
- SVG 아이콘
- 가볍고 커스터마이징 쉬움
- MIT 라이센스

**Usage**:
```vue
<template>
  <ShoppingCartIcon class="w-6 h-6" />
</template>
```

**Alternatives Considered**:
- Font Awesome: 더 무거움
- Material Icons: 스타일 안 맞음

---

## Form Validation

### Decision: Built-in Vue Validation
**Rationale**:
- 간단한 폼 (수량 입력만)
- Vue의 `v-model` + computed로 충분
- 외부 라이브러리 불필요

**Validation Rules**:
- 수량: 1 이상, 99 이하
- 필수 입력: 장바구니 비어있지 않음

**Alternatives Considered**:
- VeeValidate: 오버엔지니어링
- Vuelidate: 복잡한 폼 아님

---

## Date/Time Formatting

### Decision: Native JavaScript
**Rationale**:
- 간단한 포맷팅만 필요
- `Intl.DateTimeFormat` 사용
- 외부 라이브러리 불필요

**Usage**:
```javascript
new Date(order.created_at).toLocaleString('ko-KR')
```

**Alternatives Considered**:
- Day.js: 작지만 불필요
- Moment.js: 너무 무거움 (deprecated)

---

## Testing

### Decision: Vitest (Optional)
**Rationale**:
- Vite 네이티브 테스트 러너
- Jest 호환 API
- 빠른 실행
- 요구사항: 핵심 로직만 테스트

**Test Scope**:
- 계산 로직 (팁 계산)
- 유틸리티 함수
- API 호출 모킹

**Alternatives Considered**:
- Jest: 설정 복잡
- Cypress: E2E 테스트 불필요

---

## Development Tools

### ESLint
- Vue 3 권장 설정
- Prettier 통합

### Prettier
- 코드 포맷팅 자동화
- Tailwind CSS 플러그인

### TypeScript (Optional)
- 타입 안정성
- IDE 자동완성
- 선택 사항 (JavaScript도 가능)

---

## Deployment

### Decision: Static File Serving
**Rationale**:
- 로컬 개발 환경만
- `npm run build` → `dist/` 폴더
- Python HTTP 서버로 서빙 가능

**Build Command**:
```bash
npm run build
```

**Serve Command**:
```bash
python -m http.server 5173 --directory dist
```

**Alternatives Considered**:
- Docker: 오버엔지니어링
- Nginx: 로컬 개발에 불필요

---

## Package Manager

### Decision: npm
**Rationale**:
- Node.js 기본 패키지 매니저
- 충분한 성능
- 간단한 사용법

**Alternatives Considered**:
- yarn: 추가 설치 필요
- pnpm: 더 빠르지만 호환성 이슈 가능

---

## Summary

| Category | Technology | Version |
|----------|-----------|---------|
| Framework | Vue.js | 3.x |
| Build Tool | Vite | 5.x |
| Styling | Tailwind CSS | 3.x |
| State | Composition API | Built-in |
| Routing | Vue Router | 4.x |
| HTTP | Axios | 1.x |
| QR Scanner | html5-qrcode | 2.x |
| Icons | Heroicons | 2.x |
| Testing | Vitest | 1.x (Optional) |

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-09  
**Status**: Draft
