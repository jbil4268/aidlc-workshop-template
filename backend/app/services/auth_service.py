"""Authentication Service - Core business logic for authentication and token management"""
from typing import Dict
from datetime import datetime, timedelta
import bcrypt
import jwt
from ..config import settings


class AuthService:
    """Service for handling authentication and JWT token operations"""

    def hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: Plain text password
            
        Returns:
            Bcrypt hashed password
        """
        # Bcrypt has a 72 byte limit
        password_bytes = password.encode('utf-8')[:72]
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            plain_password: Plain text password
            hashed_password: Hashed password
            
        Returns:
            True if password matches, False otherwise
        """
        # Bcrypt has a 72 byte limit
        password_bytes = plain_password.encode('utf-8')[:72]
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)

    def create_jwt_token(self, payload: Dict, expires_hours: int = 16) -> str:
        """
        Create a JWT token.
        
        Args:
            payload: Data to include in token
            expires_hours: Token expiration time in hours (default 16)
            
        Returns:
            JWT token string
        """
        to_encode = payload.copy()
        expire = datetime.utcnow() + timedelta(hours=expires_hours)
        to_encode.update({"exp": expire})
        
        token = jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        return token

    def verify_jwt_token(self, token: str) -> Dict:
        """
        Verify JWT token and return payload.
        
        Args:
            token: JWT token string
            
        Returns:
            Token payload dictionary
            
        Raises:
            TokenExpiredError: If token has expired
            InvalidTokenError: If token is invalid
        """
        from ..utils.errors import TokenExpiredError, InvalidTokenError
        
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError("Token has expired")
        except jwt.InvalidTokenError:
            raise InvalidTokenError("Invalid token")
