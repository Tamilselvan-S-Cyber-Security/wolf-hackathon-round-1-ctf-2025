#!/usr/bin/env python3
"""
Challenge 3: JWT Token Manipulation
Difficulty: Intermediate
Port: 5003
Flag: WOLF{JWT03}
"""

from flask import Flask, request, jsonify, render_template_string
import jwt
import base64
import hashlib
import time

app = Flask(__name__)

# Secret keys (weak for demonstration)
SECRET_KEY = "weak_secret_key_123"
ADMIN_SECRET = "admin_secret_456"

def generate_token(username, role="user"):
    """Generate JWT token"""
    payload = {
        'username': username,
        'role': role,
        'iat': int(time.time()),
        'exp': int(time.time()) + 3600  # 1 hour expiry
    }
    
    if role == "admin":
        return jwt.encode(payload, ADMIN_SECRET, algorithm='HS256')
    else:
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Challenge 3: JWT Token Manipulation</title>
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
        .token-display { 
            background: #fff8dc; 
            padding: 20px; 
            border: 2px solid #000; 
            margin: 15px 0; 
            word-break: break-all;
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
        <h3>Challenge 3: JWT Token Manipulation</h3>
        <div class="hints-content">
            <h4>Objective</h4>
            <p>Gain admin access to retrieve the flag by manipulating JWT tokens.</p>
            
            <h4>Hints</h4>
            <ul>
                <li>JWT tokens can be manipulated by changing the algorithm or payload</li>
                <li>Try changing the algorithm to "none" to bypass signature verification</li>
                <li>Modify the role field in the token payload from "user" to "admin"</li>
                <li>Use online JWT tools like jwt.io to decode and modify tokens</li>
                <li>Remove the signature when using algorithm "none"</li>
                <li>Try different secret keys for token validation</li>
            </ul>
            
            <h4>Step-by-step</h4>
            <p>1. Login as regular user to get a token<br>
            2. Decode the token to see its structure<br>
            3. Create new token with algorithm "none"<br>
            4. Set role to "admin" in payload<br>
            5. Remove signature part<br>
            6. Use modified token</p>
            
            <h4>Flag Format</h4>
            <p><code>WOLF{XXXXX}</code></p>
            
            <h4>Difficulty</h4>
            <p>Intermediate - JWT Manipulation</p>
        </div>
    </div>

    <div class="container">
        <div class="newspaper-header">
            <h1 class="newspaper-title">Challenge 3: JWT Token Manipulation</h1>
            <p class="newspaper-subtitle">Security Testing Laboratory</p>
        </div>
        
        <div class="challenge">
            <h2>Challenge Description</h2>
            <p>This API uses JWT tokens for authentication. There's an admin panel that requires admin privileges.</p>
            <p><strong>Objective:</strong> Gain admin access to retrieve the flag.</p>
            <p><strong>Endpoints:</strong> <code>POST /api/login</code>, <code>GET /api/admin</code></p>
        </div>

        <div class="api-form">
            <h3>Login</h3>
            <form id="loginForm">
                <input type="text" id="username" placeholder="Username" required>
                <input type="password" id="password" placeholder="Password" required>
                <button type="submit">Login</button>
            </form>
            <div id="token" class="token-display"></div>
        </div>

        <div class="api-form">
            <h3>Custom Token (Advanced)</h3>
            <textarea id="customToken" placeholder="Paste your custom JWT token here..." rows="3" style="width: 100%;"></textarea>
            <button onclick="useCustomToken()">Use Custom Token</button>
        </div>

        <div class="api-form">
            <h3>Admin Panel</h3>
            <button onclick="accessAdmin()">Access Admin Panel</button>
            <div id="result" class="result"></div>
        </div>

        <div class="hint">
            <h3>Hint</h3>
            <p>JWT tokens can be manipulated. What happens when you change the algorithm or modify the payload?</p>
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
        
        let currentToken = '';

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
                if (data.token) {
                    currentToken = data.token;
                    document.getElementById('token').innerHTML = '<strong>Token:</strong><br>' + currentToken;
                }
            } catch (error) {
                document.getElementById('result').innerHTML = '<p style="color: red;">Error: ' + error.message + '</p>';
            }
        });

        function useCustomToken() {
            const customToken = document.getElementById('customToken').value;
            if (customToken) {
                currentToken = customToken;
                document.getElementById('token').innerHTML = '<strong>Custom Token:</strong><br>' + currentToken;
            }
        }

        async function accessAdmin() {
            try {
                const response = await fetch('/api/admin', {
                    headers: { 'Authorization': 'Bearer ' + currentToken }
                });
                const data = await response.json();
                document.getElementById('result').innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            } catch (error) {
                document.getElementById('result').innerHTML = '<p style="color: red;">Error: ' + error.message + '</p>';
            }
        }
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
        
        # Simple authentication (for demo purposes)
        if username == "admin" and password == "admin123":
            token = generate_token(username, "admin")
            return jsonify({'token': token, 'message': 'Login successful'})
        elif username == "user" and password == "password123":
            token = generate_token(username, "user")
            return jsonify({'token': token, 'message': 'Login successful'})
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/admin', methods=['GET'])
def admin_panel():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': 'Empty token provided'}), 401
        
        # Try to decode with different secrets and algorithms
        try:
            # Try with admin secret first
            payload = jwt.decode(token, ADMIN_SECRET, algorithms=['HS256'])
        except jwt.InvalidTokenError:
            try:
                # Try with regular secret
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            except jwt.InvalidTokenError:
                try:
                    # Try with no verification (algorithm: none)
                    payload = jwt.decode(token, options={"verify_signature": False})
                except jwt.InvalidTokenError:
                    return jsonify({'error': 'Invalid token format'}), 401
        
        if payload.get('role') == 'admin':
            return jsonify({
                'message': 'Welcome to admin panel!',
                'flag': 'WOLF{JWT03}',
                'user': payload.get('username'),
                'role': payload.get('role')
            })
        else:
            return jsonify({
                'error': 'Admin access required',
                'user_role': payload.get('role')
            }), 403
            
    except jwt.InvalidTokenError as jwt_error:
        return jsonify({'error': f'JWT error: {str(jwt_error)}'}), 401
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/debug', methods=['GET'])
def debug():
    """Debug endpoint showing token structure"""
    return jsonify({
        'message': 'JWT Debug Information',
        'algorithm': 'HS256',
        'hint': 'Try modifying the algorithm or using different secrets',
        'users': {
            'admin': 'admin123',
            'user': 'password123'
        }
    })

if __name__ == '__main__':
    print("Challenge 3: JWT Token Manipulation")
    print("Access at: http://localhost:5003")
    print("Flag: WOLF{JWT03}")
    app.run(host='0.0.0.0', port=5003, debug=True)

