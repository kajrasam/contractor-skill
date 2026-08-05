import re
import os

file_paths = ['index_render.html', 'static/index.html']

new_grid_html = '''<div class="grid grid-cols-2 gap-4">
                      <div><label class="block text-xs font-bold text-slate-600 mb-1">Employee ID <span class="text-red-500">*</span></label><input type="text" id="add-emp-id" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm"></div>
                      <div><label class="block text-xs font-bold text-slate-600 mb-1">User ID <span class="text-red-500">*</span></label><input type="text" id="add-user-id" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm"></div>
                      <div><label class="block text-xs font-bold text-slate-600 mb-1">Password</label><input type="text" id="add-password" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm"></div>
                      <div><label class="block text-xs font-bold text-slate-600 mb-1">Name <span class="text-red-500">*</span></label><input type="text" id="add-name" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm"></div>
                      
                      <div><label class="block text-xs font-bold text-slate-600 mb-1">Company</label><select id="add-company" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm bg-white"><option value="">- เลือก -</option></select></div>
                      <div><label class="block text-xs font-bold text-slate-600 mb-1">Sub1-Company</label><select id="add-sub1-comp" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm bg-white"><option value="">- เลือก -</option></select></div>
                      <div><label class="block text-xs font-bold text-slate-600 mb-1">Division</label><select id="add-division" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm bg-white"><option value="">- เลือก -</option></select></div>
                      <div><label class="block text-xs font-bold text-slate-600 mb-1">Sub1-Division</label><select id="add-sub1-div" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm bg-white"><option value="">- เลือก -</option></select></div>
                      <div><label class="block text-xs font-bold text-slate-600 mb-1">Department</label><select id="add-department" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm bg-white"><option value="">- เลือก -</option></select></div>
                      <div><label class="block text-xs font-bold text-slate-600 mb-1">Section</label><select id="add-section" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm bg-white"><option value="">- เลือก -</option></select></div>
                      <div><label class="block text-xs font-bold text-slate-600 mb-1">Position Name</label><select id="add-position" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm bg-white"><option value="">- เลือก -</option></select></div>
                      <div><label class="block text-xs font-bold text-slate-600 mb-1">Position Level</label><select id="add-level" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm bg-white"><option value="">- เลือก -</option></select></div>
                      
                      <div><label class="block text-xs font-bold text-slate-600 mb-1">Job Group</label><select id="add-job-group" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm bg-white"><option value="">- เลือก -</option></select></div>
                      <div><label class="block text-xs font-bold text-slate-600 mb-1">Report to Name</label><input type="text" id="add-report-to" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm"></div>
                      <div class="col-span-2"><label class="block text-xs font-bold text-slate-600 mb-1">Certificate</label><input type="text" id="add-certificate" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm"></div>
                  </div>'''

js_injection = '''
        // --- Cascading Dropdown Logic ---
        function getUniqueValues(data, field) {
            const vals = data.map(d => d[field]).filter(v => v);
            return [...new Set(vals)].sort();
        }

        function populateSelect(selectId, values, selectedValue) {
            const select = document.getElementById(selectId);
            if(!select) return;
            select.innerHTML = '<option value="">- เลือก -</option>';
            values.forEach(v => {
                const opt = document.createElement('option');
                opt.value = v;
                opt.textContent = v;
                if(v === selectedValue) opt.selected = true;
                select.appendChild(opt);
            });
        }

        function setupAddEmployeeCascadingDropdowns() {
            const cComp = document.getElementById('add-company');
            const cSub1Comp = document.getElementById('add-sub1-comp');
            const cDiv = document.getElementById('add-division');
            const cSub1Div = document.getElementById('add-sub1-div');
            const cDept = document.getElementById('add-department');
            const cSect = document.getElementById('add-section');
            const cPos = document.getElementById('add-position');
            const cLevel = document.getElementById('add-level');
            const cJob = document.getElementById('add-job-group');
            
            // Populate initial Company & Job Group from all data
            const allComps = getUniqueValues(employeeDataAll, 'CompanyThai');
            const allJobs = getUniqueValues(employeeDataAll, 'JobGroup');
            
            if(cComp && cComp.options.length <= 1) populateSelect('add-company', allComps, '');
            if(cJob && cJob.options.length <= 1) populateSelect('add-job-group', allJobs, '');
            
            if(cComp) cComp.onchange = () => {
                const vComp = cComp.value;
                const filtered = vComp ? employeeDataAll.filter(e => e.CompanyThai === vComp) : employeeDataAll;
                populateSelect('add-sub1-comp', getUniqueValues(filtered, 'Sub1CompanyThai'), '');
                cSub1Comp.onchange(); // trigger cascade
            };
            
            if(cSub1Comp) cSub1Comp.onchange = () => {
                const vComp = cComp.value;
                const vSub1Comp = cSub1Comp.value;
                const filtered = employeeDataAll.filter(e => (!vComp || e.CompanyThai === vComp) && (!vSub1Comp || e.Sub1CompanyThai === vSub1Comp));
                populateSelect('add-division', getUniqueValues(filtered, 'DivisionThai'), '');
                cDiv.onchange();
            };
            
            if(cDiv) cDiv.onchange = () => {
                const vComp = cComp.value;
                const vSub1Comp = cSub1Comp.value;
                const vDiv = cDiv.value;
                const filtered = employeeDataAll.filter(e => (!vComp || e.CompanyThai === vComp) && (!vSub1Comp || e.Sub1CompanyThai === vSub1Comp) && (!vDiv || e.DivisionThai === vDiv));
                populateSelect('add-sub1-div', getUniqueValues(filtered, 'Sub1DivisionThai'), '');
                cSub1Div.onchange();
            };
            
            if(cSub1Div) cSub1Div.onchange = () => {
                const vComp = cComp.value;
                const vSub1Comp = cSub1Comp.value;
                const vDiv = cDiv.value;
                const vSub1Div = cSub1Div.value;
                const filtered = employeeDataAll.filter(e => (!vComp || e.CompanyThai === vComp) && (!vSub1Comp || e.Sub1CompanyThai === vSub1Comp) && (!vDiv || e.DivisionThai === vDiv) && (!vSub1Div || e.Sub1DivisionThai === vSub1Div));
                populateSelect('add-department', getUniqueValues(filtered, 'DepartmentThai'), '');
                cDept.onchange();
            };
            
            if(cDept) cDept.onchange = () => {
                const vComp = cComp.value;
                const vSub1Comp = cSub1Comp.value;
                const vDiv = cDiv.value;
                const vSub1Div = cSub1Div.value;
                const vDept = cDept.value;
                const filtered = employeeDataAll.filter(e => (!vComp || e.CompanyThai === vComp) && (!vSub1Comp || e.Sub1CompanyThai === vSub1Comp) && (!vDiv || e.DivisionThai === vDiv) && (!vSub1Div || e.Sub1DivisionThai === vSub1Div) && (!vDept || e.DepartmentThai === vDept));
                populateSelect('add-section', getUniqueValues(filtered, 'SectionThai'), '');
                cSect.onchange();
            };
            
            if(cSect) cSect.onchange = () => {
                const vComp = cComp.value;
                const vSub1Comp = cSub1Comp.value;
                const vDiv = cDiv.value;
                const vSub1Div = cSub1Div.value;
                const vDept = cDept.value;
                const vSect = cSect.value;
                const filtered = employeeDataAll.filter(e => (!vComp || e.CompanyThai === vComp) && (!vSub1Comp || e.Sub1CompanyThai === vSub1Comp) && (!vDiv || e.DivisionThai === vDiv) && (!vSub1Div || e.Sub1DivisionThai === vSub1Div) && (!vDept || e.DepartmentThai === vDept) && (!vSect || e.SectionThai === vSect));
                populateSelect('add-position', getUniqueValues(filtered, 'PositionNameThai'), '');
                cPos.onchange();
            };
            
            if(cPos) cPos.onchange = () => {
                const vComp = cComp.value;
                const vSub1Comp = cSub1Comp.value;
                const vDiv = cDiv.value;
                const vSub1Div = cSub1Div.value;
                const vDept = cDept.value;
                const vSect = cSect.value;
                const vPos = cPos.value;
                const filtered = employeeDataAll.filter(e => (!vComp || e.CompanyThai === vComp) && (!vSub1Comp || e.Sub1CompanyThai === vSub1Comp) && (!vDiv || e.DivisionThai === vDiv) && (!vSub1Div || e.Sub1DivisionThai === vSub1Div) && (!vDept || e.DepartmentThai === vDept) && (!vSect || e.SectionThai === vSect) && (!vPos || e.PositionNameThai === vPos));
                populateSelect('add-level', getUniqueValues(filtered, 'PositionStructureLevel'), '');
            };
        }
        
        function populateEditEmployeeModal(emp) {
            setupAddEmployeeCascadingDropdowns();
            
            const cComp = document.getElementById('add-company');
            if(cComp) {
                cComp.value = emp.company || '';
                cComp.onchange(); // trigger cascade
            }
            
            setTimeout(() => {
                const cSub1Comp = document.getElementById('add-sub1-comp');
                if(cSub1Comp && emp.sub1_company) { cSub1Comp.value = emp.sub1_company; cSub1Comp.onchange(); }
                
                setTimeout(() => {
                    const cDiv = document.getElementById('add-division');
                    if(cDiv && emp.division) { cDiv.value = emp.division; cDiv.onchange(); }
                    
                    setTimeout(() => {
                        const cSub1Div = document.getElementById('add-sub1-div');
                        if(cSub1Div && emp.sub1_division) { cSub1Div.value = emp.sub1_division; cSub1Div.onchange(); }
                        
                        setTimeout(() => {
                            const cDept = document.getElementById('add-department');
                            if(cDept && emp.department) { cDept.value = emp.department; cDept.onchange(); }
                            
                            setTimeout(() => {
                                const cSect = document.getElementById('add-section');
                                if(cSect && emp.section) { cSect.value = emp.section; cSect.onchange(); }
                                
                                setTimeout(() => {
                                    const cPos = document.getElementById('add-position');
                                    if(cPos && emp.position) { cPos.value = emp.position; cPos.onchange(); }
                                    
                                    setTimeout(() => {
                                        const cLevel = document.getElementById('add-level');
                                        if(cLevel && emp.position_level) { cLevel.value = emp.position_level; }
                                    }, 10);
                                }, 10);
                            }, 10);
                        }, 10);
                    }, 10);
                }, 10);
            }, 10);
        }
'''

for file_path in file_paths:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Replace the Grid HTML
        parts1 = content.split('<div class="grid grid-cols-2 gap-4">')
        if len(parts1) > 1:
            idx = content.find('id="add-employee-modal"')
            if idx != -1:
                grid_start = content.find('<div class="grid grid-cols-2 gap-4">', idx)
                if grid_start != -1:
                    buttons_start = content.find('<div class="p-4 border-t border-slate-100 bg-slate-50 flex justify-end gap-2">', grid_start)
                    if buttons_start != -1:
                        content = content[:grid_start] + new_grid_html + "\\n              </div>\\n              " + content[buttons_start:]

        # 2. Inject JS Logic
        if 'setupAddEmployeeCascadingDropdowns' not in content:
            content = content.replace('function openAddEmployeeModal() {', js_injection + '\\n        function openAddEmployeeModal() {')
            
        # 3. Update openAddEmployeeModal
        if 'setupAddEmployeeCascadingDropdowns();' not in content:
            old_open = "function openAddEmployeeModal() {"
            new_open = "function openAddEmployeeModal() {\\n              setupAddEmployeeCascadingDropdowns();"
            content = content.replace(old_open, new_open)
            
        # 4. Update openEditEmployeeModal
        if 'populateEditEmployeeModal(emp);' not in content:
            edit_start = content.find("function openEditEmployeeModal(index) {")
            if edit_start != -1:
                edit_end = content.find("document.getElementById('add-employee-modal').classList.remove('hidden');", edit_start)
                if edit_end != -1:
                    manual_block = content[edit_start:edit_end]
                    new_manual_block = re.sub(r"document\.getElementById\('add-.*?'\)\.value\\s*=\\s*.*?;", "", manual_block)
                    new_manual_block += "              populateEditEmployeeModal(emp);\\n              "
                    content = content.replace(manual_block, new_manual_block)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Patched {file_path}")
    except Exception as e:
        print(f"Error patching {file_path}: {e}")
