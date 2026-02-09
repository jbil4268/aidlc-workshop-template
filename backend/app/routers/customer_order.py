"""Customer Order Router"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.order import OrderCreate, OrderResponse, OrderListResponse
from ..services.order_service import OrderService, OrderItemData
from ..models.table_session import TableSession
from ..utils.errors import (
    SessionNotActiveError, MenuNotAvailableError,
    InvalidQuantityError, InvalidTipRateError
)

router = APIRouter(prefix="/api/customer/order", tags=["Customer Order"])


@router.post("/create", response_model=OrderResponse)
def create_order(
    order_data: OrderCreate,
    session_token: str,
    db: Session = Depends(get_db)
):
    """
    Create a new order for the current session.
    """
    # Find session
    session = db.query(TableSession).filter_by(session_token=session_token).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Create order
    order_service = OrderService(db)
    items = [OrderItemData(**item.dict()) for item in order_data.items]
    
    try:
        order = order_service.create_order(
            session_id=session.id,
            items=items,
            tip_rate=order_data.tip_rate
        )
    except SessionNotActiveError:
        raise HTTPException(status_code=400, detail="Session is not active")
    except MenuNotAvailableError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except InvalidQuantityError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except InvalidTipRateError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return OrderResponse.from_orm(order)


@router.get("/list", response_model=OrderListResponse)
def get_order_list(
    session_token: str,
    db: Session = Depends(get_db)
):
    """
    Get all orders for the current session.
    """
    from ..models.order import Order
    
    # Find session
    session = db.query(TableSession).filter_by(session_token=session_token).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get orders
    orders = db.query(Order).filter_by(session_id=session.id).all()
    
    return OrderListResponse(
        orders=[OrderResponse.from_orm(o) for o in orders]
    )


@router.get("/{order_id}", response_model=OrderResponse)
def get_order_detail(
    order_id: int,
    session_token: str,
    db: Session = Depends(get_db)
):
    """
    Get order detail by ID.
    """
    from ..models.order import Order
    
    # Find session
    session = db.query(TableSession).filter_by(session_token=session_token).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get order
    order = db.query(Order).filter_by(id=order_id, session_id=session.id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return OrderResponse.from_orm(order)
