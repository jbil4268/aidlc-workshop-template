# Units of Work

## Architecture: Monorepo with 3 Units

### Deployment Model
- 로컬 개발 환경 (단일 머신)
- Backend: Python 서버 (단일 프로세스)
- Frontend: Vue.js 개발 서버 (Customer/Admin 분리)

---

## Unit 1: Backend API Server

### Definition
- **Name**: backend
- **Type**: Service (독립 실행)
- **Technology**: Python (FastAPI), SQLite, WebSocket
- **Purpose**: REST API + WebSocket 서버, 데이터 관리

### Responsibilities
- 모든 REST API 엔드포인트 제공
- WebSocket 실시간 통신
- JWT 인증 및 세션 관리
- 데이터베이스 CRUD
- 이미지 파일 저장
- 비즈니스 로직 처리

### Components Included
- AuthComponent
- MenuComponent
- OrderComponent
- TableComponent
- WebSocketComponent
- AuthService, MenuService, OrderService, TableService, RealtimeService

### Directory Structure
```
backend/
  app/
    main.py              # FastAPI 앱 진입점
    config.py            # 설정 (환경 변수)
    database.py          # SQLite 연결 및 세션
    models/              # SQLAlchemy 모델
      store.py
      table.py
      table_session.py
      menu.py
      category.py
      order.py
      order_item.py
      admin.py
      order_history.py
    schemas/             # Pydantic 스키마
      auth.py
      menu.py
      order.py
      table.py
    routers/             # API 라우터
      customer_auth.py
      customer_menu.py
      customer_order.py
      admin_auth.py
      admin_order.py
      admin_table.py
      admin_menu.py
      admin_category.py
    services/            # 비즈니스 로직
      auth_service.py
      menu_service.py
      order_service.py
      table_service.py
    middleware/           # 미들웨어
      auth_middleware.py
      error_handler.py
    websocket/           # WebSocket
      manager.py
      events.py
    utils/               # 유틸리티
      security.py
      validators.py
  uploads/               # 이미지 업로드 디렉토리
  tests/                 # Unit Tests
    test_auth.py
    test_order.py
    test_table.py
  requirements.txt
  .env.example
```

---

## Unit 2: Customer Frontend

### Definition
- **Name**: customer-frontend
- **Type**: Module (독립 빌드/배포 가능)
- **Technology**: Vue.js 3, Tailwind CSS
- **Purpose**: 고객용 테이블 주문 인터페이스

### Responsibilities
- 테이블 태블릿 자동 로그인
- 메뉴 탐색 및 상세 조회 (알러지 정보 포함)
- 장바구니 관리 (LocalStorage)
- 주문 생성 및 팁 추가
- 주문 내역 조회

### Components Included
- CustomerAuthModule
- MenuBrowseModule
- CartModule
- OrderModule

### Directory Structure
```
customer-frontend/
  src/
    main.js              # Vue 앱 진입점
    App.vue              # 루트 컴포넌트
    router/
      index.js           # Vue Router 설정
    stores/              # Pinia 상태 관리
      auth.js
      cart.js
      menu.js
      order.js
    views/               # 페이지 컴포넌트
      MenuView.vue       # 메뉴 탐색 (기본 화면)
      CartView.vue       # 장바구니
      OrderConfirmView.vue  # 주문 확인 + 팁
      OrderHistoryView.vue  # 주문 내역
      SetupView.vue      # 초기 설정
    components/          # 재사용 컴포넌트
      MenuCard.vue
      MenuDetail.vue
      AllergyBadge.vue
      CartItem.vue
      TipSelector.vue
      OrderStatusBadge.vue
    services/            # API 호출
      api.js             # Axios 인스턴스
      authService.js
      menuService.js
      orderService.js
    utils/
      storage.js         # LocalStorage/SessionStorage 헬퍼
  public/
  index.html
  package.json
  vite.config.js
  tailwind.config.js
```

---

## Unit 3: Admin Frontend

### Definition
- **Name**: admin-frontend
- **Type**: Module (독립 빌드/배포 가능)
- **Technology**: Vue.js 3, Tailwind CSS
- **Purpose**: 관리자용 매장 관리 인터페이스

### Responsibilities
- 관리자 인증 (JWT)
- 실시간 주문 모니터링 (WebSocket + 알림음)
- 주문 상태 변경
- 테이블 관리 (초기 설정, 세션 종료, 주문 삭제)
- 메뉴 관리 (CRUD + 이미지 업로드)
- 과거 주문 내역 조회

### Components Included
- AdminAuthModule
- OrderDashboardModule
- TableManagementModule
- MenuManagementModule

### Directory Structure
```
admin-frontend/
  src/
    main.js              # Vue 앱 진입점
    App.vue              # 루트 컴포넌트
    router/
      index.js           # Vue Router 설정
    stores/              # Pinia 상태 관리
      auth.js
      orders.js
      tables.js
      menus.js
    views/               # 페이지 컴포넌트
      LoginView.vue      # 로그인
      DashboardView.vue  # 주문 대시보드 (기본 화면)
      MenuManageView.vue # 메뉴 관리
    components/          # 재사용 컴포넌트
      TableCard.vue
      OrderDetail.vue
      OrderStatusButton.vue
      TableSessionControl.vue
      OrderHistoryModal.vue
      MenuForm.vue
      MenuList.vue
      CategoryManager.vue
      ImageUploader.vue
      SoundToggle.vue
    services/            # API 호출 + WebSocket
      api.js             # Axios 인스턴스
      authService.js
      orderService.js
      tableService.js
      menuService.js
      websocketService.js
    utils/
      sound.js           # 알림음 관리
      storage.js
  public/
    sounds/
      notification.mp3   # 주문 알림음
  index.html
  package.json
  vite.config.js
  tailwind.config.js
```

---

## Code Organization Summary

```
workspace-root/
  backend/               # Unit 1: Backend API Server
  customer-frontend/     # Unit 2: Customer Frontend
  admin-frontend/        # Unit 3: Admin Frontend
  aidlc-docs/            # AIDLC 문서 (코드 아님)
  requirements/          # 원본 요구사항
```
