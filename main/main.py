from flask import Flask, render_template, redirect, url_for, request, session, flash
import sqlite3
import os
import hashlib

app = Flask(__name__)
app.secret_key = os.urandom(24)


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


def init_db2(username):
    conn = get_db_connection()
    curr = conn.cursor()
    curr.execute(
        f'CREATE TABLE IF NOT EXISTS {username}(name TEXT NOT NULL PRIMARY KEY, html TEXT NOT NULL, css TEXT NOT NULL, '
        f'js TEXT NOT NULL)')
    conn.commit()
    conn.close()


def get_db_connection():
    conn = sqlite3.connect('users.db')
    return conn


def hash_password(password):
    password_bytes = password.encode('utf-8')
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(password_bytes)
    hashed_password = hash_algorithm.hexdigest()
    return hashed_password


def get_user_by_username(username):
    conn = get_db_connection()
    curr = conn.cursor()
    curr.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = curr.fetchone()
    conn.close()
    return user


def fetch_code_from_database(username, proj_name):
    conn = get_db_connection()
    curr = conn.cursor()
    curr.execute(f"SELECT html, css, js FROM {username} WHERE name=?", (proj_name,))
    row = curr.fetchone()
    conn.close()

    if row:
        return row
    else:
        return None


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
        username = session['username']
        init_db2(username=username)
        conn = get_db_connection()
        curr = conn.cursor()
        curr.execute(f"SELECT name FROM {username}")
        databases = curr.fetchall()
        conn.close()
        return render_template("main.html", username=session['username'], databases=databases)
    else:
        flash('You are not logged in.', 'danger')
        return redirect(url_for('login'))


@app.route("/projects")
def create_project():
    if 'username' in session:
        return render_template("create_project.html")
    else:
        flash('You are not logged in.', 'danger')
        return redirect(url_for('login'))


@app.route("/load/<proj_name>")
def load(proj_name):
    if 'username' in session:
        html_code, css_code, js_code = fetch_code_from_database(session['username'], proj_name)

        if html_code or css_code or js_code:
            return render_template("load_file.html", name=proj_name, html_code=html_code, css_code=css_code,
                                   js_code=js_code)
        else:
            return "Error: Project not found."
    else:
        flash('You are not logged in.', 'danger')
        return redirect(url_for('login'))


@app.route("/delete/<proj_name>", methods=['GET', 'POST'])
def delete(proj_name):
    if 'username' in session:
        username = session['username']
        conn = get_db_connection()
        curr = conn.cursor()
        try:
            curr.execute(f'DELETE FROM {username} WHERE name = ?', (proj_name,))
            conn.commit()
        finally:
            conn.close()
            return redirect(url_for('login_successful'))
    else:
        flash('You are not logged in.', 'danger')
        return redirect(url_for('login'))


@app.route("/save", methods=['POST'])
def save_project():
    if 'username' not in session:
        flash('You are not logged in.', 'danger')
        return redirect(url_for('login'))

    username = session['username']
    data = request.get_json()
    proj_name = data.get('name')
    html = data.get('html')
    css = data.get('css')
    js = data.get('js')

    conn = get_db_connection()
    curr = conn.cursor()
    try:
        curr.execute(f'INSERT INTO {username} (name, html, css, js) VALUES (?, ?, ?, ?)',
                     (proj_name, html, css, js))
        conn.commit()
        flash('Project saved successfully!', 'success')
        return redirect(url_for('login_successful'))
    except sqlite3.IntegrityError:
        flash('A project with this name already exists.', 'danger')
        return redirect(url_for('login_successful'))
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'danger')
        return redirect(url_for('login_successful'))
    finally:
        conn.close()


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
