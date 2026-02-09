"""Table Session Service - Core business logic for table session lifecycle management"""
from typing import Optional
from datetime import datetime
import secrets
from sqlalchemy.orm import Session
from ..models.table_session import TableSession
from ..utils.errors import ActiveSessionExistsError, SessionNotFoundError, SessionAlreadyEndedError


class TableSessionService:
    """Service for handling table session lifecycle"""

    def __init__(self, db: Session):
        self.db = db

    def create_session(self, table_id: int) -> TableSession:
        """
        Create a new table session.
        If an active session exists, it will be automatically ended.
        
        Args:
            table_id: Table ID
            
        Returns:
            Created TableSession object
        """
        # Check for existing active session and end it
        active = self.get_active_session(table_id)
        if active:
            # Automatically end the existing session
            active.ended_at = datetime.utcnow()
            self.db.commit()
        
        # Generate session token
        session_token = secrets.token_urlsafe(32)
        
        # Create new session
        session = TableSession(
            table_id=table_id,
            session_token=session_token,
            started_at=datetime.utcnow()
        )
        
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        
        return session

    def get_active_session(self, table_id: int) -> Optional[TableSession]:
        """
        Get active session for a table.
        
        Args:
            table_id: Table ID
            
        Returns:
            Active TableSession or None
        """
        return self.db.query(TableSession).filter(
            TableSession.table_id == table_id,
            TableSession.ended_at.is_(None)
        ).first()

    def end_session(self, session_id: int) -> bool:
        """
        End a session and archive orders.
        
        Args:
            session_id: Session ID
            
        Returns:
            True if successful
            
        Raises:
            SessionNotFoundError: If session does not exist
            SessionAlreadyEndedError: If session is already ended
        """
        session = self.db.query(TableSession).filter_by(id=session_id).first()
        
        if not session:
            raise SessionNotFoundError(f"Session {session_id} not found")
        
        if session.ended_at is not None:
            raise SessionAlreadyEndedError(f"Session {session_id} is already ended")
        
        # End session
        session.ended_at = datetime.utcnow()
        self.db.commit()
        
        return True
