from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TableBase(BaseModel):
    table_number: str


class TableCreate(TableBase):
    qr_code: str


class TableUpdate(BaseModel):
    table_number: Optional[str] = None
    is_active: Optional[bool] = None


class TableResponse(TableBase):
    id: int
    store_id: int
    qr_code: str
    is_active: bool

    class Config:
        from_attributes = True


class TableSessionResponse(BaseModel):
    id: int
    table_id: int
    session_token: str
    started_at: datetime
    ended_at: Optional[datetime] = None

    class Config:
        from_attributes = True
