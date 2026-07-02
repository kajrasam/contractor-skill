import os

def patch_app():
    filepath = 'app.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    target = """active_sessions = {}

@app.route('/api/ping', methods=['POST'])
def ping():
    data = request.json
    uid = data.get('userId')
    if uid:
        active_sessions[uid] = time.time()
    return jsonify({"status": "ok"})

@app.route('/api/online_status', methods=['GET'])
def online_status():
    now = time.time()
    # Consider online if pinged in the last 5 minutes (300 seconds)
    online_users = [uid for uid, last_time in active_sessions.items() if now - last_time < 300]
    return jsonify({"online_users": online_users})"""

    replacement = """import json

SESSION_FILE = 'sessions.json'

def get_sessions():
    if not os.path.exists(SESSION_FILE):
        return {}
    try:
        with open(SESSION_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_sessions(sessions):
    try:
        with open(SESSION_FILE, 'w') as f:
            json.dump(sessions, f)
    except:
        pass

@app.route('/api/ping', methods=['POST'])
def ping():
    data = request.json
    uid = data.get('userId')
    if uid:
        sessions = get_sessions()
        sessions[uid] = time.time()
        save_sessions(sessions)
    return jsonify({"status": "ok"})

@app.route('/api/online_status', methods=['GET'])
def online_status():
    now = time.time()
    sessions = get_sessions()
    online_users = [uid for uid, last_time in sessions.items() if now - last_time < 300]
    return jsonify({"online_users": online_users})"""

    if "active_sessions = {}" in content:
        content = content.replace(target, replacement)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Patched app.py with file-based sessions")
    else:
        print("Target not found in app.py")

patch_app()
