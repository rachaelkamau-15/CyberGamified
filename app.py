from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import re
import secrets
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_very_secret_key_here'

# Database initialization function
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Create users table
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
    
    conn.commit()
    conn.close()

# Initialize the database
init_db()


conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM users")
if cursor.fetchone()[0] == 0:  # If no users exist
    cursor.execute(
        "INSERT INTO users (full_name, email, hashed_password, is_admin) VALUES (?, ?, ?, ?)",
        ("Admin", "adminshujaa@gmail.com", generate_password_hash("Admin@123"), 1)
    )
    conn.commit()
conn.close()
# --- Helper Functions ---
def is_password_strong(password):
    if len(password) < 8: return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password): return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password): return False, "Password must contain at least one lowercase letter."
    if not re.search(r"[0-9]", password): return False, "Password must contain at least one number."
    if not re.search(r"[\W_]", password): return False, "Password must contain at least one symbol."
    return True, None

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- Decorators ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "error")
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def api_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify(error="Authentication required. Please log in."), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash("Admin privileges required.", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Main Routes ---
@app.route('/')
def index():
    if 'user_id' in session:
        if session.get('is_admin'):
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    user = conn.execute("SELECT full_name FROM users WHERE id = ?", (session['user_id'],)).fetchone()
    conn.close()
    return render_template('user_dashboard.html', user_full_name=user['full_name'])

@app.route('/my-dashboard')
@login_required
def my_dashboard():
    conn = get_db_connection()
    user = conn.execute("SELECT full_name FROM users WHERE id = ?", (session['user_id'],)).fetchone()
    
    completed_quizzes = conn.execute(
        "SELECT * FROM user_progress WHERE user_id = ?", 
        (session['user_id'],)
    ).fetchall()
    
    all_categories = conn.execute("SELECT DISTINCT category FROM questions").fetchall()
    conn.close()
    
    all_categories = {row['category'] for row in all_categories}
    completed_categories = {quiz['category'] for quiz in completed_quizzes}
    uncompleted_quizzes = list(all_categories - completed_categories)
    
    total_quizzes = len(all_categories)
    average_score = round(sum(q['high_score'] for q in completed_quizzes) / len(completed_quizzes)) if completed_quizzes else 0
    
    return render_template('my_dashboard.html',
                         user_full_name=user['full_name'],
                         completed_quizzes=completed_quizzes,
                         uncompleted_quizzes=uncompleted_quizzes,
                         total_quizzes=total_quizzes,
                         average_score=average_score)

# --- Static Pages ---
@app.route('/about')
def about(): return render_template('about.html')

@app.route('/contact')
def contact(): return render_template('contact.html')

@app.route('/for-whom')
def for_whom(): return render_template('for_whom.html')

# --- Authentication Routes ---
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        
        if not all([full_name, email, password]):
            flash('All fields are required', 'error')
            return redirect(url_for('signup'))
        
        is_strong, error_message = is_password_strong(password)
        if not is_strong:
            flash(error_message, 'error')
            return redirect(url_for('signup'))
        
        hashed_password = generate_password_hash(password)
        conn = get_db_connection()
        
        try:
            # Check if this is the first user (make them admin)
            user_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
            is_admin = 1 if user_count == 0 else 0
            
            conn.execute(
                "INSERT INTO users (full_name, email,  hashed_password, is_admin) VALUES (?, ?, ?, ?)",
                (full_name, email, hashed_password, is_admin)
            )
            conn.commit()
            
            user_id = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()[0]
            session['user_id'] = user_id
            session['is_admin'] = is_admin
            
            flash('Account created successfully!', 'success')
            return redirect(url_for('admin_dashboard' if is_admin else 'dashboard'))
            
        except sqlite3.IntegrityError:
            flash('Email address already registered', 'error')
        finally:
            conn.close()
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        hashed_password = generate_password_hash(password)
        user = conn.execute(
            "SELECT id, hashed_password, is_admin FROM users WHERE email = ?", 
            (email,)
        ).fetchone()
        conn.close()
        
        if user and check_password_hash(user['hashed_password'], password):
            session['user_id'] = user['id']
            session['is_admin'] = user['is_admin']
            flash('Logged in successfully!', 'success')
            return redirect(url_for('admin_dashboard' if user['is_admin'] else 'dashboard'))
        
        flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        conn = get_db_connection()
        user = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
        
        if user:
            token = secrets.token_urlsafe(32)
            expiration = datetime.utcnow() + timedelta(hours=1)
            conn.execute(
                "UPDATE users SET reset_token = ?, reset_token_expiration = ? WHERE id = ?",
                (token, expiration, user['id'])
            )
            conn.commit()
            
            # In production, you would send an email here
            reset_link = url_for('reset_password', token=token, _external=True)
            print(f"Password reset link: {reset_link}")  # For development only
        
        flash('If an account exists with that email, a reset link has been generated.', 'info')
        conn.close()
        return redirect(url_for('forgot_password'))
    
    return render_template('forgot_password.html')

# @app.route('/reset-password/<token>', methods=['GET', 'POST'])
# def reset_password(token):
#     conn = get_db_connection()
#     user = conn.execute(
#         "SELECT id, reset_token_expiration FROM users WHERE reset_token = ?", 
#         (token,)
#     ).fetchone()
    
#     if not user or datetime.utcnow() > datetime.fromisoformat(user['reset_token_expiration']):
#         flash('Invalid or expired reset token.', 'error')
#         conn.close()
#         return redirect(url_for('forgot_password'))
    
#     if request.method == 'POST':
#         password = request.form['password']
#         is_strong, error_message = is_password_strong(password)
        
#         if not is_strong:
#             conn.close()
#             return render_template('reset_password.html', token=token, error=error_message)
        
#         hashed_password = generate_password_hash(password)
#         conn.execute(
#             "UPDATE users SET password = ?, reset_token = NULL, reset_token_expiration = NULL WHERE id = ?",
#             (hashed_password, user['id'])
#         )
#         conn.commit()
#         conn.close()
        
#         flash('Your password has been updated! Please log in.', 'success')
#         return redirect(url_for('login'))
    
#     conn.close()
#     return render_template('reset_password.html', token=token)

# --- Quiz API Routes ---
@app.route('/api/questions/<category>')
@api_login_required
def get_questions(category):
    conn = get_db_connection()
    questions = conn.execute(
        "SELECT * FROM questions WHERE category = ?", 
        (category,)
    ).fetchall()
    conn.close()
    
    formatted_questions = []
    for q in questions:
        formatted_questions.append({
            'id': q['id'],
            'question': q['question'],
            'answers': [
                {'text': q['answer1'], 'correct': bool(q['correct1'])},
                {'text': q['answer2'], 'correct': bool(q['correct2'])},
                {'text': q['answer3'], 'correct': bool(q['correct3'])},
                {'text': q['answer4'], 'correct': bool(q['correct4'])}
            ],
            'feedback': q['feedback']
        })
    
    return jsonify(formatted_questions)

@app.route('/api/save-score', methods=['POST'])
@api_login_required
def save_score():
    data = request.get_json()
    if not data or 'category' not in data or 'score' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    user_id = session['user_id']
    category = data['category']
    score = int(data['score'])
    
    conn = get_db_connection()
    existing = conn.execute(
        "SELECT high_score FROM user_progress WHERE user_id = ? AND category = ?",
        (user_id, category)
    ).fetchone()
    
    if existing:
        if score > existing['high_score']:
            conn.execute(
                "UPDATE user_progress SET high_score = ?, last_played_on = ? WHERE user_id = ? AND category = ?",
                (score, datetime.utcnow(), user_id, category)
            )
    else:
        conn.execute(
            "INSERT INTO user_progress (user_id, category, high_score, last_played_on) VALUES (?, ?, ?, ?)",
            (user_id, category, score, datetime.utcnow())
        )
    
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# --- Admin Routes ---
@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    conn = get_db_connection()
    
    stats = {
        'users': conn.execute("SELECT COUNT(*) FROM users").fetchone()[0],
        'questions': conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0],
        'categories': conn.execute("SELECT COUNT(DISTINCT category) FROM questions").fetchone()[0],
        'attempts': conn.execute("SELECT COUNT(*) FROM user_progress").fetchone()[0]
    }
    
    recent_activity = conn.execute('''
        SELECT u.full_name, u.email, up.category, up.high_score, up.last_played_on
        FROM user_progress up
        JOIN users u ON up.user_id = u.id
        ORDER BY up.last_played_on DESC
        LIMIT 5
    ''').fetchall()
    
    conn.close()
    return render_template('admin/dashboard.html', stats=stats, recent_activity=recent_activity)

@app.route('/admin/users')
@admin_required
def admin_users():
    search = request.args.get('search', '')
    conn = get_db_connection()
    
    query = "SELECT id, full_name, email, created_at FROM users"
    params = []
    
    if search:
        query += " WHERE email LIKE ? OR full_name LIKE ?"
        params = [f'%{search}%', f'%{search}%']
    
    users = conn.execute(query, params).fetchall()
    conn.close()
    return render_template('admin/users.html', users=users, search=search)

@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    if user_id == session.get('user_id'):
        flash("Cannot delete your own account", "error")
        return redirect(url_for('admin_users'))
    
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.execute("DELETE FROM user_progress WHERE user_id = ?", (user_id,))
        conn.commit()
        flash('User deleted successfully', 'success')
    except sqlite3.Error as e:
        conn.rollback()
        flash(f'Error deleting user: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('admin_users'))

@app.route('/admin/questions')
@admin_required
def admin_questions():
    category = request.args.get('category', '')
    conn = get_db_connection()
    
    query = "SELECT id, category, question FROM questions"
    params = []
    
    if category:
        query += " WHERE category = ?"
        params = [category]
    
    questions = conn.execute(query, params).fetchall()
    categories = conn.execute("SELECT DISTINCT category FROM questions").fetchall()
    conn.close()
    
    return render_template('admin/questions.html',
                         questions=questions,
                         categories=categories,
                         current_category=category)

@app.route('/admin/questions/add', methods=['GET', 'POST'])
@admin_required
def add_question():
    if request.method == 'POST':
        data = request.form
        correct_count = sum(1 for i in range(1, 5) if data.get(f'correct{i}'))
        
        if correct_count != 1:
            flash("Exactly one answer must be marked as correct", "error")
            return redirect(url_for('add_question'))
        
        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT INTO questions (
                    category, question,
                    answer1, correct1,
                    answer2, correct2,
                    answer3, correct3,
                    answer4, correct4,
                    feedback
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['category'], data['question'],
                data['answer1'], 1 if data.get('correct1') else 0,
                data['answer2'], 1 if data.get('correct2') else 0,
                data['answer3'], 1 if data.get('correct3') else 0,
                data['answer4'], 1 if data.get('correct4') else 0,
                data['feedback']
            ))
            conn.commit()
            flash('Question added successfully', 'success')
            return redirect(url_for('admin_questions'))
        except sqlite3.Error as e:
            conn.rollback()
            flash(f'Error adding question: {str(e)}', 'error')
        finally:
            conn.close()
    
    return render_template('admin/add_question.html')

@app.route('/admin/questions/<int:question_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_question(question_id):
    conn = get_db_connection()
    
    if request.method == 'POST':
        data = request.form
        correct_count = sum(1 for i in range(1, 5) if data.get(f'correct{i}'))
        
        if correct_count != 1:
            flash("Exactly one answer must be marked as correct", "error")
            return redirect(url_for('edit_question', question_id=question_id))
        
        try:
            conn.execute('''
                UPDATE questions SET
                    category = ?,
                    question = ?,
                    answer1 = ?, correct1 = ?,
                    answer2 = ?, correct2 = ?,
                    answer3 = ?, correct3 = ?,
                    answer4 = ?, correct4 = ?,
                    feedback = ?
                WHERE id = ?
            ''', (
                data['category'], data['question'],
                data['answer1'], 1 if data.get('correct1') else 0,
                data['answer2'], 1 if data.get('correct2') else 0,
                data['answer3'], 1 if data.get('correct3') else 0,
                data['answer4'], 1 if data.get('correct4') else 0,
                data['feedback'], question_id
            ))
            conn.commit()
            flash('Question updated successfully', 'success')
            return redirect(url_for('admin_questions'))
        except sqlite3.Error as e:
            conn.rollback()
            flash(f'Error updating question: {str(e)}', 'error')
        finally:
            conn.close()
    
    question = conn.execute("SELECT * FROM questions WHERE id = ?", (question_id,)).fetchone()
    conn.close()
    
    if not question:
        flash('Question not found', 'error')
        return redirect(url_for('admin_questions'))
    
    return render_template('admin/edit_question.html', question=question)

@app.route('/admin/questions/<int:question_id>/delete', methods=['POST'])
@admin_required
def delete_question(question_id):
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM questions WHERE id = ?", (question_id,))
        conn.commit()
        flash('Question deleted successfully', 'success')
    except sqlite3.Error as e:
        conn.rollback()
        flash(f'Error deleting question: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('admin_questions'))

@app.route('/admin/analytics')
@admin_required
def admin_analytics():
    conn = get_db_connection()
    
    # Quiz performance by category
    categories = conn.execute('''
        SELECT 
            category,
            COUNT(*) as attempts,
            ROUND(AVG(high_score), 1) as avg_score,
            MAX(high_score) as max_score
        FROM user_progress
        GROUP BY category
        ORDER BY avg_score DESC
    ''').fetchall()
    
    # User engagement stats
    engagement = conn.execute('''
    SELECT
        COUNT(DISTINCT user_id) as active_users,
        COUNT(*) as total_attempts,
        -- Use COALESCE to default NULL averages to 0
        ROUND(COALESCE(AVG(high_score), 0), 1) as avg_score
    FROM user_progress
''').fetchone()
    
    conn.close()
    return render_template('admin/analytics.html',
                         categories=categories,
                         engagement=engagement)

if __name__ == '__main__':
    app.run(debug=True)