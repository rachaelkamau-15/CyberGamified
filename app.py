# File: app.py
from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

# This route now serves the new landing page
@app.route('/')
def landing():
    return render_template('landing.html')

# This is the "Home" page with the game categories
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

# Route for the Login page
@app.route('/login.html')
def login():
    return render_template('login.html')

# Route for the Signup page
@app.route('/signup.html')
def signup():
    return render_template('signup.html')

# This route handles fetching questions for a specific category
@app.route('/questions/<category>')
def get_questions(category):
    conn = sqlite3.connect('questions.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions WHERE category = ?", (category,))
    rows = cursor.fetchall()
    conn.close()

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