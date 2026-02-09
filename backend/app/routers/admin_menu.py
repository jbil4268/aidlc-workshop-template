"""Admin Menu Management Router"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from ..database import get_db
from ..schemas.menu import MenuResponse, MenuCreate, MenuUpdate
from ..models.menu import Menu
from ..config import settings

router = APIRouter(prefix="/api/admin/menu", tags=["Admin Menu"])


@router.get("/list", response_model=List[MenuResponse])
def get_all_menus(db: Session = Depends(get_db)):
    """
    Get all menus.
    """
    menus = db.query(Menu).all()
    return [MenuResponse.from_orm(m) for m in menus]


@router.get("/{menu_id}", response_model=MenuResponse)
def get_menu_detail(
    menu_id: int,
    db: Session = Depends(get_db)
):
    """
    Get menu detail by ID.
    """
    menu = db.query(Menu).filter_by(id=menu_id).first()
    
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    
    return MenuResponse.from_orm(menu)


@router.post("/create", response_model=MenuResponse)
def create_menu(
    menu_data: MenuCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new menu.
    """
    menu = Menu(**menu_data.dict())
    
    db.add(menu)
    db.commit()
    db.refresh(menu)
    
    return MenuResponse.from_orm(menu)


@router.patch("/{menu_id}", response_model=MenuResponse)
def update_menu(
    menu_id: int,
    menu_data: MenuUpdate,
    db: Session = Depends(get_db)
):
    """
    Update menu information.
    """
    menu = db.query(Menu).filter_by(id=menu_id).first()
    
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    
    # Update fields
    update_data = menu_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(menu, field, value)
    
    db.commit()
    db.refresh(menu)
    
    return MenuResponse.from_orm(menu)


@router.post("/{menu_id}/upload-image")
def upload_menu_image(
    menu_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload menu image.
    """
    menu = db.query(Menu).filter_by(id=menu_id).first()
    
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    
    # Validate file extension
    file_ext = file.filename.split(".")[-1].lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed: {settings.ALLOWED_EXTENSIONS}"
        )
    
    # Create upload directory if not exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # Save file
    file_path = f"{settings.UPLOAD_DIR}/{menu_id}.{file_ext}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update menu image URL
    menu.image_url = f"/uploads/{menu_id}.{file_ext}"
    db.commit()
    
    return {"message": "Image uploaded successfully", "image_url": menu.image_url}


@router.delete("/{menu_id}")
def delete_menu(
    menu_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete menu (soft delete - set is_available to False).
    """
    menu = db.query(Menu).filter_by(id=menu_id).first()
    
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    
    menu.is_available = False
    db.commit()
    
    return {"message": "Menu deleted successfully"}
