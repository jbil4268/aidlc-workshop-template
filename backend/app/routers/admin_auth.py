"""Admin Authentication Router"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.auth import AdminLoginRequest, AdminLoginResponse
from ..models.admin import Admin
from ..services.auth_service import AuthService
from ..config import settings

router = APIRouter(prefix="/api/admin/auth", tags=["Admin Auth"])


@router.post("/login", response_model=AdminLoginResponse)
def admin_login(
    request: AdminLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Admin login with username and password.
    Returns JWT token.
    """
    # Find admin
    admin = db.query(Admin).filter_by(username=request.username).first()
    
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password
    auth_service = AuthService()
    
    if not auth_service.verify_password(request.password, admin.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create JWT token
    payload = {
        "admin_id": admin.id,
        "username": admin.username,
        "store_id": admin.store_id
    }
    
    token = auth_service.create_jwt_token(
        payload,
        expires_hours=settings.ADMIN_JWT_EXPIRE_MINUTES // 60
    )
    
    return AdminLoginResponse(access_token=token)
