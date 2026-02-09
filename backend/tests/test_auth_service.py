"""Tests for AuthService"""
import pytest
from app.services.auth_service import AuthService
from app.utils.errors import TokenExpiredError, InvalidTokenError


class TestAuthService:
    """Test suite for AuthService"""

    def setup_method(self):
        """Setup test fixtures"""
        self.auth_service = AuthService()

    # TC-backend-001: 비밀번호 해싱 성공
    def test_hash_password_success(self):
        """Test password hashing returns a valid bcrypt hash"""
        password = "test_password_123"
        hashed = self.auth_service.hash_password(password)
        
        # Bcrypt hash should start with $2b$ and be 60 characters
        assert hashed.startswith("$2b$")
        assert len(hashed) == 60
        assert hashed != password  # Should not be plain text


    # TC-backend-002: 같은 비밀번호도 다른 해시
    def test_hash_password_different_hashes(self):
        """Test that same password produces different hashes (salt)"""
        password = "test_password_123"
        hash1 = self.auth_service.hash_password(password)
        hash2 = self.auth_service.hash_password(password)
        
        # Same password should produce different hashes due to salt
        assert hash1 != hash2
        assert hash1.startswith("$2b$")
        assert hash2.startswith("$2b$")


    # TC-backend-003: 올바른 비밀번호 검증
    def test_verify_password_correct(self):
        """Test password verification with correct password"""
        password = "test_password_123"
        hashed = self.auth_service.hash_password(password)
        
        # Correct password should verify successfully
        assert self.auth_service.verify_password(password, hashed) is True

    # TC-backend-004: 잘못된 비밀번호 검증
    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password"""
        password = "test_password_123"
        wrong_password = "wrong_password"
        hashed = self.auth_service.hash_password(password)
        
        # Wrong password should fail verification
        assert self.auth_service.verify_password(wrong_password, hashed) is False


    # TC-backend-005: JWT 토큰 생성
    def test_create_jwt_token_success(self):
        """Test JWT token creation"""
        payload = {"user_id": 123, "username": "testuser"}
        token = self.auth_service.create_jwt_token(payload, expires_hours=1)
        
        # Token should be a non-empty string
        assert isinstance(token, str)
        assert len(token) > 0
        # JWT tokens have 3 parts separated by dots
        assert token.count('.') == 2

    # TC-backend-006: 만료 시간 설정
    def test_create_jwt_token_with_expiration(self):
        """Test JWT token creation with custom expiration"""
        payload = {"user_id": 456}
        token1 = self.auth_service.create_jwt_token(payload, expires_hours=1)
        token2 = self.auth_service.create_jwt_token(payload, expires_hours=24)
        
        # Different expiration times should produce different tokens
        assert token1 != token2
        assert isinstance(token1, str)
        assert isinstance(token2, str)


    # TC-backend-007: 유효한 토큰 검증
    def test_verify_jwt_token_valid(self):
        """Test JWT token verification with valid token"""
        payload = {"user_id": 123, "username": "testuser"}
        token = self.auth_service.create_jwt_token(payload, expires_hours=1)
        
        # Should decode successfully
        decoded = self.auth_service.verify_jwt_token(token)
        assert decoded["user_id"] == 123
        assert decoded["username"] == "testuser"
        assert "exp" in decoded

    # TC-backend-008: 만료된 토큰
    def test_verify_jwt_token_expired(self):
        """Test JWT token verification with expired token"""
        import time
        payload = {"user_id": 456}
        # Create token that expires in 1 second
        token = self.auth_service.create_jwt_token(payload, expires_hours=-1)
        
        # Should raise TokenExpiredError
        with pytest.raises(TokenExpiredError):
            self.auth_service.verify_jwt_token(token)

    # TC-backend-009: 무효한 토큰
    def test_verify_jwt_token_invalid(self):
        """Test JWT token verification with invalid token"""
        invalid_token = "invalid.token.string"
        
        # Should raise InvalidTokenError
        with pytest.raises(InvalidTokenError):
            self.auth_service.verify_jwt_token(invalid_token)
