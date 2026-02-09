# Backend Code Structure

## Directory Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration (pydantic-settings)
│   ├── database.py             # Database connection and session
│   │
│   ├── models/                 # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── store.py
│   │   ├── table.py
│   │   ├── table_session.py
│   │   ├── category.py
│   │   ├── menu.py
│   │   ├── order.py
│   │   ├── order_item.py
│   │   ├── admin.py
│   │   └── order_history.py
│   │
│   ├── schemas/                # Pydantic schemas (request/response)
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── menu.py
│   │   ├── order.py
│   │   └── table.py
│   │
│   ├── services/               # Business logic services (TDD)
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── table_session_service.py
│   │   └── order_service.py
│   │
│   ├── routers/                # API route handlers
│   │   ├── __init__.py
│   │   ├── customer_auth.py
│   │   ├── customer_menu.py
│   │   ├── customer_order.py
│   │   ├── admin_auth.py
│   │   ├── admin_order.py
│   │   ├── admin_table.py
│   │   ├── admin_menu.py
│   │   ├── admin_category.py
│   │   └── websocket.py
│   │
│   └── utils/                  # Utilities
│       ├── __init__.py
│       ├── errors.py           # Custom exception classes
│       ├── dependencies.py     # Dependency injection functions
│       └── websocket.py        # WebSocket connection manager
│
├── tests/                      # Test files
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   ├── test_auth_service.py
│   ├── test_table_session_service.py
│   └── test_order_service.py
│
├── alembic/                    # Database migrations
│   ├── versions/
│   │   └── 001_initial_schema.py
│   ├── env.py
│   ├── script.py.mako
│   └── README
│
├── uploads/                    # Uploaded menu images
├── alembic.ini                 # Alembic configuration
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
└── README.md                   # Project documentation
```

## Layer Architecture

### 1. API Layer (routers/)
- Handles HTTP requests and responses
- Input validation using Pydantic schemas
- Calls service layer for business logic
- Returns appropriate HTTP status codes

### 2. Service Layer (services/)
- Contains core business logic
- Implemented with TDD (Test-Driven Development)
- Independent of HTTP/API concerns
- Raises custom exceptions for error cases

### 3. Data Layer (models/)
- SQLAlchemy ORM models
- Database schema definitions
- Relationships between entities

### 4. Schema Layer (schemas/)
- Pydantic models for request/response validation
- Data serialization/deserialization
- Type safety

## Key Components

### AuthService
- Password hashing (bcrypt)
- JWT token creation and verification
- Token expiration handling

### TableSessionService
- Session lifecycle management
- Active session tracking
- Session ending and cleanup

### OrderService
- Order number generation (daily sequential)
- Tip calculation with rounding
- Order creation with validation
- Order status updates with history

### ConnectionManager (WebSocket)
- Manages WebSocket connections per store
- Broadcasts order updates to admin clients
- Handles connection/disconnection

## Design Patterns

### Dependency Injection
- Database sessions injected via `Depends(get_db)`
- Authentication via `Depends(get_current_admin)`
- Promotes testability and loose coupling

### Repository Pattern
- Services use SQLAlchemy ORM for data access
- Business logic separated from data access

### Exception Handling
- Custom exception classes for business errors
- Global exception handlers in main.py
- Consistent error responses

### Service Layer Pattern
- Business logic isolated in service classes
- Services are stateless (except db session)
- Easy to test with mocks

## Testing Strategy

### TDD Approach
- Tests written before implementation
- RED-GREEN-REFACTOR cycle
- 30 test cases for core business logic

### Test Coverage
- AuthService: 9 tests
- TableSessionService: 7 tests
- OrderService: 14 tests

### Test Fixtures
- In-memory SQLite database
- Fresh database for each test
- Isolated test environment

## Configuration

### Environment Variables
- `DATABASE_URL` - Database connection string
- `JWT_SECRET_KEY` - Secret key for JWT signing
- `JWT_ALGORITHM` - JWT algorithm (HS256)
- `JWT_EXPIRE_MINUTES` - Token expiration time
- `UPLOAD_DIR` - Directory for uploaded files
- `CORS_ORIGINS` - Allowed CORS origins

### Settings Management
- Uses pydantic-settings for type-safe configuration
- Loads from .env file
- Provides defaults for development

## Database

### ORM: SQLAlchemy
- Declarative base for models
- Relationship definitions
- Automatic schema generation

### Migrations: Alembic
- Version-controlled schema changes
- Upgrade/downgrade support
- Auto-generation from models

### Database: SQLite
- File-based database for development
- Easy setup, no server required
- Can be replaced with PostgreSQL/MySQL for production

## API Documentation

### Automatic Documentation
- Swagger UI at `/docs`
- ReDoc at `/redoc`
- Generated from Pydantic schemas and route definitions

### OpenAPI Specification
- Automatically generated
- Includes request/response schemas
- Authentication requirements documented
