# NFR Design Plan - Unit 1: Backend API Server

## Plan Overview
Backend API Server의 NFR Requirements를 구현하기 위한 디자인 패턴과 논리적 컴포넌트를 설계합니다.

## Execution Steps

- [x] Step 1: NFR Requirements 분석
- [x] Step 2: 질문 수집 및 사용자 답변 대기
- [x] Step 3: NFR Design Patterns 문서 생성
- [x] Step 4: Logical Components 문서 생성
- [x] Step 5: 사용자 승인 대기

---

## Step 2: NFR Design Questions

아래 질문들에 답변해 주세요. 각 질문의 `[Answer]:` 뒤에 선택지 또는 자유 입력으로 답변해 주시면 됩니다.

**Note**: 로컬 개발 환경이므로 복잡한 인프라 패턴은 불필요합니다. 핵심적인 설계 결정만 확인합니다.

---

### Q1. 에러 핸들링 패턴
API 에러 처리를 위한 패턴을 선택해 주세요.

A) Global Exception Handler (FastAPI exception_handler 사용)
B) Try-Catch per Endpoint (각 엔드포인트에서 개별 처리)
C) 혼합 (Global + 특정 엔드포인트 추가 처리)
D) 기타 (직접 입력)

[Answer]:A

---

### Q2. 인증 미들웨어 구현 방식
JWT 토큰 검증을 위한 미들웨어 구현 방식을 선택해 주세요.

A) FastAPI Depends (함수 의존성 주입)
B) Middleware Class (모든 요청 인터셉트)
C) Decorator (라우터별 적용)
D) 기타 (직접 입력)

[Answer]:A

---

### Q3. 데이터베이스 세션 관리 패턴
SQLAlchemy 세션 관리 방식을 선택해 주세요.

A) Dependency Injection (FastAPI Depends로 세션 주입)
B) Context Manager (with 문 사용)
C) Global Session (앱 전역 세션)
D) 기타 (직접 입력)

[Answer]:A

---

### Q4. WebSocket 연결 관리 패턴
WebSocket 연결 관리를 위한 패턴을 선택해 주세요.

A) Connection Manager (매장별 연결 그룹 관리)
B) Simple List (단순 연결 리스트)
C) Redis Pub/Sub (확장성 고려, 현재는 과도함)
D) 기타 (직접 입력)

[Answer]:A

---

### Q5. 비즈니스 로직 레이어 분리
비즈니스 로직을 어떻게 구조화할지 선택해 주세요.

A) Service Layer (routers → services → models)
B) Fat Models (모델에 비즈니스 로직 포함)
C) Thin Controllers (라우터에 직접 로직 작성)
D) 기타 (직접 입력)

[Answer]:C

---

### Q6. 파일 업로드 처리 패턴
이미지 업로드 처리 방식을 선택해 주세요.

A) 동기 처리 (업로드 완료 후 응답)
B) 비동기 처리 (aiofiles 사용)
C) 백그라운드 태스크 (FastAPI BackgroundTasks)
D) 기타 (직접 입력)

[Answer]:A

---

### Q7. 트랜잭션 관리 패턴
데이터베이스 트랜잭션 관리 방식을 선택해 주세요.

A) Explicit Commit (명시적 commit/rollback)
B) Context Manager (자동 commit/rollback)
C) Decorator (트랜잭션 데코레이터)
D) 기타 (직접 입력)

[Answer]:A

---

### Q8. 로깅 구조화
로그 출력 구조를 선택해 주세요.

A) Structured Logging (JSON 형식)
B) Plain Text (일반 텍스트)
C) 혼합 (개발: Plain, 프로덕션: JSON)
D) 기타 (직접 입력)

[Answer]:B

---

**Note**: 모든 질문에 답변 후 "완료"라고 입력해 주세요.
