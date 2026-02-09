from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import re

app = Flask(__name__)
app.secret_key = os.urandom(24)

# In-memory user store (for demonstration purposes)
# In a real application, use a database.
users = {
    'demo': {'password': 'Demo@123'}  # Demo user credentials
}

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('Username and password are required.', 'danger')
        return redirect(url_for('index'))

    if username in users:
        flash('Username already exists.', 'danger')
        return redirect(url_for('index'))

    # Basic password policy
    if len(password) < 8 or not re.search("[a-z]", password) or \
       not re.search("[A-Z]", password) or not re.search("[0-9]", password):
        flash('Password must be at least 8 characters long and contain at least one lowercase letter, one uppercase letter, and one number.', 'danger')
        return redirect(url_for('index'))

    # Hashing will be implemented in a later step
    users[username] = {'password': password}
    flash('Registration successful! Please log in.', 'success')
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('Username and password are required.', 'danger')
        return redirect(url_for('index'))

    user = users.get(username)

    # Hashing will be implemented in a later step
    if user and user['password'] == password:
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid username or password.', 'danger')
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('You need to be logged in to view this page.', 'warning')
        return redirect(url_for('index'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
