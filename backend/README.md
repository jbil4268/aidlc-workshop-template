# Table Order Backend API Server

테이블오더 서비스의 백엔드 API 서버입니다.

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite + SQLAlchemy ORM
- **Migration**: Alembic
- **Validation**: Pydantic
- **Authentication**: JWT (PyJWT)
- **Password Hashing**: passlib (bcrypt)
- **Testing**: pytest
- **Server**: uvicorn

## Project Structure

```
backend/
├── app/
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic services
│   ├── routers/         # API endpoints
│   ├── utils/           # Utilities (auth, errors, websocket)
│   ├── database.py      # Database connection
│   ├── config.py        # Configuration
│   └── main.py          # FastAPI app
├── tests/               # Test files
├── uploads/             # Uploaded menu images
├── alembic/             # Database migrations
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── README.md            # This file
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and update values:

```bash
cp .env.example .env
```

### 3. Initialize Database

```bash
# Run migrations
alembic upgrade head

# (Optional) Seed initial data
python -m app.seed
```

### 4. Run Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server will be available at: http://localhost:8000

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run all tests:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app --cov-report=html
```

## Development

### Database Migrations

Create a new migration:

```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:

```bash
alembic upgrade head
```

Rollback:

```bash
alembic downgrade -1
```

## License

MIT
