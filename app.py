# File: app.py
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a random secret key

# Initialize users database
def init_users_db():
    conn = sqlite3.connect('questions.db')
    c = conn.cursor()
    
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

# Call this function when the app starts
init_users_db()

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# This route serves the main page (index.html)
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

# Route for the "For Whom?" page
@app.route('/for_whom.html')
def for_whom():
    return render_template('for_whom.html')

# Route for the "About Us" page
@app.route('/about.html')
def about():
    return render_template('about.html')

# Route for the "Contact Us" page
@app.route('/contact.html')
def contact():
    return render_template('contact.html')

# Route for the Login page (GET)
@app.route('/login.html')
def login_page():
    return render_template('login.html')

# Route for handling login form submission (POST)
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    password_hash = hash_password(password)
    
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", (username, password_hash))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        flash('Login successful!', 'success')
        return redirect(url_for('index'))
    else:
        flash('Invalid username or password', 'error')
        return redirect(url_for('login_page'))

# Route for the Signup page (GET)
@app.route('/signup.html')
def signup_page():
    return render_template('signup.html')

# Route for handling signup form submission (POST)
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    password_hash = hash_password(password)
    
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", 
                      (username, email, password_hash))
        conn.commit()
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login_page'))
    except sqlite3.IntegrityError:
        flash('Username or email already exists', 'error')
        return redirect(url_for('signup_page'))
    finally:
        conn.close()

# This route handles fetching questions for a specific category
@app.route('/questions/<category>')
def get_questions(category):
    conn = sqlite3.connect('questions.db')
    conn.row_factory = sqlite3.Row  # This lets us access columns by name
    cursor = conn.cursor()
    
    # Select all columns from the questions table where the category matches the one in the URL
    cursor.execute("SELECT * FROM questions WHERE category = ?", (category,))
    rows = cursor.fetchall()
    conn.close()

    # Format the data into a list of dictionaries that the JavaScript can easily use
    questions = []
    for row in rows:
        questions.append({
            'question': row['question'],
            'answers': [
                {'text': row['answer1'], 'correct': bool(row['correct1'])},
                {'text': row['answer2'], 'correct': bool(row['correct2'])},
                {'text': row['answer3'], 'correct': bool(row['correct3'])},
                {'text': row['answer4'], 'correct': bool(row['correct4'])}
            ],
            'feedback': row['feedback']
        })
        
    return jsonify(questions)

if __name__ == '__main__':
    app.run(debug=True)