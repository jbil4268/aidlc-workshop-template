# 테이블오더 서비스 - User Stories

## Story Organization
- **분류 방식**: User Journey-Based (사용자 워크플로우 순서)
- **Acceptance Criteria**: 상세 (Given/When/Then + edge case + 에러 시나리오)
- **우선순위**: MoSCoW (Must/Should/Could/Won't)
- **에러 처리**: 주요 에러는 별도 스토리, 나머지는 acceptance criteria에 포함

---

# 고객 Journey

## Epic 1: 테이블 접근 및 인증

### US-1.1: 테이블 태블릿 자동 로그인
**Priority**: Must

**As a** 고객 (김민지/박영수)  
**I want to** 테이블에 앉으면 별도 로그인 없이 바로 메뉴를 볼 수 있도록  
**So that** 대기 시간 없이 즉시 주문을 시작할 수 있다

**Acceptance Criteria**:

```gherkin
Scenario: 자동 로그인 성공
  Given 관리자가 테이블 태블릿에 초기 설정을 완료한 상태
  And SessionStorage에 로그인 정보가 저장되어 있을 때
  When 태블릿 브라우저가 열리면
  Then 자동으로 로그인되어 메뉴 화면이 표시된다
  And 로그인 과정이 사용자에게 보이지 않는다

Scenario: 세션 만료 후 재로그인
  Given 16시간 세션이 만료된 상태
  When 태블릿 브라우저가 열리면
  Then 저장된 정보로 자동 재로그인을 시도한다
  And 성공 시 메뉴 화면이 표시된다

Scenario: 초기 설정 미완료
  Given 태블릿에 초기 설정이 되어있지 않은 상태
  When 태블릿 브라우저가 열리면
  Then 초기 설정 화면이 표시된다
  And 매장 식별자, 테이블 번호, 비밀번호 입력을 요구한다
```

---

## Epic 2: 메뉴 탐색

### US-2.1: 카테고리별 메뉴 조회
**Priority**: Must

**As a** 고객 (김민지/박영수)  
**I want to** 카테고리별로 메뉴를 탐색할 수 있도록  
**So that** 원하는 종류의 음식을 쉽게 찾을 수 있다

**Acceptance Criteria**:

```gherkin
Scenario: 메뉴 화면 기본 표시
  Given 로그인이 완료된 상태
  When 메뉴 화면이 로드되면
  Then 첫 번째 카테고리의 메뉴가 카드 형태로 표시된다
  And 카테고리 탭이 상단에 표시된다
  And 각 메뉴 카드에 메뉴명, 가격, 이미지가 표시된다

Scenario: 카테고리 전환
  Given 메뉴 화면이 표시된 상태
  When 다른 카테고리 탭을 터치하면
  Then 해당 카테고리의 메뉴 목록으로 전환된다
  And 전환이 부드럽게 이루어진다

Scenario: 메뉴 로딩 실패
  Given 네트워크 오류가 발생한 상태
  When 메뉴 화면을 로드하면
  Then 에러 메시지가 표시된다
  And 재시도 버튼이 제공된다
```

---

### US-2.2: 메뉴 상세 정보 및 알러지 확인
**Priority**: Must

**As a** 고객 (김민지)  
**I want to** 메뉴의 상세 설명과 알러지 정보를 확인할 수 있도록  
**So that** 안전하게 메뉴를 선택할 수 있다

**Acceptance Criteria**:

```gherkin
Scenario: 메뉴 상세 정보 조회
  Given 메뉴 목록이 표시된 상태
  When 메뉴 카드를 터치하면
  Then 메뉴 상세 정보가 표시된다 (메뉴명, 가격, 설명, 이미지, 알러지 정보)
  And 알러지 정보가 아이콘/뱃지 형태로 명확히 표시된다

Scenario: 알러지 정보가 없는 메뉴
  Given 알러지 정보가 등록되지 않은 메뉴
  When 메뉴 상세를 조회하면
  Then 알러지 정보 영역이 "알러지 정보 없음"으로 표시된다

Scenario: 터치 친화적 UI
  Given 메뉴 카드가 표시된 상태
  When 사용자가 터치하면
  Then 모든 버튼이 최소 44x44px 크기를 충족한다
  And 명확한 시각적 피드백이 제공된다
```

---

## Epic 3: 장바구니 관리

### US-3.1: 메뉴를 장바구니에 추가
**Priority**: Must

**As a** 고객 (김민지/박영수)  
**I want to** 원하는 메뉴를 장바구니에 담을 수 있도록  
**So that** 여러 메뉴를 한 번에 주문할 수 있다

**Acceptance Criteria**:

```gherkin
Scenario: 메뉴 추가
  Given 메뉴 목록이 표시된 상태
  When 메뉴의 "담기" 버튼을 터치하면
  Then 해당 메뉴가 장바구니에 추가된다
  And 장바구니 아이콘에 수량이 업데이트된다
  And 추가 성공 피드백이 표시된다

Scenario: 동일 메뉴 재추가
  Given 장바구니에 "김치찌개"가 1개 있는 상태
  When "김치찌개"를 다시 담기하면
  Then 수량이 2개로 증가한다
  And 총 금액이 재계산된다

Scenario: 페이지 새로고침 후 장바구니 유지
  Given 장바구니에 메뉴가 담긴 상태
  When 페이지를 새로고침하면
  Then 장바구니 내용이 그대로 유지된다 (LocalStorage)
```

---

### US-3.2: 장바구니 수량 조절 및 삭제
**Priority**: Must

**As a** 고객 (김민지/박영수)  
**I want to** 장바구니에서 수량을 조절하거나 메뉴를 삭제할 수 있도록  
**So that** 주문 전에 내용을 수정할 수 있다

**Acceptance Criteria**:

```gherkin
Scenario: 수량 증가
  Given 장바구니에 "김치찌개" 1개가 있는 상태
  When "+" 버튼을 터치하면
  Then 수량이 2개로 증가한다
  And 총 금액이 실시간으로 재계산된다

Scenario: 수량 감소
  Given 장바구니에 "김치찌개" 2개가 있는 상태
  When "-" 버튼을 터치하면
  Then 수량이 1개로 감소한다
  And 총 금액이 실시간으로 재계산된다

Scenario: 수량 1에서 감소 시 삭제
  Given 장바구니에 "김치찌개" 1개가 있는 상태
  When "-" 버튼을 터치하면
  Then 해당 메뉴가 장바구니에서 삭제된다

Scenario: 장바구니 비우기
  Given 장바구니에 여러 메뉴가 있는 상태
  When "장바구니 비우기" 버튼을 터치하면
  Then 확인 팝업이 표시된다
  And 확인 시 모든 메뉴가 삭제된다
  And 총 금액이 0원으로 표시된다
```

---

## Epic 4: 주문 생성

### US-4.1: 주문 확정 및 팁 추가
**Priority**: Must

**As a** 고객 (김민지)  
**I want to** 장바구니 내용을 확인하고 팁을 추가하여 주문을 확정할 수 있도록  
**So that** 최종 주문이 매장에 전달된다

**Acceptance Criteria**:

```gherkin
Scenario: 주문 확인 화면 표시
  Given 장바구니에 메뉴가 있는 상태
  When "주문하기" 버튼을 터치하면
  Then 주문 확인 화면이 표시된다
  And 메뉴 목록, 수량, 단가, 소계가 표시된다
  And 팁 비율 선택 UI가 표시된다 (0%, 5%, 10%, 15%, 20%)
  And 기본값은 0%로 선택되어 있다

Scenario: 팁 비율 선택
  Given 주문 확인 화면이 표시된 상태 (소계 30,000원)
  When 10% 팁을 선택하면
  Then 팁 금액이 3,000원으로 계산되어 표시된다
  And 최종 금액이 33,000원으로 표시된다

Scenario: 주문 확정 성공
  Given 주문 확인 화면에서 팁을 선택한 상태
  When "주문 확정" 버튼을 터치하면
  Then 주문이 서버에 전송된다
  And 주문 번호가 5초간 표시된다
  And 장바구니가 자동으로 비워진다
  And 메뉴 화면으로 자동 리다이렉트된다

Scenario: 주문 확정 실패
  Given 네트워크 오류가 발생한 상태
  When "주문 확정" 버튼을 터치하면
  Then 에러 메시지가 표시된다
  And 장바구니 내용이 유지된다
  And 재시도가 가능하다

Scenario: 빈 장바구니로 주문 시도
  Given 장바구니가 비어있는 상태
  When "주문하기" 버튼을 터치하면
  Then "장바구니가 비어있습니다" 메시지가 표시된다
  And 주문 확인 화면으로 이동하지 않는다
```

---

## Epic 5: 주문 내역 확인

### US-5.1: 현재 세션 주문 내역 조회
**Priority**: Must

**As a** 고객 (김민지/박영수)  
**I want to** 현재 테이블에서 주문한 내역을 확인할 수 있도록  
**So that** 주문 상태와 총 금액을 파악할 수 있다

**Acceptance Criteria**:

```gherkin
Scenario: 주문 내역 조회
  Given 현재 세션에서 주문이 있는 상태
  When 주문 내역 탭을 터치하면
  Then 현재 세션의 주문 목록이 최신순으로 표시된다
  And 각 주문에 주문 번호, 시각, 메뉴, 수량, 금액, 상태가 표시된다

Scenario: 주문 상태 표시
  Given 주문 내역이 표시된 상태
  When 주문 상태가 변경되면
  Then 대기중/준비중/완료 상태가 시각적으로 구분되어 표시된다

Scenario: 이전 세션 주문 미표시
  Given 이전 세션의 주문이 존재하는 상태
  When 주문 내역을 조회하면
  Then 현재 세션의 주문만 표시된다
  And 이전 세션의 주문은 표시되지 않는다

Scenario: 주문 없음
  Given 현재 세션에서 주문이 없는 상태
  When 주문 내역 탭을 터치하면
  Then "주문 내역이 없습니다" 메시지가 표시된다
```

---

# 관리자 Journey

## Epic 6: 매장 인증

### US-6.1: 관리자 로그인
**Priority**: Must

**As a** 매장 관리자 (이준호/최서연)  
**I want to** 매장 식별자와 계정으로 로그인할 수 있도록  
**So that** 주문 관리 시스템에 접근할 수 있다

**Acceptance Criteria**:

```gherkin
Scenario: 로그인 성공
  Given 로그인 화면이 표시된 상태
  When 올바른 매장 식별자, 사용자명, 비밀번호를 입력하고 로그인하면
  Then JWT 토큰이 발급되어 SessionStorage에 저장된다
  And 주문 모니터링 대시보드로 이동한다
  And 16시간 세션이 시작된다

Scenario: 로그인 실패
  Given 로그인 화면이 표시된 상태
  When 잘못된 비밀번호를 입력하면
  Then "아이디 또는 비밀번호가 올바르지 않습니다" 에러가 표시된다
  And 로그인 시도 횟수가 증가한다

Scenario: 로그인 시도 제한
  Given 5회 연속 로그인 실패한 상태
  When 다시 로그인을 시도하면
  Then "5분 후 다시 시도해주세요" 메시지가 표시된다
  And 5분간 로그인이 차단된다

Scenario: 세션 유지
  Given 로그인된 상태
  When 브라우저를 새로고침하면
  Then SessionStorage의 JWT로 세션이 유지된다
  And 대시보드가 다시 로드된다

Scenario: 자동 로그아웃
  Given 16시간이 경과한 상태
  When 다음 API 요청을 보내면
  Then 세션이 만료되어 로그인 화면으로 이동한다
  And "세션이 만료되었습니다" 메시지가 표시된다
```

---

## Epic 7: 실시간 주문 모니터링

### US-7.1: 실시간 주문 대시보드
**Priority**: Must

**As a** 매장 관리자 (이준호/최서연)  
**I want to** 들어오는 주문을 실시간으로 확인할 수 있도록  
**So that** 신속하게 주문을 처리할 수 있다

**Acceptance Criteria**:

```gherkin
Scenario: 대시보드 기본 표시
  Given 로그인이 완료된 상태
  When 대시보드가 로드되면
  Then 테이블별 카드가 그리드 형태로 표시된다
  And 각 카드에 테이블 번호, 총 주문액, 최신 주문 미리보기가 표시된다

Scenario: 신규 주문 실시간 수신
  Given 대시보드가 표시된 상태
  When 고객이 새 주문을 생성하면
  Then 2초 이내에 해당 테이블 카드에 주문이 표시된다
  And 알림음이 재생된다
  And 신규 주문이 시각적으로 강조된다 (색상 변경, 애니메이션)

Scenario: 알림음 토글
  Given 대시보드가 표시된 상태
  When 알림음 off 버튼을 터치하면
  Then 신규 주문 시 알림음이 재생되지 않는다
  And 시각적 강조는 유지된다

Scenario: 주문 상세 보기
  Given 테이블 카드가 표시된 상태
  When 테이블 카드를 클릭하면
  Then 해당 테이블의 전체 주문 목록이 상세히 표시된다
  And 각 주문의 메뉴, 수량, 금액, 팁, 상태가 표시된다

Scenario: WebSocket 연결 끊김
  Given WebSocket 연결이 끊어진 상태
  When 연결이 끊어지면
  Then "연결이 끊어졌습니다" 알림이 표시된다
  And 자동 재연결을 시도한다
  And 재연결 성공 시 최신 데이터를 동기화한다
```

---

### US-7.2: 주문 상태 변경
**Priority**: Must

**As a** 매장 관리자 (이준호/최서연)  
**I want to** 주문 상태를 변경할 수 있도록  
**So that** 주문 처리 진행 상황을 추적할 수 있다

**Acceptance Criteria**:

```gherkin
Scenario: 상태 변경 (대기중 → 준비중)
  Given 대기중 상태의 주문이 있는 상태
  When "준비중" 버튼을 터치하면
  Then 주문 상태가 "준비중"으로 변경된다
  And 고객 화면에도 상태가 업데이트된다

Scenario: 상태 변경 (준비중 → 완료)
  Given 준비중 상태의 주문이 있는 상태
  When "완료" 버튼을 터치하면
  Then 주문 상태가 "완료"로 변경된다
  And 고객 화면에도 상태가 업데이트된다

Scenario: 테이블별 필터링
  Given 여러 테이블의 주문이 표시된 상태
  When 특정 테이블 번호로 필터링하면
  Then 해당 테이블의 주문만 표시된다
```

---

## Epic 8: 테이블 관리

### US-8.1: 테이블 태블릿 초기 설정
**Priority**: Must

**As a** 매장 관리자 (이준호)  
**I want to** 테이블 태블릿의 초기 설정을 할 수 있도록  
**So that** 고객이 해당 테이블에서 주문할 수 있다

**Acceptance Criteria**:

```gherkin
Scenario: 테이블 초기 설정
  Given 관리자 대시보드에서 테이블 관리 화면
  When 테이블 번호와 비밀번호를 입력하고 저장하면
  Then 테이블이 생성되고 16시간 세션이 시작된다
  And 해당 태블릿에서 자동 로그인이 활성화된다

Scenario: 중복 테이블 번호
  Given 이미 존재하는 테이블 번호
  When 같은 번호로 테이블을 생성하려 하면
  Then "이미 존재하는 테이블 번호입니다" 에러가 표시된다
```

---

### US-8.2: 주문 삭제 (직권 수정)
**Priority**: Must

**As a** 매장 관리자 (이준호/최서연)  
**I want to** 잘못된 주문을 삭제할 수 있도록  
**So that** 정확한 주문 내역을 유지할 수 있다

**Acceptance Criteria**:

```gherkin
Scenario: 주문 삭제
  Given 테이블의 주문 상세가 표시된 상태
  When 특정 주문의 "삭제" 버튼을 터치하면
  Then 확인 팝업이 표시된다
  And 확인 시 주문이 즉시 삭제된다
  And 테이블 총 주문액이 재계산된다
  And 성공 피드백이 표시된다

Scenario: 주문 삭제 취소
  Given 삭제 확인 팝업이 표시된 상태
  When "취소" 버튼을 터치하면
  Then 팝업이 닫히고 주문이 유지된다
```

---

### US-8.3: 테이블 세션 종료 (이용 완료)
**Priority**: Must

**As a** 매장 관리자 (이준호/최서연)  
**I want to** 고객이 떠난 후 테이블 세션을 종료할 수 있도록  
**So that** 다음 고객이 깨끗한 상태에서 시작할 수 있다

**Acceptance Criteria**:

```gherkin
Scenario: 테이블 이용 완료
  Given 활성 세션이 있는 테이블
  When "이용 완료" 버튼을 터치하면
  Then 확인 팝업이 표시된다
  And 확인 시 현재 세션의 주문 내역이 과거 이력으로 이동한다
  And 테이블의 현재 주문 목록이 비워진다
  And 총 주문액이 0원으로 리셋된다
  And 성공 피드백이 표시된다

Scenario: 새 고객 시작
  Given 이전 세션이 종료된 테이블
  When 새 고객이 첫 주문을 생성하면
  Then 새로운 세션이 자동으로 시작된다
  And 이전 주문 내역이 표시되지 않는다
```

---

### US-8.4: 과거 주문 내역 조회
**Priority**: Should

**As a** 매장 관리자 (이준호)  
**I want to** 테이블의 과거 주문 내역을 조회할 수 있도록  
**So that** 이전 매출과 주문 패턴을 확인할 수 있다

**Acceptance Criteria**:

```gherkin
Scenario: 과거 내역 조회
  Given 테이블 상세 화면이 표시된 상태
  When "과거 내역" 버튼을 터치하면
  Then 해당 테이블의 과거 주문 목록이 시간 역순으로 표시된다
  And 각 주문에 주문 번호, 시각, 메뉴 목록, 총 금액, 완료 시각이 표시된다

Scenario: 날짜 필터링
  Given 과거 내역이 표시된 상태
  When 특정 날짜 범위를 선택하면
  Then 해당 기간의 주문만 필터링되어 표시된다

Scenario: 대시보드 복귀
  Given 과거 내역 화면이 표시된 상태
  When "닫기" 버튼을 터치하면
  Then 대시보드 화면으로 복귀한다
```

---

## Epic 9: 메뉴 관리

### US-9.1: 메뉴 등록
**Priority**: Must

**As a** 매장 관리자 (이준호)  
**I want to** 새로운 메뉴를 등록할 수 있도록  
**So that** 고객에게 최신 메뉴를 제공할 수 있다

**Acceptance Criteria**:

```gherkin
Scenario: 메뉴 등록 성공
  Given 메뉴 관리 화면이 표시된 상태
  When 메뉴명, 가격, 설명, 카테고리, 이미지, 알러지 정보를 입력하고 저장하면
  Then 메뉴가 등록되고 목록에 표시된다
  And 고객 화면에도 즉시 반영된다
  And 성공 피드백이 표시된다

Scenario: 필수 필드 누락
  Given 메뉴 등록 화면이 표시된 상태
  When 메뉴명 없이 저장을 시도하면
  Then "메뉴명은 필수 항목입니다" 에러가 표시된다
  And 저장이 진행되지 않는다

Scenario: 가격 검증
  Given 메뉴 등록 화면이 표시된 상태
  When 가격에 음수 값을 입력하면
  Then "가격은 0 이상이어야 합니다" 에러가 표시된다
```

---

### US-9.2: 메뉴 수정 및 삭제
**Priority**: Must

**As a** 매장 관리자 (이준호)  
**I want to** 기존 메뉴를 수정하거나 삭제할 수 있도록  
**So that** 메뉴 정보를 최신 상태로 유지할 수 있다

**Acceptance Criteria**:

```gherkin
Scenario: 메뉴 수정
  Given 메뉴 목록이 표시된 상태
  When 메뉴의 "수정" 버튼을 터치하고 정보를 변경하여 저장하면
  Then 메뉴 정보가 업데이트된다
  And 고객 화면에도 즉시 반영된다

Scenario: 메뉴 삭제
  Given 메뉴 목록이 표시된 상태
  When 메뉴의 "삭제" 버튼을 터치하면
  Then 확인 팝업이 표시된다
  And 확인 시 메뉴가 삭제된다

Scenario: 메뉴 노출 순서 조정
  Given 메뉴 목록이 표시된 상태
  When 메뉴의 순서를 드래그하여 변경하면
  Then 변경된 순서가 저장된다
  And 고객 화면에도 순서가 반영된다
```

---

# 별도 에러 스토리

## US-ERR-1: 네트워크 오류 시 주문 실패 처리
**Priority**: Must

**As a** 고객  
**I want to** 네트워크 오류 시 명확한 안내를 받을 수 있도록  
**So that** 주문 상태를 정확히 파악하고 재시도할 수 있다

**Acceptance Criteria**:

```gherkin
Scenario: 주문 전송 중 네트워크 오류
  Given 주문 확정 버튼을 터치한 상태
  When 네트워크 오류가 발생하면
  Then "네트워크 오류가 발생했습니다. 다시 시도해주세요" 메시지가 표시된다
  And 장바구니 내용이 유지된다
  And "재시도" 버튼이 제공된다

Scenario: 메뉴 로딩 중 네트워크 오류
  Given 메뉴 화면을 로드하는 중
  When 네트워크 오류가 발생하면
  Then 에러 메시지와 재시도 버튼이 표시된다
```

---

## US-ERR-2: WebSocket 연결 끊김 처리
**Priority**: Must

**As a** 매장 관리자  
**I want to** WebSocket 연결이 끊어졌을 때 자동 복구되도록  
**So that** 주문을 놓치지 않을 수 있다

**Acceptance Criteria**:

```gherkin
Scenario: WebSocket 자동 재연결
  Given WebSocket 연결이 끊어진 상태
  When 자동 재연결을 시도하면
  Then 최대 5회까지 재연결을 시도한다
  And 재연결 성공 시 놓친 주문을 동기화한다
  And "연결이 복구되었습니다" 알림이 표시된다

Scenario: 재연결 실패
  Given 5회 재연결 시도가 모두 실패한 상태
  When 재연결이 불가능하면
  Then "서버 연결에 실패했습니다. 페이지를 새로고침해주세요" 메시지가 표시된다
  And 수동 새로고침 버튼이 제공된다
```

---

# Story Summary

## MoSCoW Priority Map

### Must Have (필수)
| Story | 설명 |
|-------|------|
| US-1.1 | 테이블 태블릿 자동 로그인 |
| US-2.1 | 카테고리별 메뉴 조회 |
| US-2.2 | 메뉴 상세 정보 및 알러지 확인 |
| US-3.1 | 메뉴를 장바구니에 추가 |
| US-3.2 | 장바구니 수량 조절 및 삭제 |
| US-4.1 | 주문 확정 및 팁 추가 |
| US-5.1 | 현재 세션 주문 내역 조회 |
| US-6.1 | 관리자 로그인 |
| US-7.1 | 실시간 주문 대시보드 |
| US-7.2 | 주문 상태 변경 |
| US-8.1 | 테이블 태블릿 초기 설정 |
| US-8.2 | 주문 삭제 (직권 수정) |
| US-8.3 | 테이블 세션 종료 |
| US-9.1 | 메뉴 등록 |
| US-9.2 | 메뉴 수정 및 삭제 |
| US-ERR-1 | 네트워크 오류 시 주문 실패 처리 |
| US-ERR-2 | WebSocket 연결 끊김 처리 |

### Should Have (권장)
| Story | 설명 |
|-------|------|
| US-8.4 | 과거 주문 내역 조회 |

---

## INVEST Criteria Verification

모든 스토리가 INVEST 기준을 충족하는지 검증:

- **I (Independent)**: 각 스토리가 독립적으로 구현 가능 ✅
- **N (Negotiable)**: acceptance criteria 내에서 구현 방식 협상 가능 ✅
- **V (Valuable)**: 각 스토리가 사용자에게 명확한 가치 제공 ✅
- **E (Estimable)**: 구현 범위가 명확하여 추정 가능 ✅
- **S (Small)**: 각 스토리가 하나의 기능 단위로 적절한 크기 ✅
- **T (Testable)**: Given/When/Then 형식의 acceptance criteria로 테스트 가능 ✅
