"""Customer Menu Router"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.menu import MenuResponse, CategoryResponse, MenuListResponse
from ..models import Menu, Category

router = APIRouter(prefix="/api/customer/menu", tags=["Customer Menu"])


@router.get("/list", response_model=MenuListResponse)
def get_menu_list(db: Session = Depends(get_db)):
    """
    Get all categories and menus.
    """
    categories = db.query(Category).order_by(Category.display_order).all()
    menus = db.query(Menu).all()
    
    return MenuListResponse(
        categories=[CategoryResponse.from_orm(c) for c in categories],
        menus=[MenuResponse.from_orm(m) for m in menus]
    )


@router.get("/{menu_id}", response_model=MenuResponse)
def get_menu_detail(menu_id: int, db: Session = Depends(get_db)):
    """
    Get menu detail by ID.
    """
    from fastapi import HTTPException
    
    menu = db.query(Menu).filter_by(id=menu_id).first()
    
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    
    return MenuResponse.from_orm(menu)
