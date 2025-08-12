from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import re
import secrets
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_very_secret_key_for_flashing'

# --- Password Validation ---
def is_password_strong(password):
    if len(password) < 8: return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password): return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password): return False, "Password must contain at least one lowercase letter."
    if not re.search(r"[0-9]", password): return False, "Password must contain at least one number."
    if not re.search(r"[\W_]", password): return False, "Password must contain at least one symbol."
    return True, None

# --- DECORATORS ---
# For redirecting browser pages
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# --- NEW DECORATOR: For protecting JSON-based API endpoints ---
def api_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify(error="Authentication required. Please log in."), 401
        return f(*args, **kwargs)
    return decorated_function


# --- PAGE ROUTES ---
@app.route('/')
def index():
    if 'user_id' in session: return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user = sqlite3.connect('database.db').cursor().execute("SELECT first_name, last_name FROM users WHERE id = ?", (session['user_id'],)).fetchone()
    user_full_name = f"{user[0]} {user[1]}" if user else "User"
    return render_template('user_dashboard.html', user_full_name=user_full_name)

@app.route('/my-dashboard')
@login_required
def my_dashboard():
    # This logic is correct and remains the same
    user_id = session['user_id']
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    user = cursor.execute("SELECT first_name, last_name FROM users WHERE id = ?", (user_id,)).fetchone()
    user_full_name = f"{user['first_name']} {user['last_name']}" if user else "User"
    completed_quizzes = cursor.execute("SELECT * FROM user_progress WHERE user_id = ?", (user_id,)).fetchall()
    all_categories_query = cursor.execute("SELECT DISTINCT category FROM questions").fetchall()
    all_categories = {row['category'] for row in all_categories_query}
    completed_categories = {quiz['category'] for quiz in completed_quizzes}
    uncompleted_quizzes = list(all_categories - completed_categories)
    total_quizzes = len(all_categories)
    average_score = round(sum(q['high_score'] for q in completed_quizzes) / len(completed_quizzes)) if completed_quizzes else 0
    conn.close()
    return render_template('my_dashboard.html', user_full_name=user_full_name, completed_quizzes=completed_quizzes, uncompleted_quizzes=uncompleted_quizzes, total_quizzes=total_quizzes, average_score=average_score)

# --- STATIC & PLACEHOLDER PAGES ---
@app.route('/for_whom.html')
def for_whom(): return render_template('for_whom.html')
@app.route('/about.html')
def about(): return render_template('about.html')
@app.route('/contact.html')
def contact(): return render_template('contact.html')
@app.route('/update-profile')
@login_required
def update_profile(): return "<h1>Update Profile Page</h1><p>Coming Soon</p>"
@app.route('/change-password')
@login_required
def change_password(): return "<h1>Change Password Page</h1><p>Coming Soon</p>"

# --- AUTHENTICATION ROUTES ---
# ... (signup, login, logout, and password reset routes are unchanged) ...
@app.route('/signup.html', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name, last_name, email, password = request.form['first_name'], request.form['last_name'], request.form['email'], request.form['password']
        is_strong, error_message = is_password_strong(password)
        if not is_strong: return render_template('signup.html', error=error_message)
        hashed_password = generate_password_hash(password)
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (?, ?, ?, ?)", (first_name, last_name, email, hashed_password))
            conn.commit()
            session['user_id'] = cursor.lastrowid
            conn.close()
            return redirect(url_for('dashboard'))
        except sqlite3.IntegrityError:
            return render_template('signup.html', error='Email address already registered.')
    return render_template('signup.html')

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email, password = request.form['email'], request.form['password']
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        user = conn.cursor().execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid email or password.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been successfully logged out.", "success")
    return redirect(url_for('index'))

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        user = cursor.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
        if user:
            token = secrets.token_urlsafe(16)
            expiration = datetime.utcnow() + timedelta(hours=1)
            cursor.execute("UPDATE users SET reset_token = ?, reset_token_expiration = ? WHERE email = ?", (token, expiration, email))
            conn.commit()
            reset_link = url_for('reset_password', token=token, _external=True)
            print("="*80); print(f"PASSWORD RESET LINK: {reset_link}"); print("="*80)
        flash("If an account exists, check your terminal for a reset link.", "success")
        conn.close()
        return redirect(url_for('forgot_password'))
    return render_template('forgot_password.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    user = cursor.execute("SELECT id, reset_token_expiration FROM users WHERE reset_token = ?", (token,)).fetchone()
    if not user or datetime.utcnow() > datetime.strptime(user[1], '%Y-%m-%d %H:%M:%S.%f'):
        flash("The password reset link is invalid or has expired.", "error")
        conn.close()
        return redirect(url_for('forgot_password'))
    if request.method == 'POST':
        password = request.form['password']
        is_strong, error_message = is_password_strong(password)
        if not is_strong: return render_template('reset_password.html', token=token, error=error_message)
        hashed_password = generate_password_hash(password)
        cursor.execute("UPDATE users SET password = ?, reset_token = NULL, reset_token_expiration = NULL WHERE id = ?", (hashed_password, user[0]))
        conn.commit()
        flash("Your password has been reset successfully. Please log in.", "success")
        return redirect(url_for('login'))
    conn.close()
    return render_template('reset_password.html', token=token)


# --- API ENDPOINTS ---
@app.route('/questions/<category>')
@api_login_required # <-- USE THE NEW DECORATOR HERE
def get_questions(category):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    rows = conn.cursor().execute("SELECT * FROM questions WHERE category = ?", (category,)).fetchall()
    conn.close()
    questions = [{'question': row['question'], 'answers': [{'text': row['answer1'], 'correct': bool(row['correct1'])},{'text': row['answer2'], 'correct': bool(row['correct2'])},{'text': row['answer3'], 'correct': bool(row['correct3'])},{'text': row['answer4'], 'correct': bool(row['correct4'])}],'feedback': row['feedback']} for row in rows]
    return jsonify(questions)

@app.route('/save-score', methods=['POST'])
@api_login_required # <-- USE THE NEW DECORATOR HERE TOO
def save_score():
    data = request.get_json()
    user_id, category, score = session['user_id'], data.get('category'), data.get('score')
    if not all([category, isinstance(score, int)]):
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    existing = cursor.execute("SELECT high_score FROM user_progress WHERE user_id = ? AND category = ?", (user_id, category)).fetchone()
    if existing:
        if score > existing[0]: cursor.execute("UPDATE user_progress SET high_score = ?, last_played_on = ? WHERE user_id = ? AND category = ?", (score, datetime.utcnow(), user_id, category))
    else:
        cursor.execute("INSERT INTO user_progress (user_id, category, high_score, last_played_on) VALUES (?, ?, ?, ?)", (user_id, category, score, datetime.utcnow()))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)