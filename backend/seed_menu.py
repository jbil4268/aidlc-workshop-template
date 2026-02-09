"""Seed menu and category data"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.category import Category
from app.models.menu import Menu

# Database setup
DATABASE_URL = "sqlite:///./table_order.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_data():
    """Seed categories and menus"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_categories = db.query(Category).count()
        if existing_categories > 0:
            print(f"⚠️  이미 {existing_categories}개의 카테고리가 있습니다.")
            response = input("기존 데이터를 삭제하고 새로 생성하시겠습니까? (y/N): ")
            if response.lower() != 'y':
                print("취소되었습니다.")
                return
            
            # Delete existing data
            db.query(Menu).delete()
            db.query(Category).delete()
            db.commit()
            print("✅ 기존 데이터를 삭제했습니다.")
        
        # Create categories
        categories = [
            Category(name="메인 요리", display_order=1, store_id=1),
            Category(name="사이드 메뉴", display_order=2, store_id=1),
            Category(name="음료", display_order=3, store_id=1),
            Category(name="디저트", display_order=4, store_id=1),
        ]
        
        for cat in categories:
            db.add(cat)
        db.commit()
        
        # Refresh to get IDs
        for cat in categories:
            db.refresh(cat)
        
        print(f"✅ {len(categories)}개의 카테고리를 생성했습니다.")
        
        # Create menus
        menus = [
            # 메인 요리
            Menu(name="김치찌개", description="얼큰한 김치찌개", price=9000, category_id=categories[0].id, is_available=True),
            Menu(name="된장찌개", description="구수한 된장찌개", price=8000, category_id=categories[0].id, is_available=True),
            Menu(name="불고기", description="달콤한 불고기", price=15000, category_id=categories[0].id, is_available=True),
            Menu(name="비빔밥", description="영양 가득 비빔밥", price=10000, category_id=categories[0].id, is_available=True),
            
            # 사이드 메뉴
            Menu(name="계란말이", description="부드러운 계란말이", price=5000, category_id=categories[1].id, is_available=True),
            Menu(name="김치전", description="바삭한 김치전", price=6000, category_id=categories[1].id, is_available=True),
            Menu(name="떡볶이", description="매콤한 떡볶이", price=5000, category_id=categories[1].id, is_available=True),
            
            # 음료
            Menu(name="콜라", description="시원한 콜라", price=2000, category_id=categories[2].id, is_available=True),
            Menu(name="사이다", description="청량한 사이다", price=2000, category_id=categories[2].id, is_available=True),
            Menu(name="아메리카노", description="진한 아메리카노", price=3000, category_id=categories[2].id, is_available=True),
            
            # 디저트
            Menu(name="아이스크림", description="달콤한 아이스크림", price=3000, category_id=categories[3].id, is_available=True),
            Menu(name="케이크", description="부드러운 케이크", price=5000, category_id=categories[3].id, is_available=True),
        ]
        
        for menu in menus:
            db.add(menu)
        db.commit()
        
        print(f"✅ {len(menus)}개의 메뉴를 생성했습니다.")
        print("\n📋 생성된 데이터:")
        print(f"   - 카테고리: {len(categories)}개")
        print(f"   - 메뉴: {len(menus)}개")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
