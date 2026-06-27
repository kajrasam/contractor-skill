import os

def fix_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add Select Element
    s1 = '''                        <div>
                            <label class="block text-xs font-bold text-slate-500 mb-1">Scope Department</label>
                            <input type="text" id="admin-scope-dep" placeholder="ALL หรือ ชื่อ Department" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm bg-white">
                        </div>'''
    r1 = s1 + '''
                        <div class="md:col-span-2">
                            <label class="block text-xs font-bold text-slate-500 mb-1">Scope Division</label>
                            <select id="admin-scope-div" multiple class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm bg-white h-24">
                                <option value="Concrete Technology">Concrete Technology</option>
                                <option value="Drying and Firing Technology">Drying and Firing Technology</option>
                                <option value="Fiber Cement Technology">Fiber Cement Technology</option>
                                <option value="Operation Excellence and Industry 4.0">Operation Excellence and Industry 4.0</option>
                                <option value="Strategic Materials and Living Solution Procurement">Strategic Materials and Living Solution Procurement</option>
                                <option value="Other">Other</option>
                            </select>
                            <p class="text-[10px] text-slate-400 mt-1">กด Ctrl (หรือ Cmd) ค้างไว้เพื่อเลือกหลายรายการ หรือไม่เลือกเลย (ALL)</p>
                        </div>'''
    # Note: s1 might use ALL   Department if garbled. 
    # Actually I fixed it so it's probably standard Thai or maybe it's still garbled?
    # I didn't replace ALL   Department in my last fix! So it might be garbled in index_render.html
    # I will just regex or use a robust replace
    
    import re
    content = re.sub(
        r'(<label class="block text-xs font-bold text-slate-500 mb-1">Scope Department</label>\s*<input type="text" id="admin-scope-dep" [^>]*>)(\s*</div>)',
        r'\1\2' + '''
                        <div class="md:col-span-2">
                            <label class="block text-xs font-bold text-slate-500 mb-1">Scope Division</label>
                            <select id="admin-scope-div" multiple class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm bg-white h-28">
                                <option value="Concrete Technology">Concrete Technology</option>
                                <option value="Drying and Firing Technology">Drying and Firing Technology</option>
                                <option value="Fiber Cement Technology">Fiber Cement Technology</option>
                                <option value="Operation Excellence and Industry 4.0">Operation Excellence and Industry 4.0</option>
                                <option value="Strategic Materials and Living Solution Procurement">Strategic Materials and Living Solution Procurement</option>
                                <option value="Other">Other</option>
                            </select>
                            <p class="text-[10px] text-slate-400 mt-1">กด Ctrl (หรือ Cmd) ค้างไว้เพื่อเลือกหลายรายการ หากไม่เลือกจะถือเป็น (ALL)</p>
                        </div>''', content)

    # 2. Table header
    content = re.sub(
        r'(<th class="py-3 px-4">Dept Scope</th>)',
        r'\1\n                                <th class="py-3 px-4">Div Scope</th>', content)

    # 3. clearAdminForm
    content = content.replace(
        "document.getElementById('admin-scope-dep').value = '';",
        "document.getElementById('admin-scope-dep').value = '';\n            Array.from(document.getElementById('admin-scope-div').options).forEach(o => o.selected = false);"
    )

    # 4. renderAdminUsersTable
    content = re.sub(
        r'(<td class="py-3 px-4">\$\{u\.scope_department \|\| \'ALL\'\}</td>)',
        r'\1\n                        <td class="py-3 px-4">${u.scope_division && u.scope_division.length > 0 ? u.scope_division.join(\', \') : \'ALL\'}</td>', content)

    # 5. editAdminUser
    s_edit = "document.getElementById('admin-scope-dep').value = u.scope_department || '';"
    r_edit = s_edit + '''
            const divSelect = document.getElementById('admin-scope-div');
            Array.from(divSelect.options).forEach(o => o.selected = false);
            if (u.scope_division && Array.isArray(u.scope_division)) {
                Array.from(divSelect.options).forEach(o => {
                    if (u.scope_division.includes(o.value)) o.selected = true;
                });
            }'''
    content = content.replace(s_edit, r_edit)

    # 6. saveAdminUser
    s_save = "let dep = document.getElementById('admin-scope-dep').value.trim();"
    r_save = s_save + "\n            let div = Array.from(document.getElementById('admin-scope-div').selectedOptions).map(o => o.value);"
    content = content.replace(s_save, r_save)

    s_body = "scope_department: dep"
    r_body = s_body + ",\n                        scope_division: div"
    content = content.replace(s_body, r_body)

    s_db = "dbUsers[uid].scope_department = dep;"
    r_db = s_db + "\n                    dbUsers[uid].scope_division = div;"
    content = content.replace(s_db, r_db)

    # 7. setupAdminTab
    s_setup = "filteredEmployeeDataAll = filteredEmployeeDataAll.filter(e => e.SectionThai === currentUser.scope_section || e.section === currentUser.scope_section);\n                }"
    r_setup = s_setup + '''
                if (currentUser.scope_division && Array.isArray(currentUser.scope_division) && currentUser.scope_division.length > 0) {
                    filteredEmployeeDataAll = filteredEmployeeDataAll.filter(e => currentUser.scope_division.includes(e.DivisionThai) || currentUser.scope_division.includes(e.division));
                }'''
    content = content.replace(s_setup, r_setup)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_html('index_render.html')
fix_html('static/index.html')
