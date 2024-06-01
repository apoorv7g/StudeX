from flask import Flask, render_template, redirect, url_for, request, session, flash
import sqlite3
import os
import hashlib

app = Flask(__name__)
app.secret_key = os.urandom(24)


# Initialize the database
def init_db():
    conn = sqlite3.connect('users.db')
    curr = conn.cursor()
    curr.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# Get database connection
def get_db_connection():
    conn = sqlite3.connect('users.db')
    return conn


# Hash password
def hash_password(password):
    password_bytes = password.encode('utf-8')
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(password_bytes)
    hashed_password = hash_algorithm.hexdigest()
    return hashed_password


# Check if username exists
def get_user_by_username(username):
    conn = get_db_connection()
    curr = conn.cursor()
    curr.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = curr.fetchone()
    conn.close()
    return user


# Routes
@app.route("/")
def main():
    return redirect(url_for('index'))


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        if user and user[1] == hash_password(password):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('login_successful'))
        else:
            flash('Invalid credentials, please try again.', 'danger')
    return render_template("login.html")


@app.route("/login/successful")
def login_successful():
    if 'username' in session:
        return render_template("main.html", username=session['username'])
    else:
        flash('You are not logged in.', 'danger')
        return redirect(url_for('login'))


@app.route("/logout")
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password == confirm_password:
            hashed_password = hash_password(password)
            conn = get_db_connection()
            curr = conn.cursor()
            try:
                curr.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                             (username, hashed_password))
                conn.commit()
                flash('Account created successfully! Please log in.', 'success')
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash('Username already exists. Please choose another.', 'danger')
            finally:
                conn.close()
        else:
            flash('Passwords do not match. Please try again.', 'danger')
    return render_template("signup.html")


if __name__ == "__main__":
    init_db()
    app.run(port=9999, debug=True)
