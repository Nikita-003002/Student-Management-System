import os
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

db = mysql.connector.connect(
        host="localhost",
            user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                    database=os.getenv('DB_NAME')
)

cursor = db.cursor()

@app.route('/')
def index():
    cursor.execute("SELECT * FROM student")
    student = cursor.fetchall()
    return render_template("index.html", student=student)


@app.route('/add', methods=['POST'])
def add_students():
    name = request.form['name']
    age = request.form['age']
    grade = request.form['grade']
    cursor.execute("INSERT INTO student (name, age, grade) VALUES (%s, %s, %s)", (name, age, grade))
    db.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_student(id):
    cursor.execute("DELETE FROM student WHERE id=%s", (id,))
    db.commit()
    return redirect(url_for('index'))


if __name__  == '__main__':
    app.run(debug=True)