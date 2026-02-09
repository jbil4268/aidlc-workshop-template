"""Tests for TableSessionService"""
import pytest
from datetime import datetime
from app.services.table_session_service import TableSessionService
from app.models import Store, Table, TableSession
from app.utils.errors import ActiveSessionExistsError, SessionNotFoundError, SessionAlreadyEndedError


class TestTableSessionService:
    """Test suite for TableSessionService"""

    def setup_method(self, db_session):
        """Setup test fixtures"""
        self.db = db_session
        self.service = TableSessionService(self.db)
        
        # Create test store and table
        store = Store(id=1, name="Test Store")
        self.db.add(store)
        
        table = Table(
            id=1,
            store_id=1,
            table_number="T1",
            qr_code="QR001",
            is_active=True
        )
        self.db.add(table)
        self.db.commit()

    # TC-backend-010: 세션 생성 성공
    def test_create_session_success(self, db_session):
        """Test successful session creation"""
        self.setup_method(db_session)
        
        session = self.service.create_session(table_id=1)
        
        assert session is not None
        assert session.table_id == 1
        assert session.session_token is not None
        assert session.started_at is not None
        assert session.ended_at is None

    # TC-backend-011: 이미 활성 세션 존재
    def test_create_session_active_exists(self, db_session):
        """Test session creation when active session already exists"""
        self.setup_method(db_session)
        
        # Create first session
        self.service.create_session(table_id=1)
        
        # Try to create second session - should fail
        with pytest.raises(ActiveSessionExistsError):
            self.service.create_session(table_id=1)

    # TC-backend-012: 활성 세션 조회
    def test_get_active_session_exists(self, db_session):
        """Test getting active session when it exists"""
        self.setup_method(db_session)
        
        # Create session
        created = self.service.create_session(table_id=1)
        
        # Get active session
        active = self.service.get_active_session(table_id=1)
        
        assert active is not None
        assert active.id == created.id
        assert active.table_id == 1

    # TC-backend-013: 활성 세션 없음
    def test_get_active_session_none(self, db_session):
        """Test getting active session when none exists"""
        self.setup_method(db_session)
        
        active = self.service.get_active_session(table_id=1)
        
        assert active is None

    # TC-backend-014: 세션 종료 성공
    def test_end_session_success(self, db_session):
        """Test successful session ending"""
        self.setup_method(db_session)
        
        # Create session
        session = self.service.create_session(table_id=1)
        
        # End session
        result = self.service.end_session(session_id=session.id)
        
        assert result is True
        
        # Verify session is ended
        ended = self.db.query(TableSession).filter_by(id=session.id).first()
        assert ended.ended_at is not None

    # TC-backend-015: 존재하지 않는 세션
    def test_end_session_not_found(self, db_session):
        """Test ending non-existent session"""
        self.setup_method(db_session)
        
        with pytest.raises(SessionNotFoundError):
            self.service.end_session(session_id=999)

    # TC-backend-016: 이미 종료된 세션
    def test_end_session_already_ended(self, db_session):
        """Test ending already ended session"""
        self.setup_method(db_session)
        
        # Create and end session
        session = self.service.create_session(table_id=1)
        self.service.end_session(session_id=session.id)
        
        # Try to end again
        with pytest.raises(SessionAlreadyEndedError):
            self.service.end_session(session_id=session.id)

