# db_setup.py
import sqlite3

def create_database():
    conn = sqlite3.connect('student_recognition.db')
    cursor = conn.cursor()

    # Create students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gpa REAL NOT NULL,
            consistency_score REAL NOT NULL,
            hackathon_participation INTEGER NOT NULL,
            paper_presentations INTEGER NOT NULL,
            contributions INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()