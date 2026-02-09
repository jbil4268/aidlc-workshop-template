"""Dependency injection functions for FastAPI"""
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from ..services.auth_service import AuthService
from ..models.table_session import TableSession
from ..models.admin import Admin
from ..utils.errors import TokenExpiredError, InvalidTokenError


def verify_token(token: str) -> dict:
    """
    Verify JWT token and return payload.
    
    Args:
        token: JWT token string
        
    Returns:
        Token payload
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    auth_service = AuthService()
    
    try:
        payload = auth_service.verify_jwt_token(token)
        return payload
    except TokenExpiredError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_table(
    session_token: str = Header(...),
    db: Session = Depends(get_db)
) -> TableSession:
    """
    Get current table session from session token.
    
    Args:
        session_token: Session token from header
        db: Database session
        
    Returns:
        TableSession object
        
    Raises:
        HTTPException: If session not found or ended
    """
    session = db.query(TableSession).filter_by(session_token=session_token).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.ended_at is not None:
        raise HTTPException(status_code=400, detail="Session has ended")
    
    return session


def get_current_admin(
    authorization: str = Header(...),
    db: Session = Depends(get_db)
) -> Admin:
    """
    Get current admin from JWT token.
    
    Args:
        authorization: Authorization header (Bearer token)
        db: Database session
        
    Returns:
        Admin object
        
    Raises:
        HTTPException: If token invalid or admin not found
    """
    # Extract token from "Bearer <token>"
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = authorization.replace("Bearer ", "")
    
    # Verify token
    payload = verify_token(token)
    
    # Get admin
    admin_id = payload.get("admin_id")
    if not admin_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    admin = db.query(Admin).filter_by(id=admin_id).first()
    
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    return admin
