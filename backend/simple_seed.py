"""
Simple seeding without bcrypt issues
"""
import sqlite3
import bcrypt

# Connect to database
conn = sqlite3.connect('table_order.db')
cursor = conn.cursor()

try:
    # Check if store exists
    cursor.execute("SELECT id FROM stores LIMIT 1")
    store = cursor.fetchone()
    
    if not store:
        cursor.execute("INSERT INTO stores (name, created_at, updated_at) VALUES (?, datetime('now'), datetime('now'))", 
                      ("My Restaurant",))
        store_id = cursor.lastrowid
        print(f"✓ Store created")
    else:
        store_id = store[0]
        print(f"✓ Store exists (ID: {store_id})")
    
    # Hash password using bcrypt directly
    password = "admin123"
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Check if admin exists
    cursor.execute("SELECT id FROM admins WHERE username = ?", ("admin",))
    admin = cursor.fetchone()
    
    if admin:
        # Update password
        cursor.execute("UPDATE admins SET password_hash = ? WHERE username = ?", 
                      (password_hash, "admin"))
        print("✓ Admin password updated")
    else:
        # Create admin
        cursor.execute("""
            INSERT INTO admins (username, password_hash, store_id, created_at, updated_at) 
            VALUES (?, ?, ?, datetime('now'), datetime('now'))
        """, ("admin", password_hash, store_id))
        print("✓ Admin created")
    
    conn.commit()
    print("\n✅ Setup complete!")
    print("Login with:")
    print("  Username: admin")
    print("  Password: admin123")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()
finally:
    conn.close()
