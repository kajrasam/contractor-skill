import os

def patch_file(filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    target = """function openManageAdminsModal() {
            document.getElementById('manage-admins-modal').classList.remove('hidden');
            renderAdminUsersTable();
        }"""
    
    replacement = """async function openManageAdminsModal() {
            document.getElementById('manage-admins-modal').classList.remove('hidden');
            try {
                const res = await fetch(API_BASE + '/online_status');
                const data = await res.json();
                window.onlineUsers = data.online_users || [];
            } catch(e) {}
            renderAdminUsersTable();
        }"""

    if target in html:
        html = html.replace(target, replacement)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Patched {filepath}")
    else:
        print(f"Target not found in {filepath}")

patch_file('index_render.html')
patch_file('static/index.html')
