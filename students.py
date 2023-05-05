from flask import Flask, render_template, request, redirect
import sqlite3
app = Flask(__name__)

CREDENTIALS = {'admin': 'password'}

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
    with sqlite3.connect('hw13.db') as con:
        cur = con.cursor()
        cur.execute("SELECT id, first_name, last_name FROM Students")
        students = cur.fetchall()
        cur.execute("SELECT * FROM Quizzes")
        quizzes = cur.fetchall()

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

@app.route('/student/delete/<student_id>')
def delete_student(student_id=None):
    return student_id

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
    return id

@app.route('/results/add')
def add_quiz_result():
    pass

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
    app.run()