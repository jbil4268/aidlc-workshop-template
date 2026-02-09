# Story Generation Plan

## Overview
테이블오더 서비스의 User Stories 및 Personas 생성 계획

## Story Generation Questions

아래 질문에 답변해주세요. 각 질문의 [Answer]: 태그 뒤에 선택한 옵션의 문자를 입력해주세요.

---

### Question 1
User Story 분류 방식은 어떤 것을 선호하시나요?

A) User Journey-Based - 사용자 워크플로우 순서대로 (입장 → 메뉴 탐색 → 주문 → 확인)
B) Feature-Based - 시스템 기능 단위로 (인증, 메뉴, 장바구니, 주문, 모니터링)
C) Persona-Based - 사용자 유형별로 (고객 스토리, 관리자 스토리)
D) Epic-Based - 대분류 Epic 아래 세부 스토리 계층 구조
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

### Question 2
Acceptance Criteria의 상세 수준은 어느 정도를 원하시나요?

A) 간결 - 핵심 조건만 (3-5개 항목)
B) 표준 - Given/When/Then 형식으로 주요 시나리오 포함
C) 상세 - Given/When/Then + edge case + 에러 시나리오 포함
D) Other (please describe after [Answer]: tag below)

[Answer]: C

---

### Question 3
고객 페르소나에서 가장 중요하게 고려할 사용자 특성은 무엇인가요?

A) 연령대 (디지털 기기 친숙도 차이)
B) 방문 빈도 (첫 방문 vs 단골)
C) 주문 패턴 (혼자 vs 그룹)
D) 모두 고려
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

### Question 4
관리자 페르소나에서 구분이 필요한 역할이 있나요?

A) 단일 관리자 역할 (매장 사장님이 모든 관리 수행)
B) 매장 사장님 + 직원 (권한 차이 있음)
C) 매장 사장님만 (직원은 시스템 사용 안 함)
D) Other (please describe after [Answer]: tag below)

[Answer]: B

---

### Question 5
스토리 우선순위 기준은 무엇을 사용하시겠습니까?

A) MoSCoW (Must/Should/Could/Won't)
B) High/Medium/Low
C) 숫자 (1-5)
D) 우선순위 없이 동일 취급
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

### Question 6
에러 시나리오 및 edge case를 별도 스토리로 분리하시겠습니까?

A) 별도 스토리로 분리 (예: "네트워크 오류 시 주문 실패 처리")
B) 해당 기능 스토리의 acceptance criteria에 포함
C) 주요 에러만 별도 스토리, 나머지는 acceptance criteria에 포함
D) Other (please describe after [Answer]: tag below)

[Answer]: C

---

## Execution Plan

### Part 1: Personas 생성
- [x] 고객 페르소나 정의
- [x] 관리자 페르소나 정의
- [x] 페르소나별 목표, 동기, 불편사항 정리

### Part 2: User Stories 생성
- [x] 고객용 스토리 작성 (인증, 메뉴, 장바구니, 주문, 주문내역)
- [x] 관리자용 스토리 작성 (인증, 주문 모니터링, 테이블 관리, 메뉴 관리)
- [x] 각 스토리에 acceptance criteria 추가
- [x] INVEST 기준 검증

### Part 3: Story Map
- [x] 스토리 우선순위 지정
- [x] 페르소나-스토리 매핑
- [x] MVP 범위 확인

---

**작성 완료 후 "완료" 또는 "done"이라고 알려주세요.**
