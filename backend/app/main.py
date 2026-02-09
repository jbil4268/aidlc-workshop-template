"""FastAPI Application Entry Point"""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from .config import settings
from .database import Base, engine

# Import routers
from .routers import (
    customer_auth,
    customer_menu,
    customer_order,
    admin_auth,
    admin_order,
    admin_table,
    admin_menu,
    admin_category,
    websocket
)

# Import custom errors
from .utils.errors import (
    TokenExpiredError,
    InvalidTokenError,
    ActiveSessionExistsError,
    SessionNotFoundError,
    SessionAlreadyEndedError,
    InvalidTipRateError,
    SessionNotActiveError,
    MenuNotAvailableError,
    InvalidQuantityError,
    OrderNotFoundError,
    InvalidStatusError
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Table Order API",
    description="Backend API for Table Order Service",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handlers
@app.exception_handler(TokenExpiredError)
async def token_expired_handler(request: Request, exc: TokenExpiredError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(exc)}
    )


@app.exception_handler(InvalidTokenError)
async def invalid_token_handler(request: Request, exc: InvalidTokenError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(exc)}
    )


@app.exception_handler(ActiveSessionExistsError)
async def active_session_exists_handler(request: Request, exc: ActiveSessionExistsError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )


@app.exception_handler(SessionNotFoundError)
async def session_not_found_handler(request: Request, exc: SessionNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)}
    )


@app.exception_handler(SessionAlreadyEndedError)
async def session_already_ended_handler(request: Request, exc: SessionAlreadyEndedError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )


@app.exception_handler(InvalidTipRateError)
async def invalid_tip_rate_handler(request: Request, exc: InvalidTipRateError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )


@app.exception_handler(SessionNotActiveError)
async def session_not_active_handler(request: Request, exc: SessionNotActiveError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )


@app.exception_handler(MenuNotAvailableError)
async def menu_not_available_handler(request: Request, exc: MenuNotAvailableError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )


@app.exception_handler(InvalidQuantityError)
async def invalid_quantity_handler(request: Request, exc: InvalidQuantityError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )


@app.exception_handler(OrderNotFoundError)
async def order_not_found_handler(request: Request, exc: OrderNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)}
    )


@app.exception_handler(InvalidStatusError)
async def invalid_status_handler(request: Request, exc: InvalidStatusError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )


# Register routers
app.include_router(customer_auth.router)
app.include_router(customer_menu.router)
app.include_router(customer_order.router)
app.include_router(admin_auth.router)
app.include_router(admin_order.router)
app.include_router(admin_table.router)
app.include_router(admin_menu.router)
app.include_router(admin_category.router)
app.include_router(websocket.router)

# Static files for uploads
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Table Order API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
