from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    tables = relationship("Table", back_populates="store", cascade="all, delete-orphan")
    categories = relationship("Category", back_populates="store", cascade="all, delete-orphan")
    admins = relationship("Admin", back_populates="store", cascade="all, delete-orphan")
