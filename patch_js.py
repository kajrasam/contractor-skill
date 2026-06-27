import os

js_code = '''
        function openManageAdminsModal() {
            document.getElementById('manage-admins-modal').classList.remove('hidden');
            renderAdminUsersTable();
        }

        function clearAdminForm() {
            document.getElementById('admin-uid').value = '';
            document.getElementById('admin-pass').value = '';
            document.getElementById('admin-name').value = '';
            document.getElementById('admin-scope-sec').value = '';
            document.getElementById('admin-scope-dep').value = '';
        }

        function renderAdminUsersTable() {
            const tbody = document.getElementById('admin-users-table-body');
            tbody.innerHTML = '';
            
            for (const uid in dbUsers) {
                const u = dbUsers[uid];
                if (u.role === 'Admin' || u.role === 'Super Admin') {
                    const tr = document.createElement('tr');
                    tr.className = 'hover:bg-slate-50 transition-colors';
                    tr.innerHTML = `
                        <td class="py-3 px-4">${uid} ${u.role === 'Super Admin' ? '<span class="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded-full">Super</span>' : ''}</td>
                        <td class="py-3 px-4">${u.name || '-'}</td>
                        <td class="py-3 px-4">${u.scope_section || 'ALL'}</td>
                        <td class="py-3 px-4">${u.scope_department || 'ALL'}</td>
                        <td class="py-3 px-4 text-center">
                            ${u.role !== 'Super Admin' ? `
                                <button onclick="editAdminUser('${uid}')" class="text-blue-500 hover:text-blue-700 mr-2"><i class="fa-solid fa-edit"></i></button>
                                <button onclick="deleteAdminUser('${uid}')" class="text-red-500 hover:text-red-700"><i class="fa-solid fa-trash"></i></button>
                            ` : ''}
                        </td>
                    `;
                    tbody.appendChild(tr);
                }
            }
        }

        function editAdminUser(uid) {
            const u = dbUsers[uid];
            if (!u) return;
            document.getElementById('admin-uid').value = uid;
            document.getElementById('admin-pass').value = u.pass || '';
            document.getElementById('admin-name').value = u.name || '';
            document.getElementById('admin-scope-sec').value = u.scope_section || '';
            document.getElementById('admin-scope-dep').value = u.scope_department || '';
        }

        async function saveAdminUser() {
            const uid = document.getElementById('admin-uid').value.trim();
            const pass = document.getElementById('admin-pass').value.trim();
            const name = document.getElementById('admin-name').value.trim();
            let sec = document.getElementById('admin-scope-sec').value.trim();
            let dep = document.getElementById('admin-scope-dep').value.trim();
            
            if (!uid || !pass) {
                if (typeof showToast === 'function') showToast('กรุณากรอก ID และ Password', 'error');
                return;
            }
            if (sec.toUpperCase() === 'ALL') sec = '';
            if (dep.toUpperCase() === 'ALL') dep = '';

            try {
                const res = await fetch('/api/admin_users', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        uid: uid,
                        pass: pass,
                        name: name,
                        scope_section: sec,
                        scope_department: dep
                    })
                });
                if (res.ok) {
                    if (typeof showToast === 'function') showToast('บันทึกสำเร็จ', 'success');
                    if (!dbUsers[uid]) dbUsers[uid] = {};
                    dbUsers[uid].pass = pass;
                    dbUsers[uid].name = name;
                    dbUsers[uid].role = 'Admin';
                    dbUsers[uid].scope_section = sec;
                    dbUsers[uid].scope_department = dep;
                    renderAdminUsersTable();
                    clearAdminForm();
                } else {
                    if (typeof showToast === 'function') showToast('Error saving admin', 'error');
                }
            } catch (e) {
                console.error(e);
            }
        }

        async function deleteAdminUser(uid) {
            if (!confirm('ยืนยันการลบ Admin ' + uid + '?')) return;
            try {
                const res = await fetch('/api/admin_users/' + encodeURIComponent(uid), {
                    method: 'DELETE'
                });
                if (res.ok) {
                    delete dbUsers[uid];
                    renderAdminUsersTable();
                    if (typeof showToast === 'function') showToast('ลบสำเร็จ', 'success');
                }
            } catch (e) {
                console.error(e);
            }
        }
'''

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add JS functions at the end of scripts
    if 'function openManageAdminsModal()' not in content:
        target_script = '</script>'
        content = content.replace('</script>', js_code + '\n</script>', 1)
        
    # 2. Patch handleLogin
    if "currentUser.scope_section = 'ALL';" not in content:
        old_login = """            currentUser = { id: username, name: user.name, role: user.role };
            if (user.role === 'Admin') {
                updateUIForRole('Admin');
                document.getElementById('login-modal').classList.add('hidden');"""
                
        new_login = """            currentUser = { id: username, name: user.name, role: user.role };
            if (user.role === 'Super Admin') {
                currentUser.scope_section = 'ALL';
                currentUser.scope_department = 'ALL';
                const btn = document.getElementById('btn-manage-admins');
                if (btn) btn.classList.remove('hidden');
                updateUIForRole('Admin');
                document.getElementById('login-modal').classList.add('hidden');
            } else if (user.role === 'Admin') {
                currentUser.scope_section = user.scope_section || 'ALL';
                currentUser.scope_department = user.scope_department || 'ALL';
                const btn = document.getElementById('btn-manage-admins');
                if (btn) btn.classList.add('hidden');
                updateUIForRole('Admin');
                document.getElementById('login-modal').classList.add('hidden');"""
        content = content.replace(old_login, new_login)
        
    # 3. Patch initFilters
    if "depEl.disabled = true;" not in content:
        old_filter = """        function initFilters() {
            const departments = new Set();
            const sections = new Set();"""
            
        new_filter = """        function initFilters() {
            const departments = new Set();
            const sections = new Set();"""
            
        content = content.replace(old_filter, new_filter) # Just a marker, let's replace at the end of initFilters
        
        old_filter_end = """            populateDropdown('filter-section', Array.from(sections).sort());
        }"""
        new_filter_end = """            populateDropdown('filter-section', Array.from(sections).sort());
            
            if (currentUser && currentUser.role === 'Admin') {
                if (currentUser.scope_department && currentUser.scope_department !== 'ALL') {
                    const depEl = document.getElementById('filter-department');
                    if (depEl) {
                        depEl.value = currentUser.scope_department;
                        depEl.disabled = true;
                        depEl.classList.add('bg-slate-100');
                    }
                }
                if (currentUser.scope_section && currentUser.scope_section !== 'ALL') {
                    const secEl = document.getElementById('filter-section');
                    if (secEl) {
                        secEl.value = currentUser.scope_section;
                        secEl.disabled = true;
                        secEl.classList.add('bg-slate-100');
                    }
                }
            }
        }"""
        content = content.replace(old_filter_end, new_filter_end)

    # 4. Patch setupAdminTab
    if "let filteredEmployeeDataAll = employeeDataAll;" not in content:
        old_setup = """        function setupAdminTab() {
            adminTempData = employeeDataAll.map(e => {"""
        new_setup = """        function setupAdminTab() {
            let filteredEmployeeDataAll = employeeDataAll;
            if (currentUser && currentUser.role === 'Admin') {
                if (currentUser.scope_department && currentUser.scope_department !== 'ALL') {
                    filteredEmployeeDataAll = filteredEmployeeDataAll.filter(e => e.DepartmentThai === currentUser.scope_department || e.department === currentUser.scope_department);
                }
                if (currentUser.scope_section && currentUser.scope_section !== 'ALL') {
                    filteredEmployeeDataAll = filteredEmployeeDataAll.filter(e => e.SectionThai === currentUser.scope_section || e.section === currentUser.scope_section);
                }
            }

            adminTempData = filteredEmployeeDataAll.map(e => {"""
        content = content.replace(old_setup, new_setup)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

patch_file('index_render.html')
patch_file('static/index.html')
print("JS Patched successfully.")
