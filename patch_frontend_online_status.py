import os
import re

def patch_file(filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add window.onlineUsers and startHeartbeat function at the start of JAVASCRIPT LOGIC
    if 'window.onlineUsers' not in html:
        target_js_start = "const API_BASE = '/api';"
        replacement_js_start = """const API_BASE = '/api';

        window.onlineUsers = [];
        let pingInterval = null;
        function startHeartbeat() {
            if (pingInterval) clearInterval(pingInterval);
            const doPing = async () => {
                if (!currentUser) return;
                try {
                    await fetch(API_BASE + '/ping', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ userId: currentUser })
                    });
                } catch(e) {}
            };
            pingInterval = setInterval(doPing, 60000);
            doPing();
        }"""
        html = html.replace(target_js_start, replacement_js_start)

    # 2. Call startHeartbeat() in fetchInitialData
    target_fetch = """setTimeout(() => { if(typeof buildFiltersUI === 'function') buildFiltersUI(); }, 50);"""
    replacement_fetch = """setTimeout(() => { if(typeof buildFiltersUI === 'function') buildFiltersUI(); }, 50);
                startHeartbeat();"""
    if 'startHeartbeat();' not in html:
        html = html.replace(target_fetch, replacement_fetch)

    # 3. Update switchTab to fetch online_status
    target_switch = """if (tabId === 'admin') {
                    compContainer.classList.add('hidden');
                } else {"""
    replacement_switch = """if (tabId === 'admin') {
                    compContainer.classList.add('hidden');
                    fetch(API_BASE + '/online_status').then(r => r.json()).then(data => {
                        window.onlineUsers = data.online_users || [];
                        if (typeof renderAdminUsersTable === 'function') renderAdminUsersTable();
                    }).catch(e => {});
                } else {"""
    if '/online_status' not in html:
        html = html.replace(target_switch, replacement_switch)

    # 4. Update renderAdminUsersTable to show Online status
    target_table = """<td class="py-3 px-4">${uid} ${u.role === 'Super Admin' ? '<span class="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded-full">Super</span>' : ''}</td>
                        <td class="py-3 px-4">${u.name || '-'}</td>"""
    replacement_table = """<td class="py-3 px-4">${uid} ${u.role === 'Super Admin' ? '<span class="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded-full">Super</span>' : ''}</td>
                        <td class="py-3 px-4">
                            <div class="flex items-center">
                                ${u.name || '-'}
                                ${window.onlineUsers.includes(uid) ? '<span class="ml-2 flex items-center text-xs text-green-600 bg-green-50 px-2 py-0.5 rounded-full border border-green-200"><span class="w-2 h-2 rounded-full bg-green-500 mr-1 animate-pulse"></span> Log in</span>' : ''}
                            </div>
                        </td>"""
    if 'window.onlineUsers.includes(uid)' not in html:
        html = html.replace(target_table, replacement_table)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Patched {filepath}")

patch_file('index_render.html')
patch_file('static/index.html')
