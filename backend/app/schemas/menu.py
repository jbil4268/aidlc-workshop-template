from pydantic import BaseModel
from typing import Optional, List


class CategoryBase(BaseModel):
    name: str
    display_order: int = 0


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    display_order: Optional[int] = None


class CategoryResponse(CategoryBase):
    id: int
    store_id: int

    class Config:
        from_attributes = True


class MenuBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: int
    allergens: Optional[str] = None
    is_available: bool = True


class MenuCreate(MenuBase):
    category_id: int


class MenuUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    category_id: Optional[int] = None
    allergens: Optional[str] = None
    is_available: Optional[bool] = None


class MenuResponse(MenuBase):
    id: int
    category_id: int
    image_url: Optional[str] = None

    class Config:
        from_attributes = True


class MenuListResponse(BaseModel):
    categories: List[CategoryResponse]
    menus: List[MenuResponse]
