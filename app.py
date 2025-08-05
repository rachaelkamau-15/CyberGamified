# File: app.py
from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

# This route serves the main page (index.html)
@app.route('/')
def index():
    return render_template('index.html')

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
                {'text': row['answer2'], 'correct': bool(row['correct2'])}
            ],
            'feedback': row['feedback']
        })
        
    return jsonify(questions)

if __name__ == '__main__':
    app.run(debug=True)
    