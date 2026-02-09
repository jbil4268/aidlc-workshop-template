# Tech Stack Decisions - Backend API Server

## Overview
Backend API Server 구현을 위한 기술 스택 결정 사항을 문서화합니다.

---

## Core Framework

### Decision: FastAPI
**Selected**: FastAPI 0.104+ (최신 안정 버전)

**Rationale**:
- **비동기 지원**: WebSocket 네이티브 지원, 비동기 처리 우수
- **빠른 성능**: Starlette 기반, 높은 처리량
- **자동 API 문서**: Swagger/OpenAPI 자동 생성
- **타입 힌트**: Pydantic 통합, 타입 안전성
- **간결한 코드**: 보일러플레이트 최소화

**Alternatives Considered**:
- Django + DRF: 무겁고 복잡, WebSocket 지원 약함
- Flask: 비동기 지원 약함, 수동 설정 많음

**Dependencies**:
```
fastapi==0.104.1
uvicorn[standard]==0.24.0  # ASGI 서버
```

---

## Database

### Decision: SQLite + SQLAlchemy
**Selected**: 
- SQLite 3.35+
- SQLAlchemy 2.0+

**Rationale**:
- **SQLite**: 로컬 개발 환경, 설정 불필요, 단일 파일 DB
- **SQLAlchemy**: ORM, 타입 안전성, 마이그레이션 지원

**Configuration**:
- Connection Pool: 기본 설정 사용 (pool 없음)
- Database URL: `sqlite:///./table_order.db`
- Check same thread: False (FastAPI 비동기 지원)

**Dependencies**:
```
sqlalchemy==2.0.23
```

**Future Migration Path**:
- PostgreSQL 또는 MySQL로 전환 가능 (SQLAlchemy 덕분)

---

## Database Migration

### Decision: Alembic
**Selected**: Alembic 1.12+

**Rationale**:
- SQLAlchemy 공식 마이그레이션 도구
- 자동 마이그레이션 스크립트 생성
- 버전 관리 및 롤백 지원

**Usage**:
```bash
# 초기화
alembic init alembic

# 마이그레이션 생성
alembic revision --autogenerate -m "Create tables"

# 마이그레이션 적용
alembic upgrade head
```

**Dependencies**:
```
alembic==1.12.1
```

---

## Data Validation

### Decision: Pydantic
**Selected**: Pydantic 2.5+ (FastAPI 기본 포함)

**Rationale**:
- FastAPI 네이티브 통합
- 타입 힌트 기반 검증
- 자동 JSON 직렬화/역직렬화
- 명확한 에러 메시지

**Usage**:
```python
from pydantic import BaseModel, Field

class OrderCreateSchema(BaseModel):
    session_id: UUID
    items: List[OrderItemSchema]
    tip_rate: int = Field(ge=0, le=20)
```

**Dependencies**:
- FastAPI에 포함됨 (별도 설치 불필요)

---

## Authentication

### Decision: JWT + PyJWT
**Selected**: 
- PyJWT 2.8+
- passlib[bcrypt] 1.7+

**Rationale**:
- **PyJWT**: 경량, 표준 JWT 구현
- **passlib**: bcrypt 해싱, 보안성 우수

**JWT Configuration**:
- Algorithm: HS256
- Expiration: 16시간
- Secret Key: 환경 변수 (SECRET_KEY)

**Dependencies**:
```
PyJWT==2.8.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6  # Form 데이터 파싱
```

---

## WebSocket

### Decision: FastAPI WebSocket
**Selected**: FastAPI 내장 WebSocket

**Rationale**:
- FastAPI 네이티브 지원
- 추가 라이브러리 불필요
- 간단한 구현

**Implementation**:
```python
from fastapi import WebSocket

@app.websocket("/ws/{store_id}")
async def websocket_endpoint(websocket: WebSocket, store_id: str):
    await websocket.accept()
    # ...
```

**Dependencies**:
- FastAPI에 포함됨

---

## Environment Variables

### Decision: Pydantic Settings
**Selected**: pydantic-settings 2.1+

**Rationale**:
- FastAPI 권장 방식
- 타입 안전성
- .env 파일 자동 로드
- 검증 기능

**Usage**:
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    
    class Config:
        env_file = ".env"
```

**Dependencies**:
```
pydantic-settings==2.1.0
python-dotenv==1.0.0  # .env 파일 로드
```

---

## CORS

### Decision: FastAPI CORSMiddleware
**Selected**: FastAPI 내장 CORSMiddleware

**Configuration**:
- 개발 환경: 모든 origin 허용 (*)
- Allow credentials: True
- Allow methods: ["*"]
- Allow headers: ["*"]

**Implementation**:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Dependencies**:
- FastAPI에 포함됨

---

## API Documentation

### Decision: Swagger/OpenAPI
**Selected**: FastAPI 자동 생성 (Swagger UI)

**Rationale**:
- FastAPI 기본 제공
- 자동 생성, 유지보수 불필요
- 인터랙티브 테스트 가능

**Access URLs**:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

**Dependencies**:
- FastAPI에 포함됨

---

## Testing

### Decision: pytest
**Selected**: pytest 7.4+

**Rationale**:
- Python 표준 테스트 프레임워크
- 강력한 fixture 시스템
- 플러그인 생태계 풍부
- FastAPI 공식 권장

**Test Structure**:
```
backend/tests/
  conftest.py          # Fixtures
  test_auth.py
  test_order.py
  test_table.py
  test_menu.py
```

**Dependencies**:
```
pytest==7.4.3
pytest-asyncio==0.21.1  # 비동기 테스트
httpx==0.25.2           # FastAPI 테스트 클라이언트
```

---

## Logging

### Decision: Python logging + uvicorn logging
**Selected**: Python 표준 logging 모듈

**Configuration**:
- Log Level: INFO + ERROR
- Output: Console (stdout)
- Format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`

**Implementation**:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
```

**Dependencies**:
- Python 표준 라이브러리 (별도 설치 불필요)

---

## File Upload

### Decision: FastAPI UploadFile
**Selected**: FastAPI 내장 UploadFile

**Configuration**:
- 최대 크기: 10MB
- 허용 형식: JPEG, PNG, WebP
- 저장 경로: `/uploads/{menu_id}.{ext}` (단순 구조)

**Implementation**:
```python
from fastapi import UploadFile, File

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    # 파일 검증 및 저장
    pass
```

**Dependencies**:
```
python-multipart==0.0.6  # 파일 업로드 지원
aiofiles==23.2.1         # 비동기 파일 I/O
```

---

## ASGI Server

### Decision: Uvicorn
**Selected**: Uvicorn 0.24+ with standard extras

**Rationale**:
- FastAPI 권장 ASGI 서버
- 빠른 성능
- WebSocket 지원
- Auto-reload (개발 시)

**Run Command**:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Dependencies**:
```
uvicorn[standard]==0.24.0
```

---

## Development Tools

### Code Formatting
**Selected**: Black (optional)

**Rationale**:
- 일관된 코드 스타일
- 자동 포매팅

**Dependencies**:
```
black==23.12.0  # Optional
```

---

### Linting
**Selected**: flake8 (optional)

**Rationale**:
- PEP 8 준수 확인
- 코드 품질 향상

**Dependencies**:
```
flake8==6.1.0  # Optional
```

---

## Complete Dependencies List

### requirements.txt
```txt
# Core Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0

# Database
sqlalchemy==2.0.23
alembic==1.12.1

# Authentication
PyJWT==2.8.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Environment Variables
pydantic-settings==2.1.0
python-dotenv==1.0.0

# File Upload
aiofiles==23.2.1

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2

# Development Tools (Optional)
black==23.12.0
flake8==6.1.0
```

---

## Architecture Patterns

### Pattern 1: Layered Architecture
```
app/
  main.py              # FastAPI 앱 진입점
  config.py            # 설정 (pydantic-settings)
  database.py          # SQLAlchemy 연결
  models/              # SQLAlchemy 모델 (Domain Entities)
  schemas/             # Pydantic 스키마 (DTO)
  routers/             # API 라우터 (Controller)
  services/            # 비즈니스 로직 (Service Layer)
  middleware/          # 미들웨어 (인증, 에러 핸들링)
  websocket/           # WebSocket 관리
  utils/               # 유틸리티 (security, validators)
```

### Pattern 2: Dependency Injection
- FastAPI Depends를 사용한 의존성 주입
- Database session, 인증 정보 주입

### Pattern 3: Repository Pattern (Optional)
- 데이터 접근 로직 분리
- 테스트 용이성 향상

---

## Performance Optimizations

### 1. Database Indexes
- domain-entities.md에 정의된 인덱스 적용
- 쿼리 성능 최적화

### 2. Eager Loading
- SQLAlchemy joinedload/selectinload 사용
- N+1 쿼리 방지

### 3. Connection Pooling
- SQLite 기본 설정 사용 (pool 없음)
- 필요 시 pool_size 조정 가능

---

## Security Best Practices

### 1. 환경 변수
- 민감 정보 코드에 포함 금지
- .env 파일 사용, .gitignore에 추가

### 2. 비밀번호 해싱
- bcrypt 사용 (salt rounds: 10)
- 평문 저장 금지

### 3. JWT 보안
- Secret Key 강력하게 설정
- 토큰 만료 시간 설정 (16시간)

### 4. 입력 검증
- Pydantic 스키마로 모든 입력 검증
- SQL Injection 방지 (ORM 사용)

---

## Deployment Considerations

### Development Environment
- 로컬 개발 환경만 지원
- SQLite 데이터베이스
- Uvicorn 개발 서버

### Future Production Considerations
- PostgreSQL/MySQL 전환
- Gunicorn + Uvicorn workers
- HTTPS 적용
- 환경 변수 관리 (AWS Secrets Manager)

---

## Decision Summary

| Category | Technology | Rationale |
|----------|-----------|-----------|
| Framework | FastAPI | 비동기, WebSocket, 자동 문서 |
| Database | SQLite + SQLAlchemy | 로컬 환경, ORM |
| Migration | Alembic | SQLAlchemy 공식 도구 |
| Validation | Pydantic | FastAPI 네이티브 |
| Auth | PyJWT + passlib | 경량, 보안성 |
| WebSocket | FastAPI WebSocket | 내장 지원 |
| Env Vars | pydantic-settings | 타입 안전성 |
| CORS | FastAPI CORSMiddleware | 내장 지원 |
| API Docs | Swagger/OpenAPI | 자동 생성 |
| Testing | pytest | 표준, 강력함 |
| Logging | Python logging | 표준 라이브러리 |
| File Upload | FastAPI UploadFile | 내장 지원 |
| ASGI Server | Uvicorn | FastAPI 권장 |

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-09  
**Status**: Draft
