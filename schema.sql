CREATE TABLE IF NOT EXISTS Students (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT);

CREATE TABLE IF NOT EXISTS Quizzes (id INTEGER PRIMARY KEY, subject TEXT, num_questions INT, date TEXT);

CREATE TABLE IF NOT EXISTS Results (student_id INT, quiz_id INT, score INT, PRIMARY KEY (student_id, quiz_id));
