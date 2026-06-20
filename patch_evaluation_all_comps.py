import re

files = [
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html',
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/index_render.html'
]

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update buildFiltersUI to remove visiblePos.includes(posName) check
    pattern1 = re.compile(r'if\s*\(\s*posName\s*&&\s*visiblePos\.includes\(posName\)\s*\)\s*\{', re.DOTALL)
    content = pattern1.sub('if (posName) {', content)

    # 2. Update buildIDPFilters to map positions from employeeData exactly like buildRoleResponseSection does
    pattern2 = re.compile(r'visibleUsers\.forEach\(uid => \{\s*const emp = dbUsers\[uid\];\s*if\s*\(emp\)\s*\{\s*if\(emp\.position\)\s*posSet\.add\(emp\.position\);\s*emps\.push\(\{\s*id:\s*uid,\s*name:\s*emp\.name,\s*position:\s*emp\.position\s*\}\);\s*\}\s*\}\);', re.DOTALL)
    new_idp_filters = """visibleUsers.forEach(uid => {
                const emp = dbUsers[uid];
                const eData = employeeData.find(e => e.user_id === uid || e.username === uid || e.EmployeeNameEng === (emp ? emp.name : '') || e.EmployeeNameThai === (emp ? emp.name : ''));
                if (emp) {
                    let pName = emp.position;
                    if(eData && eData.PositionNameThai) pName = eData.PositionNameThai;
                    else if(eData && eData.position_name) pName = eData.position_name;
                    
                    if(pName) posSet.add(pName);
                    emps.push({ id: uid, name: emp.name, position: pName });
                }
            });"""
    content = pattern2.sub(new_idp_filters, content)

    # 3. In updateEvalUI(), remove `if (targetVal === 0) continue;` and fix `currentVal`
    content = content.replace('const targetVal = targets[i] || 0;\n                if (targetVal === 0) continue; // Skip competencies with target 0', 'const targetVal = targets[i] || 0;')
    content = re.sub(r'const currentVal = emp\.actuals\[i\] === 0 \? 1 : emp\.actuals\[i\];', r'const currentVal = (emp.actuals[i] || 0) === 0 ? 1 : emp.actuals[i];', content)

    # 4. In updateEvalUI() radar chart code
    content = content.replace('const t = targets[i] || 0;\n                if (t === 0) continue; // Only show on radar if target > 0', 'const t = targets[i] || 0;')

    # 5. In drawIDPRadar()
    content = content.replace('const t = targets[i] || 0;\n                if (t === 0) continue; \n                cleanLabels.push(allLabels[i]);', 'const t = targets[i] || 0;\n                cleanLabels.push(allLabels[i]);')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Patch applied for linking position filter and showing all competencies safely.")
