# Requirements Verification Questions

요구사항을 명확히 하기 위한 질문입니다. 각 질문에 대해 [Answer]: 태그 뒤에 선택한 옵션의 문자를 입력해주세요.

---

## Question 1
Backend 기술 스택으로 어떤 것을 선호하시나요?

A) Node.js (Express/Fastify)
B) Python (FastAPI/Django)
C) Java (Spring Boot)
D) Go
E) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 2
Frontend 기술 스택으로 어떤 것을 선호하시나요?

A) React
B) Vue.js
C) Angular
D) Vanilla JavaScript (프레임워크 없음)
E) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 3
데이터베이스는 어떤 것을 사용하시겠습니까?

A) PostgreSQL
B) MySQL
C) MongoDB
D) SQLite (개발/테스트용)
E) Other (please describe after [Answer]: tag below)

[Answer]: D

---

## Question 4
실시간 주문 모니터링을 위한 Server-Sent Events (SSE) 구현 시, fallback 메커니즘이 필요한가요?

A) SSE만 사용 (모던 브라우저만 지원)
B) SSE + Polling fallback (구형 브라우저 지원)
C) WebSocket 사용
D) Polling만 사용
E) Other (please describe after [Answer]: tag below)

[Answer]: C

---

## Question 5
테이블 태블릿의 자동 로그인 정보는 어디에 저장하시겠습니까?

A) LocalStorage
B) SessionStorage
C) Cookie
D) IndexedDB
E) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 6
매장 관리자 인증에 사용할 JWT 토큰은 어디에 저장하시겠습니까?

A) LocalStorage
B) SessionStorage
C) HttpOnly Cookie
D) Memory only (새로고침 시 재로그인)
E) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 7
메뉴 이미지는 어떻게 관리하시겠습니까?

A) 외부 URL만 저장 (이미지는 외부 호스팅)
B) 서버에 업로드 및 저장
C) CDN 사용
D) Base64 인코딩하여 DB 저장
E) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 8
배포 환경은 어디인가요?

A) 로컬 개발 환경만
B) 클라우드 (AWS/Azure/GCP)
C) On-premise 서버
D) Docker 컨테이너
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 9
API 인증 방식은 무엇을 사용하시겠습니까?

A) JWT (JSON Web Token)
B) Session-based authentication
C) API Key
D) OAuth 2.0
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 10
에러 처리 및 로깅은 어느 수준까지 필요한가요?

A) 기본 console.log만
B) 구조화된 로깅 (Winston/Pino 등)
C) 중앙 집중식 로깅 시스템 (ELK/CloudWatch)
D) 에러 추적 서비스 (Sentry 등)
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 11
테스트 커버리지는 어느 수준을 목표로 하시나요?

A) 테스트 없음 (MVP 빠른 개발)
B) 핵심 비즈니스 로직만 Unit Test
C) Unit Test + Integration Test
D) Unit + Integration + E2E Test
E) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 12
주문 데이터의 보관 기간 정책이 있나요?

A) 영구 보관
B) 1년 후 아카이빙
C) 6개월 후 삭제
D) 정책 없음 (무제한 저장)
E) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 13
동시 접속 테이블 수는 최대 몇 개를 예상하시나요?

A) 10개 이하 (소규모 매장)
B) 10-50개 (중규모 매장)
C) 50-100개 (대규모 매장)
D) 100개 이상 (체인점/다중 매장)
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 14
다중 매장 지원이 필요한가요?

A) 단일 매장만 (매장 식별자는 설정용)
B) 다중 매장 지원 (하나의 시스템에서 여러 매장 관리)
C) 추후 확장 가능하도록 설계만
D) 필요 없음
E) Other (please describe after [Answer]: tag below)

[Answer]: C

---

## Question 15
UI/UX 디자인 시스템이나 컴포넌트 라이브러리를 사용하시겠습니까?

A) Material-UI (MUI)
B) Ant Design
C) Tailwind CSS
D) Bootstrap
E) Other (please describe after [Answer]: tag below)

[Answer]: C

---

**작성 완료 후 "완료" 또는 "done"이라고 알려주세요.**
