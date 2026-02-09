from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class OrderHistory(Base):
    __tablename__ = "order_history"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    old_status = Column(String(20), nullable=False)
    new_status = Column(String(20), nullable=False)
    changed_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    order = relationship("Order", back_populates="history")
