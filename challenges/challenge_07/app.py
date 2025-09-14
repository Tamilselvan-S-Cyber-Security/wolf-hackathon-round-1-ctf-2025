#!/usr/bin/env python3
"""
Challenge 7: LDAP Injection
Difficulty: Advanced
Port: 5007
Flag: WOLF{LDA07}
"""

from flask import Flask, request, jsonify, render_template_string
import re

app = Flask(__name__)

# Simulate LDAP directory
ldap_users = {
    "cn=admin,dc=company,dc=com": {
        "cn": "admin",
        "uid": "admin",
        "userPassword": "admin123",
        "objectClass": ["person", "organizationalPerson", "inetOrgPerson"],
        "secret": "WOLF{LDA07}"
    },
    "cn=john,dc=company,dc=com": {
        "cn": "john",
        "uid": "john",
        "userPassword": "password123",
        "objectClass": ["person", "organizationalPerson", "inetOrgPerson"],
        "secret": "User secret"
    },
    "cn=alice,dc=company,dc=com": {
        "cn": "alice",
        "uid": "alice",
        "userPassword": "alice123",
        "objectClass": ["person", "organizationalPerson", "inetOrgPerson"],
        "secret": "Alice secret"
    }
}

def simulate_ldap_search(filter_str):
    """Simulate LDAP search with basic injection detection"""
    results = []
    
    # Basic LDAP filter parsing (simplified)
    for dn, attrs in ldap_users.items():
        # Replace filter with actual values for matching
        test_filter = filter_str
        
        # Replace uid with actual value
        if "uid=" in test_filter:
            uid_match = re.search(r'uid=([^)]+)', test_filter)
            if uid_match:
                uid_value = uid_match.group(1)
                # Remove LDAP injection characters for comparison
                clean_uid = re.sub(r'[)(&|!]', '', uid_value)
                if clean_uid == attrs.get("uid", ""):
                    results.append({"dn": dn, "attributes": attrs})
        
        # Replace userPassword with actual value
        elif "userPassword=" in test_filter:
            pass_match = re.search(r'userPassword=([^)]+)', test_filter)
            if pass_match:
                pass_value = pass_match.group(1)
                # Remove LDAP injection characters for comparison
                clean_pass = re.sub(r'[)(&|!]', '', pass_value)
                if clean_pass == attrs.get("userPassword", ""):
                    results.append({"dn": dn, "attributes": attrs})
    
    return results

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Challenge 7: LDAP Injection</title>
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
        .ldap-example { 
            background: #fff8dc; 
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
        <h3>Challenge 7: LDAP Injection</h3>
        <div class="hints-content">
            <h4>Objective</h4>
            <p>Extract the admin's secret using LDAP injection.</p>
            
            <h4>Hints</h4>
            <ul>
                <li>LDAP filters use special characters: & (AND), | (OR), ! (NOT)</li>
                <li>Use wildcard * to match any value</li>
                <li>Try manipulating the filter logic with parentheses</li>
                <li>Use custom filter input for advanced payloads</li>
                <li>The secret attribute contains the flag for admin user</li>
                <li>Try: admin)(&(uid=admin)(userPassword=*))</li>
            </ul>
            
            <h4>Example Payload</h4>
            <p><code>admin)(&(uid=admin)(userPassword=*))</code></p>
            
            <h4>Flag Format</h4>
            <p><code>WOLF{XXXXX}</code></p>
            
            <h4>Difficulty</h4>
            <p>Advanced - LDAP Injection</p>
        </div>
    </div>

    <div class="container">
        <div class="newspaper-header">
            <h1 class="newspaper-title">Challenge 7: LDAP Injection</h1>
            <p class="newspaper-subtitle">Security Testing Laboratory</p>
        </div>
        
        <div class="challenge">
            <h2>Challenge Description</h2>
            <p>This API interfaces with an LDAP directory. The admin user has a secret attribute containing the flag.</p>
            <p><strong>Objective:</strong> Extract the admin's secret using LDAP injection.</p>
            <p><strong>Endpoint:</strong> <code>POST /api/ldap</code></p>
        </div>

        <div class="ldap-example">
            <h3>Example LDAP Filter:</h3>
            <pre>(&(uid=admin)(userPassword=admin123))</pre>
        </div>

        <div class="api-form">
            <h3>LDAP Search</h3>
            <input type="text" id="uid" placeholder="UID" value="admin">
            <input type="password" id="password" placeholder="Password" value="admin123">
            <button onclick="searchLDAP()">Search LDAP</button>
            <div id="result" class="result"></div>
        </div>

        <div class="api-form">
            <h3>Advanced LDAP Filter</h3>
            <textarea id="customFilter" rows="3" style="width: 100%;" placeholder="Enter custom LDAP filter...">(&(uid=admin)(userPassword=admin123))</textarea>
            <button onclick="customSearch()">Custom Search</button>
            <div id="customResult" class="result"></div>
        </div>

        <div class="hint">
            <h3>Hint</h3>
            <p>LDAP filters use special characters like &, |, !. What happens when you manipulate the filter logic?</p>
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
        
        async function searchLDAP() {
            const uid = document.getElementById('uid').value;
            const password = document.getElementById('password').value;
            
            try {
                const response = await fetch('/api/ldap', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ uid, password })
                });
                const data = await response.json();
                document.getElementById('result').innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            } catch (error) {
                document.getElementById('result').innerHTML = '<p style="color: red;">Error: ' + error.message + '</p>';
            }
        }

        async function customSearch() {
            const filter = document.getElementById('customFilter').value;
            
            try {
                const response = await fetch('/api/ldap/custom', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ filter })
                });
                const data = await response.json();
                document.getElementById('customResult').innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            } catch (error) {
                document.getElementById('customResult').innerHTML = '<p style="color: red;">Error: ' + error.message + '</p>';
            }
        }
    </script>
</body>
</html>
    ''')

@app.route('/api/ldap', methods=['POST'])
def ldap_search():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        uid = data.get('uid', '')
        password = data.get('password', '')
        
        if not uid or not password:
            return jsonify({'error': 'UID and password are required'}), 400
        
        # Construct LDAP filter (vulnerable to injection!)
        filter_str = f"(&(uid={uid})(userPassword={password}))"
        
        # Simulate LDAP search
        results = simulate_ldap_search(filter_str)
        
        if results:
            return jsonify({
                'message': 'LDAP search successful',
                'results': results,
                'filter_used': filter_str
            })
        else:
            return jsonify({'error': 'No matching entries found'}), 404
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/ldap/custom', methods=['POST'])
def ldap_custom_search():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        filter_str = data.get('filter', '')
        
        if not filter_str:
            return jsonify({'error': 'Filter is required'}), 400
        
        # Simulate LDAP search with custom filter
        results = simulate_ldap_search(filter_str)
        
        return jsonify({
            'message': 'Custom LDAP search completed',
            'results': results,
            'filter_used': filter_str
        })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/info', methods=['GET'])
def info():
    """Information endpoint"""
    return jsonify({
        'message': 'LDAP Directory API',
        'hint': 'LDAP filters can be manipulated using special characters',
        'operators': ['& (AND)', '| (OR)', '! (NOT)'],
        'example_payloads': [
            '(&(uid=admin)(userPassword=*))',
            '(|(uid=admin)(uid=*))',
            '(&(uid=admin)(|(userPassword=*)(userPassword=wrong)))'
        ]
    })

if __name__ == '__main__':
    print("Challenge 7: LDAP Injection")
    print("Access at: http://localhost:5007")
    print("Flag: WOLF{LDA07}")
    app.run(host='0.0.0.0', port=5007, debug=True)

