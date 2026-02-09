"""Admin Table Management Router"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.table import TableResponse, TableCreate, TableUpdate
from ..models.table import Table

router = APIRouter(prefix="/api/admin/table", tags=["Admin Table"])


@router.get("/list", response_model=List[TableResponse])
def get_all_tables(db: Session = Depends(get_db)):
    """
    Get all tables.
    """
    tables = db.query(Table).all()
    return [TableResponse.from_orm(t) for t in tables]


@router.get("/{table_id}", response_model=TableResponse)
def get_table_detail(
    table_id: int,
    db: Session = Depends(get_db)
):
    """
    Get table detail by ID.
    """
    table = db.query(Table).filter_by(id=table_id).first()
    
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    return TableResponse.from_orm(table)


@router.post("/create", response_model=TableResponse)
def create_table(
    table_data: TableCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new table.
    """
    # Check if QR code already exists
    existing = db.query(Table).filter_by(qr_code=table_data.qr_code).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="QR code already exists")
    
    # Create table (assuming store_id=1 for now)
    table = Table(
        store_id=1,
        table_number=table_data.table_number,
        qr_code=table_data.qr_code,
        is_active=True
    )
    
    db.add(table)
    db.commit()
    db.refresh(table)
    
    return TableResponse.from_orm(table)


@router.patch("/{table_id}", response_model=TableResponse)
def update_table(
    table_id: int,
    table_data: TableUpdate,
    db: Session = Depends(get_db)
):
    """
    Update table information.
    """
    table = db.query(Table).filter_by(id=table_id).first()
    
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    # Update fields
    if table_data.table_number is not None:
        table.table_number = table_data.table_number
    
    if table_data.is_active is not None:
        table.is_active = table_data.is_active
    
    db.commit()
    db.refresh(table)
    
    return TableResponse.from_orm(table)
