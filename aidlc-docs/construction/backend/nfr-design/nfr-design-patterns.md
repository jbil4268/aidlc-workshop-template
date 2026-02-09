# NFR Design Patterns - Backend API Server

## Overview
Backend API Server의 NFR Requirements를 충족하기 위한 디자인 패턴을 정의합니다.

---

## 1. Error Handling Pattern

### Pattern: Global Exception Handler
**Selected**: FastAPI Global Exception Handler

**Implementation**:
```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": str(exc)
            }
        }
    )

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "code": "INVALID_INPUT",
                "message": str(exc)
            }
        }
    )
```

**Benefits**:
- 일관된 에러 응답 형식
- 중복 코드 제거
- 중앙 집중식 에러 로깅

**Error Response Format**:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {}
  }
}
```

---

## 2. Authentication Pattern

### Pattern: Dependency Injection (FastAPI Depends)
**Selected**: FastAPI Depends를 사용한 인증 미들웨어

**Implementation**:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """JWT 토큰 검증"""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

def get_current_table(payload: dict = Depends(verify_token)):
    """테이블 인증 정보 추출"""
    if "table_id" not in payload:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token type"
        )
    return payload

def get_current_admin(payload: dict = Depends(verify_token)):
    """관리자 인증 정보 추출"""
    if payload.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return payload

# 사용 예시
@app.get("/api/customer/orders")
async def get_orders(table_info: dict = Depends(get_current_table)):
    # table_info에 table_id, session_id 등 포함
    pass

@app.get("/api/admin/orders")
async def get_admin_orders(admin_info: dict = Depends(get_current_admin)):
    # admin_info에 admin_id, store_id 등 포함
    pass
```

**Benefits**:
- 선언적 인증 (라우터 함수 시그니처에 명시)
- 재사용 가능
- 테스트 용이 (Depends 오버라이드 가능)

---

## 3. Database Session Management Pattern

### Pattern: Dependency Injection
**Selected**: FastAPI Depends를 사용한 세션 주입

**Implementation**:
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

engine = create_engine("sqlite:///./table_order.db")
SessionLocal = sessionmaker(bind=engine)

def get_db():
    """데이터베이스 세션 생성 및 정리"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 사용 예시
@app.post("/api/customer/orders")
async def create_order(
    order_data: OrderCreateSchema,
    db: Session = Depends(get_db),
    table_info: dict = Depends(get_current_table)
):
    try:
        order = Order(**order_data.dict())
        db.add(order)
        db.commit()
        db.refresh(order)
        return order
    except Exception as e:
        db.rollback()
        raise
```

**Benefits**:
- 자동 세션 정리 (finally 블록)
- 요청당 세션 격리
- 테스트 시 세션 오버라이드 가능

---

## 4. WebSocket Connection Management Pattern

### Pattern: Connection Manager
**Selected**: 매장별 연결 그룹 관리

**Implementation**:
```python
from fastapi import WebSocket
from typing import Dict, List

class ConnectionManager:
    def __init__(self):
        # store_id -> List[WebSocket]
        self.active_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, store_id: str):
        """WebSocket 연결 추가"""
        await websocket.accept()
        if store_id not in self.active_connections:
            self.active_connections[store_id] = []
        self.active_connections[store_id].append(websocket)
    
    def disconnect(self, websocket: WebSocket, store_id: str):
        """WebSocket 연결 제거"""
        if store_id in self.active_connections:
            self.active_connections[store_id].remove(websocket)
            if not self.active_connections[store_id]:
                del self.active_connections[store_id]
    
    async def broadcast(self, store_id: str, message: dict):
        """매장별 브로드캐스트"""
        if store_id in self.active_connections:
            for connection in self.active_connections[store_id]:
                await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/{store_id}")
async def websocket_endpoint(websocket: WebSocket, store_id: str):
    await manager.connect(websocket, store_id)
    try:
        while True:
            data = await websocket.receive_text()
            # 메시지 처리
    except WebSocketDisconnect:
        manager.disconnect(websocket, store_id)
```

**Benefits**:
- 매장별 연결 격리
- 효율적인 브로드캐스트
- 연결 상태 관리 중앙화

---

## 5. Business Logic Layer Pattern

### Pattern: Thin Controllers
**Selected**: 라우터에 직접 비즈니스 로직 작성

**Rationale**:
- 소규모 프로젝트, 복잡도 낮음
- Service Layer 추가 시 오버엔지니어링
- 빠른 개발 속도

**Implementation**:
```python
@app.post("/api/customer/orders")
async def create_order(
    order_data: OrderCreateSchema,
    db: Session = Depends(get_db),
    table_info: dict = Depends(get_current_table)
):
    """주문 생성 - 비즈니스 로직 포함"""
    # 1. 세션 검증
    session = db.query(TableSession).filter(
        TableSession.session_id == table_info["session_id"],
        TableSession.is_active == True
    ).first()
    if not session:
        raise HTTPException(400, "Session not active")
    
    # 2. 메뉴 검증
    for item in order_data.items:
        menu = db.query(Menu).filter(
            Menu.menu_id == item.menu_id,
            Menu.is_available == True
        ).first()
        if not menu:
            raise HTTPException(400, f"Menu not available: {item.menu_id}")
    
    # 3. 주문 생성
    order = Order(
        session_id=session.session_id,
        table_id=table_info["table_id"],
        store_id=table_info["store_id"],
        order_number=generate_order_number(db, table_info["store_id"]),
        tip_rate=order_data.tip_rate
    )
    
    # 4. 주문 항목 생성 및 금액 계산
    subtotal = 0
    for item_data in order_data.items:
        menu = db.query(Menu).get(item_data.menu_id)
        item = OrderItem(
            menu_id=menu.menu_id,
            menu_name=menu.menu_name,
            quantity=item_data.quantity,
            unit_price=menu.price,
            subtotal=menu.price * item_data.quantity
        )
        order.items.append(item)
        subtotal += item.subtotal
    
    order.subtotal_amount = subtotal
    order.tip_amount = round(subtotal * order.tip_rate / 100)
    order.total_amount = order.subtotal_amount + order.tip_amount
    
    # 5. 저장
    db.add(order)
    db.commit()
    db.refresh(order)
    
    # 6. WebSocket 브로드캐스트
    await manager.broadcast(table_info["store_id"], {
        "event": "new_order",
        "data": order.to_dict()
    })
    
    return order
```

**Trade-offs**:
- 장점: 간단, 빠른 개발, 코드 추적 용이
- 단점: 라우터 함수가 길어질 수 있음, 재사용성 낮음

**Future Refactoring**:
- 프로젝트 복잡도 증가 시 Service Layer로 리팩토링 고려

---

## 6. File Upload Pattern

### Pattern: Synchronous Processing
**Selected**: 동기 처리 (업로드 완료 후 응답)

**Implementation**:
```python
import os
import shutil
from fastapi import UploadFile, File, HTTPException

UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}

@app.post("/api/admin/menus/upload-image")
async def upload_image(
    file: UploadFile = File(...),
    admin_info: dict = Depends(get_current_admin)
):
    # 1. 파일 크기 검증
    file.file.seek(0, 2)  # 파일 끝으로 이동
    file_size = file.file.tell()
    file.file.seek(0)  # 파일 시작으로 복귀
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(400, "File size exceeds 10MB")
    
    # 2. 파일 형식 검증
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "Invalid file format")
    
    # 3. 파일 저장
    menu_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{menu_id}.{ext}")
    
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 4. URL 반환
    image_url = f"/uploads/{menu_id}.{ext}"
    return {"image_url": image_url}
```

**Benefits**:
- 간단한 구현
- 에러 처리 용이
- 파일 크기 작음 (10MB 이하)

**Trade-offs**:
- 대용량 파일 시 블로킹 가능 (현재는 문제 없음)

---

## 7. Transaction Management Pattern

### Pattern: Explicit Commit
**Selected**: 명시적 commit/rollback

**Implementation**:
```python
@app.post("/api/admin/tables/{table_id}/session/end")
async def end_session(
    table_id: str,
    db: Session = Depends(get_db),
    admin_info: dict = Depends(get_current_admin)
):
    try:
        # 1. 테이블 조회
        table = db.query(Table).get(table_id)
        if not table:
            raise HTTPException(404, "Table not found")
        
        # 2. 활성 세션 조회
        session = db.query(TableSession).get(table.current_session_id)
        if not session:
            raise HTTPException(400, "No active session")
        
        # 3. 주문 아카이빙
        orders = db.query(Order).filter(Order.session_id == session.session_id).all()
        for order in orders:
            history = OrderHistory(
                order_id=order.order_id,
                session_id=session.session_id,
                table_id=table.table_id,
                store_id=table.store_id,
                order_number=order.order_number,
                order_data=order.to_json(),
                archived_at=datetime.utcnow()
            )
            db.add(history)
        
        # 4. 세션 종료
        session.end_time = datetime.utcnow()
        session.is_active = False
        
        # 5. 테이블 리셋
        table.current_session_id = None
        
        # 6. 커밋
        db.commit()
        
        return {"message": "Session ended successfully"}
    
    except Exception as e:
        db.rollback()
        raise
```

**Benefits**:
- 명확한 트랜잭션 경계
- 에러 발생 시 자동 롤백
- 디버깅 용이

---

## 8. Logging Pattern

### Pattern: Plain Text Logging
**Selected**: 일반 텍스트 로깅

**Implementation**:
```python
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

# 사용 예시
@app.post("/api/customer/orders")
async def create_order(...):
    logger.info(f"Creating order for table {table_info['table_id']}")
    
    try:
        # 주문 생성 로직
        order = ...
        logger.info(f"Order created: {order.order_number}")
        return order
    except Exception as e:
        logger.error(f"Failed to create order: {str(e)}", exc_info=True)
        raise

# 에러 핸들러에서 로깅
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(...)
```

**Log Levels**:
- INFO: 주문 생성, 상태 변경, 세션 시작/종료, 로그인
- ERROR: 예외 발생, 데이터베이스 에러, 검증 실패

**Benefits**:
- 읽기 쉬움 (개발 환경)
- 설정 간단
- 표준 라이브러리 사용

---

## 9. Validation Pattern

### Pattern: Pydantic Schemas
**Selected**: Pydantic 모델을 사용한 입력 검증

**Implementation**:
```python
from pydantic import BaseModel, Field, validator
from typing import List
from uuid import UUID

class OrderItemSchema(BaseModel):
    menu_id: UUID
    quantity: int = Field(gt=0, description="Quantity must be greater than 0")

class OrderCreateSchema(BaseModel):
    session_id: UUID
    items: List[OrderItemSchema] = Field(min_items=1)
    tip_rate: int = Field(ge=0, le=20, description="Tip rate must be 0-20")
    
    @validator('tip_rate')
    def validate_tip_rate(cls, v):
        if v not in [0, 5, 10, 15, 20]:
            raise ValueError('tip_rate must be 0, 5, 10, 15, or 20')
        return v

# FastAPI가 자동으로 검증
@app.post("/api/customer/orders")
async def create_order(order_data: OrderCreateSchema, ...):
    # order_data는 이미 검증됨
    pass
```

**Benefits**:
- 자동 검증
- 자동 API 문서 생성
- 타입 안전성

---

## 10. API Response Pattern

### Pattern: Consistent JSON Response
**Selected**: 일관된 JSON 응답 형식

**Success Response**:
```json
{
  "data": {
    "order_id": "uuid",
    "order_number": "#001",
    "total_amount": 16500
  }
}
```

**Error Response**:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {}
  }
}
```

**Implementation**:
```python
from pydantic import BaseModel

class SuccessResponse(BaseModel):
    data: dict

class ErrorResponse(BaseModel):
    error: dict

# 사용 예시
@app.get("/api/customer/orders/{order_id}")
async def get_order(order_id: str, ...):
    order = db.query(Order).get(order_id)
    if not order:
        raise HTTPException(404, "Order not found")
    return {"data": order.to_dict()}
```

---

## Pattern Summary

| Pattern | Implementation | Rationale |
|---------|---------------|-----------|
| Error Handling | Global Exception Handler | 일관성, 중앙 집중 |
| Authentication | FastAPI Depends | 선언적, 재사용 가능 |
| DB Session | Dependency Injection | 자동 정리, 격리 |
| WebSocket | Connection Manager | 매장별 격리, 효율성 |
| Business Logic | Thin Controllers | 간단, 빠른 개발 |
| File Upload | Synchronous | 간단, 파일 작음 |
| Transaction | Explicit Commit | 명확한 경계 |
| Logging | Plain Text | 읽기 쉬움 |
| Validation | Pydantic | 자동, 타입 안전 |
| API Response | Consistent JSON | 일관성 |

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-09  
**Status**: Draft
