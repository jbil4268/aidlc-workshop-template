# NFR Requirements - Backend API Server

## Overview
Backend API Server의 Non-Functional Requirements를 정의합니다. 이 문서는 Requirements 문서의 NFR을 기반으로 Backend 구현에 필요한 세부 사항을 추가합니다.

---

## Performance Requirements

### PR-1: API 응답 시간
**Priority**: High

**Requirements**:
| API | Target Response Time | Rationale |
|-----|---------------------|-----------|
| 주문 생성 | 2초 이내 | 고객 경험 중요, 즉각적인 피드백 필요 |
| 메뉴 목록 조회 | 5초 이내 | 초기 로딩, 캐싱 가능 |
| 주문 상태 변경 | 5초 이내 | 관리자 작업, 실시간성 중요도 중간 |
| 테이블 세션 종료 | 5초 이내 | 백그라운드 작업 포함, 복잡도 높음 |
| WebSocket 메시지 전달 | 2초 이내 | 실시간 모니터링 핵심 |

**Measurement**:
- 응답 시간 = 요청 수신 ~ 응답 전송 완료
- 95 percentile 기준

**Actions on Violation**:
- 로그 기록
- 성능 병목 지점 분석
- 쿼리 최적화 또는 캐싱 적용

---

### PR-2: 동시 요청 처리 능력
**Priority**: Medium

**Requirements**:
- 동시 접속 테이블: 최대 10개
- 테이블당 평균 요청: 1-2 req/s
- 총 처리 능력: 10-20 req/s
- 피크 시간 버퍼: 2배 (20-40 req/s)

**Rationale**:
- 소규모 매장 대상
- 로컬 개발 환경
- 과도한 최적화 불필요

**Testing**:
- 부하 테스트 도구: Locust 또는 Apache Bench
- 시나리오: 10개 테이블에서 동시 주문 생성

---

### PR-3: 데이터베이스 쿼리 성능
**Priority**: Medium

**Requirements**:
- 단일 쿼리: 100ms 이내
- Join 쿼리: 500ms 이내
- N+1 쿼리 방지 (Eager loading 사용)

**Optimization Strategies**:
- Index 활용 (domain-entities.md 참조)
- SQLAlchemy relationship lazy loading 설정
- 필요 시 쿼리 결과 캐싱

---

### PR-4: 이미지 로딩 성능
**Priority**: Low

**Requirements**:
- 이미지 크기: 최대 10MB
- Lazy loading 적용 (Frontend)
- 이미지 최적화: 권장하지만 필수 아님

**Future Enhancement**:
- 이미지 리사이징 (Pillow 라이브러리)
- WebP 변환
- CDN 전환

---

## Scalability Requirements

### SC-1: 수평 확장성 (Horizontal Scaling)
**Priority**: Low (현재 단계에서는 불필요)

**Current State**:
- 단일 서버 인스턴스
- SQLite (단일 파일 DB)
- 로컬 개발 환경

**Future Considerations**:
- 다중 매장 지원 시 매장별 데이터 분리
- PostgreSQL/MySQL 전환 고려
- Load Balancer + 다중 인스턴스

---

### SC-2: 데이터 증가 대응
**Priority**: Medium

**Requirements**:
- 주문 데이터 1년 후 아카이빙
- OrderHistory 테이블 정기 정리
- 이미지 파일 정리 (미사용 이미지 삭제)

**Implementation**:
- Cron job 또는 스케줄러 (APScheduler)
- 아카이빙 스크립트

---

## Availability Requirements

### AV-1: 서비스 가용성
**Priority**: Medium

**Requirements**:
- 목표 가용성: 95% (로컬 개발 환경)
- 계획된 다운타임: 허용 (유지보수 시)
- 무중단 배포: 불필요 (로컬 환경)

**Rationale**:
- 프로덕션 환경 아님
- 소규모 매장, 영업 시간 외 재시작 가능

---

### AV-2: 에러 복구
**Priority**: High

**Requirements**:
- 에러 발생 시 자동 재시작 (프로세스 매니저 사용 권장)
- 트랜잭션 롤백으로 데이터 무결성 보장
- 에러 로그 기록 (INFO + ERROR 레벨)

**Error Handling**:
- try-except 블록으로 에러 캐치
- 명확한 에러 메시지 반환
- 500 에러 시 스택 트레이스 로그

---

### AV-3: 데이터 백업
**Priority**: Medium

**Requirements**:
- SQLite 파일 정기 백업 권장
- 백업 주기: 일일 (수동 또는 스크립트)
- 백업 보관: 최소 7일

**Implementation**:
- 파일 복사 스크립트
- 백업 디렉토리: /backups/{date}.db

---

## Security Requirements

### SE-1: 인증 및 권한
**Priority**: High

**Requirements**:
- JWT 토큰 기반 인증
- 토큰 만료: 16시간
- bcrypt 비밀번호 해싱 (salt rounds: 10)
- 로그인 시도 제한: 5회 실패 시 5분 잠금

**Implementation**:
- FastAPI Depends를 사용한 인증 미들웨어
- JWT 라이브러리: PyJWT 또는 python-jose
- bcrypt 라이브러리: passlib

---

### SE-2: 데이터 보호
**Priority**: High

**Requirements**:
- 비밀번호 평문 저장 금지 (bcrypt 해싱)
- SQL Injection 방지 (SQLAlchemy ORM 사용)
- XSS 방지 (입력 검증 및 sanitization)
- HTTPS 사용 권장 (프로덕션 환경)

**Validation**:
- Pydantic 스키마로 입력 검증
- 특수 문자 이스케이프
- 파일 업로드 검증 (크기, 형식)

---

### SE-3: CORS 정책
**Priority**: Medium

**Requirements**:
- 개발 환경: 모든 origin 허용 (*)
- 프로덕션 환경: 특정 origin만 허용 (권장)

**Implementation**:
- FastAPI CORSMiddleware
- 환경 변수로 origin 설정

---

### SE-4: Rate Limiting
**Priority**: Low (현재 단계에서는 불필요)

**Requirements**:
- 적용 안 함 (로컬 개발 환경, 신뢰된 사용자만)

**Future Considerations**:
- 프로덕션 환경 시 적용 고려
- slowapi 라이브러리 사용

---

## Reliability Requirements

### RE-1: 에러 처리
**Priority**: High

**Requirements**:
- 모든 API 엔드포인트에 try-except 블록
- 트랜잭션 롤백으로 데이터 무결성 보장
- 일관된 에러 응답 형식

**Error Response Format**:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {}
  }
}
```

---

### RE-2: 로깅
**Priority**: Medium

**Requirements**:
- 로그 레벨: INFO + ERROR
- 로그 출력: Console (stdout)
- 로그 형식: 타임스탬프 + 레벨 + 메시지

**Logged Events**:
- INFO: 주문 생성, 상태 변경, 세션 시작/종료, 로그인
- ERROR: 예외 발생, 데이터베이스 에러, 검증 실패

**Implementation**:
- Python logging 모듈
- FastAPI 로깅 설정

---

### RE-3: 데이터 무결성
**Priority**: High

**Requirements**:
- 트랜잭션 사용 (주문 생성, 세션 종료)
- FK 제약 조건 적용
- Snapshot 패턴 (OrderItem, OrderHistory)

**Implementation**:
- SQLAlchemy session.commit() / session.rollback()
- Database constraints (UNIQUE, FK, CHECK)

---

### RE-4: WebSocket 재연결
**Priority**: Medium

**Requirements**:
- 연결 끊김 시 자동 재연결 (Frontend)
- 재연결 시 누락된 이벤트 복구 (선택)

**Implementation**:
- Frontend: WebSocket 재연결 로직
- Backend: 연결 상태 관리

---

## Maintainability Requirements

### MA-1: 코드 품질
**Priority**: Medium

**Requirements**:
- 타입 힌트 사용 (Python 3.9+)
- Pydantic 모델로 데이터 검증
- 함수/클래스 docstring 작성
- 모듈화 및 컴포넌트 분리

**Code Style**:
- PEP 8 준수
- Black 포매터 사용 권장
- Linter: flake8 또는 pylint

---

### MA-2: API 문서화
**Priority**: High

**Requirements**:
- Swagger/OpenAPI 자동 생성 (FastAPI 기본 제공)
- API 엔드포인트 설명 작성
- 요청/응답 스키마 명시

**Access**:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

### MA-3: 테스트
**Priority**: High

**Requirements**:
- 핵심 비즈니스 로직 Unit Test
- 테스트 프레임워크: pytest
- 테스트 커버리지: 주문 생성, 세션 관리, 인증 로직

**Test Structure**:
```
backend/tests/
  test_auth.py
  test_order.py
  test_table.py
  test_menu.py
```

---

### MA-4: 환경 변수 관리
**Priority**: High

**Requirements**:
- .env 파일 + pydantic-settings
- 환경 변수 예시: .env.example 제공
- 민감 정보 코드에 포함 금지

**Environment Variables**:
```
DATABASE_URL=sqlite:///./table_order.db
SECRET_KEY=your-secret-key-here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
STORE_IDENTIFIER=store001
```

---

## Usability Requirements

### US-1: API 응답 일관성
**Priority**: High

**Requirements**:
- 일관된 JSON 응답 형식
- 성공: { "data": {...} }
- 에러: { "error": {...} }
- HTTP 상태 코드 적절히 사용

**Status Codes**:
- 200: 성공
- 201: 생성 성공
- 400: 잘못된 요청
- 401: 인증 실패
- 403: 권한 없음
- 404: 리소스 없음
- 422: 검증 실패
- 500: 서버 에러

---

### US-2: 명확한 에러 메시지
**Priority**: High

**Requirements**:
- 사용자 친화적인 에러 메시지
- 에러 원인 명시
- 해결 방법 제시 (가능한 경우)

**Examples**:
- "Menu not available: 김치찌개"
- "Session not active. Please login again."
- "Account locked. Try again after 5 minutes."

---

## Monitoring & Observability

### MO-1: 로그 모니터링
**Priority**: Low (현재 단계)

**Requirements**:
- Console 로그 출력
- 에러 발생 시 스택 트레이스 기록

**Future Enhancements**:
- 로그 파일 저장
- 로그 집계 도구 (ELK Stack, Grafana)

---

### MO-2: 성능 모니터링
**Priority**: Low (현재 단계)

**Requirements**:
- 불필요 (로컬 개발 환경)

**Future Enhancements**:
- APM 도구 (New Relic, Datadog)
- 응답 시간 메트릭 수집

---

## Compliance & Standards

### CO-1: 데이터 보존
**Priority**: Medium

**Requirements**:
- 주문 데이터 1년 보존
- 1년 후 아카이빙 또는 삭제
- 개인정보 없음 (테이블 번호만 사용)

---

### CO-2: 접근성
**Priority**: Low (Backend API)

**Requirements**:
- API는 접근성 요구사항 없음
- Frontend에서 처리

---

## Technology Constraints

### TC-1: 개발 환경
**Priority**: High

**Requirements**:
- 로컬 개발 환경만 지원
- 단일 서버 인스턴스
- SQLite 데이터베이스

**Limitations**:
- 클라우드 배포 고려 안 함
- 분산 시스템 아님
- 고가용성 불필요

---

### TC-2: 리소스 제약
**Priority**: Medium

**Requirements**:
- 메모리: 512MB 이하 (권장)
- CPU: 단일 코어로 충분
- 디스크: 1GB 이하 (이미지 포함)

**Rationale**:
- 소규모 매장
- 제한된 데이터 볼륨
- 로컬 환경

---

## Summary

### Critical NFRs (Must Have)
1. API 응답 시간 (주문 생성 2초, 기타 5초)
2. JWT 인증 및 bcrypt 해싱
3. 에러 처리 및 트랜잭션 무결성
4. API 문서화 (Swagger)
5. 핵심 비즈니스 로직 Unit Test

### Important NFRs (Should Have)
1. 동시 요청 처리 (10-20 req/s)
2. 로깅 (INFO + ERROR)
3. 데이터 백업 권장
4. 코드 품질 (타입 힌트, docstring)

### Nice to Have NFRs (Could Have)
1. 성능 모니터링
2. 이미지 최적화
3. Rate Limiting

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-09  
**Status**: Draft
