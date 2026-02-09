from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class TableSession(Base):
    __tablename__ = "table_sessions"

    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False, index=True)
    session_token = Column(String(255), unique=True, nullable=False, index=True)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ended_at = Column(DateTime, nullable=True)

    # Relationships
    table = relationship("Table", back_populates="sessions")
    orders = relationship("Order", back_populates="session", cascade="all, delete-orphan")
