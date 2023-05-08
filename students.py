import conda.exceptions
from flask import Flask, render_template, request, redirect
import sqlite3
app = Flask(__name__)

CREDENTIALS = {'admin': 'password'}

def get_db_connection():
    con = sqlite3.connect('hw13.db')
    con.row_factory = sqlite3.Row
    return con

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in CREDENTIALS and password == CREDENTIALS[username]:
            return redirect('/dashboard')
        else:
            error = "Invalid username or password"
            return render_template('login.html', error=error)
    else:
        return render_template('login.html', error=None)
@app.route('/dashboard')
def dashboard():
    con = get_db_connection()
    students = con.execute("SELECT id, first_name, last_name FROM Students")
    quizzes = con.execute("SELECT * FROM Quizzes")
    return render_template('dashboard.html', students=students, quizzes=quizzes)

@app.route('/student/add', methods = ['POST', 'GET'])
def add_student():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        if first_name and last_name:
            with sqlite3.connect('hw13.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Students (first_name, last_name) VALUES (?, ?)", (first_name, last_name))
                con.commit()
                return redirect('/dashboard')
        else:
            error = "Please check that all fields are filled out before submitting"
            return render_template('addStudentPage.html', error=error)
    else:
        return render_template('addStudentPage.html')

@app.route('/student/delete/<id>')
def delete_student(id=None):
    return id

@app.route('/quizzes/add', methods = ['POST', 'GET'])
def add_quizzes():
    if request.method == 'POST':
        subject = request.form['subject']
        num_questions = request.form['num_questions']
        date = request.form['date']
        if subject and num_questions and date:
            with sqlite3.connect('hw13.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Quizzes (subject, num_questions, date) VALUES (?, ?, ?)", (subject, num_questions, date))
                con.commit()
                return redirect('/dashboard')
        else:
            error = "Please check that all fields are filled out before submitting"
            return render_template('addQuizPage.html', error=error)
    else:
        return render_template('addQuizPage.html')

@app.route('/student/<id>')
def view_results(id):
    con = get_db_connection()
    results = con.execute('''SELECT Results.quiz_id, Results.score, Students.id, Quizzes.id FROM Results
    INNER JOIN Students ON Students.id = Results.Student_id 
    INNER JOIN Quizzes ON Quizzes.id = Results.quiz_id WHERE Students.id = ?''', (id))
    student = con.execute("SELECT first_name, last_name FROM Students WHERE id = ?", (id))
    return render_template('quizResults.html', student=student, results=results)

@app.route('/results/add', methods=['POST', 'GET'])
def add_quiz_result():
    con = get_db_connection()
    student_id = con.execute("SELECT id FROM Students")
    quiz_id = con.execute("SELECT id FROM quizzes")
    if request.method == 'POST':
        student = request.form['student']
        quiz = request.form['quiz']
        grade = request.form['grade']
        cur = con.cursor()
#        cur.execute("UPDATE Results SET score = ? WHERE (student_id = ? AND quiz_id = ?)", (grade, student, quiz))
        cur.execute("INSERT INTO Results (student_id, quiz_id, score) VALUES (?, ?, ?)", (grade, student, quiz))
        con.commit()
        return redirect('/dashboard')
    else:
        return render_template('enterScore.html', student_id=student_id, quiz_id=quiz_id)

def read_data():
    f = open('schema.sql', 'r')
    with f:
        data = f.read()
        return data

def init_db():
    con = sqlite3.connect('hw13.db')
    with con:
        cur = con.cursor()
        sql = read_data()
        cur.executescript(sql)
        cur.execute("SELECT * FROM Students")
        students = cur.fetchall()
        if students == []:
            cur.execute("INSERT INTO Students (first_name, last_name) VALUES ('John', 'Smith')")
            cur.execute("INSERT INTO Quizzes (subject, num_questions, date) VALUES ('Python Basics', 5, 'February, 5th, 2015')")
            cur.execute("INSERT INTO Results (student_id, quiz_id, score) VALUES (1, 1, 85)")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)