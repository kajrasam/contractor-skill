import re

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add employeeDataAll declaration
    html = re.sub(r'let employeeData = \[\];', r'let employeeData = [];\n        let employeeDataAll = [];', html, count=1)
    
    # 2. Update fetchInitialData
    html = re.sub(r'employeeData = data\.employeeData \|\| \[\];', 
                  r"employeeDataAll = data.employeeData || [];\n                employeeData = employeeDataAll.filter(e => e.Pipeline === 'Evaluated');", 
                  html, count=1)
                  
    # 3. Replace tab-admin HTML
    new_admin_html = """
            <section id="tab-admin" class="tab-content hidden">
                <div class="mb-6 flex justify-between items-end">
                    <div>
                        <h2 class="text-2xl font-bold text-scg-900">Admin Control Panel</h2>
                        <p class="text-slate-500 text-sm">บริหารจัดการสิทธิผู้ถูกประเมิน และผูกสายบังคับบัญชา (Master Data)</p>
                    </div>
                    <div class="flex gap-2">
                        <button onclick="saveAdminData()" class="bg-scg-600 hover:bg-scg-700 text-white px-5 py-2.5 rounded-xl font-bold shadow-md flex items-center gap-2 transition-colors">
                            <i class="fa-solid fa-save"></i> บันทึกข้อมูล (Save)
                        </button>
                        <button onclick="exportToExcel()" class="bg-green-600 hover:bg-green-700 text-white px-5 py-2.5 rounded-xl font-bold shadow-md flex items-center gap-2 transition-colors shrink-0">
                            <i class="fa-solid fa-file-excel"></i> Export Data (Excel)
                        </button>
                    </div>
                </div>

                <div class="bg-white rounded-3xl shadow-sm border border-slate-100 flex flex-col" style="max-height: calc(100vh - 150px);">
                    <div class="p-4 border-b border-slate-100 bg-slate-50 flex justify-between items-center rounded-t-3xl">
                        <div class="flex items-center gap-4">
                            <input type="text" id="admin-search" placeholder="ค้นหาชื่อ, รหัส..." class="px-3 py-2 border border-slate-200 rounded-lg text-sm w-64 focus:outline-none focus:border-scg-500" onkeyup="renderAdminTable()">
                            <label class="flex items-center gap-2 cursor-pointer text-sm font-bold text-slate-700">
                                <input type="checkbox" id="admin-select-all" class="w-4 h-4 rounded border-slate-300 text-scg-600 focus:ring-scg-500" onchange="toggleAdminSelectAll(this)">
                                เลือกทั้งหมด (Select All)
                            </label>
                        </div>
                        <div class="text-sm text-slate-500 font-bold" id="admin-count-info">กำลังโหลด...</div>
                    </div>
                    <div class="overflow-auto w-full custom-scrollbar flex-1 relative" style="min-height: 400px;">
                        <table class="w-full text-left border-collapse whitespace-nowrap text-sm min-w-max relative" id="admin-table">
                            <thead class="sticky top-0 z-30 bg-slate-50 shadow-[0_1px_2px_rgba(0,0,0,0.05)]">
                                <tr class="text-slate-600 font-bold border-b border-slate-200 text-xs uppercase tracking-wider">
                                    <th class="py-3 px-4 border-r border-slate-100 text-center w-24">Evaluate?</th>
                                    <th class="py-3 px-4 border-r border-slate-100">Person ID</th>
                                    <th class="py-3 px-4 border-r border-slate-100">Name (TH)</th>
                                    <th class="py-3 px-4 border-r border-slate-100">Name (EN)</th>
                                    <th class="py-3 px-4 border-r border-slate-100 text-scg-700">Username</th>
                                    <th class="py-3 px-4 border-r border-slate-100 text-slate-500">Password</th>
                                    <th class="py-3 px-4 border-r border-slate-100">Report To Name</th>
                                </tr>
                            </thead>
                            <tbody id="admin-tbody" class="text-slate-700">
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>
"""
    # Replace tab-admin section
    html = re.sub(r'<section id="tab-admin" class="tab-content.*?</section>', new_admin_html, html, count=1, flags=re.DOTALL)
    
    # 4. Replace setupAdminTab() function and add new admin JS functions
    new_admin_js = """
        let adminTempData = [];
        
        function setupAdminTab() {
            adminTempData = employeeDataAll.map(e => {
                let n_en = e.name_en;
                if(!n_en) {
                    n_en = e.FullNameENG;
                    if(!n_en) {
                        const first = e.FirstNameEnglish;
                        if(first) {
                            const prefix = e.NamePrefixEnglish || '';
                            const last = e.LastNameEnglish || '';
                            n_en = (prefix ? prefix + ' ' : '') + first + ' ' + last;
                        } else {
                            n_en = '';
                        }
                    }
                }
                
                return {
                    pk_field: e.PersonID ? 'PersonID' : (e.id ? 'id' : 'person_id'),
                    pk_value: e.PersonID || e.id || e.person_id,
                    person_id: e.PersonID || e.person_id || '-',
                    name_th: e.FullNameTH || e.name_th || e.FullName || '-',
                    name_en: n_en ? n_en.trim() : '-',
                    user_id: e.user_id || e.username || e.USER || '',
                    password: e.password || '',
                    report_to_name: e.ReportToName || e.report_to_name || '',
                    is_evaluated: e.Pipeline === 'Evaluated',
                    position: e.PositionNameThai || e.position_name || ''
                };
            });
            renderAdminTable();
        }
        
        function renderAdminTable() {
            const tbody = document.getElementById('admin-tbody');
            if(!tbody) return;
            
            const search = document.getElementById('admin-search').value.toLowerCase();
            
            // Build unique English names for the dropdown
            const allEngNames = [...new Set(adminTempData.map(e => e.name_en).filter(n => n && n !== '-'))].sort();
            let optionsHtml = `<option value="">-- ไม่ระบุ --</option>`;
            allEngNames.forEach(n => {
                optionsHtml += `<option value="${n}">${n}</option>`;
            });

            let html = '';
            let count = 0;
            
            adminTempData.forEach((emp, index) => {
                const searchStr = `${emp.person_id} ${emp.name_th} ${emp.name_en} ${emp.user_id}`.toLowerCase();
                if(search && !searchStr.includes(search)) return;
                
                count++;
                
                let rowOpts = optionsHtml;
                if(emp.report_to_name) {
                    rowOpts = rowOpts.replace(`value="${emp.report_to_name}"`, `value="${emp.report_to_name}" selected`);
                }
                
                html += `
                    <tr class="hover:bg-slate-50 transition-colors border-b border-slate-100">
                        <td class="py-2 px-4 border-r border-slate-100 text-center">
                            <input type="checkbox" class="w-5 h-5 rounded border-slate-300 text-scg-600 focus:ring-scg-500 cursor-pointer" 
                                   ${emp.is_evaluated ? 'checked' : ''} 
                                   onchange="adminTempData[${index}].is_evaluated = this.checked">
                        </td>
                        <td class="py-2 px-4 border-r border-slate-100 font-medium">${emp.person_id}</td>
                        <td class="py-2 px-4 border-r border-slate-100">${emp.name_th}</td>
                        <td class="py-2 px-4 border-r border-slate-100">${emp.name_en}</td>
                        <td class="py-2 px-4 border-r border-slate-100">
                            <input type="text" class="px-2 py-1.5 border border-slate-200 rounded-lg w-full text-xs font-bold text-scg-700" 
                                   value="${emp.user_id}" 
                                   onchange="adminTempData[${index}].user_id = this.value">
                        </td>
                        <td class="py-2 px-4 border-r border-slate-100">
                            <input type="text" class="px-2 py-1.5 border border-slate-200 rounded-lg w-full text-xs" 
                                   value="${emp.password}" 
                                   onchange="adminTempData[${index}].password = this.value">
                        </td>
                        <td class="py-2 px-4 border-r border-slate-100">
                            <select class="px-2 py-1.5 border border-slate-200 rounded-lg w-full text-xs bg-white cursor-pointer" 
                                    onchange="adminTempData[${index}].report_to_name = this.value">
                                ${rowOpts}
                            </select>
                        </td>
                    </tr>
                `;
            });
            
            tbody.innerHTML = html;
            document.getElementById('admin-count-info').innerText = `แสดง ${count} รายการ`;
        }

        function toggleAdminSelectAll(cb) {
            const search = document.getElementById('admin-search').value.toLowerCase();
            adminTempData.forEach((emp, index) => {
                const searchStr = `${emp.person_id} ${emp.name_th} ${emp.name_en} ${emp.user_id}`.toLowerCase();
                if(search && !searchStr.includes(search)) return;
                emp.is_evaluated = cb.checked;
            });
            renderAdminTable();
        }

        async function saveAdminData() {
            const btn = document.querySelector('button[onclick="saveAdminData()"]');
            const oldHtml = btn.innerHTML;
            btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> กำลังบันทึก...`;
            btn.disabled = true;
            
            try {
                const response = await fetch(API_BASE + '/admin/sync_employees', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ employees: adminTempData })
                });
                
                const result = await response.json();
                if(result.status === 'success') {
                    alert('บันทึกข้อมูลและอัปเดตสิทธิการเข้าถึงเรียบร้อยแล้ว!');
                    window.location.reload();
                } else {
                    alert('Error: ' + result.message);
                }
            } catch (err) {
                console.error(err);
                alert('Failed to save data. Check console.');
            } finally {
                btn.innerHTML = oldHtml;
                btn.disabled = false;
            }
        }
"""
    html = re.sub(r'function setupAdminTab\(\).*?document\.getElementById\(\'admin-hierarchy-list\'\)\.innerHTML = hHtml;\n        }', new_admin_js, html, count=1, flags=re.DOTALL)
    
    # 5. Remove any old add_user and update_manager functions if needed (optional, keeping them won't break things)

    # 6. Add "ถูกประเมิน" column to Employee Data table
    # Replace headers
    html = html.replace('<th class="align-top py-4 px-6 border-r border-slate-100 text-scg-700">User ID</th>',
                        '<th class="align-top py-4 px-6 border-r border-slate-100 text-center text-scg-600">ถูกประเมิน</th>\n                                    <th class="align-top py-4 px-6 border-r border-slate-100 text-scg-700">User ID</th>')
    
    # Replace body
    html = html.replace('<td class="py-3 px-6 border-r border-slate-100 text-scg-700 font-medium">${emp.user_id || emp.username || emp.USER || \'-\'}</td>',
                        '<td class="py-3 px-6 border-r border-slate-100 text-center"><i class="fa-solid fa-check-circle text-green-500 text-lg" title="Evaluated"></i></td>\n                        <td class="py-3 px-6 border-r border-slate-100 text-scg-700 font-medium">${emp.user_id || emp.username || emp.USER || \'-\'}</td>')

    # Wait, there's another replace for the export button logic if needed, but the requirements just said Employee Data table.
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Patched {filepath}")

patch_file('static/index.html')
patch_file('index_render.html')
