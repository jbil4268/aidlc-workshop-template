"""Clear all active table sessions"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Database setup
DATABASE_URL = "sqlite:///./table_order.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def clear_all_sessions():
    """Clear all active sessions"""
    db = SessionLocal()
    
    try:
        # End all active sessions by setting ended_at to current time
        result = db.execute(text("""
            UPDATE table_sessions 
            SET ended_at = CURRENT_TIMESTAMP 
            WHERE ended_at IS NULL
        """))
        
        db.commit()
        count = result.rowcount
        print(f"✅ {count}개의 활성 세션을 종료했습니다.")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    clear_all_sessions()
