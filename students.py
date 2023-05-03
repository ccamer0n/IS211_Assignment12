from flask import Flask, render_template, request, redirect
import sqlite3
app = Flask(__name__)

credentials = {'admin': 'password'}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods = ['POST'])
def login():
    try:
        if request.form['password'] == credentials[request.form['username']]:
            return redirect('/dashboard')
        else:
            error = "Invalid password"
            return render_template('login.html', error=error)
    except:
        error = "Invalid username"
        return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    with sqlite3.connect('hw13.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Students")
        students = cur.fetchall()
        cur.execute("SELECT * FROM Quizzes")
        quizzes = cur.fetchall()

    return render_template('dashboard.html', students=students, quizzes=quizzes)

@app.route('/student')
def student_form():
    return render_template('addStudentPage.html')

@app.route('/student/add', methods = ['POST'])
def add_student():
    try:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        with sqlite3.connect('hw13.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Students (first_name, last_name) VALUES (?, ?)", (first_name, last_name))
            con.commit()
            return redirect('/dashboard')
    except:
        con.rollback()
        error = "Error in insert operation"
        return render_template('addStudentPage.html', error=error)

@app.route('/quizzes')
def quizzes_form():
    return render_template('addQuizPage.html')

@app.route('/quizzes/add', methods = ['POST'])
def add_quizzes():
    try:
        subject = request.form['subject']
        num_questions = request.form['num_questions']
        date = request.form['date']
        with sqlite3.connect('hw13.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Quizzes (subject, num_questions, date) VALUES (?, ?, ?)", (subject, num_questions, date))
            con.commit()
            return redirect('/dashboard')
    except:
        con.rollback()
        error = "Error in insert operation"
        return render_template('addQuizPage.html', error=error)

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