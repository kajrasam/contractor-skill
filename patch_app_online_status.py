import os

def patch_app():
    filepath = 'app.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add import time and active_sessions if not present
    if 'import time' not in content:
        content = content.replace('import os', 'import os\nimport time')
    
    if 'active_sessions = {}' not in content:
        content = content.replace('supabase: Client = create_client(url, key)', 'supabase: Client = create_client(url, key)\n\nactive_sessions = {}')

    # Add endpoints at the end before if __name__ == '__main__'
    endpoints = """
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
    return jsonify({"online_users": online_users})

if __name__ == '__main__':
"""
    if '/api/ping' not in content:
        content = content.replace("if __name__ == '__main__':", endpoints.strip())
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Patched app.py with online status endpoints")
    else:
        print("Endpoints already present in app.py")

patch_app()
