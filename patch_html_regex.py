import re

def fix_html_file(fp):
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. Replace the position and level select elements, and inject the shift element before them.
    # Note: Using non-greedy `.*?` to match anything in between the label and select closure.
    pattern_pos = r'<div><label[^>]*>Position Name</label>\s*<select id="add-position".*?</select>\s*</div>'
    pattern_lvl = r'<div><label[^>]*>Position Level</label>\s*<select id="add-level".*?</select>\s*</div>'
    
    # Check if they match
    if re.search(pattern_pos, c):
        print(f"Found Position Name select in {fp}")
        new_pos = '''<div><label class="block text-xs font-bold text-slate-600 mb-1">เครื่อง (Shift)</label><input type="text" id="add-shift" list="dl-add-shift" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm bg-white" placeholder="- เลือกหรือพิมพ์ -"><datalist id="dl-add-shift"></datalist></div>
                        <div><label class="block text-xs font-bold text-slate-600 mb-1">Position Name</label><input type="text" id="add-position" list="dl-add-position" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm bg-white" placeholder="- เลือกหรือพิมพ์ -"><datalist id="dl-add-position"></datalist></div>'''
        c = re.sub(pattern_pos, new_pos, c)
        
    if re.search(pattern_lvl, c):
        print(f"Found Position Level select in {fp}")
        new_lvl = '''<div><label class="block text-xs font-bold text-slate-600 mb-1">Position Level</label><input type="text" id="add-level" list="dl-add-level" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm bg-white" placeholder="- เลือกหรือพิมพ์ -"><datalist id="dl-add-level"></datalist></div>'''
        c = re.sub(pattern_lvl, new_lvl, c)

    # 2. Add populateDatalist function if it doesn't exist
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
        
    # 3. Replace populateSelect with populateDatalist for position, level, and add for shift.
    # We look for where `populateSelect('add-position', ...)` is called.
    # In the cascading function:
    # populateSelect('add-position', getUniqueValues(filtered, 'PositionNameThai, position_name'), '');
    # populateSelect('add-level', getUniqueValues(filtered, 'PositionStructureLevel, position_level'), '');
    pattern_pop_pos = r"populateSelect\('add-position',\s*getUniqueValues\([^,]+,\s*'PositionNameThai,\s*position_name'\)[^;]*;"
    pattern_pop_lvl = r"populateSelect\('add-level',\s*getUniqueValues\([^,]+,\s*'PositionStructureLevel,\s*position_level'\)[^;]*;"

    if re.search(pattern_pop_pos, c):
        print(f"Found populateSelect for add-position in {fp}")
        new_pop_pos = "populateDatalist('dl-add-shift', getUniqueValues(filtered, 'ShiftThai, shift_thai'));\n                populateDatalist('dl-add-position', getUniqueValues(filtered, 'PositionNameThai, position_name'));"
        c = re.sub(pattern_pop_pos, new_pop_pos, c)

    if re.search(pattern_pop_lvl, c):
        print(f"Found populateSelect for add-level in {fp}")
        new_pop_lvl = "populateDatalist('dl-add-level', getUniqueValues(filtered, 'PositionStructureLevel, position_level'));"
        c = re.sub(pattern_pop_lvl, new_pop_lvl, c)

    # 4. Check if we need to remove `cPos.options.length <= 1` references if they exist
    # (actually they are probably not there for position)

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(c)

for fp in ['index_render.html', 'static/index.html']:
    fix_html_file(fp)

print("Done patching.")
