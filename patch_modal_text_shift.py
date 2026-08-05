import sys

def patch_file(fp):
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. Add populateDatalist function if not exists
    if 'function populateDatalist' not in c:
        c = c.replace('function populateSelect', 
'''function populateDatalist(datalistId, optionsArray) {
            const dl = document.getElementById(datalistId);
            if(!dl) return;
            dl.innerHTML = '';
            optionsArray.forEach(opt => {
                const o = document.createElement('option');
                o.value = opt;
                dl.appendChild(o);
            });
        }

        function populateSelect''')

    # 2. Replace <select> with <input list="..."> + <datalist> for position, level, and add shift
    old_pos_html = '''<div><label class="block text-xs font-bold text-slate-600 mb-1">Position Name</label><select id="add-position" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm bg-white"><option value="">- เลือก -</option></select></div>
                        <div><label class="block text-xs font-bold text-slate-600 mb-1">Position Level</label><select id="add-level" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm bg-white"><option value="">- เลือก -</option></select></div>'''

    new_pos_html = '''<div><label class="block text-xs font-bold text-slate-600 mb-1">เครื่อง (Shift)</label><input type="text" id="add-shift" list="dl-add-shift" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm" placeholder="- เลือกหรือพิมพ์ -"><datalist id="dl-add-shift"></datalist></div>
                        <div><label class="block text-xs font-bold text-slate-600 mb-1">Position Name</label><input type="text" id="add-position" list="dl-add-position" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm" placeholder="- เลือกหรือพิมพ์ -"><datalist id="dl-add-position"></datalist></div>
                        <div><label class="block text-xs font-bold text-slate-600 mb-1">Position Level</label><input type="text" id="add-level" list="dl-add-level" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm" placeholder="- เลือกหรือพิมพ์ -"><datalist id="dl-add-level"></datalist></div>'''
    
    if old_pos_html in c:
        c = c.replace(old_pos_html, new_pos_html)

    # 3. Update setupAddEmployeeCascadingDropdowns to cascade to datalists
    old_onchange = '''populateSelect('add-position', getUniqueValues(filtered, 'PositionNameThai, position_name'), '');
                  populateSelect('add-level', getUniqueValues(filtered, 'PositionStructureLevel, position_level'), '');'''
    new_onchange = '''populateDatalist('dl-add-shift', getUniqueValues(filtered, 'ShiftThai, shift_thai'));
                  populateDatalist('dl-add-position', getUniqueValues(filtered, 'PositionNameThai, position_name'));
                  populateDatalist('dl-add-level', getUniqueValues(filtered, 'PositionStructureLevel, position_level'));'''
    
    if old_onchange in c:
        c = c.replace(old_onchange, new_onchange)

    # 4. In submitAddEmployee, add shift_thai
    if "emp.company = document.getElementById('add-company').value;" in c and "emp.shift_thai =" not in c:
        c = c.replace("emp.company = document.getElementById('add-company').value;", 
                      "emp.company = document.getElementById('add-company').value;\n                  emp.shift_thai = document.getElementById('add-shift').value;")

    if "company: document.getElementById('add-company').value" in c and "shift_thai: document.getElementById('add-shift').value" not in c:
        c = c.replace("company: document.getElementById('add-company').value\n                  };",
                      "company: document.getElementById('add-company').value,\n                      shift_thai: document.getElementById('add-shift').value\n                  };")

    # 5. In openEditEmployeeModal, populate add-shift
    if "document.getElementById('add-company').value = emp.company || '';" in c and "emp.shift_thai || ''" not in c:
        c = c.replace("document.getElementById('add-company').value = emp.company || '';",
                      "document.getElementById('add-company').value = emp.company || '';\n              document.getElementById('add-shift').value = emp.shift_thai || '';")
        
    # Also in openAddEmployeeModal reset fields
    if "document.querySelectorAll('#add-employee-modal input').forEach(input => input.value = '');" in c:
        # already resets all inputs, which covers add-shift, add-position, and add-level!
        pass

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"Patched {fp}")

for fp in ['index_render.html', 'static/index.html']:
    patch_file(fp)

# Patch app.py
with open('app.py', 'r', encoding='utf-8') as f:
    app_c = f.read()

if '"ShiftThai": emp.get(\'shift_thai\', \'\')' not in app_c:
    app_c = app_c.replace('"CompanyThai": emp.get(\'company\', \'\'),',
                          '"CompanyThai": emp.get(\'company\', \'\'),\n                    "ShiftThai": emp.get(\'shift_thai\', \'\'),')
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(app_c)
    print("Patched app.py")
