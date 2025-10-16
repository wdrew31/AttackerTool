#!/usr/bin/env python3
"""
Simple Vulnerable Web Application for Testing AttackerTool
WARNING: This application is INTENTIONALLY VULNERABLE - DO NOT deploy to production!
"""

from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)

# Initialize database
def init_db():
    """Create and populate test database"""
    if os.path.exists('test.db'):
        os.remove('test.db')
    
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT
        )
    ''')
    
    # Insert test data
    test_users = [
        (1, 'admin', 'admin123', 'admin@example.com'),
        (2, 'user', 'user123', 'user@example.com'),
        (3, 'test', 'test123', 'test@example.com'),
    ]
    
    cursor.executemany('INSERT INTO users VALUES (?, ?, ?, ?)', test_users)
    conn.commit()
    conn.close()
    print("✓ Database initialized with test data")


# HTML Templates
HOME_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Vulnerable Test App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
        }
        .warning {
            background: #ff6b6b;
            color: white;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .section {
            background: #f8f9fa;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }
        form {
            margin: 10px 0;
        }
        input {
            padding: 8px;
            margin: 5px;
            border: 1px solid #ddd;
            border-radius: 3px;
        }
        button {
            padding: 10px 20px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 3px;
            cursor: pointer;
        }
        button:hover {
            background: #45a049;
        }
        .result {
            background: #fff;
            padding: 15px;
            margin: 15px 0;
            border-left: 4px solid #4CAF50;
        }
        a {
            color: #2196F3;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="warning">
        ⚠️ <strong>WARNING:</strong> This is an INTENTIONALLY VULNERABLE application for testing security tools.
        Never deploy this to production or expose it to the internet!
    </div>
    
    <h1>🎯 Vulnerable Test Application</h1>
    <p>This application contains intentional SQL injection vulnerabilities for testing AttackerTool.</p>
    
    <div class="section">
        <h2>Vulnerable Endpoints:</h2>
        <ul>
            <li><a href="/login">Login Form (POST)</a></li>
            <li><a href="/search">Search Users (GET)</a></li>
            <li><a href="/profile?id=1">User Profile (GET with parameter)</a></li>
        </ul>
    </div>
    
    <div class="section">
        <h2>Test Instructions:</h2>
        <ol>
            <li>Keep this application running</li>
            <li>Start AttackerTool API server</li>
            <li>Run a scan targeting: <code>http://localhost:5001</code></li>
            <li>AttackerTool should detect multiple SQL injection vulnerabilities</li>
        </ol>
    </div>
</body>
</html>
'''

LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Login - Vulnerable Test App</title>
    <style>
        body { font-family: Arial; max-width: 500px; margin: 50px auto; padding: 20px; }
        input { display: block; width: 100%; padding: 10px; margin: 10px 0; }
        button { width: 100%; padding: 12px; background: #4CAF50; color: white; border: none; cursor: pointer; }
        .result { background: #f8f9fa; padding: 15px; margin: 15px 0; }
        .error { color: #d32f2f; }
        a { color: #2196F3; }
    </style>
</head>
<body>
    <h2>🔓 Login Form (Vulnerable)</h2>
    <form method="POST" action="/login">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Login</button>
    </form>
    {% if result %}
        <div class="result">{{ result|safe }}</div>
    {% endif %}
    <p><a href="/">← Back to Home</a></p>
</body>
</html>
'''

SEARCH_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Search Users - Vulnerable Test App</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; }
        input { width: 70%; padding: 10px; }
        button { padding: 10px 20px; background: #4CAF50; color: white; border: none; cursor: pointer; }
        .result { background: #f8f9fa; padding: 15px; margin: 15px 0; }
        table { width: 100%; border-collapse: collapse; margin: 10px 0; }
        th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
        a { color: #2196F3; }
    </style>
</head>
<body>
    <h2>🔍 Search Users (Vulnerable)</h2>
    <form method="GET" action="/search">
        <input type="text" name="q" placeholder="Search by username..." value="{{ query }}">
        <button type="submit">Search</button>
    </form>
    {% if results %}
        <div class="result">
            <h3>Results:</h3>
            <table>
                <tr><th>ID</th><th>Username</th><th>Email</th></tr>
                {% for user in results %}
                <tr><td>{{ user[0] }}</td><td>{{ user[1] }}</td><td>{{ user[3] }}</td></tr>
                {% endfor %}
            </table>
        </div>
    {% endif %}
    {% if error %}
        <div class="result" style="color: #d32f2f;">Error: {{ error }}</div>
    {% endif %}
    <p><a href="/">← Back to Home</a></p>
</body>
</html>
'''

PROFILE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>User Profile - Vulnerable Test App</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; }
        .profile { background: #f8f9fa; padding: 20px; border-radius: 5px; }
        .field { margin: 10px 0; }
        .label { font-weight: bold; color: #666; }
        a { color: #2196F3; }
    </style>
</head>
<body>
    <h2>👤 User Profile (Vulnerable)</h2>
    {% if user %}
        <div class="profile">
            <div class="field"><span class="label">ID:</span> {{ user[0] }}</div>
            <div class="field"><span class="label">Username:</span> {{ user[1] }}</div>
            <div class="field"><span class="label">Email:</span> {{ user[3] }}</div>
        </div>
    {% elif error %}
        <div class="profile" style="color: #d32f2f;">Error: {{ error }}</div>
    {% else %}
        <p>User not found</p>
    {% endif %}
    <p><a href="/">← Back to Home</a></p>
</body>
</html>
'''


# Routes
@app.route('/')
def home():
    """Home page"""
    return render_template_string(HOME_TEMPLATE)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Vulnerable login - SQL Injection via POST"""
    if request.method == 'GET':
        return render_template_string(LOGIN_TEMPLATE)
    
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    # VULNERABLE: String concatenation in SQL query
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    try:
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute(query)  # Vulnerable to SQL injection!
        user = cursor.fetchone()
        conn.close()
        
        if user:
            result = f"✓ Login successful! Welcome {user[1]}"
        else:
            result = "✗ Invalid credentials"
            
    except sqlite3.Error as e:
        result = f"<span class='error'>Database Error: {str(e)}</span>"
    
    return render_template_string(LOGIN_TEMPLATE, result=result)


@app.route('/search')
def search():
    """Vulnerable search - SQL Injection via GET parameter"""
    query = request.args.get('q', '')
    results = None
    error = None
    
    if query:
        # VULNERABLE: String concatenation in SQL query
        sql = f"SELECT * FROM users WHERE username LIKE '%{query}%'"
        
        try:
            conn = sqlite3.connect('test.db')
            cursor = conn.cursor()
            cursor.execute(sql)  # Vulnerable to SQL injection!
            results = cursor.fetchall()
            conn.close()
        except sqlite3.Error as e:
            error = str(e)
    
    return render_template_string(SEARCH_TEMPLATE, query=query, results=results, error=error)


@app.route('/profile')
def profile():
    """Vulnerable profile - SQL Injection via GET parameter"""
    user_id = request.args.get('id', '')
    user = None
    error = None
    
    if user_id:
        # VULNERABLE: String concatenation in SQL query
        query = f"SELECT * FROM users WHERE id = {user_id}"
        
        try:
            conn = sqlite3.connect('test.db')
            cursor = conn.cursor()
            cursor.execute(query)  # Vulnerable to SQL injection!
            user = cursor.fetchone()
            conn.close()
        except sqlite3.Error as e:
            error = str(e)
    
    return render_template_string(PROFILE_TEMPLATE, user=user, error=error)


if __name__ == '__main__':
    print("=" * 60)
    print("  Vulnerable Test Application")
    print("  WARNING: For Testing Only!")
    print("=" * 60)
    print()
    
    # Initialize database
    init_db()
    
    print("\n🚀 Starting server on http://localhost:5001")
    print("📝 Visit http://localhost:5001 for instructions")
    print("\n⚠️  Press Ctrl+C to stop\n")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5001, debug=False)
