from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./table_order.db"
    
    # JWT
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60
    
    # Admin JWT
    ADMIN_JWT_EXPIRE_MINUTES: int = 480  # 8 hours
    
    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {"jpg", "jpeg", "png", "webp"}
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    
    # Seed Data
    SEED_STORE_NAME: str = "My Restaurant"
    SEED_ADMIN_USERNAME: str = "admin"
    SEED_ADMIN_PASSWORD: str = "admin123"
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"  # Ignore extra fields from .env
    )


settings = Settings()
