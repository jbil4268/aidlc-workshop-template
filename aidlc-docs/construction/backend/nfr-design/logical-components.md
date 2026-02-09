# Logical Components - Backend API Server

## Overview
Backend API Server의 논리적 컴포넌트와 인프라 요소를 정의합니다. 로컬 개발 환경이므로 복잡한 인프라는 불필요하며, 핵심 컴포넌트만 포함합니다.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Customer   │  │    Admin     │  │   Admin      │      │
│  │   Frontend   │  │   Frontend   │  │  WebSocket   │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
          │ HTTP/REST        │ HTTP/REST        │ WebSocket
          │                  │                  │
┌─────────┼──────────────────┼──────────────────┼─────────────┐
│         ▼                  ▼                  ▼              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              FastAPI Application                      │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │         CORS Middleware                        │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │    Global Exception Handler                    │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  │                                                        │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │   │
│  │  │  Customer   │  │    Admin    │  │  WebSocket  │  │   │
│  │  │   Routers   │  │   Routers   │  │   Manager   │  │   │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  │   │
│  │         │                │                │          │   │
│  │         └────────────────┼────────────────┘          │   │
│  │                          ▼                           │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │      Authentication (JWT Depends)              │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  │                          │                           │   │
│  │                          ▼                           │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │      Database Session (Depends)                │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  │                          │                           │   │
│  │                          ▼                           │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │         SQLAlchemy Models                      │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
│                           │                                  │
│                           ▼                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              SQLite Database                          │   │
│  │              (table_order.db)                         │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              File System                              │   │
│  │              (uploads/)                               │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. FastAPI Application
**Type**: Application Framework
**Purpose**: HTTP 서버 및 API 엔드포인트 제공

**Responsibilities**:
- HTTP 요청 라우팅
- WebSocket 연결 관리
- 미들웨어 실행
- 자동 API 문서 생성

**Configuration**:
```python
from fastapi import FastAPI

app = FastAPI(
    title="Table Order API",
    description="테이블오더 서비스 Backend API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
```

---

### 2. CORS Middleware
**Type**: Middleware
**Purpose**: Cross-Origin Resource Sharing 처리

**Configuration**:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 환경
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Rationale**:
- Frontend와 Backend가 다른 포트에서 실행
- 개발 환경이므로 모든 origin 허용

---

### 3. Global Exception Handler
**Type**: Error Handler
**Purpose**: 전역 에러 처리 및 일관된 응답 형식

**Implementation**:
```python
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": str(exc)
            }
        }
    )
```

---

### 4. Authentication Component
**Type**: Security Component
**Purpose**: JWT 토큰 검증 및 인증 정보 추출

**Sub-components**:
- `verify_token()`: JWT 토큰 검증
- `get_current_table()`: 테이블 인증 정보 추출
- `get_current_admin()`: 관리자 인증 정보 추출

**Dependencies**:
- PyJWT: JWT 토큰 처리
- passlib: 비밀번호 해싱

---

### 5. Database Session Manager
**Type**: Data Access Component
**Purpose**: SQLAlchemy 세션 생성 및 관리

**Implementation**:
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "sqlite:///./table_order.db",
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Lifecycle**:
- 요청 시작: 세션 생성
- 요청 처리: 세션 사용
- 요청 종료: 세션 정리 (자동)

---

### 6. WebSocket Connection Manager
**Type**: Real-time Communication Component
**Purpose**: WebSocket 연결 관리 및 브로드캐스트

**Responsibilities**:
- 매장별 연결 그룹 관리
- 신규 주문 이벤트 브로드캐스트
- 주문 상태 변경 이벤트 브로드캐스트
- 주문 삭제 이벤트 브로드캐스트

**Data Structure**:
```python
{
    "store_id_1": [websocket1, websocket2],
    "store_id_2": [websocket3]
}
```

---

### 7. API Routers
**Type**: Controller Components
**Purpose**: API 엔드포인트 정의 및 요청 처리

**Router Groups**:
- **Customer Routers**:
  - `customer_auth.py`: 테이블 로그인
  - `customer_menu.py`: 메뉴 조회
  - `customer_order.py`: 주문 생성 및 조회
  
- **Admin Routers**:
  - `admin_auth.py`: 관리자 로그인
  - `admin_order.py`: 주문 관리
  - `admin_table.py`: 테이블 관리
  - `admin_menu.py`: 메뉴 관리
  - `admin_category.py`: 카테고리 관리

**Router Registration**:
```python
app.include_router(customer_auth.router, prefix="/api/customer/auth", tags=["Customer Auth"])
app.include_router(admin_auth.router, prefix="/api/admin/auth", tags=["Admin Auth"])
# ...
```

---

### 8. SQLAlchemy Models
**Type**: Data Models
**Purpose**: 데이터베이스 엔티티 정의

**Models**:
- `Store`: 매장
- `Table`: 테이블
- `TableSession`: 테이블 세션
- `Category`: 카테고리
- `Menu`: 메뉴
- `Order`: 주문
- `OrderItem`: 주문 항목
- `Admin`: 관리자
- `OrderHistory`: 주문 이력

**Relationships**:
- One-to-Many: Store → Table, Store → Menu, Order → OrderItem
- Many-to-One: Menu → Category, Order → TableSession

---

### 9. Pydantic Schemas
**Type**: Data Transfer Objects (DTO)
**Purpose**: API 요청/응답 데이터 검증 및 직렬화

**Schema Groups**:
- `auth.py`: 로그인 요청/응답
- `menu.py`: 메뉴 CRUD 스키마
- `order.py`: 주문 생성/조회 스키마
- `table.py`: 테이블 관리 스키마

**Example**:
```python
class OrderCreateSchema(BaseModel):
    session_id: UUID
    items: List[OrderItemSchema]
    tip_rate: int = Field(ge=0, le=20)
```

---

### 10. Utility Components
**Type**: Helper Components
**Purpose**: 공통 유틸리티 함수

**Utilities**:
- `security.py`: JWT 토큰 생성/검증, 비밀번호 해싱
- `validators.py`: 커스텀 검증 함수
- `helpers.py`: 주문 번호 생성, 팁 계산 등

---

## Infrastructure Components

### 1. SQLite Database
**Type**: Relational Database
**Purpose**: 데이터 영속성

**Configuration**:
- File: `table_order.db`
- Location: 프로젝트 루트
- Connection: SQLAlchemy ORM

**Characteristics**:
- 단일 파일 DB
- 설정 불필요
- 로컬 개발 환경 적합

**Limitations**:
- 동시 쓰기 제한
- 확장성 제한 (프로덕션 부적합)

---

### 2. File System (Uploads)
**Type**: File Storage
**Purpose**: 메뉴 이미지 저장

**Configuration**:
- Directory: `uploads/`
- Path Structure: `/uploads/{menu_id}.{ext}`
- Max Size: 10MB per file
- Allowed Formats: JPEG, PNG, WebP

**Access**:
- Static file serving: FastAPI StaticFiles
- URL: `http://localhost:8000/uploads/{menu_id}.{ext}`

**Implementation**:
```python
from fastapi.staticfiles import StaticFiles

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
```

---

### 3. Uvicorn ASGI Server
**Type**: Application Server
**Purpose**: FastAPI 애플리케이션 실행

**Configuration**:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Features**:
- 비동기 지원
- WebSocket 지원
- Auto-reload (개발 시)
- 빠른 성능

---

### 4. Python Logging
**Type**: Logging System
**Purpose**: 애플리케이션 로그 기록

**Configuration**:
```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
```

**Output**: Console (stdout)

---

## Component Interactions

### 1. Customer Order Creation Flow
```
Customer Frontend
    ↓ POST /api/customer/orders
FastAPI Router (customer_order.py)
    ↓ Depends(get_current_table)
Authentication Component
    ↓ verify JWT
    ↓ Depends(get_db)
Database Session Manager
    ↓ provide session
Router Business Logic
    ↓ validate session
    ↓ validate menus
    ↓ create order
    ↓ calculate amounts
SQLAlchemy Models
    ↓ save to DB
SQLite Database
    ↓ commit
WebSocket Manager
    ↓ broadcast new_order
Admin Frontend (WebSocket)
    ↓ receive event
```

### 2. Admin Order Status Update Flow
```
Admin Frontend
    ↓ PATCH /api/admin/orders/{id}/status
FastAPI Router (admin_order.py)
    ↓ Depends(get_current_admin)
Authentication Component
    ↓ verify JWT (admin role)
    ↓ Depends(get_db)
Database Session Manager
    ↓ provide session
Router Business Logic
    ↓ update order status
SQLAlchemy Models
    ↓ save to DB
SQLite Database
    ↓ commit
WebSocket Manager
    ↓ broadcast order_updated
Admin Frontend (WebSocket)
    ↓ receive event
```

### 3. Menu Image Upload Flow
```
Admin Frontend
    ↓ POST /api/admin/menus/upload-image
FastAPI Router (admin_menu.py)
    ↓ Depends(get_current_admin)
Authentication Component
    ↓ verify JWT (admin role)
Router Business Logic
    ↓ validate file size
    ↓ validate file format
    ↓ save to uploads/
File System
    ↓ write file
Router
    ↓ return image_url
Admin Frontend
    ↓ use image_url in menu form
```

---

## Deployment Components

### 1. Environment Variables (.env)
**Type**: Configuration
**Purpose**: 환경별 설정 관리

**Variables**:
```
DATABASE_URL=sqlite:///./table_order.db
SECRET_KEY=your-secret-key-here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
STORE_IDENTIFIER=store001
```

**Loading**: pydantic-settings

---

### 2. Database Migration (Alembic)
**Type**: Schema Management
**Purpose**: 데이터베이스 스키마 버전 관리

**Commands**:
```bash
# 마이그레이션 생성
alembic revision --autogenerate -m "Create tables"

# 마이그레이션 적용
alembic upgrade head
```

---

### 3. Seed Data Script
**Type**: Initialization
**Purpose**: 초기 데이터 생성

**Responsibilities**:
- 기본 매장 생성
- 관리자 계정 생성
- "미분류" 카테고리 생성

**Execution**: 서버 시작 시 자동 실행 (선택)

---

## Component Summary

| Component | Type | Purpose | Technology |
|-----------|------|---------|------------|
| FastAPI App | Framework | HTTP/WebSocket 서버 | FastAPI |
| CORS Middleware | Middleware | CORS 처리 | FastAPI |
| Exception Handler | Error Handler | 전역 에러 처리 | FastAPI |
| Authentication | Security | JWT 검증 | PyJWT |
| DB Session | Data Access | 세션 관리 | SQLAlchemy |
| WebSocket Manager | Real-time | 연결 관리 | FastAPI |
| Routers | Controllers | API 엔드포인트 | FastAPI |
| Models | Data Models | 엔티티 정의 | SQLAlchemy |
| Schemas | DTOs | 데이터 검증 | Pydantic |
| Utilities | Helpers | 공통 함수 | Python |
| SQLite | Database | 데이터 저장 | SQLite |
| File System | Storage | 이미지 저장 | OS |
| Uvicorn | Server | ASGI 서버 | Uvicorn |
| Logging | Monitoring | 로그 기록 | Python logging |

---

## Scalability Considerations

### Current State (로컬 개발)
- 단일 서버 인스턴스
- SQLite 데이터베이스
- 로컬 파일 시스템

### Future Enhancements (프로덕션)
- PostgreSQL/MySQL 전환
- Redis (캐싱, WebSocket Pub/Sub)
- CDN (이미지 서빙)
- Load Balancer (다중 인스턴스)
- Monitoring (APM, 로그 집계)

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-09  
**Status**: Draft
