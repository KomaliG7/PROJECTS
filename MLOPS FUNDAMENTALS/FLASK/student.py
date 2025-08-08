from flask import Flask, render_template, request
import sqlite3

def init_db():
    conn=sqlite3.connect('student.db')
    cursor=conn.cursor()
    cursor.execute('''
                   create table student(
                   id int,
                   name text,
                   email text,
                   phone int,
                   address text
                   )
                ''')
    conn.commit()
    conn.close()
init_db()

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template('homepage.html')

@app.route('/add', methods=['get','post'])
def addStudent():
    if request.method=='post':
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        conn=sqlite3.connect('student.db')
        cursor=conn.cursor()
        cursor.execute("insert into Student(id,name,email,phone,address)values(?,?,?,?,?)",(id,name,email,phone,address))
        conn.commit()
        conn.close()
    return render_template('homepage.html')

if __name__=='__main__':
    app.run(debug=True)