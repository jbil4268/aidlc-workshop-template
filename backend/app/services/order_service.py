"""Order Service - Core business logic for order creation and management"""
from typing import List
from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.order import Order, OrderStatus
from ..models.order_item import OrderItem
from ..models.order_history import OrderHistory
from ..models.table_session import TableSession
from ..models.menu import Menu
from ..utils.errors import (
    InvalidTipRateError, SessionNotActiveError,
    MenuNotAvailableError, InvalidQuantityError,
    OrderNotFoundError, InvalidStatusError
)
from pydantic import BaseModel


class OrderItemData(BaseModel):
    """Data structure for order item"""
    menu_id: int
    quantity: int


class OrderService:
    """Service for handling order operations"""

    ALLOWED_TIP_RATES = [0, 5, 10, 15, 20]

    def __init__(self, db: Session):
        self.db = db

    def generate_order_number(self, store_id: int, order_date: date) -> str:
        """
        Generate sequential order number per store per day.
        
        Args:
            store_id: Store ID
            order_date: Order date
            
        Returns:
            Order number (e.g., "#001")
        """
        # Get today's orders count
        start_of_day = datetime(order_date.year, order_date.month, order_date.day)
        end_of_day = datetime(order_date.year, order_date.month, order_date.day, 23, 59, 59)
        
        count = self.db.query(func.count(Order.id)).filter(
            Order.created_at >= start_of_day,
            Order.created_at <= end_of_day
        ).scalar()
        
        next_number = count + 1
        return f"#{next_number:03d}"

    def calculate_tip(self, subtotal: int, tip_rate: int) -> int:
        """
        Calculate tip amount with rounding.
        
        Args:
            subtotal: Subtotal amount in KRW
            tip_rate: Tip rate (0, 5, 10, 15, 20)
            
        Returns:
            Tip amount in KRW
            
        Raises:
            InvalidTipRateError: If tip rate is not in allowed values
        """
        if tip_rate not in self.ALLOWED_TIP_RATES:
            raise InvalidTipRateError(f"Tip rate must be one of {self.ALLOWED_TIP_RATES}")
        
        tip_amount = subtotal * tip_rate / 100
        return round(tip_amount)

    def create_order(
        self, 
        session_id: int, 
        items: List[OrderItemData], 
        tip_rate: int
    ) -> Order:
        """
        Create a new order.
        
        Args:
            session_id: Session ID
            items: List of order items (menu_id, quantity)
            tip_rate: Tip rate
            
        Returns:
            Created Order object
            
        Raises:
            SessionNotActiveError: If session is not active
            MenuNotAvailableError: If menu is not available
            InvalidQuantityError: If quantity is <= 0
        """
        # Validate session is active
        session = self.db.query(TableSession).filter_by(id=session_id).first()
        if not session or session.ended_at is not None:
            raise SessionNotActiveError(f"Session {session_id} is not active")
        
        # Validate items
        subtotal = 0
        order_items = []
        
        for item in items:
            if item.quantity <= 0:
                raise InvalidQuantityError(f"Quantity must be greater than 0")
            
            menu = self.db.query(Menu).filter_by(id=item.menu_id).first()
            if not menu or not menu.is_available:
                raise MenuNotAvailableError(f"Menu {item.menu_id} is not available")
            
            item_subtotal = menu.price * item.quantity
            subtotal += item_subtotal
            
            order_items.append({
                "menu_id": menu.id,
                "menu_name": menu.name,
                "menu_price": menu.price,
                "quantity": item.quantity,
                "subtotal": item_subtotal
            })
        
        # Calculate tip and total
        tip_amount = self.calculate_tip(subtotal, tip_rate)
        total_amount = subtotal + tip_amount
        
        # Generate order number
        order_number = self.generate_order_number(store_id=1, order_date=date.today())
        
        # Create order
        order = Order(
            session_id=session_id,
            order_number=order_number,
            subtotal_amount=subtotal,
            tip_rate=tip_rate,
            tip_amount=tip_amount,
            total_amount=total_amount,
            status=OrderStatus.PENDING
        )
        
        self.db.add(order)
        self.db.flush()
        
        # Create order items
        for item_data in order_items:
            order_item = OrderItem(
                order_id=order.id,
                **item_data
            )
            self.db.add(order_item)
        
        self.db.commit()
        self.db.refresh(order)
        
        return order

    def update_order_status(self, order_id: int, new_status: str) -> Order:
        """
        Update order status.
        
        Args:
            order_id: Order ID
            new_status: New status value
            
        Returns:
            Updated Order object
            
        Raises:
            OrderNotFoundError: If order does not exist
            InvalidStatusError: If status value is invalid
        """
        order = self.db.query(Order).filter_by(id=order_id).first()
        
        if not order:
            raise OrderNotFoundError(f"Order {order_id} not found")
        
        # Validate status
        try:
            status_enum = OrderStatus(new_status)
        except ValueError:
            raise InvalidStatusError(f"Invalid status: {new_status}")
        
        # Record history
        history = OrderHistory(
            order_id=order.id,
            old_status=order.status.value,
            new_status=new_status
        )
        self.db.add(history)
        
        # Update status
        order.status = status_enum
        self.db.commit()
        self.db.refresh(order)
        
        return order
