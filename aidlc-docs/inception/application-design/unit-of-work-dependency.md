# Unit of Work Dependencies

## Dependency Matrix

| Unit | Depends On | Communication |
|------|-----------|---------------|
| Backend API Server | - (독립) | - |
| Customer Frontend | Backend API Server | REST API (HTTP) |
| Admin Frontend | Backend API Server | REST API (HTTP) + WebSocket |

## Dependency Details

### Backend API Server (Unit 1)
- **External Dependencies**: 없음 (독립 실행)
- **Database**: SQLite (내장, 별도 서버 불필요)
- **Build Order**: 1번째 (다른 Unit의 기반)

### Customer Frontend (Unit 2)
- **Depends On**: Backend API Server (REST API)
- **Communication**: HTTP REST API 호출
- **Build Order**: Backend 이후 (API 엔드포인트 필요)
- **Offline Capability**: 장바구니는 LocalStorage로 오프라인 유지

### Admin Frontend (Unit 3)
- **Depends On**: Backend API Server (REST API + WebSocket)
- **Communication**: HTTP REST API + WebSocket 실시간 통신
- **Build Order**: Backend 이후 (API + WebSocket 필요)

## Build & Development Order

```
Phase 1: Backend API Server
  - DB 모델 및 마이그레이션
  - REST API 엔드포인트
  - WebSocket 서버
  - 인증 미들웨어
  - Unit Tests

Phase 2: Customer Frontend (Backend 완료 후)
  - 인증 모듈
  - 메뉴 탐색
  - 장바구니
  - 주문 생성

Phase 3: Admin Frontend (Backend 완료 후, Phase 2와 병렬 가능)
  - 관리자 인증
  - 실시간 대시보드
  - 테이블 관리
  - 메뉴 관리
```

## Integration Points

| Integration | Source | Target | Protocol | Data |
|------------|--------|--------|----------|------|
| 메뉴 조회 | Customer FE | Backend | REST GET | Menu[] |
| 주문 생성 | Customer FE | Backend | REST POST | Order |
| 주문 내역 | Customer FE | Backend | REST GET | Order[] |
| 관리자 인증 | Admin FE | Backend | REST POST | JWT |
| 주문 모니터링 | Backend | Admin FE | WebSocket | OrderEvent |
| 주문 상태 변경 | Admin FE | Backend | REST PATCH | OrderStatus |
| 테이블 관리 | Admin FE | Backend | REST | Table |
| 메뉴 관리 | Admin FE | Backend | REST + File | Menu |
