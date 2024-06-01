from flask import Flask, render_template, redirect, url_for, request, session, flash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# Dummy user data for demonstration
USERS = {
    "user1": "p1",
    "user2": "p2"
}


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USERS and USERS[username] == password:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('login_successful'))
        else:
            flash('Invalid credentials, please try again.', 'danger')
    return render_template("login.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['confirm_password']
        if username in USERS:
            flash('Username already exists. Please choose a different username.', 'danger')
        else:
            USERS[username] = password
            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template("signup.html")


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


if __name__ == "__main__":
    app.run(port=9999, debug=True)
