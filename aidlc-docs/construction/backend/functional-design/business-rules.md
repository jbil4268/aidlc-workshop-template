# Business Rules - Backend API Server

## Authentication & Authorization Rules

### AR-1: 테이블 로그인 규칙
**Rule**: 테이블은 매장 식별자, 테이블 번호, 비밀번호로 인증

**Conditions**:
- store_identifier가 존재하는 매장이어야 함
- table_number가 해당 매장에 존재해야 함
- table_password가 bcrypt 검증을 통과해야 함

**Actions**:
- 성공 시: JWT 토큰 발급 (16시간 만료)
- 실패 시: 401 Unauthorized 반환

**Exceptions**:
- 매장 또는 테이블이 존재하지 않음: 404 Not Found
- 비밀번호 불일치: 401 Unauthorized

---

### AR-2: 관리자 로그인 규칙
**Rule**: 관리자는 매장 식별자, 사용자명, 비밀번호로 인증하며, 로그인 시도 제한 적용

**Conditions**:
- 계정이 잠금 상태가 아니어야 함 (locked_until <= now())
- store_identifier가 존재하는 매장이어야 함
- username이 해당 매장에 존재해야 함
- password가 bcrypt 검증을 통과해야 함

**Actions**:
- 성공 시:
  - login_attempts = 0
  - last_login = now()
  - locked_until = NULL
  - JWT 토큰 발급 (16시간 만료)
- 실패 시:
  - login_attempts += 1
  - login_attempts >= 5 → locked_until = now() + 5분
  - 403 Forbidden 반환 (계정 잠금 시)
  - 401 Unauthorized 반환 (비밀번호 불일치 시)

**Exceptions**:
- 계정 잠금 중: 403 Forbidden, "Account locked. Try again after {time}"
- 매장 또는 관리자 존재하지 않음: 401 Unauthorized

---

### AR-3: JWT 토큰 검증 규칙
**Rule**: 모든 보호된 API는 유효한 JWT 토큰 필요

**Conditions**:
- Authorization 헤더에 "Bearer {token}" 형식으로 토큰 제공
- 토큰이 만료되지 않음 (exp > now())
- 토큰 서명이 유효함

**Actions**:
- 성공 시: 요청 처리
- 실패 시: 401 Unauthorized 반환

**Exceptions**:
- 토큰 없음: 401 Unauthorized, "Token required"
- 토큰 만료: 401 Unauthorized, "Token expired"
- 토큰 무효: 401 Unauthorized, "Invalid token"

---

## Session Management Rules

### SM-1: 세션 생성 규칙
**Rule**: 테이블 로그인 시 활성 세션이 없으면 자동 생성

**Conditions**:
- 테이블에 활성 세션이 없음 (current_session_id = NULL 또는 is_active = FALSE)

**Actions**:
- 새 TableSession 생성:
  - session_id = UUID
  - table_id = 로그인한 테이블
  - start_time = now()
  - is_active = TRUE
  - total_amount = 0
- Table.current_session_id = 새 session_id

**Exceptions**:
- 활성 세션이 이미 존재: 기존 세션 재사용

---

### SM-2: 세션 종료 규칙
**Rule**: 관리자가 "이용 완료" 처리 시 세션 종료 및 주문 아카이빙

**Conditions**:
- 테이블에 활성 세션이 존재함
- 관리자 권한 필요

**Actions**:
1. 세션의 모든 주문을 OrderHistory로 아카이빙 (현재 상태 그대로)
2. TableSession 종료:
   - end_time = now()
   - is_active = FALSE
3. Table.current_session_id = NULL

**Exceptions**:
- 활성 세션 없음: 400 Bad Request, "No active session"

---

### SM-3: 세션 만료 규칙
**Rule**: JWT 토큰 만료 시 세션도 만료 (16시간)

**Conditions**:
- JWT 토큰 만료 (exp <= now())

**Actions**:
- 401 Unauthorized 반환
- 클라이언트는 재로그인 필요

**Exceptions**:
- 없음 (자동 처리)

---

## Order Management Rules

### OM-1: 주문 생성 규칙
**Rule**: 고객이 장바구니를 주문으로 전환

**Conditions**:
- 세션이 활성 상태여야 함 (is_active = TRUE)
- 모든 메뉴가 주문 가능해야 함 (is_available = TRUE)
- 수량이 1 이상이어야 함

**Actions**:
1. 기존 미완료 주문 확인 (같은 세션, status = pending 또는 preparing)
   - 있음: 기존 Order에 OrderItem 추가
   - 없음: 새 Order 생성
2. 주문 번호 생성 (매장별 일일 순차)
3. OrderItem 생성 (menu snapshot 저장)
4. 금액 계산:
   - subtotal_amount = sum(unit_price × quantity)
   - tip_amount = round(subtotal_amount × tip_rate / 100)
   - total_amount = subtotal_amount + tip_amount
5. Order 저장
6. TableSession.total_amount 업데이트 (누적)
7. WebSocket 브로드캐스트 (new_order 이벤트)

**Exceptions**:
- 세션 비활성: 400 Bad Request, "Session not active"
- 메뉴 주문 불가: 400 Bad Request, "Menu not available: {menu_name}"
- 수량 0 이하: 400 Bad Request, "Quantity must be greater than 0"

---

### OM-2: 주문 번호 생성 규칙
**Rule**: 매장별 일일 순차 번호 생성 (형식: #{일련번호:03d})

**Conditions**:
- 매장 ID 필요
- 오늘 날짜 기준

**Actions**:
1. 오늘 생성된 주문 수 조회 (store_id + date(created_at) = today)
2. 다음 번호 = count + 1
3. 형식: f"#{next_number:03d}" (예: #001, #002, ..., #999)

**Exceptions**:
- 중복 번호 생성 시: UNIQUE constraint 위반 → 재시도 (최대 3회)

---

### OM-3: 팁 계산 규칙
**Rule**: 팁은 비율 기반으로 계산하며 반올림 적용

**Conditions**:
- tip_rate는 0, 5, 10, 15, 20 중 하나
- subtotal_amount >= 0

**Actions**:
- tip_amount = round(subtotal_amount × tip_rate / 100)
- total_amount = subtotal_amount + tip_amount

**Examples**:
- subtotal: 15,000원, tip_rate: 10% → tip: 1,500원, total: 16,500원
- subtotal: 15,000원, tip_rate: 15% → tip: 2,250원, total: 17,250원
- subtotal: 15,333원, tip_rate: 10% → tip: 1,533원 (반올림), total: 16,866원

**Exceptions**:
- 잘못된 tip_rate: 400 Bad Request, "Invalid tip_rate"

---

### OM-4: 주문 상태 전이 규칙
**Rule**: 주문 상태는 모든 방향으로 자유롭게 전이 가능

**Allowed Transitions**:
- pending → preparing
- pending → completed
- preparing → pending
- preparing → completed
- completed → preparing
- completed → pending

**Actions**:
- Order.status 업데이트
- Order.updated_at = now()
- WebSocket 브로드캐스트 (order_updated 이벤트)

**Exceptions**:
- 없음 (모든 전이 허용)

---

### OM-5: 주문 삭제 규칙
**Rule**: 관리자가 직권으로 주문 삭제 가능 (물리적 삭제)

**Conditions**:
- 관리자 권한 필요
- 주문이 존재해야 함

**Actions**:
1. OrderItem 삭제 (CASCADE)
2. Order 삭제
3. TableSession.total_amount 재계산 (해당 세션의 남은 주문 합계)
4. WebSocket 브로드캐스트 (order_deleted 이벤트)

**Exceptions**:
- 주문 없음: 404 Not Found

---

### OM-6: 재주문 처리 규칙
**Rule**: 같은 세션에서 재주문 시 기존 미완료 주문에 항목 추가

**Conditions**:
- 같은 세션에 pending 또는 preparing 상태 주문 존재

**Actions**:
- 기존 Order에 새 OrderItem 추가
- subtotal_amount, total_amount 재계산
- Order.updated_at = now()

**Exceptions**:
- 미완료 주문 없음: 새 Order 생성

---

## Menu Management Rules

### MM-1: 메뉴 생성 규칙
**Rule**: 관리자가 메뉴 등록 시 필수 필드 검증

**Conditions**:
- menu_name: 필수, 1~100자
- price: 필수, 0 이상
- category_id: 필수, 존재하는 카테고리
- allergens: 선택, 쉼표 구분 문자열
- image_file: 선택, 최대 10MB, JPEG/PNG/WebP

**Actions**:
1. 데이터 검증
2. 이미지 업로드 (있으면):
   - 파일 크기 검증 (최대 10MB)
   - 파일 형식 검증 (MIME type)
   - 저장 경로: /uploads/{store_id}/menus/{menu_id}.{ext}
3. Menu 생성 (is_available = TRUE)

**Exceptions**:
- 필수 필드 누락: 400 Bad Request
- 가격 음수: 400 Bad Request, "Price must be >= 0"
- 이미지 크기 초과: 400 Bad Request, "Image size exceeds 10MB"
- 이미지 형식 불일치: 400 Bad Request, "Invalid image format"

---

### MM-2: 메뉴 삭제 규칙
**Rule**: 메뉴 삭제는 Soft Delete (is_available = FALSE)

**Conditions**:
- 메뉴가 존재해야 함

**Actions**:
- Menu.is_available = FALSE
- Menu.updated_at = now()

**Rationale**:
- 기존 주문의 snapshot 데이터 보호
- 과거 주문 내역 무결성 유지

**Exceptions**:
- 메뉴 없음: 404 Not Found

---

### MM-3: 메뉴 이미지 업로드 규칙
**Rule**: 이미지는 최대 10MB, JPEG/PNG/WebP만 허용

**Conditions**:
- 파일 크기 <= 10MB
- MIME type: image/jpeg, image/png, image/webp

**Actions**:
1. 파일 검증
2. 파일명 생성: {menu_id}.{ext}
3. 저장 경로: /uploads/{store_id}/menus/{menu_id}.{ext}
4. 파일 저장
5. image_url 반환 (상대 경로)

**Exceptions**:
- 파일 크기 초과: 400 Bad Request
- 형식 불일치: 400 Bad Request
- 저장 실패: 500 Internal Server Error

---

## Category Management Rules

### CM-1: 카테고리 생성 규칙
**Rule**: 매장 생성 시 기본 카테고리("미분류") 자동 생성

**Conditions**:
- 새 매장 생성 시

**Actions**:
- Category 생성:
  - category_name = "미분류"
  - is_default = TRUE
  - display_order = 0

**Exceptions**:
- 없음 (자동 처리)

---

### CM-2: 카테고리 삭제 규칙
**Rule**: 카테고리 삭제 시 소속 메뉴를 "미분류"로 이동

**Conditions**:
- 카테고리가 기본 카테고리가 아니어야 함 (is_default = FALSE)

**Actions**:
1. "미분류" 카테고리 조회 (같은 store_id, is_default = TRUE)
2. 소속 메뉴의 category_id를 "미분류" category_id로 변경
3. Category 삭제

**Exceptions**:
- 기본 카테고리 삭제 시도: 400 Bad Request, "Cannot delete default category"
- 카테고리 없음: 404 Not Found

---

## Data Integrity Rules

### DI-1: Snapshot 데이터 규칙
**Rule**: 주문 시점의 메뉴 정보를 OrderItem에 snapshot으로 저장

**Conditions**:
- 주문 생성 시

**Actions**:
- OrderItem에 저장:
  - menu_name = Menu.menu_name (현재 값)
  - unit_price = Menu.price (현재 값)

**Rationale**:
- 메뉴 정보 변경 시에도 과거 주문 데이터 무결성 유지

**Exceptions**:
- 없음 (자동 처리)

---

### DI-2: 주문 아카이빙 규칙
**Rule**: 세션 종료 시 모든 주문을 OrderHistory로 아카이빙

**Conditions**:
- 세션 종료 시

**Actions**:
1. 세션의 모든 주문 조회
2. 각 주문을 JSON으로 직렬화 (Order + OrderItem)
3. OrderHistory 레코드 생성:
   - order_id = 원본 order_id
   - session_id = 원본 session_id
   - order_data = JSON 직렬화 데이터
   - archived_at = now()

**JSON Structure**:
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

**Exceptions**:
- 없음 (자동 처리)

---

### DI-3: 참조 무결성 규칙
**Rule**: FK 제약 조건 적용

**Constraints**:
- Store 삭제: RESTRICT (하위 데이터 존재 시 삭제 불가)
- Table 삭제: RESTRICT (활성 세션 존재 시 삭제 불가)
- Category 삭제: 소속 메뉴를 "미분류"로 이동 후 삭제
- Menu 삭제: Soft Delete (is_available = FALSE)
- Order 삭제: OrderItem CASCADE 삭제

**Exceptions**:
- FK 제약 위반: 400 Bad Request

---

## Validation Rules

### VR-1: 입력 데이터 검증 규칙
**Rule**: 모든 API 입력 데이터는 Pydantic 스키마로 검증

**Validations**:
- **String**: 최소/최대 길이, 패턴 매칭
- **Integer**: 최소/최대 값, 범위
- **Enum**: 허용된 값 목록
- **Email**: 이메일 형식
- **UUID**: UUID 형식

**Actions**:
- 검증 실패 시: 422 Unprocessable Entity 반환

**Examples**:
```python
class OrderCreateSchema(BaseModel):
    session_id: UUID
    items: List[OrderItemSchema]
    tip_rate: int = Field(ge=0, le=20)  # 0~20
    
    @validator('tip_rate')
    def validate_tip_rate(cls, v):
        if v not in [0, 5, 10, 15, 20]:
            raise ValueError('tip_rate must be 0, 5, 10, 15, or 20')
        return v
```

**Exceptions**:
- 검증 실패: 422 Unprocessable Entity

---

### VR-2: 비즈니스 로직 검증 규칙
**Rule**: 비즈니스 규칙 위반 시 명확한 에러 메시지 반환

**Validations**:
- 세션 활성 여부
- 메뉴 주문 가능 여부
- 계정 잠금 상태
- 권한 확인

**Actions**:
- 검증 실패 시: 400 Bad Request 또는 403 Forbidden 반환

**Exceptions**:
- 세션 비활성: 400 Bad Request, "Session not active"
- 메뉴 주문 불가: 400 Bad Request, "Menu not available"
- 계정 잠금: 403 Forbidden, "Account locked"
- 권한 없음: 403 Forbidden, "Insufficient permissions"

---

## Security Rules

### SR-1: 비밀번호 해싱 규칙
**Rule**: 모든 비밀번호는 bcrypt로 해싱

**Conditions**:
- 관리자 비밀번호
- 테이블 비밀번호

**Actions**:
- bcrypt.hashpw(password, bcrypt.gensalt(rounds=10))

**Exceptions**:
- 없음 (자동 처리)

---

### SR-2: JWT 토큰 규칙
**Rule**: JWT 토큰은 16시간 만료

**Payload**:
- **테이블 토큰**: { table_id, session_id, store_id, exp }
- **관리자 토큰**: { admin_id, store_id, role: 'admin', exp }

**Actions**:
- 토큰 발급 시 exp = now() + 16시간

**Exceptions**:
- 토큰 만료: 401 Unauthorized

---

### SR-3: 권한 검증 규칙
**Rule**: API별 권한 확인

**Permissions**:
- **Customer API**: 테이블 JWT 필요
- **Admin API**: 관리자 JWT 필요
- **WebSocket**: 관리자 JWT 필요

**Actions**:
- JWT payload의 role 확인
- 권한 없음 시: 403 Forbidden 반환

**Exceptions**:
- 권한 없음: 403 Forbidden, "Insufficient permissions"

---

## Performance Rules

### PR-1: 쿼리 최적화 규칙
**Rule**: N+1 쿼리 방지

**Actions**:
- Eager loading 사용 (Order + OrderItem)
- Join 최적화
- Index 활용

**Examples**:
```python
# Bad: N+1 query
orders = Order.query.all()
for order in orders:
    items = order.items  # N queries

# Good: Eager loading
orders = Order.query.options(
    joinedload(Order.items)
).all()
```

**Exceptions**:
- 없음 (개발 시 적용)

---

### PR-2: 캐싱 규칙
**Rule**: 자주 조회되는 데이터는 캐싱

**Cache Targets**:
- 메뉴 목록 (TTL: 5분)
- 카테고리 목록 (TTL: 10분)

**Actions**:
- Redis 캐싱
- Cache invalidation: 데이터 수정 시

**Exceptions**:
- 캐시 미스: DB 조회 후 캐싱

---

## Error Handling Rules

### EH-1: 에러 응답 형식 규칙
**Rule**: 모든 에러는 일관된 형식으로 반환

**Format**:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "error detail"
    }
  }
}
```

**Examples**:
- 400 Bad Request:
  ```json
  {
    "error": {
      "code": "INVALID_INPUT",
      "message": "Menu not available",
      "details": {
        "menu_id": "uuid",
        "menu_name": "김치찌개"
      }
    }
  }
  ```
- 401 Unauthorized:
  ```json
  {
    "error": {
      "code": "UNAUTHORIZED",
      "message": "Token expired"
    }
  }
  ```

**Exceptions**:
- 없음 (모든 에러에 적용)

---

### EH-2: 트랜잭션 롤백 규칙
**Rule**: 에러 발생 시 트랜잭션 롤백

**Actions**:
- try-except 블록으로 에러 캐치
- db.session.rollback() 호출
- 에러 응답 반환

**Examples**:
```python
try:
    order = create_order(...)
    db.session.commit()
except Exception as e:
    db.session.rollback()
    raise
```

**Exceptions**:
- 없음 (자동 처리)

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-09  
**Status**: Draft
