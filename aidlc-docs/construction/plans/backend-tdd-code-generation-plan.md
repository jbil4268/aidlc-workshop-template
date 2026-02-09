# TDD Code Generation Plan for Backend API Server

## Unit Context
- **Workspace Root**: workspace root (from aidlc-state.md)
- **Project Type**: Greenfield (single unit)
- **Stories**: US-1.1, US-2.1, US-2.2, US-4.1, US-5.1, US-6.1, US-7.1, US-7.2, US-8.1, US-8.2, US-8.3, US-8.4, US-9.1, US-9.2, US-ERR-1, US-ERR-2
- **Code Location**: `backend/` (workspace root)
- **Test Location**: `backend/tests/`

## TDD Scope
핵심 비즈니스 로직만 TDD 적용:
1. AuthService (9 tests)
2. TableSessionService (7 tests)
3. OrderService (14 tests)

나머지 코드는 TDD 없이 직접 생성합니다.

---

## Plan Step 0: Project Structure Setup
- [x] 프로젝트 디렉토리 구조 생성
- [x] requirements.txt 생성
- [x] .env.example 생성
- [x] README.md 생성

---

## Plan Step 1: Database Models 생성 (TDD 없음)
- [x] SQLAlchemy 모델 생성 (Store, Table, TableSession, Category, Menu, Order, OrderItem, Admin, OrderHistory)
- [x] database.py 생성 (engine, SessionLocal)
- [x] Alembic 초기화 및 마이그레이션 스크립트 생성

---

## Plan Step 2: Pydantic Schemas 생성 (TDD 없음)
- [x] auth.py 스키마 생성
- [x] menu.py 스키마 생성
- [x] order.py 스키마 생성
- [x] table.py 스키마 생성

---

## Plan Step 3: Error Classes 생성 (TDD 없음)
- [x] 커스텀 에러 클래스 정의 (TokenExpiredError, InvalidTokenError, ActiveSessionExistsError, SessionNotFoundError, SessionAlreadyEndedError, InvalidTipRateError, SessionNotActiveError, MenuNotAvailableError, InvalidQuantityError, OrderNotFoundError, InvalidStatusError)

---

## Plan Step 4: Contract Skeletons 생성
- [x] AuthService skeleton 생성 (모든 메서드 NotImplementedError)
- [x] TableSessionService skeleton 생성
- [x] OrderService skeleton 생성
- [x] 컴파일 확인

---

## Plan Step 5: AuthService TDD (9 tests)

### 5.1 hash_password() - RED-GREEN-REFACTOR
- [x] RED: TC-backend-001 작성 (비밀번호 해싱 성공)
- [x] GREEN: 최소 구현
- [x] RED: TC-backend-002 작성 (같은 비밀번호도 다른 해시)
- [x] GREEN: 구현 (이미 만족)
- [x] REFACTOR: 코드 개선
- [x] VERIFY: 모든 테스트 통과
- Story: US-6.1

### 5.2 verify_password() - RED-GREEN-REFACTOR
- [x] RED: TC-backend-003 작성 (올바른 비밀번호 검증)
- [x] GREEN: 최소 구현
- [x] RED: TC-backend-004 작성 (잘못된 비밀번호 검증)
- [x] GREEN: 구현 (이미 만족)
- [x] REFACTOR: 코드 개선
- [x] VERIFY: 모든 테스트 통과
- Story: US-6.1

### 5.3 create_jwt_token() - RED-GREEN-REFACTOR
- [x] RED: TC-backend-005 작성 (JWT 토큰 생성)
- [x] GREEN: 최소 구현
- [x] RED: TC-backend-006 작성 (만료 시간 설정)
- [x] GREEN: 구현 확장
- [x] REFACTOR: 코드 개선
- [x] VERIFY: 모든 테스트 통과
- Story: US-6.1, US-1.1

### 5.4 verify_jwt_token() - RED-GREEN-REFACTOR
- [x] RED: TC-backend-007 작성 (유효한 토큰 검증)
- [x] GREEN: 최소 구현
- [x] RED: TC-backend-008 작성 (만료된 토큰)
- [x] GREEN: 예외 처리 추가
- [x] RED: TC-backend-009 작성 (무효한 토큰)
- [x] GREEN: 예외 처리 추가
- [x] REFACTOR: 코드 개선
- [x] VERIFY: 모든 테스트 통과
- Story: US-6.1, US-1.1

---

## Plan Step 6: TableSessionService TDD (7 tests)

### 6.1 create_session() - RED-GREEN-REFACTOR
- [x] RED: TC-backend-010 작성 (세션 생성 성공)
- [x] GREEN: 최소 구현
- [x] RED: TC-backend-011 작성 (이미 활성 세션 존재)
- [x] GREEN: 검증 로직 추가
- [x] REFACTOR: 코드 개선
- [x] VERIFY: 모든 테스트 통과
- Story: US-1.1

### 6.2 get_active_session() - RED-GREEN-REFACTOR
- [x] RED: TC-backend-012 작성 (활성 세션 조회)
- [x] GREEN: 최소 구현
- [x] RED: TC-backend-013 작성 (활성 세션 없음)
- [x] GREEN: 구현 (이미 만족)
- [x] REFACTOR: 코드 개선
- [x] VERIFY: 모든 테스트 통과
- Story: US-1.1

### 6.3 end_session() - RED-GREEN-REFACTOR
- [x] RED: TC-backend-014 작성 (세션 종료 성공)
- [x] GREEN: 최소 구현
- [x] RED: TC-backend-015 작성 (존재하지 않는 세션)
- [x] GREEN: 예외 처리 추가
- [x] RED: TC-backend-016 작성 (이미 종료된 세션)
- [x] GREEN: 예외 처리 추가
- [x] REFACTOR: 코드 개선
- [x] VERIFY: 모든 테스트 통과
- Story: US-8.3

---

## Plan Step 7: OrderService TDD (14 tests)

### 7.1 generate_order_number() - RED-GREEN-REFACTOR
- [x] RED: TC-backend-017 작성 (첫 주문 번호)
- [x] GREEN: 최소 구현
- [x] RED: TC-backend-018 작성 (순차 번호)
- [x] GREEN: 구현 확장
- [x] RED: TC-backend-019 작성 (다른 날짜 리셋)
- [x] GREEN: 날짜 필터링 추가
- [x] REFACTOR: 코드 개선
- [x] VERIFY: 모든 테스트 통과
- Story: US-4.1

### 7.2 calculate_tip() - RED-GREEN-REFACTOR
- [x] RED: TC-backend-020 작성 (팁 0%)
- [x] GREEN: 최소 구현
- [x] RED: TC-backend-021 작성 (팁 10%)
- [x] GREEN: 구현 확장
- [x] RED: TC-backend-022 작성 (팁 15% 반올림)
- [x] GREEN: 반올림 로직 추가
- [x] RED: TC-backend-023 작성 (잘못된 팁 비율)
- [x] GREEN: 검증 로직 추가
- [x] REFACTOR: 코드 개선
- [x] VERIFY: 모든 테스트 통과
- Story: US-4.1

### 7.3 create_order() - RED-GREEN-REFACTOR
- [x] RED: TC-backend-024 작성 (주문 생성 성공)
- [x] GREEN: 최소 구현
- [x] RED: TC-backend-025 작성 (비활성 세션)
- [x] GREEN: 세션 검증 추가
- [x] RED: TC-backend-026 작성 (주문 불가능한 메뉴)
- [x] GREEN: 메뉴 검증 추가
- [x] RED: TC-backend-027 작성 (수량 0 이하)
- [x] GREEN: 수량 검증 추가
- [x] REFACTOR: 코드 개선
- [x] VERIFY: 모든 테스트 통과
- Story: US-4.1

### 7.4 update_order_status() - RED-GREEN-REFACTOR
- [x] RED: TC-backend-028 작성 (상태 변경 성공)
- [x] GREEN: 최소 구현
- [x] RED: TC-backend-029 작성 (존재하지 않는 주문)
- [x] GREEN: 주문 검증 추가
- [x] RED: TC-backend-030 작성 (잘못된 상태 값)
- [x] GREEN: 상태 검증 추가
- [x] REFACTOR: 코드 개선
- [x] VERIFY: 모든 테스트 통과
- Story: US-7.2

---

## Plan Step 8: API Routers 생성 (TDD 없음)
- [x] customer_auth.py 라우터 생성
- [x] customer_menu.py 라우터 생성
- [x] customer_order.py 라우터 생성
- [x] admin_auth.py 라우터 생성
- [x] admin_order.py 라우터 생성
- [x] admin_table.py 라우터 생성
- [x] admin_menu.py 라우터 생성
- [x] admin_category.py 라우터 생성

---

## Plan Step 9: Dependency Injection 함수 생성 (TDD 없음)
- [x] get_db() 함수 생성
- [x] verify_token() 함수 생성
- [x] get_current_table() 함수 생성
- [x] get_current_admin() 함수 생성

---

## Plan Step 10: WebSocket Manager 생성 (TDD 없음)
- [x] ConnectionManager 클래스 생성
- [x] WebSocket 엔드포인트 생성

---

## Plan Step 11: FastAPI App 설정 (TDD 없음)
- [x] main.py 생성 (FastAPI 앱)
- [x] CORS 미들웨어 추가
- [x] Global Exception Handler 추가
- [x] 라우터 등록
- [x] Static files 설정 (uploads/)

---

## Plan Step 12: Configuration 생성 (TDD 없음)
- [x] config.py 생성 (pydantic-settings)
- [x] 환경 변수 로딩

---

## Plan Step 13: Documentation 생성
- [x] API 문서 요약 (aidlc-docs/construction/backend/code/api-summary.md)
- [x] 코드 구조 요약 (aidlc-docs/construction/backend/code/code-structure.md)
- [x] README.md 업데이트

---

## Story Traceability

| Story | Plan Steps | Status |
|-------|-----------|--------|
| US-1.1 | 5.3, 5.4, 6.1, 6.2 | ⬜ Pending |
| US-4.1 | 7.1, 7.2, 7.3 | ⬜ Pending |
| US-6.1 | 5.1, 5.2, 5.3, 5.4 | ⬜ Pending |
| US-7.2 | 7.4 | ⬜ Pending |
| US-8.3 | 6.3 | ⬜ Pending |

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-09  
**Status**: Draft
