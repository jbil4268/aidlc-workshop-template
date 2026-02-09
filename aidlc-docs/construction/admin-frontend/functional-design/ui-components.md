# Admin Frontend - UI Components

## Component Hierarchy

```
App
├── LoginPage
├── DashboardPage
│   ├── OrderList
│   ├── OrderCard
│   └── OrderDetailModal
├── TableManagementPage
│   ├── TableList
│   └── TableForm
├── MenuManagementPage
│   ├── CategoryList
│   ├── MenuList
│   └── MenuForm
└── CategoryManagementPage
    ├── CategoryList
    └── CategoryForm
```

## Core Components

### 1. LoginPage
**Purpose**: 관리자 로그인

**State**:
- `username`: string
- `password`: string
- `loading`: boolean
- `error`: string | null

**API Calls**:
- `POST /api/admin/auth/login`

**Navigation**:
- Success → DashboardPage

---

### 2. DashboardPage
**Purpose**: 실시간 주문 모니터링

**State**:
- `orders`: Order[]
- `selectedOrder`: Order | null
- `statusFilter`: string | null
- `wsConnected`: boolean

**Events**:
- `onOrderSelect(order)`: 주문 상세 보기
- `onStatusChange(orderId, status)`: 주문 상태 변경
- `onFilterChange(status)`: 상태 필터

**WebSocket**:
- `WS /ws/admin/{store_id}` - 실시간 주문 알림

**API Calls**:
- `GET /api/admin/order/list`
- `PATCH /api/admin/order/{id}/status`

---

### 3. TableManagementPage
**Purpose**: 테이블 관리

**State**:
- `tables`: Table[]
- `editingTable`: Table | null
- `showForm`: boolean

**API Calls**:
- `GET /api/admin/table/list`
- `POST /api/admin/table/create`
- `PATCH /api/admin/table/{id}`

---

### 4. MenuManagementPage
**Purpose**: 메뉴 관리

**State**:
- `menus`: Menu[]
- `categories`: Category[]
- `editingMenu`: Menu | null
- `showForm`: boolean

**API Calls**:
- `GET /api/admin/menu/list`
- `POST /api/admin/menu/create`
- `PATCH /api/admin/menu/{id}`
- `POST /api/admin/menu/{id}/upload-image`
- `DELETE /api/admin/menu/{id}`

---

### 5. CategoryManagementPage
**Purpose**: 카테고리 관리

**State**:
- `categories`: Category[]
- `editingCategory`: Category | null
- `showForm`: boolean

**API Calls**:
- `GET /api/admin/category/list`
- `POST /api/admin/category/create`
- `PATCH /api/admin/category/{id}`
- `DELETE /api/admin/category/{id}`

---

## Routing

```
/admin
├── /login              - LoginPage
├── /dashboard          - DashboardPage (protected)
├── /tables             - TableManagementPage (protected)
├── /menus              - MenuManagementPage (protected)
└── /categories         - CategoryManagementPage (protected)
```

**Protected Routes**: JWT 토큰 필요

---

## Key Features

1. ✅ JWT 기반 인증
2. ✅ 실시간 주문 알림 (WebSocket)
3. ✅ 주문 상태 관리
4. ✅ 테이블 CRUD
5. ✅ 메뉴 CRUD (이미지 업로드 포함)
6. ✅ 카테고리 CRUD

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-09  
**Status**: Draft
