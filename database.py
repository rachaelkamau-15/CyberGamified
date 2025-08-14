import sqlite3
from werkzeug.security import generate_password_hash

def init_db():
    """
    Initializes a fresh database with the correct schema and a default admin user.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create users table with full_name
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        hashed_password TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0,
        reset_token TEXT,
        reset_token_expiration TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create questions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        question TEXT NOT NULL,
        answer1 TEXT NOT NULL,
        correct1 INTEGER DEFAULT 0,
        answer2 TEXT NOT NULL,
        correct2 INTEGER DEFAULT 0,
        answer3 TEXT NOT NULL,
        correct3 INTEGER DEFAULT 0,
        answer4 TEXT NOT NULL,
        correct4 INTEGER DEFAULT 0,
        feedback TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create user progress table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        high_score INTEGER NOT NULL,
        last_played_on TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')

    # Create admin user if it does not already exist
    admin_email = "adminshujaa@gmail.com"
    admin_password = generate_password_hash("Admin@123")

    cursor.execute("SELECT id FROM users WHERE email = ?", (admin_email,))
    if not cursor.fetchone():
        cursor.execute(
    "INSERT INTO users (full_name, email, password, is_admin) VALUES (?, ?, ?, ?)",
    ("Admin Shujaa", "adminshujaa@gmail.com", generate_password_hash("Admin@123"), 1)
)
        print("Default admin user created successfully.")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")