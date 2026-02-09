# Functional Design Plan - Unit 1: Backend API Server

## Plan Overview
Backend API Server의 상세 비즈니스 로직, Domain Entity, Business Rule을 설계합니다.

## Execution Steps

- [x] Step 1: Unit Context 분석 (unit-of-work.md, story-map.md 기반)
- [x] Step 2: 질문 수집 및 사용자 답변 대기
- [x] Step 3: Domain Entities 상세 설계
- [x] Step 4: Business Logic Model 설계
- [x] Step 5: Business Rules 정의
- [x] Step 6: 산출물 생성 및 검증
- [x] Step 7: 사용자 승인 대기

---

## Step 2: Clarification Questions

아래 질문들에 답변해 주세요. 각 질문의 `[Answer]:` 뒤에 선택지 또는 자유 입력으로 답변해 주시면 됩니다.

---

### Q1. 주문 번호 생성 규칙
주문 번호(order_number) 생성 방식을 선택해 주세요.

A) 순차 번호 (매장별 일일 리셋, 예: #001, #002, ...)
B) 타임스탬프 기반 (예: ORD-20260209-001)
C) 랜덤 코드 (예: A3F7, 4자리 영숫자)
D) 기타 (직접 입력)

[Answer]: A

---

### Q2. 주문 상태 전이 규칙
주문 상태 변경 시 허용되는 전이 규칙을 선택해 주세요.

A) 단방향만 허용: pending → preparing → completed (역방향 불가)
B) 유연한 전이: pending ↔ preparing → completed (preparing에서 pending으로 되돌리기 가능)
C) 완전 자유: 모든 상태 간 전이 가능
D) 기타 (직접 입력)

[Answer]: C

---

### Q3. 세션 시작 시점
테이블 세션(TableSession)이 시작되는 시점을 선택해 주세요.

A) 테이블 로그인 시 자동 생성 (활성 세션이 없으면)
B) 첫 주문 생성 시 자동 생성
C) 관리자가 수동으로 세션 시작
D) 기타 (직접 입력)

[Answer]: A

---

### Q4. 메뉴 삭제 시 기존 주문 처리
이미 주문된 메뉴를 삭제할 때 처리 방식을 선택해 주세요.

A) 삭제 불가 - 활성 주문에 포함된 메뉴는 삭제 차단
B) Soft Delete - 메뉴를 비활성화(is_available=false)하고 신규 주문에서만 숨김
C) 강제 삭제 - 메뉴 삭제, 기존 주문은 snapshot 데이터로 유지
D) 기타 (직접 입력)

[Answer]: B

---

### Q5. 카테고리 삭제 시 메뉴 처리
카테고리를 삭제할 때 해당 카테고리에 속한 메뉴 처리 방식을 선택해 주세요.

A) 삭제 차단 - 메뉴가 있는 카테고리는 삭제 불가
B) 메뉴 이동 - "미분류" 카테고리로 자동 이동
C) 함께 삭제 - 카테고리와 소속 메뉴 모두 삭제
D) 기타 (직접 입력)

[Answer]: B

---

### Q6. 팁 계산 시 소수점 처리
팁 금액 계산 시 소수점 처리 방식을 선택해 주세요.
(예: subtotal 15,000원 × 15% = 2,250원 → 정확히 나누어 떨어지지 않는 경우)

A) 반올림 (round)
B) 올림 (ceil)
C) 내림 (floor, 버림)
D) 기타 (직접 입력)

[Answer]: A

---

### Q7. 이미지 업로드 제한
메뉴 이미지 업로드 시 제한 사항을 선택해 주세요.

A) 최대 5MB, JPEG/PNG만 허용
B) 최대 10MB, JPEG/PNG/WebP 허용
C) 제한 없음 (서버 기본 설정 사용)
D) 기타 (직접 입력)

[Answer]: B

---

### Q8. 세션 종료 시 진행 중인 주문 처리
테이블 세션 종료(이용 완료) 시 아직 완료되지 않은 주문(pending/preparing)의 처리 방식을 선택해 주세요.

A) 종료 차단 - 모든 주문이 completed 상태여야 세션 종료 가능
B) 강제 완료 - 미완료 주문을 자동으로 completed로 변경 후 종료
C) 그대로 아카이빙 - 현재 상태 그대로 이력에 저장
D) 기타 (직접 입력)

[Answer]: C

---

### Q9. 관리자 계정 초기 생성
최초 관리자 계정 생성 방식을 선택해 주세요.

A) Seed 데이터 - 서버 시작 시 기본 관리자 계정 자동 생성 (환경 변수 기반)
B) CLI 명령어 - 별도 스크립트로 관리자 계정 생성
C) 회원가입 API - 관리자 등록 API 제공 (보안 키 필요)
D) 기타 (직접 입력)

[Answer]: A

---

### Q10. 동일 메뉴 재주문 처리
같은 세션에서 이전에 주문한 메뉴를 다시 주문할 때 처리 방식을 선택해 주세요.

A) 별도 주문 - 매번 새로운 Order로 생성 (주문 이력 분리)
B) 기존 주문에 추가 - 같은 Order에 항목 추가 (주문 합산)
C) 기타 (직접 입력)

[Answer]: B

---

**Note**: 모든 질문에 답변 후 "완료"라고 입력해 주세요.
