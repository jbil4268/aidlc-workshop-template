# Service Layer Design

## Backend Services

### 1. AuthService
**Purpose**: 인증 흐름 오케스트레이션
**Components Used**: AuthComponent
**Orchestration**:
- 관리자 로그인: 로그인 시도 제한 확인 → 비밀번호 검증 → JWT 발급
- 테이블 로그인: 테이블 정보 검증 → JWT 발급
- 토큰 갱신: 기존 토큰 검증 → 새 토큰 발급

### 2. MenuService
**Purpose**: 메뉴 관리 오케스트레이션
**Components Used**: MenuComponent
**Orchestration**:
- 메뉴 등록: 데이터 검증 → 이미지 저장 → 메뉴 생성
- 메뉴 수정: 데이터 검증 → 이미지 교체(선택) → 메뉴 업데이트
- 메뉴 삭제: 참조 확인 → 이미지 정리 → 메뉴 삭제

### 3. OrderService
**Purpose**: 주문 처리 오케스트레이션
**Components Used**: OrderComponent, TableComponent, WebSocketComponent
**Orchestration**:
- 주문 생성: 세션 확인 → 메뉴 유효성 검증 → 팁 계산 → 주문 저장 → WebSocket 브로드캐스트
- 주문 상태 변경: 상태 전이 검증 → 상태 업데이트 → WebSocket 브로드캐스트
- 주문 삭제: 주문 확인 → 삭제 → 총액 재계산 → WebSocket 브로드캐스트

### 4. TableService
**Purpose**: 테이블 세션 라이프사이클 오케스트레이션
**Components Used**: TableComponent, OrderComponent
**Orchestration**:
- 세션 시작: 첫 주문 시 자동 세션 생성
- 세션 종료: 주문 이력 아카이빙 → 테이블 리셋 → 세션 종료
- 과거 내역 조회: 날짜 필터링 → 이력 데이터 조회

### 5. RealtimeService
**Purpose**: 실시간 통신 관리
**Components Used**: WebSocketComponent
**Orchestration**:
- 연결 관리: 매장별 채널 구독/해제
- 이벤트 라우팅: 주문 이벤트를 해당 매장 채널로 전달

---

## Frontend Services

### Customer Frontend

#### CustomerAuthService
- 자동 로그인 처리 (SessionStorage 확인 → API 호출)
- 세션 만료 감지 및 재로그인

#### CustomerMenuService
- 메뉴/카테고리 데이터 fetch 및 캐싱
- 메뉴 상세 조회

#### CartService
- LocalStorage 기반 장바구니 CRUD
- 총 금액 계산
- 장바구니 → 주문 데이터 변환

#### CustomerOrderService
- 주문 생성 API 호출
- 팁 계산
- 주문 내역 조회

### Admin Frontend

#### AdminAuthService
- 로그인/로그아웃 API 호출
- JWT 토큰 관리 (SessionStorage)
- 자동 로그아웃 타이머

#### DashboardService
- WebSocket 연결 및 이벤트 수신
- 주문 데이터 실시간 업데이트
- 알림음 재생 관리

#### TableManagementService
- 테이블 CRUD API 호출
- 세션 종료 API 호출
- 과거 내역 조회

#### MenuManagementService
- 메뉴 CRUD API 호출
- 이미지 업로드
- 카테고리 관리
