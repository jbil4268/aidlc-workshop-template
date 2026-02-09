"""Reset admin account with new password hashing logic"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.services.auth_service import AuthService

# Database setup
DATABASE_URL = "sqlite:///./table_order.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def reset_admin():
    """Reset admin account password"""
    db = SessionLocal()
    auth_service = AuthService()
    
    try:
        # Delete existing admin
        db.execute(text("DELETE FROM admins WHERE username = 'admin'"))
        
        # Create new admin with proper password hashing
        hashed_password = auth_service.hash_password("admin123")
        
        from datetime import datetime
        now = datetime.utcnow()
        
        db.execute(text("""
            INSERT INTO admins (username, password_hash, store_id, created_at, updated_at)
            VALUES (:username, :password, :store_id, :created_at, :updated_at)
        """), {
            "username": "admin",
            "password": hashed_password,
            "store_id": 1,
            "created_at": now,
            "updated_at": now
        })
        
        db.commit()
        print("✅ Admin account reset successfully!")
        print("   Username: admin")
        print("   Password: admin123")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    reset_admin()
