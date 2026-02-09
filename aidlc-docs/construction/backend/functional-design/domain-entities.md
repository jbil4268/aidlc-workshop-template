# Domain Entities - Backend API Server

## Entity Relationship Overview

```
Store (1) ----< (N) Table
Store (1) ----< (N) Menu
Store (1) ----< (N) Category
Store (1) ----< (N) Admin
Store (1) ----< (N) Order

Table (1) ----< (N) TableSession
Table (1) ----< (N) Order

TableSession (1) ----< (N) Order
TableSession (1) ----< (N) OrderHistory

Menu (N) >---- (1) Category

Order (1) ----< (N) OrderItem
Order (N) >---- (1) Menu (snapshot)

OrderHistory (1) ---- (1) Order (archived)
```

---

## Entity Definitions

### 1. Store (매장)

**Purpose**: 다중 매장 지원을 위한 최상위 엔티티

**Attributes**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| store_id | UUID | PK | 매장 고유 식별자 |
| store_name | String(100) | NOT NULL | 매장 이름 |
| store_identifier | String(50) | UNIQUE, NOT NULL | 로그인용 매장 식별자 |
| created_at | DateTime | NOT NULL | 생성 시각 |

**Business Rules**:
- store_identifier는 영문 소문자, 숫자, 하이픈만 허용
- 삭제 불가 (소프트 삭제 또는 비활성화 권장)

**Indexes**:
- PRIMARY KEY: store_id
- UNIQUE INDEX: store_identifier

---

### 2. Table (테이블)

**Purpose**: 매장 내 물리적 테이블 정보

**Attributes**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| table_id | UUID | PK | 테이블 고유 식별자 |
| store_id | UUID | FK, NOT NULL | 소속 매장 |
| table_number | Integer | NOT NULL | 테이블 번호 (매장 내 고유) |
| table_password | String(255) | NOT NULL | bcrypt 해시된 비밀번호 |
| current_session_id | UUID | FK, NULLABLE | 현재 활성 세션 (없으면 NULL) |
| created_at | DateTime | NOT NULL | 생성 시각 |

**Business Rules**:
- (store_id, table_number) 조합은 UNIQUE
- table_password는 bcrypt로 해싱 (salt rounds: 10)
- current_session_id는 활성 세션이 있을 때만 값 존재

**Indexes**:
- PRIMARY KEY: table_id
- UNIQUE INDEX: (store_id, table_number)
- INDEX: current_session_id

---

### 3. TableSession (테이블 세션)

**Purpose**: 고객의 테이블 이용 세션 (착석 ~ 이용 완료)

**Attributes**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| session_id | UUID | PK | 세션 고유 식별자 |
| table_id | UUID | FK, NOT NULL | 소속 테이블 |
| start_time | DateTime | NOT NULL | 세션 시작 시각 |
| end_time | DateTime | NULLABLE | 세션 종료 시각 (NULL이면 활성) |
| is_active | Boolean | NOT NULL, DEFAULT TRUE | 활성 여부 |
| total_amount | Integer | NOT NULL, DEFAULT 0 | 세션 총 주문 금액 (원) |

**Business Rules**:
- 세션 시작: 테이블 로그인 시 활성 세션이 없으면 자동 생성 (Q3: A)
- 세션 종료: 관리자가 "이용 완료" 처리 시 end_time 설정, is_active = FALSE
- 한 테이블에 동시에 활성 세션은 1개만 존재
- 세션 종료 시 모든 주문을 OrderHistory로 아카이빙 (Q8: C - 현재 상태 그대로)
- 16시간 후 자동 만료 (JWT 토큰 만료와 동일)

**Indexes**:
- PRIMARY KEY: session_id
- INDEX: table_id
- INDEX: (table_id, is_active) - 활성 세션 조회 최적화

---

### 4. Category (카테고리)

**Purpose**: 메뉴 분류

**Attributes**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| category_id | UUID | PK | 카테고리 고유 식별자 |
| store_id | UUID | FK, NOT NULL | 소속 매장 |
| category_name | String(50) | NOT NULL | 카테고리 이름 |
| display_order | Integer | NOT NULL, DEFAULT 0 | 노출 순서 |
| is_default | Boolean | NOT NULL, DEFAULT FALSE | 기본 카테고리 여부 ("미분류") |

**Business Rules**:
- 매장당 1개의 기본 카테고리 필수 (is_default=TRUE, category_name="미분류")
- 카테고리 삭제 시: 소속 메뉴를 "미분류" 카테고리로 이동 (Q5: B)
- 기본 카테고리는 삭제 불가

**Indexes**:
- PRIMARY KEY: category_id
- INDEX: (store_id, display_order)

---

### 5. Menu (메뉴)

**Purpose**: 주문 가능한 메뉴 항목

**Attributes**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| menu_id | UUID | PK | 메뉴 고유 식별자 |
| store_id | UUID | FK, NOT NULL | 소속 매장 |
| category_id | UUID | FK, NOT NULL | 소속 카테고리 |
| menu_name | String(100) | NOT NULL | 메뉴 이름 |
| price | Integer | NOT NULL, CHECK >= 0 | 가격 (원) |
| description | Text | NULLABLE | 메뉴 설명 |
| image_url | String(500) | NULLABLE | 이미지 URL (상대 경로) |
| allergens | String(200) | NULLABLE | 알러지 정보 (쉼표 구분, 예: "우유,계란,밀") |
| display_order | Integer | NOT NULL, DEFAULT 0 | 카테고리 내 노출 순서 |
| is_available | Boolean | NOT NULL, DEFAULT TRUE | 주문 가능 여부 |
| created_at | DateTime | NOT NULL | 생성 시각 |
| updated_at | DateTime | NOT NULL | 수정 시각 |

**Business Rules**:
- 메뉴 삭제 시: Soft Delete (is_available=FALSE) (Q4: B)
- 이미지 업로드: 최대 10MB, JPEG/PNG/WebP 허용 (Q7: B)
- 이미지 저장 경로: `/uploads/{store_id}/menus/{menu_id}.{ext}`
- allergens 값 예시: "우유,계란,밀,대두,땅콩,갑각류,생선,견과류"

**Indexes**:
- PRIMARY KEY: menu_id
- INDEX: (store_id, category_id, display_order)
- INDEX: (store_id, is_available)

---

### 6. Order (주문)

**Purpose**: 고객의 주문 정보

**Attributes**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| order_id | UUID | PK | 주문 고유 식별자 |
| session_id | UUID | FK, NOT NULL | 소속 세션 |
| table_id | UUID | FK, NOT NULL | 소속 테이블 |
| store_id | UUID | FK, NOT NULL | 소속 매장 |
| order_number | String(20) | UNIQUE, NOT NULL | 주문 번호 (예: #001) |
| subtotal_amount | Integer | NOT NULL, CHECK >= 0 | 메뉴 금액 합계 (원) |
| tip_rate | Integer | NOT NULL, DEFAULT 0, CHECK IN (0,5,10,15,20) | 팁 비율 (%) |
| tip_amount | Integer | NOT NULL, DEFAULT 0, CHECK >= 0 | 팁 금액 (원, 계산값) |
| total_amount | Integer | NOT NULL, CHECK >= 0 | 총 금액 (subtotal + tip) |
| status | Enum | NOT NULL, DEFAULT 'pending' | 주문 상태 |
| created_at | DateTime | NOT NULL | 주문 생성 시각 |
| updated_at | DateTime | NOT NULL | 수정 시각 |

**Status Enum**: `pending`, `preparing`, `completed`

**Business Rules**:
- order_number 생성: 매장별 일일 리셋 순차 번호 (Q1: A)
  - 형식: `#{일련번호:03d}` (예: #001, #002, ..., #999)
  - 매일 00:00 기준으로 리셋
- tip_amount 계산: `round(subtotal_amount * tip_rate / 100)` (Q6: A - 반올림)
- total_amount 계산: `subtotal_amount + tip_amount`
- 상태 전이: 모든 상태 간 자유롭게 전이 가능 (Q2: C)
- 재주문 처리: 같은 세션에서 재주문 시 기존 Order에 OrderItem 추가 (Q10: B)
  - 단, 이미 completed 상태인 주문은 새 Order 생성

**Indexes**:
- PRIMARY KEY: order_id
- UNIQUE INDEX: order_number
- INDEX: (store_id, created_at) - 일일 주문 번호 생성 최적화
- INDEX: (session_id, status)
- INDEX: (table_id, created_at)

---

### 7. OrderItem (주문 항목)

**Purpose**: 주문에 포함된 개별 메뉴 항목

**Attributes**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| order_item_id | UUID | PK | 주문 항목 고유 식별자 |
| order_id | UUID | FK, NOT NULL | 소속 주문 |
| menu_id | UUID | FK, NOT NULL | 메뉴 참조 |
| menu_name | String(100) | NOT NULL | 메뉴 이름 (snapshot) |
| quantity | Integer | NOT NULL, CHECK > 0 | 수량 |
| unit_price | Integer | NOT NULL, CHECK >= 0 | 단가 (원, snapshot) |
| subtotal | Integer | NOT NULL, CHECK >= 0 | 소계 (unit_price × quantity) |

**Business Rules**:
- menu_name, unit_price는 주문 시점의 snapshot (메뉴 수정/삭제 시에도 유지)
- subtotal 계산: `unit_price * quantity`
- 메뉴 삭제 후에도 OrderItem은 snapshot 데이터로 유지

**Indexes**:
- PRIMARY KEY: order_item_id
- INDEX: order_id
- INDEX: menu_id

---

### 8. Admin (관리자)

**Purpose**: 매장 관리자 계정

**Attributes**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| admin_id | UUID | PK | 관리자 고유 식별자 |
| store_id | UUID | FK, NOT NULL | 소속 매장 |
| username | String(50) | UNIQUE, NOT NULL | 사용자명 |
| password_hash | String(255) | NOT NULL | bcrypt 해시된 비밀번호 |
| created_at | DateTime | NOT NULL | 생성 시각 |
| last_login | DateTime | NULLABLE | 마지막 로그인 시각 |
| login_attempts | Integer | NOT NULL, DEFAULT 0 | 로그인 실패 횟수 |
| locked_until | DateTime | NULLABLE | 계정 잠금 해제 시각 |

**Business Rules**:
- password_hash는 bcrypt로 해싱 (salt rounds: 10)
- 로그인 실패 5회 시 5분간 계정 잠금
- 초기 관리자 생성: Seed 데이터 (환경 변수 기반) (Q9: A)
  - 환경 변수: `ADMIN_USERNAME`, `ADMIN_PASSWORD`, `STORE_IDENTIFIER`

**Indexes**:
- PRIMARY KEY: admin_id
- UNIQUE INDEX: username
- INDEX: store_id

---

### 9. OrderHistory (주문 이력)

**Purpose**: 세션 종료 후 아카이빙된 주문 데이터

**Attributes**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| history_id | UUID | PK | 이력 고유 식별자 |
| order_id | UUID | FK, NOT NULL | 원본 주문 참조 |
| session_id | UUID | FK, NOT NULL | 소속 세션 |
| table_id | UUID | FK, NOT NULL | 소속 테이블 |
| store_id | UUID | FK, NOT NULL | 소속 매장 |
| order_number | String(20) | NOT NULL | 주문 번호 (snapshot) |
| order_data | JSON | NOT NULL | 주문 전체 데이터 (Order + OrderItem) |
| archived_at | DateTime | NOT NULL | 아카이빙 시각 |

**Business Rules**:
- 세션 종료 시 모든 주문을 현재 상태 그대로 아카이빙 (Q8: C)
- order_data JSON 구조:
  ```json
  {
    "order_id": "uuid",
    "order_number": "#001",
    "subtotal_amount": 15000,
    "tip_rate": 10,
    "tip_amount": 1500,
    "total_amount": 16500,
    "status": "completed",
    "created_at": "2026-02-09T12:00:00Z",
    "items": [
      {
        "menu_name": "김치찌개",
        "quantity": 2,
        "unit_price": 7500,
        "subtotal": 15000
      }
    ]
  }
  ```
- 1년 후 별도 아카이빙 스토리지로 이동 권장

**Indexes**:
- PRIMARY KEY: history_id
- INDEX: (table_id, archived_at)
- INDEX: (store_id, archived_at)
- INDEX: session_id

---

## Data Integrity Rules

### Referential Integrity
- 모든 FK는 CASCADE DELETE 또는 RESTRICT 정책 적용
- Store 삭제 시: RESTRICT (하위 데이터 존재 시 삭제 불가)
- Table 삭제 시: RESTRICT (활성 세션 존재 시 삭제 불가)
- Category 삭제 시: 소속 메뉴를 "미분류"로 이동 후 삭제
- Menu 삭제 시: Soft Delete (is_available=FALSE)

### Transaction Boundaries
- 주문 생성: Order + OrderItem 생성은 단일 트랜잭션
- 세션 종료: Order → OrderHistory 이동 + TableSession 종료는 단일 트랜잭션
- 주문 상태 변경: Order 업데이트 + WebSocket 브로드캐스트는 단일 트랜잭션

### Concurrency Control
- 주문 번호 생성: 매장별 일일 카운터에 대한 락 필요
- 세션 생성: 테이블당 활성 세션 1개 제약 (UNIQUE INDEX 활용)

---

## Entity Lifecycle

### Store
- 생성: 초기 설정 시 (Seed 데이터 또는 관리자 등록)
- 수정: 매장 정보 변경
- 삭제: 불가 (비활성화 권장)

### Table
- 생성: 관리자가 테이블 초기 설정
- 수정: 테이블 번호 또는 비밀번호 변경
- 삭제: 활성 세션 없을 때만 가능

### TableSession
- 생성: 테이블 로그인 시 (활성 세션 없으면)
- 종료: 관리자가 "이용 완료" 처리
- 삭제: 불가 (이력 보존)

### Menu
- 생성: 관리자가 메뉴 등록
- 수정: 관리자가 메뉴 정보 변경
- 삭제: Soft Delete (is_available=FALSE)

### Order
- 생성: 고객이 주문 확정
- 수정: 관리자가 상태 변경
- 삭제: 관리자 직권 삭제 (물리적 삭제)
- 아카이빙: 세션 종료 시 OrderHistory로 이동

---

## Snapshot Pattern

**Purpose**: 메뉴 정보 변경 시에도 과거 주문 데이터 무결성 유지

**Entities Using Snapshot**:
- OrderItem: menu_name, unit_price (주문 시점 값 저장)
- OrderHistory: order_data (전체 주문 정보 JSON 저장)

**Implementation**:
- 주문 생성 시 Menu 테이블에서 현재 값을 복사하여 OrderItem에 저장
- 세션 종료 시 Order + OrderItem 전체를 JSON으로 직렬화하여 OrderHistory에 저장

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-09  
**Status**: Draft
