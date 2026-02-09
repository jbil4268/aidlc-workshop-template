# Unit of Work - Story Map

## Unit 1: Backend API Server

| Story | Priority | Description |
|-------|----------|-------------|
| US-1.1 | Must | 테이블 태블릿 자동 로그인 (API) |
| US-2.1 | Must | 카테고리별 메뉴 조회 (API) |
| US-2.2 | Must | 메뉴 상세 정보 및 알러지 (API) |
| US-4.1 | Must | 주문 확정 및 팁 계산 (API) |
| US-5.1 | Must | 현재 세션 주문 내역 조회 (API) |
| US-6.1 | Must | 관리자 로그인 (API) |
| US-7.1 | Must | 실시간 주문 대시보드 (WebSocket) |
| US-7.2 | Must | 주문 상태 변경 (API) |
| US-8.1 | Must | 테이블 태블릿 초기 설정 (API) |
| US-8.2 | Must | 주문 삭제 (API) |
| US-8.3 | Must | 테이블 세션 종료 (API) |
| US-8.4 | Should | 과거 주문 내역 조회 (API) |
| US-9.1 | Must | 메뉴 등록 (API) |
| US-9.2 | Must | 메뉴 수정 및 삭제 (API) |
| US-ERR-1 | Must | 네트워크 오류 처리 (에러 응답) |
| US-ERR-2 | Must | WebSocket 연결 관리 |

---

## Unit 2: Customer Frontend

| Story | Priority | Description |
|-------|----------|-------------|
| US-1.1 | Must | 테이블 태블릿 자동 로그인 (UI) |
| US-2.1 | Must | 카테고리별 메뉴 조회 (UI) |
| US-2.2 | Must | 메뉴 상세 정보 및 알러지 (UI) |
| US-3.1 | Must | 메뉴를 장바구니에 추가 (UI) |
| US-3.2 | Must | 장바구니 수량 조절 및 삭제 (UI) |
| US-4.1 | Must | 주문 확정 및 팁 추가 (UI) |
| US-5.1 | Must | 현재 세션 주문 내역 조회 (UI) |
| US-ERR-1 | Must | 네트워크 오류 시 주문 실패 처리 (UI) |

---

## Unit 3: Admin Frontend

| Story | Priority | Description |
|-------|----------|-------------|
| US-6.1 | Must | 관리자 로그인 (UI) |
| US-7.1 | Must | 실시간 주문 대시보드 (UI + WebSocket) |
| US-7.2 | Must | 주문 상태 변경 (UI) |
| US-8.1 | Must | 테이블 태블릿 초기 설정 (UI) |
| US-8.2 | Must | 주문 삭제 (UI) |
| US-8.3 | Must | 테이블 세션 종료 (UI) |
| US-8.4 | Should | 과거 주문 내역 조회 (UI) |
| US-9.1 | Must | 메뉴 등록 (UI) |
| US-9.2 | Must | 메뉴 수정 및 삭제 (UI) |
| US-ERR-2 | Must | WebSocket 연결 끊김 처리 (UI) |

---

## Coverage Verification

모든 User Story가 최소 1개 Unit에 할당되었는지 확인:

| Story | Backend | Customer FE | Admin FE |
|-------|---------|-------------|----------|
| US-1.1 | ✅ | ✅ | - |
| US-2.1 | ✅ | ✅ | - |
| US-2.2 | ✅ | ✅ | - |
| US-3.1 | - | ✅ | - |
| US-3.2 | - | ✅ | - |
| US-4.1 | ✅ | ✅ | - |
| US-5.1 | ✅ | ✅ | - |
| US-6.1 | ✅ | - | ✅ |
| US-7.1 | ✅ | - | ✅ |
| US-7.2 | ✅ | - | ✅ |
| US-8.1 | ✅ | - | ✅ |
| US-8.2 | ✅ | - | ✅ |
| US-8.3 | ✅ | - | ✅ |
| US-8.4 | ✅ | - | ✅ |
| US-9.1 | ✅ | - | ✅ |
| US-9.2 | ✅ | - | ✅ |
| US-ERR-1 | ✅ | ✅ | - |
| US-ERR-2 | ✅ | - | ✅ |

**Result**: 모든 스토리가 할당됨 ✅
