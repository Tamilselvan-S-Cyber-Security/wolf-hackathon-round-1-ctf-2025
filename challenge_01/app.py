#!/usr/bin/env python3
"""
Challenge 1: SQL Injection API
Difficulty: Beginner
Port: 5001
Flag: WOLF{SQL01}
"""

from flask import Flask, request, jsonify, render_template_string
import sqlite3
import os

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT DEFAULT 'user',
            secret_note TEXT
        )
    ''')
    
    # Insert sample data
    users = [
        ('admin', 'admin123', 'admin', 'WOLF{SQL01}'),
        ('john', 'password123', 'user', 'This is a secret note for John'),
        ('alice', 'alice123', 'user', 'Alice loves security'),
        ('bob', 'bob456', 'moderator', 'Bob is a moderator')
    ]
    
    for user in users:
        cursor.execute('INSERT INTO users (username, password, role, secret_note) VALUES (?, ?, ?, ?)', user)
    
    conn.commit()
    return conn

# Global database connection
db_conn = init_db()

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Challenge 1: SQL Injection API</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Serif+Pro:wght@400;600&display=swap');
        
        body { 
            font-family: 'Source Serif Pro', serif; 
            margin: 0; 
            padding: 20px; 
            background: #f5f5f5; 
            color: #2c2c2c;
            line-height: 1.6;
        }
        .container { 
            max-width: 900px; 
            margin: 0 auto; 
            background: white; 
            padding: 40px; 
            border: 3px solid #000; 
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }
        .newspaper-header {
            text-align: center;
            border-bottom: 3px double #000;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        .newspaper-title {
            font-family: 'Playfair Display', serif;
            font-size: 2.5rem;
            font-weight: 900;
            margin: 0;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        .newspaper-subtitle {
            font-size: 1.1rem;
            margin: 10px 0 0 0;
            font-style: italic;
        }
        .challenge { 
            background: #f8f8f8; 
            padding: 25px; 
            border: 2px solid #000; 
            margin: 25px 0; 
            border-left: 8px solid #000;
        }
        .challenge h2 {
            font-family: 'Playfair Display', serif;
            font-size: 1.8rem;
            margin: 0 0 15px 0;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .api-form { 
            background: #ffffff; 
            padding: 25px; 
            border: 2px solid #000; 
            margin: 25px 0; 
        }
        .api-form h3 {
            font-family: 'Playfair Display', serif;
            font-size: 1.4rem;
            margin: 0 0 20px 0;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        input, button, textarea { 
            padding: 12px; 
            margin: 8px 0; 
            border: 2px solid #000; 
            font-family: 'Source Serif Pro', serif;
            font-size: 1rem;
        }
        input, textarea {
            width: 100%;
            box-sizing: border-box;
        }
        button { 
            background: #000; 
            color: white; 
            cursor: pointer; 
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
        }
        button:hover { 
            background: #333; 
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }
        .result { 
            background: #f8f8f8; 
            padding: 20px; 
            border: 2px solid #000; 
            margin: 15px 0; 
            font-family: 'Courier New', monospace;
        }
        .hint {
            background: #fff8dc;
            padding: 20px;
            border: 2px solid #000;
            margin: 20px 0;
            border-left: 8px solid #000;
        }
        .hint h3 {
            font-family: 'Playfair Display', serif;
            font-size: 1.3rem;
            margin: 0 0 10px 0;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* Hints Button and Popup */
        .hints-button {
            position: fixed;
            top: 20px;
            left: 20px;
            background: #000;
            color: white;
            border: 2px solid #000;
            padding: 10px 15px;
            cursor: pointer;
            font-family: 'Source Serif Pro', serif;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            z-index: 1000;
            transition: all 0.3s ease;
        }
        
        .hints-button:hover {
            background: #333;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }
        
        .hints-popup {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            border: 3px solid #000;
            padding: 20px;
            max-width: 400px;
            max-height: 500px;
            overflow-y: auto;
            z-index: 1001;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            display: none;
        }
        
        .hints-popup h3 {
            font-family: 'Playfair Display', serif;
            font-size: 1.5rem;
            margin: 0 0 15px 0;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #000;
        }
        
        .hints-content {
            font-family: 'Source Serif Pro', serif;
            line-height: 1.6;
            color: #2c2c2c;
        }
        
        .hints-content h4 {
            font-family: 'Playfair Display', serif;
            font-size: 1.2rem;
            margin: 15px 0 8px 0;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #000;
        }
        
        .hints-content ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        
        .hints-content li {
            margin: 5px 0;
        }
        
        .hints-content code {
            background: #f8f8f8;
            padding: 2px 6px;
            border: 1px solid #000;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
        }
        
        .close-button {
            position: absolute;
            top: 10px;
            right: 15px;
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: #000;
            font-weight: bold;
            padding: 0;
            width: 25px;
            height: 25px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .close-button:hover {
            color: #666;
        }
        
        .popup-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
            display: none;
        }
        
                /* Responsive Design - Optimized for Perfect Fit */
        @media (max-width: 1200px) {
            .container {
                max-width: 95%;
                padding: 30px;
            }
            .hints-popup {
                max-width: 90%;
                max-height: 85%;
                left: 50%;
                transform: translateX(-50%);
            }
        }
        
        @media (max-width: 768px) {
            body {
                padding: 10px;
                margin: 0;
            }
            .container {
                padding: 20px;
                border-width: 2px;
                margin: 0 auto;
                width: 100%;
                box-sizing: border-box;
            }
            .newspaper-title {
                font-size: 2rem;
                letter-spacing: 1px;
                word-wrap: break-word;
            }
            .newspaper-subtitle {
                font-size: 1rem;
                word-wrap: break-word;
            }
            .challenge, .api-form, .hint {
                padding: 20px;
                margin: 20px 0;
                box-sizing: border-box;
            }
            .challenge h2, .api-form h3 {
                font-size: 1.5rem;
                word-wrap: break-word;
            }
            input, textarea, button {
                padding: 10px;
                font-size: 0.9rem;
                width: 100%;
                box-sizing: border-box;
            }
            .hints-button {
                top: 15px;
                left: 15px;
                padding: 8px 12px;
                font-size: 0.8rem;
                z-index: 1001;
                position: fixed;
            }
            .hints-popup {
                max-width: 95%;
                max-height: 90%;
                padding: 20px;
                left: 50%;
                top: 50%;
                transform: translate(-50%, -50%);
                box-sizing: border-box;
                overflow-y: auto;
            }
            .hints-popup h3 {
                font-size: 1.3rem;
                word-wrap: break-word;
                margin-top: 0;
            }
            .hints-content h4 {
                font-size: 1.1rem;
                word-wrap: break-word;
            }
        }
        
        @media (max-width: 480px) {
            body {
                padding: 5px;
                margin: 0;
            }
            .container {
                padding: 15px;
                margin: 0;
                width: 100%;
                box-sizing: border-box;
            }
            .newspaper-title {
                font-size: 1.5rem;
                letter-spacing: 0.5px;
                word-wrap: break-word;
                line-height: 1.2;
            }
            .challenge, .api-form, .hint {
                padding: 15px;
                margin: 15px 0;
                box-sizing: border-box;
            }
            .challenge h2, .api-form h3 {
                font-size: 1.2rem;
                word-wrap: break-word;
            }
            input, textarea, button {
                padding: 8px;
                font-size: 0.8rem;
                width: 100%;
                box-sizing: border-box;
            }
            .result {
                padding: 15px;
                font-size: 0.8rem;
                word-wrap: break-word;
                overflow-wrap: break-word;
            }
            .hints-button {
                top: 10px;
                left: 10px;
                padding: 6px 10px;
                font-size: 0.7rem;
                z-index: 1001;
                position: fixed;
            }
            .hints-popup {
                max-width: 95%;
                max-height: 85%;
                padding: 15px;
                margin: 10px;
                left: 50%;
                top: 50%;
                transform: translate(-50%, -50%);
                box-sizing: border-box;
                overflow-y: auto;
            }
            .hints-popup h3 {
                font-size: 1.1rem;
                margin-bottom: 10px;
                word-wrap: break-word;
                line-height: 1.2;
            }
            .hints-content h4 {
                font-size: 0.9rem;
                margin: 10px 0 5px 0;
                word-wrap: break-word;
            }
            .hints-content {
                font-size: 0.8rem;
                word-wrap: break-word;
                overflow-wrap: break-word;
            }
            .hints-content ul {
                padding-left: 15px;
                word-wrap: break-word;
            }
            .hints-content code {
                font-size: 0.7rem;
                padding: 1px 4px;
                word-wrap: break-word;
                overflow-wrap: break-word;
            }
            .close-button {
                top: 8px;
                right: 12px;
                font-size: 1.2rem;
                width: 20px;
                height: 20px;
                z-index: 1002;
            }
        }
        
        @media (max-width: 360px) {
            .hints-button {
                top: 8px;
                left: 8px;
                padding: 5px 8px;
                font-size: 0.6rem;
            }
            .hints-popup {
                max-width: 98%;
                max-height: 90%;
                padding: 12px;
                margin: 5px;
                left: 50%;
                top: 50%;
                transform: translate(-50%, -50%);
            }
            .hints-popup h3 {
                font-size: 1rem;
                margin-bottom: 8px;
                word-wrap: break-word;
                line-height: 1.1;
            }
            .hints-content h4 {
                font-size: 0.8rem;
                margin: 8px 0 4px 0;
                word-wrap: break-word;
            }
            .hints-content {
                font-size: 0.7rem;
                line-height: 1.4;
                word-wrap: break-word;
                overflow-wrap: break-word;
            }
            .hints-content ul {
                padding-left: 12px;
                word-wrap: break-word;
            }
            .hints-content li {
                margin: 3px 0;
                word-wrap: break-word;
            }
            .hints-content code {
                font-size: 0.6rem;
                padding: 1px 3px;
                word-wrap: break-word;
                overflow-wrap: break-word;
            }
            .close-button {
                top: 6px;
                right: 10px;
                font-size: 1rem;
                width: 18px;
                height: 18px;
            }
        }
        
        @media (max-width: 320px) {
            body {
                padding: 2px;
                margin: 0;
            }
            .container {
                padding: 10px;
                margin: 0;
                width: 100%;
                box-sizing: border-box;
            }
            .hints-button {
                top: 5px;
                left: 5px;
                padding: 4px 6px;
                font-size: 0.5rem;
            }
            .hints-popup {
                max-width: 99%;
                max-height: 95%;
                padding: 10px;
                margin: 2px;
                left: 50%;
                top: 50%;
                transform: translate(-50%, -50%);
            }
            .hints-popup h3 {
                font-size: 0.9rem;
                margin-bottom: 6px;
                word-wrap: break-word;
                line-height: 1.1;
            }
            .hints-content h4 {
                font-size: 0.7rem;
                margin: 6px 0 3px 0;
                word-wrap: break-word;
            }
            .hints-content {
                font-size: 0.6rem;
                line-height: 1.3;
                word-wrap: break-word;
                overflow-wrap: break-word;
            }
            .hints-content ul {
                padding-left: 10px;
                word-wrap: break-word;
            }
            .hints-content li {
                margin: 2px 0;
                word-wrap: break-word;
            }
            .hints-content code {
                font-size: 0.5rem;
                padding: 1px 2px;
                word-wrap: break-word;
                overflow-wrap: break-word;
            }
            .close-button {
                top: 4px;
                right: 8px;
                font-size: 0.8rem;
                width: 16px;
                height: 16px;
            }
        }
        
        /* Additional mobile optimizations */
        @media (max-width: 280px) {
            .hints-button {
                top: 3px;
                left: 3px;
                padding: 3px 5px;
                font-size: 0.4rem;
            }
            .hints-popup {
                max-width: 100%;
                max-height: 98%;
                padding: 8px;
                margin: 1px;
                left: 50%;
                top: 50%;
                transform: translate(-50%, -50%);
            }
            .hints-popup h3 {
                font-size: 0.8rem;
                margin-bottom: 4px;
                word-wrap: break-word;
                line-height: 1.0;
            }
            .hints-content h4 {
                font-size: 0.6rem;
                margin: 4px 0 2px 0;
                word-wrap: break-word;
            }
            .hints-content {
                font-size: 0.5rem;
                line-height: 1.2;
                word-wrap: break-word;
                overflow-wrap: break-word;
            }
            .hints-content ul {
                padding-left: 8px;
                word-wrap: break-word;
            }
            .hints-content li {
                margin: 1px 0;
                word-wrap: break-word;
            }
            .hints-content code {
                font-size: 0.4rem;
                padding: 1px 1px;
                word-wrap: break-word;
                overflow-wrap: break-word;
            }
            .close-button {
                top: 2px;
                right: 6px;
                font-size: 0.7rem;
                width: 14px;
                height: 14px;
            }
        }
    </style>
</head>
<body>
    <button class="hints-button" onclick="showHints()">Hints</button>
    
    <div class="popup-overlay" id="popupOverlay" onclick="hideHints()"></div>
    <div class="hints-popup" id="hintsPopup">
        <button class="close-button" onclick="hideHints()">&times;</button>
        <h3>Challenge 1: SQL Injection API</h3>
        <div class="hints-content">
            <h4>Objective</h4>
            <p>Extract the admin's secret note which contains the flag.</p>
            
            <h4>Hints</h4>
            <ul>
                <li>The login endpoint is vulnerable to SQL injection</li>
                <li>Try using SQL injection to bypass authentication</li>
                <li>Consider using UNION statements to extract additional data</li>
                <li>The admin user has a secret_note field that contains the flag</li>
                <li>Common SQL injection payloads: <code>' OR '1'='1' --</code></li>
                <li>UNION SELECT can help you retrieve the admin's secret_note</li>
            </ul>
            
            <h4>Example Payload</h4>
            <p><strong>Username:</strong> <code>admin' OR '1'='1' --</code><br>
            <strong>Password:</strong> anything</p>
            
            <h4>Advanced Payload</h4>
            <p><strong>Username:</strong> <code>admin' UNION SELECT 1,username,password,role,secret_note FROM users WHERE role='admin' --</code><br>
            <strong>Password:</strong> anything</p>
            
            <h4>Flag Format</h4>
            <p><code>WOLF{XXXXX}</code></p>
            
            <h4>Difficulty</h4>
            <p>Beginner - SQL Injection, Authentication Bypass</p>
        </div>
    </div>

    <div class="container">
        <div class="newspaper-header">
            <h1 class="newspaper-title">Challenge 1: SQL Injection API</h1>
            <p class="newspaper-subtitle">Security Testing Laboratory</p>
        </div>
        
        <div class="challenge">
            <h2>Challenge Description</h2>
            <p>You've found a vulnerable API endpoint that uses SQL queries. The admin user has a secret note that contains the flag.</p>
            <p><strong>Objective:</strong> Extract the admin's secret note to get the flag.</p>
            <p><strong>Endpoint:</strong> <code>POST /api/login</code></p>
        </div>

        <div class="api-form">
            <h3>API Testing Interface</h3>
            <form id="loginForm">
                <input type="text" id="username" placeholder="Username" required>
                <input type="password" id="password" placeholder="Password" required>
                <button type="submit">Login</button>
            </form>
            <div id="result" class="result"></div>
        </div>

        <div class="hint">
            <h3>Hint</h3>
            <p>What happens when you try to bypass authentication using SQL injection?</p>
        </div>
    </div>

    <script>
        function showHints() {
            document.getElementById('hintsPopup').style.display = 'block';
            document.getElementById('popupOverlay').style.display = 'block';
            document.body.style.overflow = 'hidden';
        }
        
        function hideHints() {
            document.getElementById('hintsPopup').style.display = 'none';
            document.getElementById('popupOverlay').style.display = 'none';
            document.body.style.overflow = 'auto';
        }
        
        // Close popup with Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                hideHints();
            }
        });
        
        document.getElementById('loginForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, password })
                });
                const data = await response.json();
                document.getElementById('result').innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            } catch (error) {
                document.getElementById('result').innerHTML = '<p style="color: red;">Error: ' + error.message + '</p>';
            }
        });
    </script>
</body>
</html>
    ''')

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        username = data.get('username', '')
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        # Vulnerable SQL query - no parameterization!
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        
        try:
            cursor = db_conn.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            
            if result:
                user_data = {
                    'id': result[0],
                    'username': result[1],
                    'role': result[3],
                    'message': 'Login successful!',
                    'secret_note': result[4] if result[4] else 'No secret note'
                }
                return jsonify(user_data)
            else:
                return jsonify({'error': 'Invalid credentials'}), 401
                
        except sqlite3.Error as db_error:
            return jsonify({'error': f'Database error: {str(db_error)}'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    """List all users (for debugging)"""
    try:
        cursor = db_conn.cursor()
        cursor.execute("SELECT id, username, role FROM users")
        users = cursor.fetchall()
        
        user_list = []
        for user in users:
            user_list.append({
                'id': user[0],
                'username': user[1],
                'role': user[2]
            })
        
        return jsonify({'users': user_list})
        
    except sqlite3.Error as db_error:
        return jsonify({'error': f'Database error: {str(db_error)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    print("Challenge 1: SQL Injection API")
    print("Access at: http://localhost:5001")
    print("Flag: WOLF{SQL01}")
    app.run(host='194.238.22.59', port=5001, debug=True)

