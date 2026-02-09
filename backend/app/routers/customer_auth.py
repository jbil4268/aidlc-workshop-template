"""Customer Authentication Router"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.auth import TableLoginRequest, TableLoginResponse
from ..models import Table
from ..services.auth_service import AuthService
from ..services.table_session_service import TableSessionService
from ..utils.errors import ActiveSessionExistsError

router = APIRouter(prefix="/api/customer/auth", tags=["Customer Auth"])


@router.post("/login", response_model=TableLoginResponse)
def table_login(
    request: TableLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Table login via QR code scan.
    Creates a new session for the table.
    """
    # Find table by QR code
    table = db.query(Table).filter_by(qr_code=request.qr_code, is_active=True).first()
    
    if not table:
        raise HTTPException(status_code=404, detail="Table not found or inactive")
    
    # Create session
    session_service = TableSessionService(db)
    session = session_service.create_session(table_id=table.id)
    
    return TableLoginResponse(
        session_token=session.session_token,
        table_number=table.table_number,
        table_id=table.id
    )


@router.post("/logout")
def table_logout(
    session_token: str,
    db: Session = Depends(get_db)
):
    """
    End table session.
    """
    from ..models.table_session import TableSession
    from ..utils.errors import SessionNotFoundError, SessionAlreadyEndedError
    
    # Find session
    session = db.query(TableSession).filter_by(session_token=session_token).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # End session
    session_service = TableSessionService(db)
    
    try:
        session_service.end_session(session_id=session.id)
    except SessionNotFoundError:
        raise HTTPException(status_code=404, detail="Session not found")
    except SessionAlreadyEndedError:
        raise HTTPException(status_code=400, detail="Session already ended")
    
    return {"message": "Session ended successfully"}
