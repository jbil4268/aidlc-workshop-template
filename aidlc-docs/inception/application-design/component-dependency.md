# Component Dependencies

## System Architecture Overview

```
+------------------+     +-------------------+
| Customer         |     | Admin             |
| Frontend (Vue)   |     | Frontend (Vue)    |
+--------+---------+     +--------+----------+
         |  REST API              |  REST API + WebSocket
         |                        |
+--------v------------------------v----------+
|           Backend API Server               |
|           (Python FastAPI/Django)           |
+--------+-----------------------------------+
         |
+--------v----------+
|    SQLite DB       |
+--------------------+
```

## Backend Component Dependencies

### Dependency Matrix

| Component | Depends On | Depended By |
|-----------|-----------|-------------|
| AuthComponent | DB (Admin, Table) | All API routes (middleware) |
| MenuComponent | DB (Menu, Category) | OrderComponent (메뉴 검증) |
| OrderComponent | DB (Order, OrderItem), MenuComponent, TableComponent | WebSocketComponent |
| TableComponent | DB (Table, TableSession, OrderHistory), OrderComponent | OrderComponent |
| WebSocketComponent | - | OrderService (이벤트 발행) |

### Communication Patterns

**동기 통신 (REST API)**:
- Customer Frontend → Backend: 메뉴 조회, 주문 생성, 주문 내역
- Admin Frontend → Backend: 인증, 메뉴 관리, 테이블 관리, 주문 관리

**비동기 통신 (WebSocket)**:
- Backend → Admin Frontend: 신규 주문, 주문 상태 변경, 주문 삭제 이벤트

### Data Flow

**주문 생성 플로우**:
```
Customer Frontend
  -> POST /api/customer/orders
    -> AuthMiddleware (JWT 검증)
    -> OrderService.create_order()
      -> TableComponent.get_session() (세션 확인)
      -> MenuComponent.get_menus() (메뉴 유효성)
      -> OrderComponent.calculate_tip() (팁 계산)
      -> OrderComponent.create_order() (DB 저장)
      -> WebSocketComponent.broadcast_new_order()
    -> Response (주문 번호)
```

**세션 종료 플로우**:
```
Admin Frontend
  -> POST /api/admin/tables/:id/session/end
    -> AuthMiddleware (JWT 검증)
    -> TableService.end_session()
      -> TableComponent.archive_session_orders() (이력 이동)
      -> TableComponent.end_session() (세션 종료)
      -> 테이블 리셋 (주문 목록, 총액 0)
    -> Response (성공)
```

---

## Frontend Component Dependencies

### Customer Frontend

| Module | Depends On | Purpose |
|--------|-----------|---------|
| CustomerAuthModule | Backend AuthAPI | 인증 |
| MenuBrowseModule | Backend MenuAPI | 메뉴 데이터 |
| CartModule | LocalStorage, MenuBrowseModule | 장바구니 |
| OrderModule | Backend OrderAPI, CartModule | 주문 |

### Admin Frontend

| Module | Depends On | Purpose |
|--------|-----------|---------|
| AdminAuthModule | Backend AuthAPI | 인증 |
| OrderDashboardModule | Backend OrderAPI, WebSocket | 실시간 모니터링 |
| TableManagementModule | Backend TableAPI | 테이블 관리 |
| MenuManagementModule | Backend MenuAPI | 메뉴 관리 |

---

## Shared Dependencies

### Cross-Cutting Concerns
- **Authentication Middleware**: 모든 API 요청에 JWT 검증 적용
- **Error Handling**: 통일된 에러 응답 형식
- **Validation**: 입력 데이터 검증 (Backend + Frontend)
- **CORS**: Frontend-Backend 간 Cross-Origin 설정
