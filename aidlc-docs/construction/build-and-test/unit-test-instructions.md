# Unit Test Instructions

## Unit 1: Backend API Server

### Test Framework
- **pytest**: Python testing framework
- **Coverage**: pytest-cov for code coverage

### Test Structure
```
backend/tests/
├── conftest.py                    # Pytest fixtures
├── test_auth_service.py           # AuthService tests (9 tests)
├── test_table_session_service.py  # TableSessionService tests (7 tests)
└── test_order_service.py          # OrderService tests (14 tests)
```

### Running Tests

#### Run All Tests
```bash
cd backend
pytest
```

#### Run Specific Test File
```bash
pytest tests/test_auth_service.py
```

#### Run Specific Test
```bash
pytest tests/test_auth_service.py::TestAuthService::test_hash_password_success
```

#### Run with Verbose Output
```bash
pytest -v
```

#### Run with Coverage
```bash
pytest --cov=app --cov-report=html
```

**Coverage Report**: `htmlcov/index.html`

### Test Categories

#### AuthService Tests (9 tests)
- `test_hash_password_success` - 비밀번호 해싱
- `test_hash_password_different_hashes` - Salt 검증
- `test_verify_password_correct` - 비밀번호 검증 성공
- `test_verify_password_incorrect` - 비밀번호 검증 실패
- `test_create_jwt_token_success` - JWT 생성
- `test_create_jwt_token_with_expiration` - 만료 시간 설정
- `test_verify_jwt_token_valid` - 유효한 토큰 검증
- `test_verify_jwt_token_expired` - 만료된 토큰
- `test_verify_jwt_token_invalid` - 무효한 토큰

#### TableSessionService Tests (7 tests)
- `test_create_session_success` - 세션 생성
- `test_create_session_active_exists` - 중복 세션 방지
- `test_get_active_session_exists` - 활성 세션 조회
- `test_get_active_session_none` - 세션 없음
- `test_end_session_success` - 세션 종료
- `test_end_session_not_found` - 존재하지 않는 세션
- `test_end_session_already_ended` - 이미 종료된 세션

#### OrderService Tests (14 tests)
- `test_generate_order_number_first` - 첫 주문 번호
- `test_generate_order_number_sequential` - 순차 번호
- `test_generate_order_number_different_date` - 날짜별 리셋
- `test_calculate_tip_zero` - 팁 0%
- `test_calculate_tip_ten_percent` - 팁 10%
- `test_calculate_tip_rounding` - 팁 반올림
- `test_calculate_tip_invalid_rate` - 잘못된 팁 비율
- `test_create_order_success` - 주문 생성
- `test_create_order_inactive_session` - 비활성 세션
- `test_create_order_unavailable_menu` - 품절 메뉴
- `test_create_order_invalid_quantity` - 잘못된 수량
- `test_update_order_status_success` - 상태 변경
- `test_update_order_status_not_found` - 존재하지 않는 주문
- `test_update_order_status_invalid` - 잘못된 상태

### Expected Results

**Total Tests**: 30  
**Expected Pass**: 30  
**Expected Fail**: 0

### Test Coverage Goals

- **Services**: 90%+ coverage
- **Models**: Not tested (ORM)
- **Routers**: Not tested (integration tests)

---

## Unit 2: Customer Frontend

### Test Framework (Optional)
- **Vitest**: Vite-native test runner
- **Vue Test Utils**: Vue component testing

### Note
프론트엔드 단위 테스트는 요구사항에 포함되지 않음.
필요 시 다음 명령으로 테스트 추가 가능:

```bash
cd customer-frontend
npm install -D vitest @vue/test-utils
npm run test
```

---

## Unit 3: Admin Frontend

### Test Framework (Optional)
- **Vitest**: Vite-native test runner
- **Vue Test Utils**: Vue component testing

### Note
프론트엔드 단위 테스트는 요구사항에 포함되지 않음.

---

## Continuous Testing

### Watch Mode (Backend)
```bash
cd backend
pytest --watch
```

### Pre-commit Hook (Optional)
```bash
# .git/hooks/pre-commit
#!/bin/sh
cd backend
pytest
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
```

---

## Test Data Management

### Test Database
- In-memory SQLite for tests
- Fresh database for each test
- No cleanup needed

### Test Fixtures
```python
# conftest.py
@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)
```

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-09  
**Status**: Complete
