# File: database.py
import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create users table with new columns
    # Email will be the primary login field and must be unique
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Create questions table (no changes needed here)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            question TEXT NOT NULL,
            answer1 TEXT NOT NULL,
            correct1 INTEGER NOT NULL,
            answer2 TEXT NOT NULL,
            correct2 INTEGER NOT NULL,
            answer3 TEXT NOT NULL,
            correct3 INTEGER NOT NULL,
            answer4 TEXT NOT NULL,
            correct4 INTEGER NOT NULL,
            feedback TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized with the new user schema.")