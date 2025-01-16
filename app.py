from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os

app = Flask(__name__)

# Secret key for session management
app.config['SECRET_KEY'] = 'your_secret_key'

# Path to credentials file (store it in the root directory for simplicity)
CREDENTIALS_FILE = 'credentials.txt'

# Function to read users from the credentials file (Plain text passwords)
def read_users():
    users = {}
    try:
        with open(CREDENTIALS_FILE, 'r') as file:
            for line in file:
                line = line.strip()
                if line:  # Skip empty lines
                    parts = line.split(',')
                    if len(parts) == 2:  # Ensure correct format
                        username, password = parts
                        users[username] = password  # Store plain text password
    except FileNotFoundError:
        print(f"Error: '{CREDENTIALS_FILE}' not found.")
    return users

# Home route to render home.html
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Read users from the credentials file
        users = read_users()

        # Validate username and password (plain text comparison)
        if username not in users or users[username] != password:
            flash("Invalid username or password.", "error")
            return render_template('home.html')

        # Store the user in the session and redirect to dashboard
        session['username'] = username
        return redirect(url_for('dashboard'))

    return render_template('home.html')

# Dashboard route for logged-in users
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('home'))  # Redirect to login page if the user is not logged in
    
    # Render the dashboard page, passing the logged-in username
    return render_template('dashboard.html', username=session['username'])

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the username from the session
    return redirect(url_for('home'))  # Redirect to the home page (login)

# API route to handle login requests (for AJAX)
@app.route('/login', methods=['POST'])
def login_api():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Read users from the credentials file
    users = read_users()

    # Validate username and password (plain text comparison)
    if username in users and users[username] == password:
        session['username'] = username
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
app.config['DEBUG'] = True
app.config['MAIL_DEBUG'] = True
