from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = '50k'

# DB connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        database='2',
        user='root',
        password=''
    )

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        if user:
            return redirect('/dashboard')
        else:
            flash('Invalid login details', 'danger')
        cursor.close()
        conn.close()
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = (
            request.form['full_name'],
            request.form['email'],
            request.form['username'],
            request.form['password'],
            request.form['gender'],
            request.form['contact_number'],
            request.form['address'],
            request.form['date_of_birth'],
            request.form['position']
        )
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (full_name, email, username, password, gender, contact_number, address, date_of_birth, position)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, data)
        conn.commit()
        cursor.close()
        conn.close()
        flash('Account created!', 'success')
        return redirect('/login')
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('dashboard.html', users=users)

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        data = (
            request.form['full_name'],
            request.form['email'],
            request.form['username'],
            request.form['password'],
            request.form['gender'],
            request.form['contact_number'],
            request.form['address'],
            request.form['date_of_birth'],
            request.form['position']
        )
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (full_name, email, username, password, gender, contact_number, address, date_of_birth, position)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, data)
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/dashboard')
    return render_template('add_user.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id=%s", (id,))
    user = cursor.fetchone()

    if request.method == 'POST':
        data = (
            request.form['full_name'],
            request.form['email'],
            request.form['username'],
            request.form['password'],
            request.form['gender'],
            request.form['contact_number'],
            request.form['address'],
            request.form['date_of_birth'],
            request.form['position'],
            id
        )
        cursor.execute("""
            UPDATE users SET full_name=%s, email=%s, username=%s, password=%s,
            gender=%s, contact_number=%s, address=%s, date_of_birth=%s, position=%s
            WHERE id=%s
        """, data)
        conn.commit()
        return redirect('/dashboard')

    return render_template('edit_user.html', user=user)

@app.route('/delete/<int:id>')
def delete_user(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/dashboard')

if __name__ == '__main__':
    app.run(debug=True)
