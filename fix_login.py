import re
import os

files_to_process = [
    'd:\\Work\\งานใหม่\\อบรม\\2026\\Vibe Coding Workshop\\Project\\competency-system\\static\\index.html',
    'd:\\Work\\งานใหม่\\อบรม\\2026\\Vibe Coding Workshop\\Project\\competency-system\\index_render.html'
]

for filepath in files_to_process:
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update handleLogin function
    old_login = """        function handleLogin() {
            const user = document.getElementById('login-username').value;
            const pass = document.getElementById('login-password').value;
            if (dbUsers[user] && dbUsers[user].pass === pass) {
                localStorage.setItem('comp_sys_user', user);
                checkLoginState();
            } else {
                document.getElementById('login-error').classList.remove('hidden');
            }
        }"""
    
    new_login = """        function handleLogin() {
            const user = document.getElementById('login-username').value;
            const pass = document.getElementById('login-password').value;
            
            // Case-insensitive user lookup
            const userKey = Object.keys(dbUsers).find(k => k.toLowerCase() === user.toLowerCase());
            
            if (userKey && dbUsers[userKey].pass === pass) {
                localStorage.setItem('comp_sys_user', userKey);
                checkLoginState();
            } else {
                document.getElementById('login-error').classList.remove('hidden');
            }
        }"""
    
    content = content.replace(old_login, new_login)

    # 2. Update inputs to support Enter key
    username_input = 'id="login-username"\n                        class="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-scg-500 bg-slate-50 focus:bg-white"\n                        placeholder="เช่น Admin, Supervisor, EmployeeEE"'
    new_username_input = username_input + '\n                        onkeypress="if(event.key === \'Enter\') handleLogin()"'
    content = content.replace(username_input, new_username_input)

    password_input = 'id="login-password"\n                        class="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-scg-500 bg-slate-50 focus:bg-white"\n                        placeholder="รหัสผ่านตรงกับ Username"'
    new_password_input = password_input + '\n                        onkeypress="if(event.key === \'Enter\') handleLogin()"'
    content = content.replace(password_input, new_password_input)

    # Just in case the newline spacing is slightly different, let's use regex
    if 'onkeypress="if(event.key === \'Enter\') handleLogin()"' not in content:
        content = re.sub(r'(id="login-username"[^>]*?)>', r'\1 onkeypress="if(event.key === \'Enter\') handleLogin()">', content)
        content = re.sub(r'(id="login-password"[^>]*?)>', r'\1 onkeypress="if(event.key === \'Enter\') handleLogin()">', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated login logic in {os.path.basename(filepath)}")
