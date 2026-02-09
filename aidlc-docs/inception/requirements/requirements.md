# 테이블오더 서비스 Requirements

## Intent Analysis

### User Request
테이블오더 서비스 구축 - 고객용 주문 인터페이스와 관리자용 모니터링 시스템을 포함한 디지털 주문 플랫폼

### Request Type
**New Project** - 새로운 시스템 구축

### Scope Estimate
**System-wide** - 전체 시스템 구축
- 고객용 웹 인터페이스
- 관리자용 웹 인터페이스
- Backend API 서버
- 데이터베이스

### Complexity Estimate
**Complex** - 복잡한 시스템
- 실시간 주문 모니터링 (WebSocket)
- 다중 사용자 세션 관리
- 테이블별 독립적인 주문 세션
- 관리자 인증 및 권한 관리

---

## Technical Stack Decisions

### Backend
- **Framework**: Python with FastAPI or Django
- **Authentication**: JWT (JSON Web Token)
- **Real-time Communication**: WebSocket
- **Logging**: Console.log (기본 수준)

### Frontend
- **Framework**: Vue.js
- **UI Library**: Tailwind CSS
- **Storage**: SessionStorage (테이블 로그인 정보, 관리자 JWT)

### Database
- **Primary**: SQLite (개발/테스트용)
- **Data Retention**: 1년 후 아카이빙

### Infrastructure
- **Deployment**: 로컬 개발 환경
- **Image Storage**: 서버에 업로드 및 저장
- **Scalability**: 10개 이하 테이블 동시 접속 (소규모 매장)
- **Multi-store**: 추후 확장 가능하도록 설계

### Testing Strategy
- **Level**: 핵심 비즈니스 로직만 Unit Test
- **Coverage**: 주문 생성, 세션 관리, 인증 로직

---

## Functional Requirements

### FR-1: 고객용 기능 (Customer Features)

#### FR-1.1: 테이블 태블릿 자동 로그인 및 세션 관리
**Priority**: High | **Complexity**: Medium

**Description**: 
고객이 별도 로그인 절차 없이 즉시 주문할 수 있도록 자동 인증 제공

**Acceptance Criteria**:
- 관리자가 테이블 초기 설정 시 매장 식별자, 테이블 번호, 테이블 비밀번호 입력
- 로그인 정보를 SessionStorage에 저장
- 1회 로그인 성공 후 자동 로그인 동작
- 16시간 세션 유지
- 세션 만료 시 재로그인 요구

**User Story**:
```
As a 테이블 태블릿 관리자
I want to 테이블 정보를 1회만 설정하고
So that 고객이 별도 로그인 없이 바로 주문할 수 있다
```

---

#### FR-1.2: 메뉴 조회 및 탐색
**Priority**: High | **Complexity**: Low

**Description**:
고객이 매장의 메뉴를 쉽게 탐색하고 선택할 수 있도록 지원

**Acceptance Criteria**:
- 메뉴 화면이 기본 화면으로 표시
- 카테고리별 메뉴 분류 및 표시
- 메뉴 상세 정보 표시 (메뉴명, 가격, 설명, 이미지, 알러지 정보)
- 알러지 정보 아이콘/뱃지 형태로 메뉴 카드에 표시
- 카테고리 간 빠른 이동
- 카드 형태의 메뉴 레이아웃
- 터치 친화적인 버튼 크기 (최소 44x44px)

**User Story**:
```
As a 고객
I want to 카테고리별로 메뉴를 탐색하고
So that 원하는 메뉴를 쉽게 찾아 선택할 수 있다
```

---

#### FR-1.3: 장바구니 관리
**Priority**: High | **Complexity**: Medium

**Description**:
주문 전 선택한 메뉴를 임시 저장하고 수정할 수 있는 기능

**Acceptance Criteria**:
- 메뉴 추가/삭제 기능
- 수량 조절 (증가/감소)
- 총 금액 실시간 계산
- 장바구니 비우기 기능
- LocalStorage에 저장 (페이지 새로고침 시에도 유지)
- 서버 전송은 주문 확정 시에만 수행

**User Story**:
```
As a 고객
I want to 주문 전에 장바구니에서 메뉴를 추가/삭제하고
So that 최종 주문 전에 내용을 확인하고 수정할 수 있다
```

---

#### FR-1.4: 주문 생성
**Priority**: High | **Complexity**: Medium

**Description**:
장바구니의 메뉴를 실제 주문으로 전환

**Acceptance Criteria**:
- 주문 내역 최종 확인 화면
- **팁 추가 기능**:
  - 주문 확정 전 팁 비율 선택 UI 표시
  - 미리 정의된 팁 비율 옵션 (예: 0%, 5%, 10%, 15%, 20%)
  - 팁 없음(0%) 기본 선택
  - 선택한 비율에 따라 팁 금액 자동 계산 (subtotal × 비율)
  - 계산된 팁 금액과 최종 합계가 실시간으로 표시
- 주문 확정 버튼
- 주문 성공 시:
  - 주문 번호 표시 (5초간)
  - 장바구니 자동 비우기
  - 메뉴 화면으로 자동 리다이렉트
- 주문 실패 시 에러 메시지 표시 및 장바구니 유지
- 주문 정보 포함: 매장 ID, 테이블 ID, 메뉴 목록, 총 금액, 팁 금액, 세션 ID

**User Story**:
```
As a 고객
I want to 장바구니의 메뉴를 주문 확정하고
So that 주문이 매장에 전달되어 음식을 받을 수 있다
```

---

#### FR-1.5: 주문 내역 조회
**Priority**: Medium | **Complexity**: Low

**Description**:
현재 테이블의 주문 이력을 확인

**Acceptance Criteria**:
- 주문 시간 순 정렬 (최신순)
- 주문별 상세 정보 표시 (주문 번호, 시각, 메뉴 및 수량, 금액, 상태)
- 주문 상태: 대기중/준비중/완료
- 현재 테이블 세션 주문만 표시 (이전 세션 제외)
- 매장 이용 완료 처리된 주문은 제외
- 페이지네이션 또는 무한 스크롤

**User Story**:
```
As a 고객
I want to 내가 주문한 내역을 확인하고
So that 주문 상태와 총 금액을 파악할 수 있다
```

---

### FR-2: 관리자용 기능 (Admin Features)

#### FR-2.1: 매장 인증
**Priority**: High | **Complexity**: Medium

**Description**:
관리자가 자신의 매장 관리 시스템에 접근

**Acceptance Criteria**:
- 매장 식별자, 사용자명, 비밀번호 입력
- JWT 토큰 기반 인증
- 16시간 세션 유지
- SessionStorage에 JWT 저장
- 브라우저 새로고침 시 세션 유지
- 16시간 후 자동 로그아웃
- 비밀번호 bcrypt 해싱
- 로그인 시도 제한 (5회 실패 시 5분 잠금)

**User Story**:
```
As a 매장 관리자
I want to 안전하게 로그인하고
So that 주문 관리 시스템에 접근할 수 있다
```

---

#### FR-2.2: 실시간 주문 모니터링
**Priority**: High | **Complexity**: High

**Description**:
들어오는 주문을 실시간으로 확인하고 관리

**Acceptance Criteria**:
- WebSocket 기반 실시간 주문 업데이트
- 그리드/대시보드 레이아웃 (테이블별 카드 형태)
- 각 테이블 카드에 총 주문액 표시
- 최신 주문 n개 미리보기
- 주문 카드 클릭 시 전체 메뉴 목록 상세 보기
- 주문 상태 변경 기능 (대기중/준비중/완료)
- 신규 주문 시각적 강조 (색상 변경, 애니메이션)
- 신규 주문 알림음 재생 (브라우저 Web Audio API 사용)
  - 알림음 on/off 토글 버튼
  - 기본값: on
- 2초 이내 주문 표시
- 테이블별 필터링 기능

**User Story**:
```
As a 매장 관리자
I want to 실시간으로 들어오는 주문을 확인하고
So that 신속하게 주문을 처리할 수 있다
```

---

#### FR-2.3: 테이블 관리
**Priority**: High | **Complexity**: High

**Description**:
테이블별 주문 상태 관리 및 세션 라이프사이클 관리

**Acceptance Criteria**:

**테이블 태블릿 초기 설정**:
- 테이블 번호 및 비밀번호 설정
- 16시간 세션 생성
- 설정 정보 저장 및 자동 로그인 활성화

**주문 삭제 (직권 수정)**:
- 특정 주문 삭제 버튼
- 확인 팝업 표시
- 주문 즉시 삭제
- 테이블 총 주문액 재계산
- 성공/실패 피드백

**테이블 세션 처리**:
- 테이블 세션 시작 및 종료 관리
- 확인 팝업 표시
- 세션 종료 시 주문 내역을 과거 이력으로 이동
- 세션 종료 시 테이블 현재 주문 목록 및 총 주문액 0으로 리셋
- 새 고객이 이전 주문 내역 없이 시작 가능

**과거 주문 내역 조회**:
- "과거 내역" 버튼
- 테이블별 과거 주문 목록 표시 (시간 역순)
- 각 주문 정보: 주문 번호, 시각, 메뉴 목록, 총 금액, 완료 시각
- 날짜 필터링 기능
- "닫기" 버튼으로 대시보드 복귀

**User Story**:
```
As a 매장 관리자
I want to 테이블 세션을 관리하고
So that 고객이 떠난 후 다음 고객을 위해 테이블을 초기화할 수 있다
```

---

#### FR-2.4: 메뉴 관리
**Priority**: Medium | **Complexity**: Medium

**Description**:
메뉴 정보를 동적으로 관리

**Acceptance Criteria**:
- 메뉴 조회 (카테고리별)
- 메뉴 등록 (메뉴명, 가격, 설명, 카테고리, 이미지 업로드, 알러지 정보)
- 메뉴 수정 (알러지 정보 포함)
- 메뉴 삭제
- 메뉴 노출 순서 조정
- 필수 필드 검증
- 가격 범위 검증 (0 이상)
- 이미지 파일 서버 저장

**User Story**:
```
As a 매장 관리자
I want to 메뉴를 추가/수정/삭제하고
So that 최신 메뉴 정보를 고객에게 제공할 수 있다
```

---

## Non-Functional Requirements

### NFR-1: Performance
**Priority**: High

**Requirements**:
- 주문 생성 응답 시간: 2초 이내
- WebSocket 메시지 전달: 2초 이내
- 메뉴 목록 로딩: 3초 이내
- 동시 접속 테이블: 최대 10개 지원
- 이미지 로딩: Lazy loading 적용

---

### NFR-2: Security
**Priority**: High

**Requirements**:
- 비밀번호 bcrypt 해싱 (salt rounds: 10)
- JWT 토큰 16시간 만료
- 로그인 시도 제한 (5회 실패 시 5분 잠금)
- HTTPS 사용 권장 (프로덕션 환경)
- SQL Injection 방지 (ORM 사용)
- XSS 방지 (입력 검증 및 sanitization)

---

### NFR-3: Usability
**Priority**: High

**Requirements**:
- 터치 친화적 UI (최소 버튼 크기 44x44px)
- 반응형 디자인 (태블릿 최적화)
- 직관적인 네비게이션
- 명확한 에러 메시지
- 로딩 상태 표시
- 성공/실패 피드백

---

### NFR-4: Scalability
**Priority**: Medium

**Requirements**:
- 다중 매장 지원 가능하도록 설계 (추후 확장)
- 데이터베이스 인덱싱 (매장 ID, 테이블 ID, 세션 ID)
- 이미지 파일 분리 저장 (추후 CDN 전환 가능)

---

### NFR-5: Maintainability
**Priority**: Medium

**Requirements**:
- 코드 모듈화 및 컴포넌트 분리
- API 문서화 (OpenAPI/Swagger)
- 주석 및 README 작성
- 환경 변수 사용 (.env 파일)
- Git 버전 관리

---

### NFR-6: Reliability
**Priority**: Medium

**Requirements**:
- 에러 핸들링 (try-catch, error boundary)
- 데이터 무결성 (트랜잭션 사용)
- 장바구니 데이터 로컬 저장 (새로고침 시 유지)
- WebSocket 재연결 메커니즘

---

### NFR-7: Data Management
**Priority**: Medium

**Requirements**:
- 주문 데이터 1년 후 아카이빙
- 세션 종료 시 주문 이력 보존
- 이미지 파일 정리 (미사용 이미지 삭제)
- 데이터베이스 백업 권장

---

## System Constraints

### Excluded Features (구현하지 않음)

**결제 관련**:
- 실제 결제 처리
- 결제 게이트웨이 연동
- 영수증 발행
- 환불 처리
- 포인트/쿠폰 시스템

**인증 및 보안**:
- OAuth, SNS 로그인
- 다단계 인증 (2FA, OTP)

**파일 및 컨텐츠 관리**:
- 이미지 리사이징/최적화
- 컨텐츠 관리 시스템
- 광고 기능

**알림 시스템**:
- 푸시 알림
- SMS 알림
- 이메일 발송
- 소리/진동 알림

**주방 기능**:
- 주문 내역 주방 전달
- 주방 식재료 재고 관리

**고급 기능**:
- 데이터 분석 및 대시보드
- 매출 리포트 생성
- 재고 관리 시스템
- 직원 관리 및 권한 설정
- 예약 시스템
- 고객 리뷰 시스템
- 다국어 기능

**외부 연동**:
- 배달 플랫폼 연동
- POS 시스템 연동
- 소셜 미디어 공유

---

## Data Model Overview

### Core Entities

**Store (매장)**:
- store_id (PK)
- store_name
- store_identifier (unique)
- created_at

**Table (테이블)**:
- table_id (PK)
- store_id (FK)
- table_number
- table_password (hashed)
- current_session_id (FK, nullable)
- created_at

**TableSession (테이블 세션)**:
- session_id (PK)
- table_id (FK)
- start_time
- end_time (nullable)
- is_active
- total_amount

**Menu (메뉴)**:
- menu_id (PK)
- store_id (FK)
- category_id (FK)
- menu_name
- price
- description
- image_url
- allergens (알러지 정보 - 예: 우유, 계란, 밀, 대두, 땅콩, 갑각류, 생선, 견과류 등)
- display_order
- is_available
- created_at
- updated_at

**Category (카테고리)**:
- category_id (PK)
- store_id (FK)
- category_name
- display_order

**Order (주문)**:
- order_id (PK)
- session_id (FK)
- table_id (FK)
- store_id (FK)
- order_number (unique)
- subtotal_amount (메뉴 금액 합계)
- tip_rate (팁 비율, 기본값 0 - 예: 0, 5, 10, 15, 20)
- tip_amount (계산된 팁 금액 = subtotal × tip_rate / 100)
- total_amount (subtotal + tip)
- status (pending/preparing/completed)
- created_at
- updated_at

**OrderItem (주문 항목)**:
- order_item_id (PK)
- order_id (FK)
- menu_id (FK)
- menu_name (snapshot)
- quantity
- unit_price (snapshot)
- subtotal

**Admin (관리자)**:
- admin_id (PK)
- store_id (FK)
- username (unique)
- password_hash
- created_at
- last_login

**OrderHistory (주문 이력)**:
- history_id (PK)
- order_id (FK)
- session_id (FK)
- archived_at
- (주문 및 주문 항목 정보 포함)

---

## API Endpoints Overview

### Customer API

**Authentication**:
- `POST /api/customer/auth/login` - 테이블 로그인
- `POST /api/customer/auth/refresh` - 세션 갱신

**Menu**:
- `GET /api/customer/menus` - 메뉴 목록 조회
- `GET /api/customer/menus/:id` - 메뉴 상세 조회
- `GET /api/customer/categories` - 카테고리 목록 조회

**Order**:
- `POST /api/customer/orders` - 주문 생성
- `GET /api/customer/orders` - 주문 내역 조회 (현재 세션)
- `GET /api/customer/orders/:id` - 주문 상세 조회

---

### Admin API

**Authentication**:
- `POST /api/admin/auth/login` - 관리자 로그인
- `POST /api/admin/auth/logout` - 로그아웃
- `POST /api/admin/auth/refresh` - 토큰 갱신

**Order Management**:
- `GET /api/admin/orders` - 전체 주문 조회
- `GET /api/admin/orders/:id` - 주문 상세 조회
- `PATCH /api/admin/orders/:id/status` - 주문 상태 변경
- `DELETE /api/admin/orders/:id` - 주문 삭제

**Table Management**:
- `GET /api/admin/tables` - 테이블 목록 조회
- `POST /api/admin/tables` - 테이블 생성
- `PATCH /api/admin/tables/:id` - 테이블 정보 수정
- `POST /api/admin/tables/:id/session/end` - 테이블 세션 종료
- `GET /api/admin/tables/:id/history` - 테이블 과거 주문 내역

**Menu Management**:
- `GET /api/admin/menus` - 메뉴 목록 조회
- `POST /api/admin/menus` - 메뉴 생성
- `PATCH /api/admin/menus/:id` - 메뉴 수정
- `DELETE /api/admin/menus/:id` - 메뉴 삭제
- `POST /api/admin/menus/upload-image` - 이미지 업로드

**Category Management**:
- `GET /api/admin/categories` - 카테고리 목록 조회
- `POST /api/admin/categories` - 카테고리 생성
- `PATCH /api/admin/categories/:id` - 카테고리 수정
- `DELETE /api/admin/categories/:id` - 카테고리 삭제

---

### WebSocket Events

**Client → Server**:
- `subscribe_orders` - 주문 업데이트 구독
- `unsubscribe_orders` - 구독 해제

**Server → Client**:
- `new_order` - 새 주문 알림
- `order_updated` - 주문 상태 변경 알림
- `order_deleted` - 주문 삭제 알림

---

## MVP Scope

### Phase 1: Core Features (필수)

**고객용**:
- ✅ 테이블 태블릿 자동 로그인 및 세션 관리
- ✅ 메뉴 조회 및 탐색
- ✅ 장바구니 관리
- ✅ 주문 생성 (5초 표시 후 자동 리다이렉트)
- ✅ 주문 내역 조회 (현재 세션만)

**관리자용**:
- ✅ 매장 인증 (16시간 세션)
- ✅ 실시간 주문 모니터링 (그리드 레이아웃, WebSocket)
- ✅ 테이블 관리 (초기 설정, 주문 삭제, 매장 이용 완료, 과거 내역 조회)
- ✅ 메뉴 관리 (CRUD)

---

## Success Criteria

### Business Goals
- 고객이 대기 시간 없이 즉시 주문 가능
- 관리자가 실시간으로 주문 모니터링 가능
- 테이블별 독립적인 주문 세션 관리
- 직관적이고 사용하기 쉬운 인터페이스

### Technical Goals
- 주문 생성 응답 시간 2초 이내
- WebSocket 실시간 업데이트 2초 이내
- 10개 테이블 동시 접속 지원
- 핵심 비즈니스 로직 Unit Test 커버리지

### User Experience Goals
- 터치 친화적 UI
- 명확한 피드백 (성공/실패)
- 로딩 상태 표시
- 에러 메시지 명확성

---

## Glossary

- **MVP**: Minimum Viable Product (최소 기능 제품)
- **API**: Application Programming Interface
- **UI/UX**: User Interface / User Experience
- **JWT**: JSON Web Token
- **WebSocket**: 양방향 실시간 통신 프로토콜
- **SSE**: Server-Sent Events
- **테이블 세션**: 특정 테이블에 고객이 앉아서 첫 주문 시작 후부터 해당 테이블 이용 완료 처리까지의 시간. 세션 종료 후 다른 고객의 첫 주문 시작 시 새로운 세션 시작.
- **SessionStorage**: 브라우저 세션 동안 데이터를 저장하는 Web Storage API
- **LocalStorage**: 브라우저에 영구적으로 데이터를 저장하는 Web Storage API
- **bcrypt**: 비밀번호 해싱 알고리즘

---

## References

- 원본 요구사항: `requirements/table-order-requirements.md`
- 제약사항: `requirements/constraints.md`
- 기술 스택 결정: `requirement-verification-questions.md`

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-09  
**Status**: Draft - Pending Approval
