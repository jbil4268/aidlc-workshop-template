# NFR Requirements Plan - Unit 1: Backend API Server

## Plan Overview
Backend API Server의 Non-Functional Requirements와 Tech Stack 세부 결정을 수행합니다.

## Execution Steps

- [x] Step 1: Functional Design 분석
- [x] Step 2: 질문 수집 및 사용자 답변 대기
- [x] Step 3: NFR Requirements 문서 생성
- [x] Step 4: Tech Stack Decisions 문서 생성
- [-] Step 5: 사용자 승인 대기

---

## Step 2: NFR Clarification Questions

아래 질문들에 답변해 주세요. 각 질문의 `[Answer]:` 뒤에 선택지 또는 자유 입력으로 답변해 주시면 됩니다.

**Note**: Requirements 문서에 이미 일부 NFR이 정의되어 있지만, Backend 구현을 위한 추가 세부 사항이 필요합니다.

---

### Q1. Python Backend Framework 선택
Requirements에서 "Python (FastAPI or Django)"로 명시되었습니다. 최종 선택을 해주세요.

A) FastAPI - 비동기 지원, 빠른 성능, 자동 API 문서, WebSocket 내장
B) Django + Django REST Framework - 풍부한 생태계, Admin 패널, ORM 강력
C) 기타 (직접 입력)

**고려 사항**:
- FastAPI: 가볍고 빠름, WebSocket 네이티브 지원, 비동기 처리 우수
- Django: 배터리 포함, Admin 패널 유용, 학습 자료 풍부

[Answer]: A

---

### Q2. Database Connection Pool 설정
SQLite는 단일 파일 DB이지만, 동시 접속 처리를 위한 설정이 필요합니다.

A) 기본 설정 사용 (connection pool 없음)
B) SQLAlchemy connection pool 사용 (pool_size=5, max_overflow=10)
C) 기타 (직접 입력)

[Answer]:A

---

### Q3. WebSocket 구현 방식
실시간 주문 모니터링을 위한 WebSocket 구현 방식을 선택해 주세요.

A) FastAPI WebSocket (FastAPI 선택 시)
B) Django Channels (Django 선택 시)
C) Socket.IO (프레임워크 독립적)
D) 기타 (직접 입력)

[Answer]:A

---

### Q4. API 응답 시간 목표 (상세)
Requirements에 "주문 생성 2초 이내"가 명시되었습니다. 다른 API의 목표를 설정해 주세요.

**주문 생성 API**: 2초 (이미 정의됨)
**메뉴 목록 조회 API**: [Answer]:5초
**주문 상태 변경 API**: [Answer]:5초
**테이블 세션 종료 API**: [Answer]:5초

---

### Q5. 동시 요청 처리 능력
10개 테이블 동시 접속이 명시되었습니다. 각 테이블에서 동시 요청 수를 추정해 주세요.

A) 테이블당 평균 1-2개 요청/초 (총 10-20 req/s)
B) 테이블당 평균 5-10개 요청/초 (총 50-100 req/s)
C) 기타 (직접 입력)

[Answer]:A

---

### Q6. 에러 로깅 상세 수준
Requirements에 "기본 console.log"가 명시되었습니다. 로깅 상세 수준을 선택해 주세요.

A) ERROR만 (에러 발생 시에만 로그)
B) INFO + ERROR (주요 이벤트 + 에러)
C) DEBUG + INFO + ERROR (개발 시 상세 로그)
D) 기타 (직접 입력)

[Answer]:B

---

### Q7. API 문서화 도구
API 문서 자동 생성 도구를 선택해 주세요.

A) Swagger/OpenAPI (FastAPI 자동 생성)
B) Redoc (FastAPI 자동 생성, 더 깔끔한 UI)
C) 둘 다 제공 (FastAPI 기본 제공)
D) 수동 문서 작성 (Markdown)
E) 기타 (직접 입력)

[Answer]:A

---

### Q8. CORS 설정
Frontend와 Backend가 다른 포트에서 실행됩니다. CORS 정책을 선택해 주세요.

A) 개발 환경: 모든 origin 허용 (*)
B) 개발 환경: 특정 origin만 허용 (localhost:3000, localhost:3001)
C) 기타 (직접 입력)

[Answer]:A

---

### Q9. 데이터베이스 마이그레이션 도구
스키마 변경 관리를 위한 마이그레이션 도구를 선택해 주세요.

A) Alembic (SQLAlchemy 기반, FastAPI 권장)
B) Django Migrations (Django 내장)
C) 수동 관리 (SQL 스크립트)
D) 기타 (직접 입력)

[Answer]:A

---

### Q10. 환경 변수 관리
환경 변수 관리 방식을 선택해 주세요.

A) .env 파일 + python-dotenv
B) .env 파일 + pydantic-settings (FastAPI 권장)
C) 시스템 환경 변수만 사용
D) 기타 (직접 입력)

[Answer]:B

---

### Q11. 비동기 처리 필요 여부
WebSocket 외에 비동기 처리가 필요한 작업이 있나요?

A) 필요 없음 (동기 처리로 충분)
B) 이미지 업로드 시 비동기 처리
C) 주문 생성 시 비동기 처리 (WebSocket 브로드캐스트)
D) 모든 DB 쿼리 비동기 처리
E) 기타 (직접 입력)

[Answer]:A

---

### Q12. Rate Limiting (요청 제한)
API 남용 방지를 위한 Rate Limiting 적용 여부를 선택해 주세요.

A) 적용 안 함 (로컬 개발 환경, 신뢰된 사용자만)
B) 적용 (IP당 100 req/min)
C) 적용 (사용자당 50 req/min)
D) 기타 (직접 입력)

[Answer]:A

---

### Q13. 데이터 검증 라이브러리
입력 데이터 검증을 위한 라이브러리를 선택해 주세요.

A) Pydantic (FastAPI 기본, 타입 힌트 기반)
B) Django Forms/Serializers (Django 기본)
C) Marshmallow (독립적인 검증 라이브러리)
D) 기타 (직접 입력)

[Answer]:A

---

### Q14. 테스트 프레임워크
Unit Test를 위한 테스트 프레임워크를 선택해 주세요.

A) pytest (Python 표준, 강력한 기능)
B) unittest (Python 내장)
C) Django TestCase (Django 전용)
D) 기타 (직접 입력)

[Answer]:A

---

### Q15. 이미지 저장 경로 구조
메뉴 이미지 저장 경로 구조를 선택해 주세요.

A) /uploads/{store_id}/menus/{menu_id}.{ext}
B) /uploads/menus/{year}/{month}/{menu_id}.{ext}
C) /uploads/{menu_id}.{ext} (단순 구조)
D) 기타 (직접 입력)

[Answer]:C

---

**Note**: 모든 질문에 답변 후 "완료"라고 입력해 주세요.
