#!/usr/bin/env python3
"""
Challenge 10: Advanced Backdoor
Difficulty: Expert
Port: 5010
Flag: WOLF{BD10}
"""

from flask import Flask, request, jsonify, render_template_string
import os
import base64
import pickle
import subprocess
import hashlib

app = Flask(__name__)

# Create flag file
flag_file = os.path.join(os.path.dirname(__file__), "flag_challenge10.txt")
if not os.path.exists(flag_file):
    with open(flag_file, 'w') as f:
        f.write("WOLF{BD10}")

# Hidden backdoor endpoint
BACKDOOR_SECRET = "wolf_ctf_2025_secret_key"

class BackdoorPayload:
    def __reduce__(self):
        return (subprocess.check_output, (['type', 'flag_challenge10.txt'],))

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Challenge 10: Advanced Backdoor</title>
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
        .warning { 
            background: #fff8dc; 
            border: 2px solid #000; 
            padding: 20px; 
            margin: 20px 0; 
            border-left: 8px solid #000;
        }
        .hidden { 
            background: #2c2c2c; 
            color: #fff; 
            padding: 20px; 
            border: 2px solid #000; 
            margin: 20px 0; 
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
        <h3>Challenge 10: Advanced Backdoor</h3>
        <div class="hints-content">
            <h4>Objective</h4>
            <p>Discover and exploit the hidden backdoor.</p>
            
            <h4>Hints</h4>
            <ul>
                <li>This challenge has multiple hidden backdoors</li>
                <li>Try the hash generator with secret parameter</li>
                <li>Upload a file with 'backdoor' in the filename</li>
                <li>Look for hidden admin endpoints</li>
                <li>Try different header combinations</li>
                <li>The secret parameter is: wolf_ctf_2025_secret_key</li>
            </ul>
            
            <h4>Example Payload</h4>
            <p><code>POST /api/hash?secret=wolf_ctf_2025_secret_key</code></p>
            
            <h4>Flag Format</h4>
            <p><code>WOLF{XXXXX}</code></p>
            
            <h4>Difficulty</h4>
            <p>Expert - Advanced Backdoor</p>
        </div>
    </div>

    <div class="container">
        <div class="newspaper-header">
            <h1 class="newspaper-title">Challenge 10: Advanced Backdoor</h1>
            <p class="newspaper-subtitle">Security Testing Laboratory</p>
        </div>
        
        <div class="warning">
            <strong>Expert Challenge:</strong> This is the most advanced challenge. Think outside the box!
        </div>
        
        <div class="challenge">
            <h2>Challenge Description</h2>
            <p>This API has multiple vulnerabilities and hidden functionality. Find the backdoor to get the flag.</p>
            <p><strong>Objective:</strong> Discover and exploit the hidden backdoor.</p>
            <p><strong>Endpoints:</strong> Multiple endpoints with various vulnerabilities</p>
        </div>

        <div class="api-form">
            <h3>Data Processor</h3>
            <textarea id="data" rows="4" style="width: 100%;" placeholder="Enter data to process...">{"name": "test", "value": 123}</textarea>
            <button onclick="processData()">Process Data</button>
            <div id="result1" class="result"></div>
        </div>

        <div class="api-form">
            <h3>Hash Generator</h3>
            <input type="text" id="text" placeholder="Enter text to hash" value="hello">
            <button onclick="generateHash()">Generate Hash</button>
            <div id="result2" class="result"></div>
        </div>

        <div class="api-form">
            <h3>File Upload</h3>
            <input type="file" id="fileInput" accept=".txt,.json">
            <button onclick="uploadFile()">Upload File</button>
            <div id="result3" class="result"></div>
        </div>

        <div class="hidden">
            <h3>Hidden Features (Find the backdoor!)</h3>
            <p>Look for hidden endpoints, parameters, or functionality...</p>
        </div>

        <div class="hint">
            <h3>Hint</h3>
            <p>This challenge combines multiple attack vectors. Look for serialization, hidden parameters, and unconventional endpoints.</p>
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
        
        async function processData() {
            const data = document.getElementById('data').value;
            
            try {
                const response = await fetch('/api/process', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: data
                });
                const result = await response.json();
                document.getElementById('result1').innerHTML = '<pre>' + JSON.stringify(result, null, 2) + '</pre>';
            } catch (error) {
                document.getElementById('result1').innerHTML = '<p style="color: red;">Error: ' + error.message + '</p>';
            }
        }

        async function generateHash() {
            const text = document.getElementById('text').value;
            
            try {
                const response = await fetch('/api/hash', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text })
                });
                const result = await response.json();
                document.getElementById('result2').innerHTML = '<pre>' + JSON.stringify(result, null, 2) + '</pre>';
            } catch (error) {
                document.getElementById('result2').innerHTML = '<p style="color: red;">Error: ' + error.message + '</p>';
            }
        }

        async function uploadFile() {
            const fileInput = document.getElementById('fileInput');
            const file = fileInput.files[0];
            
            if (!file) {
                document.getElementById('result3').innerHTML = '<p style="color: red;">Please select a file</p>';
                return;
            }
            
            const formData = new FormData();
            formData.append('file', file);
            
            try {
                const response = await fetch('/api/upload', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();
                document.getElementById('result3').innerHTML = '<pre>' + JSON.stringify(result, null, 2) + '</pre>';
            } catch (error) {
                document.getElementById('result3').innerHTML = '<p style="color: red;">Error: ' + error.message + '</p>';
            }
        }
    </script>
</body>
</html>
    ''')

@app.route('/api/process', methods=['POST'])
def process_data():
    try:
        # Vulnerable pickle deserialization
        data = request.get_data()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Check if it's base64 encoded
        if request.headers.get('Content-Type') == 'application/octet-stream':
            try:
                data = base64.b64decode(data)
            except Exception as decode_error:
                return jsonify({'error': f'Base64 decode error: {str(decode_error)}'}), 400
        
        # Try to deserialize with pickle (vulnerable!)
        try:
            result = pickle.loads(data)
            return jsonify({
                'message': 'Data processed successfully',
                'result': str(result),
                'type': type(result).__name__
            })
        except pickle.PickleError as pickle_error:
            return jsonify({'error': f'Pickle error: {str(pickle_error)}'}), 400
        except:
            # Fallback to JSON processing
            try:
                json_data = request.get_json()
                if json_data:
                    return jsonify({
                        'message': 'JSON data processed',
                        'data': json_data
                    })
                else:
                    return jsonify({'error': 'Invalid data format'}), 400
            except Exception as json_error:
                return jsonify({'error': f'JSON processing error: {str(json_error)}'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/hash', methods=['POST'])
def generate_hash():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'Text parameter is required'}), 400
        
        # Generate hash
        hash_result = hashlib.sha256(text.encode()).hexdigest()
        
        # Check for hidden parameter
        secret = request.args.get('secret')
        if secret == BACKDOOR_SECRET:
            return jsonify({
                'hash': hash_result,
                'message': 'Backdoor activated!',
                'flag': 'WOLF{BD10}'
            })
        
        return jsonify({
            'hash': hash_result,
            'text': text
        })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read file content
        content = file.read().decode('utf-8')
        
        # Check for backdoor file
        if 'backdoor' in file.filename.lower():
            return jsonify({
                'message': 'Backdoor file detected!',
                'flag': 'WOLF{BD10}',
                'content': content
            })
        
        return jsonify({
            'message': 'File uploaded successfully',
            'filename': file.filename,
            'content': content
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Hidden backdoor endpoint
@app.route('/api/admin/<path:endpoint>', methods=['GET', 'POST'])
def hidden_backdoor(endpoint):
    try:
        # Check for backdoor activation
        auth = request.headers.get('X-Backdoor-Auth')
        if auth != BACKDOOR_SECRET:
            return jsonify({'error': 'Unauthorized'}), 401
        
        if endpoint == 'flag':
            with open(flag_file, 'r') as f:
                flag = f.read()
            return jsonify({'flag': flag})
        elif endpoint == 'exec':
            cmd = request.args.get('cmd')
            if cmd:
                result = subprocess.check_output(cmd, shell=True, text=True)
                return jsonify({'result': result})
        
        return jsonify({'message': 'Backdoor endpoint accessed', 'endpoint': endpoint})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/info', methods=['GET'])
def info():
    """Information endpoint with hidden clues"""
    return jsonify({
        'message': 'Advanced API with multiple endpoints',
        'endpoints': [
            '/api/process - Data processing',
            '/api/hash - Hash generation',
            '/api/upload - File upload'
        ],
        'hints': [
            'Look for hidden parameters',
            'Check for serialization vulnerabilities',
            'Try unconventional endpoints',
            'Look for backdoor files or authentication'
        ]
    })

if __name__ == '__main__':
    print("Challenge 10: Advanced Backdoor")
    print("Access at: http://localhost:5010")
    print("Flag: WOLF{BD10}")
    app.run(host='0.0.0.0', port=5010, debug=True)

