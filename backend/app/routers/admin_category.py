"""Admin Category Management Router"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.menu import CategoryResponse, CategoryCreate, CategoryUpdate
from ..models.category import Category
from ..models.menu import Menu

router = APIRouter(prefix="/api/admin/category", tags=["Admin Category"])


@router.get("/list", response_model=List[CategoryResponse])
def get_all_categories(db: Session = Depends(get_db)):
    """
    Get all categories.
    """
    categories = db.query(Category).order_by(Category.display_order).all()
    return [CategoryResponse.from_orm(c) for c in categories]


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category_detail(
    category_id: int,
    db: Session = Depends(get_db)
):
    """
    Get category detail by ID.
    """
    category = db.query(Category).filter_by(id=category_id).first()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return CategoryResponse.from_orm(category)


@router.post("/create", response_model=CategoryResponse)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new category.
    """
    # Assuming store_id=1 for now
    category = Category(
        store_id=1,
        **category_data.dict()
    )
    
    db.add(category)
    db.commit()
    db.refresh(category)
    
    return CategoryResponse.from_orm(category)


@router.patch("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db)
):
    """
    Update category information.
    """
    category = db.query(Category).filter_by(id=category_id).first()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Update fields
    update_data = category_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)
    
    db.commit()
    db.refresh(category)
    
    return CategoryResponse.from_orm(category)


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete category.
    Moves all menus to "Uncategorized" category (id=1).
    """
    category = db.query(Category).filter_by(id=category_id).first()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Move menus to uncategorized (assuming category_id=1 is uncategorized)
    menus = db.query(Menu).filter_by(category_id=category_id).all()
    for menu in menus:
        menu.category_id = 1  # Move to uncategorized
    
    # Delete category
    db.delete(category)
    db.commit()
    
    return {"message": "Category deleted successfully"}
