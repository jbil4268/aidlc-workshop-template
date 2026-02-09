# Application Components

## Backend Components

### 1. AuthComponent
**Purpose**: 인증 및 세션 관리
**Responsibilities**:
- 관리자 로그인/로그아웃 처리
- 테이블 태블릿 로그인 처리
- JWT 토큰 발급 및 검증
- 비밀번호 해싱 (bcrypt)
- 로그인 시도 제한 (5회/5분)
- 세션 만료 관리 (16시간)

### 2. MenuComponent
**Purpose**: 메뉴 및 카테고리 데이터 관리
**Responsibilities**:
- 메뉴 CRUD (생성, 조회, 수정, 삭제)
- 카테고리 CRUD
- 메뉴 노출 순서 관리
- 이미지 파일 업로드 및 저장
- 알러지 정보 관리
- 데이터 검증 (필수 필드, 가격 범위)

### 3. OrderComponent
**Purpose**: 주문 생성 및 관리
**Responsibilities**:
- 주문 생성 (장바구니 → 주문 전환)
- 주문 상태 변경 (대기중/준비중/완료)
- 주문 삭제 (관리자 직권)
- 주문 조회 (세션별, 테이블별)
- 팁 금액 계산 (비율 기반)
- 주문 번호 생성

### 4. TableComponent
**Purpose**: 테이블 및 세션 라이프사이클 관리
**Responsibilities**:
- 테이블 생성 및 설정
- 테이블 세션 시작/종료
- 세션 종료 시 주문 이력 아카이빙
- 테이블 상태 리셋
- 과거 주문 내역 조회

### 5. WebSocketComponent
**Purpose**: 실시간 양방향 통신
**Responsibilities**:
- WebSocket 연결 관리
- 신규 주문 이벤트 브로드캐스트
- 주문 상태 변경 이벤트 브로드캐스트
- 주문 삭제 이벤트 브로드캐스트
- 매장별 채널 관리

---

## Frontend Components (Customer)

### 6. CustomerAuthModule
**Purpose**: 테이블 태블릿 자동 인증
**Responsibilities**:
- 초기 설정 화면 (매장 ID, 테이블 번호, 비밀번호)
- SessionStorage 기반 자동 로그인
- 세션 만료 감지 및 재로그인

### 7. MenuBrowseModule
**Purpose**: 메뉴 탐색 및 표시
**Responsibilities**:
- 카테고리별 메뉴 목록 표시
- 메뉴 카드 레이아웃 (이미지, 이름, 가격, 알러지)
- 카테고리 탭 네비게이션
- 메뉴 상세 정보 모달

### 8. CartModule
**Purpose**: 장바구니 관리
**Responsibilities**:
- 메뉴 추가/삭제
- 수량 조절
- 총 금액 실시간 계산
- LocalStorage 영속성
- 장바구니 비우기

### 9. OrderModule
**Purpose**: 주문 생성 및 내역 조회
**Responsibilities**:
- 주문 확인 화면
- 팁 비율 선택 UI
- 주문 확정 및 서버 전송
- 주문 성공/실패 처리
- 주문 내역 목록 표시

---

## Frontend Components (Admin)

### 10. AdminAuthModule
**Purpose**: 관리자 인증
**Responsibilities**:
- 로그인 폼 (매장 ID, 사용자명, 비밀번호)
- JWT 토큰 관리 (SessionStorage)
- 자동 로그아웃 (16시간)

### 11. OrderDashboardModule
**Purpose**: 실시간 주문 모니터링
**Responsibilities**:
- 테이블별 그리드 레이아웃
- WebSocket 실시간 업데이트
- 신규 주문 알림음 재생
- 주문 상태 변경 UI
- 테이블별 필터링
- 주문 상세 보기 모달

### 12. TableManagementModule
**Purpose**: 테이블 관리
**Responsibilities**:
- 테이블 초기 설정
- 주문 삭제 (확인 팝업)
- 테이블 세션 종료 (이용 완료)
- 과거 주문 내역 조회

### 13. MenuManagementModule
**Purpose**: 메뉴 관리
**Responsibilities**:
- 메뉴 목록 표시 (카테고리별)
- 메뉴 등록/수정/삭제 폼
- 이미지 업로드
- 알러지 정보 입력
- 노출 순서 조정
