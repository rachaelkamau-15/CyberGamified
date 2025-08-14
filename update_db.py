# update_db.py
import sqlite3

def update_db_schema():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    try:
        # Check existing columns
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add full_name if missing
        if 'full_name' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN full_name TEXT")
            # Migrate data from first_name + last_name
            cursor.execute("UPDATE users SET full_name = first_name || ' ' || last_name")
            print("Added full_name column and migrated data")
        
        # Add is_admin if missing
        if 'is_admin' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0")
            # Make first user admin
            cursor.execute("UPDATE users SET is_admin = 1 WHERE id = 1")
            print("Added is_admin column and set first user as admin")
        
        conn.commit()
        print("✅ Database schema updated successfully")
    except Exception as e:
        print(f"❌ Error updating schema: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    update_db_schema()