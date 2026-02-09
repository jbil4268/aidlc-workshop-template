# Build Instructions

## Prerequisites

### System Requirements
- Python 3.9+
- Node.js 18+
- npm 9+

### Tools
- Git
- Code editor (VS Code recommended)

---

## Unit 1: Backend API Server

### 1. Setup Environment

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
# (Default values work for local development)
```

### 3. Initialize Database

```bash
# Run migrations
alembic upgrade head

# (Optional) Seed initial data
# Create a seed script if needed
```

### 4. Run Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Verify**: http://localhost:8000/docs

### 5. Build for Production (Optional)

Backend은 Python 애플리케이션이므로 별도 빌드 불필요.
배포 시 requirements.txt로 의존성 설치.

---

## Unit 2: Customer Frontend

### 1. Setup Environment

```bash
cd customer-frontend

# Install dependencies
npm install
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env file
# VITE_API_URL=http://localhost:8000
```

### 3. Run Development Server

```bash
npm run dev
```

**Verify**: http://localhost:5173

### 4. Build for Production

```bash
npm run build
```

**Output**: `dist/` 폴더에 정적 파일 생성

### 5. Preview Production Build

```bash
npm run preview
```

---

## Unit 3: Admin Frontend

### 1. Setup Environment

```bash
cd admin-frontend

# Install dependencies
npm install
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env file
# VITE_API_URL=http://localhost:8000
```

### 3. Run Development Server

```bash
npm run dev
```

**Verify**: http://localhost:5174

### 4. Build for Production

```bash
npm run build
```

**Output**: `dist/` 폴더에 정적 파일 생성

### 5. Preview Production Build

```bash
npm run preview
```

---

## Running All Units Together

### Terminal 1: Backend
```bash
cd backend
venv\Scripts\activate  # Windows
uvicorn app.main:app --reload
```

### Terminal 2: Customer Frontend
```bash
cd customer-frontend
npm run dev
```

### Terminal 3: Admin Frontend
```bash
cd admin-frontend
npm run dev
```

### Access Points
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Customer App: http://localhost:5173
- Admin App: http://localhost:5174

---

## Troubleshooting

### Backend Issues

**Port already in use**:
```bash
# Change port in command
uvicorn app.main:app --reload --port 8001
```

**Database errors**:
```bash
# Reset database
rm table_order.db
alembic upgrade head
```

**Import errors**:
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend Issues

**Port already in use**:
```bash
# Vite will automatically use next available port
# Or specify in vite.config.js
```

**Module not found**:
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Build errors**:
```bash
# Clear Vite cache
rm -rf node_modules/.vite
npm run build
```

---

## Production Deployment (Optional)

### Backend
```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend
```bash
# Serve static files with Python
cd customer-frontend/dist
python -m http.server 5173

# Or use any static file server
# nginx, Apache, etc.
```

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-09  
**Status**: Complete
