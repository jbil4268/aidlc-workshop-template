# Contract/Interface Definition for Backend API Server

## Unit Context
- **Unit**: Backend API Server
- **Stories**: US-1.1, US-2.1, US-2.2, US-4.1, US-5.1, US-6.1, US-7.1, US-7.2, US-8.1, US-8.2, US-8.3, US-8.4, US-9.1, US-9.2, US-ERR-1, US-ERR-2
- **Dependencies**: None (독립 실행)
- **Database Entities**: Store, Table, TableSession, Category, Menu, Order, OrderItem, Admin, OrderHistory
- **Service Boundaries**: REST API + WebSocket 서버

## TDD Scope (핵심 비즈니스 로직만)
Requirements에 따라 다음 핵심 비즈니스 로직만 TDD로 구현:
1. **주문 생성 로직** (OrderService)
2. **세션 관리 로직** (TableSessionService)
3. **인증 로직** (AuthService)

나머지 코드(API 라우터, 모델, 스키마, 유틸리티)는 TDD 없이 직접 생성합니다.

---

## Core Business Logic Layer (TDD 적용)

### 1. AuthService
**Purpose**: 인증 및 토큰 관리

#### Methods

##### `hash_password(password: str) -> str`
비밀번호를 bcrypt로 해싱합니다.

- **Args**:
  - `password`: 평문 비밀번호
- **Returns**: bcrypt 해시된 비밀번호
- **Raises**: None

##### `verify_password(plain_password: str, hashed_password: str) -> bool`
비밀번호를 검증합니다.

- **Args**:
  - `plain_password`: 평문 비밀번호
  - `hashed_password`: 해시된 비밀번호
- **Returns**: 일치 여부 (True/False)
- **Raises**: None

##### `create_jwt_token(payload: dict, expires_hours: int = 16) -> str`
JWT 토큰을 생성합니다.

- **Args**:
  - `payload`: 토큰에 포함할 데이터 (dict)
  - `expires_hours`: 만료 시간 (기본 16시간)
- **Returns**: JWT 토큰 문자열
- **Raises**: None

##### `verify_jwt_token(token: str) -> dict`
JWT 토큰을 검증하고 payload를 반환합니다.

- **Args**:
  - `token`: JWT 토큰 문자열
- **Returns**: 토큰 payload (dict)
- **Raises**:
  - `TokenExpiredError`: 토큰 만료 시
  - `InvalidTokenError`: 토큰 무효 시

---

### 2. TableSessionService
**Purpose**: 테이블 세션 라이프사이클 관리

#### Methods

##### `create_session(table_id: str) -> TableSession`
새 테이블 세션을 생성합니다.

- **Args**:
  - `table_id`: 테이블 ID
- **Returns**: 생성된 TableSession 객체
- **Raises**:
  - `ActiveSessionExistsError`: 이미 활성 세션이 존재하는 경우

##### `get_active_session(table_id: str) -> Optional[TableSession]`
테이블의 활성 세션을 조회합니다.

- **Args**:
  - `table_id`: 테이블 ID
- **Returns**: 활성 TableSession 또는 None
- **Raises**: None

##### `end_session(session_id: str) -> bool`
세션을 종료하고 주문을 아카이빙합니다.

- **Args**:
  - `session_id`: 세션 ID
- **Returns**: 성공 여부 (True/False)
- **Raises**:
  - `SessionNotFoundError`: 세션이 존재하지 않는 경우
  - `SessionAlreadyEndedError`: 이미 종료된 세션인 경우

---

### 3. OrderService
**Purpose**: 주문 생성 및 관리

#### Methods

##### `generate_order_number(store_id: str, date: date) -> str`
매장별 일일 순차 주문 번호를 생성합니다.

- **Args**:
  - `store_id`: 매장 ID
  - `date`: 주문 날짜
- **Returns**: 주문 번호 (예: "#001")
- **Raises**: None

##### `calculate_tip(subtotal: int, tip_rate: int) -> int`
팁 금액을 계산합니다 (반올림).

- **Args**:
  - `subtotal`: 메뉴 금액 합계 (원)
  - `tip_rate`: 팁 비율 (0, 5, 10, 15, 20)
- **Returns**: 팁 금액 (원)
- **Raises**:
  - `InvalidTipRateError`: 잘못된 팁 비율인 경우

##### `create_order(session_id: str, items: List[OrderItemData], tip_rate: int) -> Order`
주문을 생성합니다.

- **Args**:
  - `session_id`: 세션 ID
  - `items`: 주문 항목 리스트 (menu_id, quantity)
  - `tip_rate`: 팁 비율
- **Returns**: 생성된 Order 객체
- **Raises**:
  - `SessionNotActiveError`: 세션이 활성 상태가 아닌 경우
  - `MenuNotAvailableError`: 메뉴가 주문 불가능한 경우
  - `InvalidQuantityError`: 수량이 0 이하인 경우

##### `update_order_status(order_id: str, new_status: str) -> Order`
주문 상태를 변경합니다.

- **Args**:
  - `order_id`: 주문 ID
  - `new_status`: 새 상태 ("pending", "preparing", "completed")
- **Returns**: 업데이트된 Order 객체
- **Raises**:
  - `OrderNotFoundError`: 주문이 존재하지 않는 경우
  - `InvalidStatusError`: 잘못된 상태 값인 경우

---

## Supporting Code (TDD 없이 직접 생성)

다음 코드는 TDD 없이 직접 생성합니다:

### API Layer
- FastAPI 라우터 (customer_auth, customer_menu, customer_order, admin_auth, admin_order, admin_table, admin_menu, admin_category)
- Pydantic 스키마 (요청/응답 검증)
- 의존성 주입 함수 (get_db, get_current_table, get_current_admin)

### Data Layer
- SQLAlchemy 모델 (Store, Table, TableSession, Category, Menu, Order, OrderItem, Admin, OrderHistory)
- Database 설정 (engine, SessionLocal)

### WebSocket Layer
- ConnectionManager 클래스
- WebSocket 엔드포인트

### Utilities
- 에러 클래스 정의
- 헬퍼 함수

### Configuration
- FastAPI 앱 설정
- CORS 미들웨어
- Global Exception Handler
- 환경 변수 설정 (pydantic-settings)

### Infrastructure
- Alembic 마이그레이션 스크립트
- requirements.txt
- .env.example
- README.md

---

## Data Types

### OrderItemData
```python
@dataclass
class OrderItemData:
    menu_id: str
    quantity: int
```

### TableSession
```python
@dataclass
class TableSession:
    session_id: str
    table_id: str
    start_time: datetime
    end_time: Optional[datetime]
    is_active: bool
    total_amount: int
```

### Order
```python
@dataclass
class Order:
    order_id: str
    session_id: str
    table_id: str
    store_id: str
    order_number: str
    subtotal_amount: int
    tip_rate: int
    tip_amount: int
    total_amount: int
    status: str
    items: List[OrderItem]
    created_at: datetime
    updated_at: datetime
```

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-09  
**Status**: Draft
