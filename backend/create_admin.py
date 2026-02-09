"""
Create admin user for the application
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Admin, Store
from app.services.auth_service import AuthService

def create_admin():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    auth_service = AuthService()
    
    try:
        # Check if store exists
        store = db.query(Store).first()
        if not store:
            store = Store(
                name="My Restaurant"
            )
            db.add(store)
            db.commit()
            db.refresh(store)
            print(f"✓ Store created: {store.name}")
        else:
            print(f"✓ Store already exists: {store.name}")
        
        # Check if admin exists
        admin = db.query(Admin).filter(Admin.username == "admin").first()
        if admin:
            print("✓ Admin user already exists")
            # Update password
            admin.password_hash = auth_service.hash_password("admin123")
            db.commit()
            print("✓ Admin password updated to: admin123")
        else:
            # Create admin
            admin = Admin(
                username="admin",
                password_hash=auth_service.hash_password("admin123"),
                store_id=store.id
            )
            db.add(admin)
            db.commit()
            print("✓ Admin user created")
            print(f"  Username: admin")
            print(f"  Password: admin123")
        
        print("\n✅ Admin setup complete!")
        print("You can now login with:")
        print("  Username: admin")
        print("  Password: admin123")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
