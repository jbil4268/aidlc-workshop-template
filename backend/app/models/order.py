from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from ..database import Base


class OrderStatus(str, Enum):
    PENDING = "pending"
    PREPARING = "preparing"
    READY = "ready"
    SERVED = "served"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("table_sessions.id"), nullable=False, index=True)
    order_number = Column(String(20), nullable=False, index=True)
    subtotal_amount = Column(Integer, nullable=False)
    tip_rate = Column(Integer, default=0, nullable=False)  # Percentage (0, 5, 10, 15, 20)
    tip_amount = Column(Integer, default=0, nullable=False)
    total_amount = Column(Integer, nullable=False)
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    session = relationship("TableSession", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    history = relationship("OrderHistory", back_populates="order", cascade="all, delete-orphan")
