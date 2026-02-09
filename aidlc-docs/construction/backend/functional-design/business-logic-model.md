# Business Logic Model - Backend API Server

## Core Business Workflows

### 1. 테이블 로그인 및 세션 관리

#### Workflow: Table Login
```
Input: store_identifier, table_number, table_password
Output: JWT token, session_id

Steps:
1. Store 조회 (store_identifier로)
2. Table 조회 (store_id + table_number로)
3. 비밀번호 검증 (bcrypt.compare)
4. 활성 세션 확인
   - 활성 세션 있음: 기존 session_id 반환
   - 활성 세션 없음: 새 TableSession 생성
5. JWT 토큰 발급 (payload: table_id, session_id, store_id)
6. 토큰 반환 (16시간 만료)
```

**Business Logic**:
- 세션 시작 시점: 테이블 로그인 시 활성 세션이 없으면 자동 생성
- 한 테이블에 동시 활성 세션은 1개만
- JWT payload: `{ table_id, session_id, store_id, exp: 16h }`

---

### 2. 메뉴 조회 및 탐색

#### Workflow: Get Menus by Category
```
Input: store_id, category_id (optional)
Output: List[Menu]

Steps:
1. Category 조회 (store_id 기준, category_id 있으면 필터링)
2. Menu 조회 (is_available=TRUE만)
3. display_order 기준 정렬
4. 메뉴 목록 반환 (이미지 URL, 알러지 정보 포함)
```

**Business Logic**:
- is_available=FALSE인 메뉴는 고객에게 노출 안 됨
- 알러지 정보는 쉼표 구분 문자열 → 배열로 파싱하여 반환
- 이미지 URL은 상대 경로 → 절대 URL로 변환

---

### 3. 주문 생성 및 팁 계산

#### Workflow: Create Order
```
Input: session_id, items (menu_id, quantity), tip_rate
Output: Order

Steps:
1. 세션 유효성 검증 (is_active=TRUE)
2. 메뉴 유효성 검증 (모든 menu_id가 is_available=TRUE)
3. 기존 주문 확인
   - 같은 세션에 pending 또는 preparing 상태 주문 있음: 기존 Order 사용
   - 없음: 새 Order 생성
4. 주문 번호 생성 (매장별 일일 순차)
5. OrderItem 생성 (menu snapshot 저장)
6. 금액 계산:
   - subtotal_amount = sum(unit_price × quantity)
   - tip_amount = round(subtotal_amount × tip_rate / 100)
   - total_amount = subtotal_amount + tip_amount
7. Order 저장
8. TableSession.total_amount 업데이트 (누적)
9. WebSocket 브로드캐스트 (new_order 이벤트)
10. Order 반환
```

**Business Logic**:
- 재주문 처리: 같은 세션에서 미완료 주문이 있으면 기존 Order에 항목 추가
- 주문 번호 생성 알고리즘:
  ```python
  def generate_order_number(store_id):
      today = date.today()
      count = Order.query.filter(
          Order.store_id == store_id,
          func.date(Order.created_at) == today
      ).count()
      return f"#{count + 1:03d}"
  ```
- 팁 계산: 반올림 (round)
- Snapshot: OrderItem에 menu_name, unit_price 복사

---

### 4. 주문 상태 변경

#### Workflow: Update Order Status
```
Input: order_id, new_status
Output: Order

Steps:
1. Order 조회
2. 상태 전이 (모든 전이 허용)
3. Order.status 업데이트
4. Order.updated_at 갱신
5. WebSocket 브로드캐스트 (order_updated 이벤트)
6. Order 반환
```

**Business Logic**:
- 상태 전이: 모든 상태 간 자유롭게 전이 가능 (pending ↔ preparing ↔ completed)
- 검증 없음 (관리자 재량)

---

### 5. 주문 삭제 (관리자 직권)

#### Workflow: Delete Order
```
Input: order_id
Output: Success

Steps:
1. Order 조회
2. OrderItem 삭제 (CASCADE)
3. Order 삭제
4. TableSession.total_amount 재계산 (해당 세션의 남은 주문 합계)
5. WebSocket 브로드캐스트 (order_deleted 이벤트)
6. Success 반환
```

**Business Logic**:
- 물리적 삭제 (Soft Delete 아님)
- 세션 총액 재계산 필수

---

### 6. 테이블 세션 종료 (이용 완료)

#### Workflow: End Table Session
```
Input: table_id
Output: Success

Steps:
1. Table 조회
2. 활성 세션 조회 (current_session_id)
3. 세션의 모든 주문 조회
4. 각 주문을 OrderHistory로 아카이빙:
   - Order + OrderItem을 JSON으로 직렬화
   - OrderHistory 레코드 생성
5. TableSession 종료:
   - end_time = now()
   - is_active = FALSE
6. Table.current_session_id = NULL
7. Success 반환
```

**Business Logic**:
- 미완료 주문(pending/preparing)도 현재 상태 그대로 아카이빙
- 주문 삭제 안 함 (이력 보존)
- 트랜잭션으로 원자성 보장

---

### 7. 메뉴 관리 (CRUD)

#### Workflow: Create Menu
```
Input: store_id, menu_data (name, price, description, category_id, allergens), image_file
Output: Menu

Steps:
1. 데이터 검증 (필수 필드, 가격 >= 0)
2. 이미지 업로드 (있으면):
   - 파일 크기 검증 (최대 10MB)
   - 파일 형식 검증 (JPEG/PNG/WebP)
   - 저장 경로: /uploads/{store_id}/menus/{menu_id}.{ext}
   - image_url 생성
3. Menu 생성 (is_available=TRUE)
4. Menu 반환
```

#### Workflow: Update Menu
```
Input: menu_id, menu_data, image_file (optional)
Output: Menu

Steps:
1. Menu 조회
2. 데이터 검증
3. 이미지 교체 (새 이미지 있으면):
   - 기존 이미지 삭제
   - 새 이미지 업로드
4. Menu 업데이트
5. updated_at 갱신
6. Menu 반환
```

#### Workflow: Delete Menu
```
Input: menu_id
Output: Success

Steps:
1. Menu 조회
2. Soft Delete: is_available = FALSE
3. updated_at 갱신
4. Success 반환
```

**Business Logic**:
- 메뉴 삭제는 Soft Delete (기존 주문 보호)
- 이미지 업로드 제한: 최대 10MB, JPEG/PNG/WebP

---

### 8. 카테고리 관리

#### Workflow: Delete Category
```
Input: category_id
Output: Success

Steps:
1. Category 조회
2. 기본 카테고리 확인 (is_default=TRUE면 삭제 불가)
3. "미분류" 카테고리 조회 (같은 store_id, is_default=TRUE)
4. 소속 메뉴를 "미분류"로 이동:
   - Menu.category_id = 미분류_category_id
5. Category 삭제
6. Success 반환
```

**Business Logic**:
- 기본 카테고리("미분류")는 삭제 불가
- 소속 메뉴는 자동으로 "미분류"로 이동

---

### 9. 관리자 인증

#### Workflow: Admin Login
```
Input: store_identifier, username, password
Output: JWT token

Steps:
1. 로그인 시도 제한 확인:
   - Admin.locked_until > now() → 에러 반환
2. Store 조회 (store_identifier로)
3. Admin 조회 (username + store_id로)
4. 비밀번호 검증 (bcrypt.compare)
5. 검증 성공:
   - login_attempts = 0
   - last_login = now()
   - locked_until = NULL
   - JWT 토큰 발급 (payload: admin_id, store_id, exp: 16h)
6. 검증 실패:
   - login_attempts += 1
   - login_attempts >= 5 → locked_until = now() + 5분
   - 에러 반환
7. 토큰 반환
```

**Business Logic**:
- 로그인 실패 5회 시 5분간 계정 잠금
- JWT payload: `{ admin_id, store_id, role: 'admin', exp: 16h }`

---

### 10. 실시간 주문 모니터링 (WebSocket)

#### Workflow: WebSocket Connection
```
Input: store_id (from JWT)
Output: WebSocket connection

Steps:
1. JWT 검증 (admin 권한 확인)
2. WebSocket 연결 생성
3. 매장 채널 구독 (store_id 기반)
4. 연결 유지
```

#### Events:
- **new_order**: 새 주문 생성 시
  ```json
  {
    "event": "new_order",
    "data": {
      "order_id": "uuid",
      "table_number": 5,
      "order_number": "#001",
      "total_amount": 16500,
      "items": [...]
    }
  }
  ```
- **order_updated**: 주문 상태 변경 시
  ```json
  {
    "event": "order_updated",
    "data": {
      "order_id": "uuid",
      "status": "preparing"
    }
  }
  ```
- **order_deleted**: 주문 삭제 시
  ```json
  {
    "event": "order_deleted",
    "data": {
      "order_id": "uuid"
    }
  }
  ```

**Business Logic**:
- 매장별 채널 분리 (store_id 기반)
- 관리자만 구독 가능 (JWT 검증)

---

## Data Flow Diagrams

### Order Creation Flow
```
Customer →장바구니 → 주문 확정
                        ↓
                  Validate Session
                        ↓
                  Validate Menus
                        ↓
              Check Existing Order
                   ↙        ↘
          기존 Order 있음   없음
                ↓            ↓
          Add Items    Create Order
                ↓            ↓
          Calculate Amounts
                ↓
          Save to DB
                ↓
          Update Session Total
                ↓
          WebSocket Broadcast
                ↓
          Return Order
```

### Session Lifecycle
```
Table Login → Create Session (if not exists)
                    ↓
              Active Session
                    ↓
              Orders Created
                    ↓
              Admin: End Session
                    ↓
              Archive Orders
                    ↓
              Close Session
                    ↓
              Reset Table
```

---

## Calculation Algorithms

### 1. Order Number Generation
```python
def generate_order_number(store_id: str) -> str:
    """
    매장별 일일 순차 번호 생성
    형식: #{일련번호:03d}
    """
    today = date.today()
    
    # 오늘 생성된 주문 수 조회
    count = db.session.query(Order).filter(
        Order.store_id == store_id,
        func.date(Order.created_at) == today
    ).count()
    
    # 다음 번호 생성
    next_number = count + 1
    return f"#{next_number:03d}"
```

### 2. Tip Calculation
```python
def calculate_tip(subtotal: int, tip_rate: int) -> int:
    """
    팁 금액 계산 (반올림)
    
    Args:
        subtotal: 메뉴 금액 합계 (원)
        tip_rate: 팁 비율 (0, 5, 10, 15, 20)
    
    Returns:
        팁 금액 (원)
    """
    if tip_rate not in [0, 5, 10, 15, 20]:
        raise ValueError("Invalid tip_rate")
    
    tip_amount = round(subtotal * tip_rate / 100)
    return tip_amount
```

### 3. Session Total Calculation
```python
def calculate_session_total(session_id: str) -> int:
    """
    세션 총 주문 금액 계산
    """
    total = db.session.query(
        func.sum(Order.total_amount)
    ).filter(
        Order.session_id == session_id
    ).scalar()
    
    return total or 0
```

---

## Error Handling Patterns

### 1. Validation Errors
- **Invalid Input**: 400 Bad Request
- **Menu Not Available**: 400 Bad Request
- **Session Expired**: 401 Unauthorized

### 2. Business Logic Errors
- **Duplicate Order Number**: Retry with new number
- **Session Not Active**: 400 Bad Request
- **Account Locked**: 403 Forbidden

### 3. System Errors
- **Database Error**: 500 Internal Server Error
- **WebSocket Connection Failed**: Retry with exponential backoff

---

## Concurrency Handling

### 1. Order Number Generation
- **Problem**: 동시 주문 시 중복 번호 생성 가능
- **Solution**: Database-level UNIQUE constraint + retry logic
  ```python
  max_retries = 3
  for attempt in range(max_retries):
      try:
          order_number = generate_order_number(store_id)
          order = Order(order_number=order_number, ...)
          db.session.add(order)
          db.session.commit()
          break
      except IntegrityError:
          db.session.rollback()
          if attempt == max_retries - 1:
              raise
  ```

### 2. Session Creation
- **Problem**: 동시 로그인 시 중복 세션 생성 가능
- **Solution**: UNIQUE INDEX on (table_id, is_active=TRUE)

---

## Performance Optimization

### 1. Database Indexes
- Order: (store_id, created_at) - 일일 주문 번호 생성
- Order: (session_id, status) - 세션별 주문 조회
- Menu: (store_id, is_available) - 메뉴 목록 조회

### 2. Caching Strategy
- Menu 목록: Redis 캐싱 (TTL: 5분)
- Category 목록: Redis 캐싱 (TTL: 10분)
- Cache invalidation: 메뉴/카테고리 수정 시

### 3. Query Optimization
- Eager loading: Order + OrderItem (N+1 방지)
- Pagination: 주문 내역 조회 시 (limit/offset)

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-09  
**Status**: Draft
