# Customer Frontend - UI Components

## Component Hierarchy

```
App
├── QRScanPage
├── MenuListPage
│   ├── CategoryTabs
│   ├── MenuCard
│   └── MenuDetailModal
├── OrderPage
│   ├── OrderSummary
│   ├── TipSelector
│   └── OrderConfirmButton
└── OrderStatusPage
    ├── OrderList
    └── OrderCard
```

## Core Components

### 1. QRScanPage
**Purpose**: QR 코드 스캔 및 테이블 로그인

**State**:
- `scanning`: boolean (스캔 중 여부)
- `error`: string | null (에러 메시지)

**Props**: None (root page)

**Events**:
- `onScanSuccess(qrCode)`: QR 코드 스캔 성공
- `onScanError(error)`: 스캔 실패

**API Calls**:
- `POST /api/customer/auth/login` - 테이블 로그인

**Navigation**:
- Success → MenuListPage
- Error → 에러 메시지 표시

---

### 2. MenuListPage
**Purpose**: 메뉴 목록 표시 및 주문 담기

**State**:
- `categories`: Category[] (카테고리 목록)
- `menus`: Menu[] (메뉴 목록)
- `selectedCategory`: number | null (선택된 카테고리)
- `cart`: CartItem[] (장바구니)
- `selectedMenu`: Menu | null (상세보기 메뉴)

**Props**: None (root page)

**Events**:
- `onCategorySelect(categoryId)`: 카테고리 선택
- `onMenuClick(menu)`: 메뉴 클릭 (상세보기)
- `onAddToCart(menu, quantity)`: 장바구니 추가
- `onCheckout()`: 주문하기

**API Calls**:
- `GET /api/customer/menu/list` - 메뉴 목록 조회

**Navigation**:
- Checkout → OrderPage

---

### 3. CategoryTabs
**Purpose**: 카테고리 탭 표시

**Props**:
- `categories`: Category[]
- `selectedCategory`: number | null
- `onSelect`: (categoryId) => void

**Rendering**:
- 가로 스크롤 가능한 탭
- 선택된 카테고리 하이라이트

---

### 4. MenuCard
**Purpose**: 메뉴 카드 표시

**Props**:
- `menu`: Menu
- `onClick`: (menu) => void

**Rendering**:
- 메뉴 이미지 (없으면 placeholder)
- 메뉴명, 가격
- 알러지 정보 (아이콘)
- 품절 표시 (is_available=false)

---

### 5. MenuDetailModal
**Purpose**: 메뉴 상세 정보 모달

**Props**:
- `menu`: Menu | null
- `onClose`: () => void
- `onAddToCart`: (menu, quantity) => void

**State**:
- `quantity`: number (수량, 기본값 1)

**Rendering**:
- 메뉴 이미지 (크게)
- 메뉴명, 설명, 가격
- 알러지 정보 (상세)
- 수량 선택 (+/- 버튼)
- 장바구니 담기 버튼

---

### 6. OrderPage
**Purpose**: 주문 확인 및 팁 선택

**State**:
- `cart`: CartItem[] (장바구니)
- `tipRate`: number (팁 비율, 기본값 0)
- `subtotal`: number (메뉴 금액 합계)
- `tipAmount`: number (팁 금액)
- `totalAmount`: number (총 금액)

**Props**: None (root page)

**Events**:
- `onTipSelect(rate)`: 팁 비율 선택
- `onConfirmOrder()`: 주문 확정
- `onBack()`: 뒤로가기

**API Calls**:
- `POST /api/customer/order/create` - 주문 생성

**Navigation**:
- Success → OrderStatusPage
- Back → MenuListPage

---

### 7. TipSelector
**Purpose**: 팁 비율 선택 UI

**Props**:
- `selectedRate`: number
- `onSelect`: (rate) => void

**Rendering**:
- 버튼 그룹: 0%, 5%, 10%, 15%, 20%
- 선택된 버튼 하이라이트

---

### 8. OrderSummary
**Purpose**: 주문 요약 표시

**Props**:
- `cart`: CartItem[]
- `subtotal`: number
- `tipRate`: number
- `tipAmount`: number
- `totalAmount`: number

**Rendering**:
- 주문 항목 목록 (메뉴명, 수량, 금액)
- 소계
- 팁 (비율 + 금액)
- 총 금액

---

### 9. OrderStatusPage
**Purpose**: 주문 상태 확인

**State**:
- `orders`: Order[] (주문 목록)
- `pollingInterval`: number (폴링 간격)

**Props**: None (root page)

**Events**:
- `onRefresh()`: 새로고침
- `onEndSession()`: 세션 종료

**API Calls**:
- `GET /api/customer/order/list` - 주문 목록 조회
- `POST /api/customer/auth/logout` - 세션 종료

**Polling**:
- 5초마다 주문 목록 자동 갱신

**Navigation**:
- End Session → QRScanPage

---

### 10. OrderList
**Purpose**: 주문 목록 표시

**Props**:
- `orders`: Order[]

**Rendering**:
- 주문 카드 목록 (최신순)

---

### 11. OrderCard
**Purpose**: 주문 카드 표시

**Props**:
- `order`: Order

**Rendering**:
- 주문 번호
- 주문 시간
- 주문 상태 (pending/preparing/ready/served)
- 주문 항목 요약
- 총 금액

**Status Colors**:
- pending: 회색
- preparing: 주황색
- ready: 초록색
- served: 파란색

---

## Data Types

### CartItem
```typescript
interface CartItem {
  menu: Menu;
  quantity: number;
}
```

### Menu
```typescript
interface Menu {
  id: number;
  category_id: number;
  name: string;
  description: string | null;
  price: number;
  image_url: string | null;
  allergens: string | null;
  is_available: boolean;
}
```

### Category
```typescript
interface Category {
  id: number;
  name: string;
  display_order: number;
}
```

### Order
```typescript
interface Order {
  id: number;
  order_number: string;
  subtotal_amount: number;
  tip_rate: number;
  tip_amount: number;
  total_amount: number;
  status: string;
  items: OrderItem[];
  created_at: string;
}
```

### OrderItem
```typescript
interface OrderItem {
  id: number;
  menu_name: string;
  menu_price: number;
  quantity: number;
  subtotal: number;
}
```

---

## State Management

### Global State (SessionStorage)
- `sessionToken`: string (세션 토큰)
- `tableNumber`: string (테이블 번호)
- `tableId`: number (테이블 ID)

### Local State
- 각 컴포넌트별 로컬 상태 관리
- Props drilling 최소화

---

## Routing

```
/ (root)
├── /scan          - QRScanPage
├── /menu          - MenuListPage
├── /order         - OrderPage
└── /status        - OrderStatusPage
```

**Protected Routes**:
- `/menu`, `/order`, `/status` - sessionToken 필요

**Redirect Logic**:
- sessionToken 없음 → `/scan`
- sessionToken 있음 → `/menu`

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-09  
**Status**: Draft
