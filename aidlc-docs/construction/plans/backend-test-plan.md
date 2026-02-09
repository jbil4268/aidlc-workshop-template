# Test Plan for Backend API Server

## Unit Overview
- **Unit**: Backend API Server
- **Stories**: US-1.1, US-2.1, US-2.2, US-4.1, US-5.1, US-6.1, US-7.1, US-7.2, US-8.1, US-8.2, US-8.3, US-8.4, US-9.1, US-9.2, US-ERR-1, US-ERR-2
- **Requirements**: FR-1.1 ~ FR-2.4, NFR-1 ~ NFR-7
- **TDD Scope**: 핵심 비즈니스 로직만 (주문 생성, 세션 관리, 인증)

---

## 1. AuthService Tests

### 1.1 hash_password()

#### TC-backend-001: 비밀번호 해싱 성공
- **Given**: 평문 비밀번호 "password123"
- **When**: hash_password("password123") 호출
- **Then**: bcrypt 해시 문자열 반환, 원본과 다름
- **Story**: US-6.1 (관리자 로그인)
- **Status**: ⬜ Not Started

#### TC-backend-002: 같은 비밀번호도 다른 해시 생성
- **Given**: 평문 비밀번호 "password123"
- **When**: hash_password("password123")를 2번 호출
- **Then**: 두 해시 값이 서로 다름 (salt 때문)
- **Story**: US-6.1
- **Status**: ⬜ Not Started

### 1.2 verify_password()

#### TC-backend-003: 올바른 비밀번호 검증 성공
- **Given**: 평문 "password123", 해시 = hash_password("password123")
- **When**: verify_password("password123", 해시) 호출
- **Then**: True 반환
- **Story**: US-6.1
- **Status**: ⬜ Not Started

#### TC-backend-004: 잘못된 비밀번호 검증 실패
- **Given**: 평문 "wrong", 해시 = hash_password("password123")
- **When**: verify_password("wrong", 해시) 호출
- **Then**: False 반환
- **Story**: US-6.1
- **Status**: ⬜ Not Started

### 1.3 create_jwt_token()

#### TC-backend-005: JWT 토큰 생성 성공
- **Given**: payload = {"user_id": "123", "role": "admin"}
- **When**: create_jwt_token(payload) 호출
- **Then**: JWT 토큰 문자열 반환 (3개 부분으로 구성)
- **Story**: US-6.1, US-1.1
- **Status**: ⬜ Not Started

#### TC-backend-006: 만료 시간 설정
- **Given**: payload = {"user_id": "123"}, expires_hours = 1
- **When**: create_jwt_token(payload, expires_hours=1) 호출
- **Then**: 토큰의 exp claim이 1시간 후로 설정됨
- **Story**: US-6.1
- **Status**: ⬜ Not Started

### 1.4 verify_jwt_token()

#### TC-backend-007: 유효한 토큰 검증 성공
- **Given**: 유효한 JWT 토큰
- **When**: verify_jwt_token(token) 호출
- **Then**: 원본 payload 반환
- **Story**: US-6.1, US-1.1
- **Status**: ⬜ Not Started

#### TC-backend-008: 만료된 토큰 검증 실패
- **Given**: 만료된 JWT 토큰
- **When**: verify_jwt_token(token) 호출
- **Then**: TokenExpiredError 발생
- **Story**: US-6.1
- **Status**: ⬜ Not Started

#### TC-backend-009: 무효한 토큰 검증 실패
- **Given**: 잘못된 형식의 토큰 "invalid.token.here"
- **When**: verify_jwt_token(token) 호출
- **Then**: InvalidTokenError 발생
- **Story**: US-6.1
- **Status**: ⬜ Not Started

---

## 2. TableSessionService Tests

### 2.1 create_session()

#### TC-backend-010: 세션 생성 성공
- **Given**: table_id = "table-001", 활성 세션 없음
- **When**: create_session("table-001") 호출
- **Then**: 새 TableSession 반환, is_active=True, start_time 설정됨
- **Story**: US-1.1 (테이블 로그인)
- **Status**: ⬜ Not Started

#### TC-backend-011: 이미 활성 세션 존재 시 에러
- **Given**: table_id = "table-001", 이미 활성 세션 존재
- **When**: create_session("table-001") 호출
- **Then**: ActiveSessionExistsError 발생
- **Story**: US-1.1
- **Status**: ⬜ Not Started

### 2.2 get_active_session()

#### TC-backend-012: 활성 세션 조회 성공
- **Given**: table_id = "table-001", 활성 세션 존재
- **When**: get_active_session("table-001") 호출
- **Then**: 활성 TableSession 반환
- **Story**: US-1.1
- **Status**: ⬜ Not Started

#### TC-backend-013: 활성 세션 없을 때 None 반환
- **Given**: table_id = "table-001", 활성 세션 없음
- **When**: get_active_session("table-001") 호출
- **Then**: None 반환
- **Story**: US-1.1
- **Status**: ⬜ Not Started

### 2.3 end_session()

#### TC-backend-014: 세션 종료 성공
- **Given**: session_id = "session-001", 활성 세션 존재
- **When**: end_session("session-001") 호출
- **Then**: True 반환, is_active=False, end_time 설정됨
- **Story**: US-8.3 (테이블 세션 종료)
- **Status**: ⬜ Not Started

#### TC-backend-015: 존재하지 않는 세션 종료 시 에러
- **Given**: session_id = "nonexistent"
- **When**: end_session("nonexistent") 호출
- **Then**: SessionNotFoundError 발생
- **Story**: US-8.3
- **Status**: ⬜ Not Started

#### TC-backend-016: 이미 종료된 세션 종료 시 에러
- **Given**: session_id = "session-001", 이미 종료된 세션
- **When**: end_session("session-001") 호출
- **Then**: SessionAlreadyEndedError 발생
- **Story**: US-8.3
- **Status**: ⬜ Not Started

---

## 3. OrderService Tests

### 3.1 generate_order_number()

#### TC-backend-017: 첫 주문 번호 생성
- **Given**: store_id = "store-001", date = 2026-02-09, 오늘 주문 없음
- **When**: generate_order_number("store-001", date(2026, 2, 9)) 호출
- **Then**: "#001" 반환
- **Story**: US-4.1 (주문 생성)
- **Status**: ⬜ Not Started

#### TC-backend-018: 순차 주문 번호 생성
- **Given**: store_id = "store-001", date = 2026-02-09, 오늘 주문 2개 존재
- **When**: generate_order_number("store-001", date(2026, 2, 9)) 호출
- **Then**: "#003" 반환
- **Story**: US-4.1
- **Status**: ⬜ Not Started

#### TC-backend-019: 다른 날짜는 번호 리셋
- **Given**: store_id = "store-001", date = 2026-02-10, 어제 주문 10개 존재
- **When**: generate_order_number("store-001", date(2026, 2, 10)) 호출
- **Then**: "#001" 반환 (일일 리셋)
- **Story**: US-4.1
- **Status**: ⬜ Not Started

### 3.2 calculate_tip()

#### TC-backend-020: 팁 0% 계산
- **Given**: subtotal = 15000, tip_rate = 0
- **When**: calculate_tip(15000, 0) 호출
- **Then**: 0 반환
- **Story**: US-4.1
- **Status**: ⬜ Not Started

#### TC-backend-021: 팁 10% 계산 (정확히 나누어떨어짐)
- **Given**: subtotal = 15000, tip_rate = 10
- **When**: calculate_tip(15000, 10) 호출
- **Then**: 1500 반환
- **Story**: US-4.1
- **Status**: ⬜ Not Started

#### TC-backend-022: 팁 15% 계산 (반올림)
- **Given**: subtotal = 15333, tip_rate = 15
- **When**: calculate_tip(15333, 15) 호출
- **Then**: 2300 반환 (15333 * 0.15 = 2299.95 → 반올림)
- **Story**: US-4.1
- **Status**: ⬜ Not Started

#### TC-backend-023: 잘못된 팁 비율 에러
- **Given**: subtotal = 15000, tip_rate = 25 (허용되지 않음)
- **When**: calculate_tip(15000, 25) 호출
- **Then**: InvalidTipRateError 발생
- **Story**: US-4.1
- **Status**: ⬜ Not Started

### 3.3 create_order()

#### TC-backend-024: 주문 생성 성공
- **Given**: 
  - session_id = "session-001" (활성 세션)
  - items = [OrderItemData("menu-001", 2), OrderItemData("menu-002", 1)]
  - tip_rate = 10
  - 모든 메뉴 is_available=True
- **When**: create_order("session-001", items, 10) 호출
- **Then**: 
  - Order 반환
  - order_number 생성됨
  - subtotal_amount = 메뉴 가격 합계
  - tip_amount = round(subtotal * 0.1)
  - total_amount = subtotal + tip
  - status = "pending"
- **Story**: US-4.1
- **Status**: ⬜ Not Started

#### TC-backend-025: 비활성 세션으로 주문 시 에러
- **Given**: session_id = "session-001" (is_active=False)
- **When**: create_order("session-001", items, 10) 호출
- **Then**: SessionNotActiveError 발생
- **Story**: US-4.1
- **Status**: ⬜ Not Started

#### TC-backend-026: 주문 불가능한 메뉴 포함 시 에러
- **Given**: 
  - session_id = "session-001" (활성)
  - items = [OrderItemData("menu-001", 2)]
  - menu-001의 is_available=False
- **When**: create_order("session-001", items, 10) 호출
- **Then**: MenuNotAvailableError 발생
- **Story**: US-4.1
- **Status**: ⬜ Not Started

#### TC-backend-027: 수량 0 이하 시 에러
- **Given**: 
  - session_id = "session-001" (활성)
  - items = [OrderItemData("menu-001", 0)]
- **When**: create_order("session-001", items, 10) 호출
- **Then**: InvalidQuantityError 발생
- **Story**: US-4.1
- **Status**: ⬜ Not Started

### 3.4 update_order_status()

#### TC-backend-028: 주문 상태 변경 성공
- **Given**: order_id = "order-001", 현재 status = "pending"
- **When**: update_order_status("order-001", "preparing") 호출
- **Then**: Order 반환, status = "preparing", updated_at 갱신됨
- **Story**: US-7.2 (주문 상태 변경)
- **Status**: ⬜ Not Started

#### TC-backend-029: 존재하지 않는 주문 상태 변경 시 에러
- **Given**: order_id = "nonexistent"
- **When**: update_order_status("nonexistent", "preparing") 호출
- **Then**: OrderNotFoundError 발생
- **Story**: US-7.2
- **Status**: ⬜ Not Started

#### TC-backend-030: 잘못된 상태 값 시 에러
- **Given**: order_id = "order-001"
- **When**: update_order_status("order-001", "invalid_status") 호출
- **Then**: InvalidStatusError 발생
- **Story**: US-7.2
- **Status**: ⬜ Not Started

---

## Requirements Coverage

| Requirement ID | Test Cases | Status |
|---------------|------------|--------|
| FR-1.1 (테이블 로그인) | TC-backend-005, 007, 010-013 | ⬜ Pending |
| FR-2.1 (관리자 로그인) | TC-backend-001-009 | ⬜ Pending |
| FR-1.4 (주문 생성) | TC-backend-017-027 | ⬜ Pending |
| FR-2.2 (주문 상태 변경) | TC-backend-028-030 | ⬜ Pending |
| FR-2.3 (세션 종료) | TC-backend-014-016 | ⬜ Pending |
| NFR-2 (보안 - bcrypt) | TC-backend-001-004 | ⬜ Pending |
| NFR-2 (보안 - JWT) | TC-backend-005-009 | ⬜ Pending |

---

## Test Summary

- **총 테스트 케이스**: 30개
- **AuthService**: 9개
- **TableSessionService**: 7개
- **OrderService**: 14개

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-09  
**Status**: Draft
