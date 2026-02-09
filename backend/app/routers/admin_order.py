"""Admin Order Management Router"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.order import OrderResponse, OrderListResponse, OrderStatusUpdate
from ..services.order_service import OrderService
from ..models.order import Order
from ..utils.errors import OrderNotFoundError, InvalidStatusError

router = APIRouter(prefix="/api/admin/order", tags=["Admin Order"])


@router.get("/list", response_model=OrderListResponse)
def get_all_orders(
    status: str = None,
    db: Session = Depends(get_db)
):
    """
    Get all orders, optionally filtered by status.
    """
    query = db.query(Order)
    
    if status:
        query = query.filter_by(status=status)
    
    orders = query.order_by(Order.created_at.desc()).all()
    
    return OrderListResponse(
        orders=[OrderResponse.from_orm(o) for o in orders]
    )


@router.get("/{order_id}", response_model=OrderResponse)
def get_order_detail(
    order_id: int,
    db: Session = Depends(get_db)
):
    """
    Get order detail by ID.
    """
    order = db.query(Order).filter_by(id=order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return OrderResponse.from_orm(order)


@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    db: Session = Depends(get_db)
):
    """
    Update order status.
    """
    order_service = OrderService(db)
    
    try:
        order = order_service.update_order_status(
            order_id=order_id,
            new_status=status_update.status
        )
    except OrderNotFoundError:
        raise HTTPException(status_code=404, detail="Order not found")
    except InvalidStatusError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return OrderResponse.from_orm(order)
