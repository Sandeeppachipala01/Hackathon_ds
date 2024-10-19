# app.py
from flask import Flask, request, jsonify
import sqlite3
import numpy as np
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('student_recognition.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/add_student', methods=['POST'])
def add_student():
    data = request.json
    name = data['name']
    gpa = data['gpa']
    consistency_score = data['consistency_score']
    hackathon_participation = data['hackathon_participation']
    paper_presentations = data['paper_presentations']
    contributions = data['contributions']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO students (name, gpa, consistency_score, hackathon_participation, paper_presentations, contributions)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, gpa, consistency_score, hackathon_participation, paper_presentations, contributions))
    
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Student added successfully!"}), 201

@app.route('/rank_students', methods=['GET'])
def rank_students():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()

    # Prepare data for ranking
    X = []
    for student in students:
        X.append([
            student['gpa'],
            student['consistency_score'],
            student['hackathon_participation'],
            student['paper_presentations'],
            student['contributions']
        ])
    
    # Simple linear regression model for ranking
    model = LinearRegression()
    
    # Dummy target variable (for demonstration purposes)
    y = np.arange(len(X))  # Just using indices as targets

    model.fit(X, y)
    
    rankings = model.predict(X)
    
    # Combine rankings with student names and sort
    ranked_students = sorted(zip(students, rankings), key=lambda x: x[1], reverse=True)
    
    top_students = [student[0]['name'] for student in ranked_students[:3]]
    
    conn.close()
    
    return jsonify({"top_students": top_students}), 200

if __name__ == "__main__":
    app.run(debug=True)