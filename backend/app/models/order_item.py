from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    menu_id = Column(Integer, ForeignKey("menus.id"), nullable=False, index=True)
    menu_name = Column(String(100), nullable=False)  # Snapshot at order time
    menu_price = Column(Integer, nullable=False)  # Snapshot at order time
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    order = relationship("Order", back_populates="items")
    menu = relationship("Menu", back_populates="order_items")
