from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class OrderItemCreate(BaseModel):
    menu_id: int
    quantity: int = Field(gt=0)


class OrderItemResponse(BaseModel):
    id: int
    menu_id: int
    menu_name: str
    menu_price: int
    quantity: int
    subtotal: int

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    tip_rate: int = Field(ge=0, le=20, default=0)  # 0, 5, 10, 15, 20


class OrderResponse(BaseModel):
    id: int
    order_number: str
    subtotal_amount: int
    tip_rate: int
    tip_amount: int
    total_amount: int
    status: str
    items: List[OrderItemResponse]
    created_at: datetime

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: str  # pending, preparing, ready, served, cancelled


class OrderListResponse(BaseModel):
    orders: List[OrderResponse]


class OrderHistoryResponse(BaseModel):
    id: int
    order_id: int
    old_status: str
    new_status: str
    changed_at: datetime

    class Config:
        from_attributes = True
