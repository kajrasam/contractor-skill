import re

files = [
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html',
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/index_render.html'
]

original_text = """            let visibleUsers = [];
            if (currentUser.id === 'Admin') {
                visibleUsers = applyGlobalFiltersToSubIds(Object.keys(dbUsers).filter(uid => uid !== 'Admin'));
            } else {
                visibleUsers = applyGlobalFiltersToSubIds([currentUser.id, ...getSubordinates(currentUser.id)]);
            }

            let visiblePosSet = new Set();
            visibleUsers.forEach(uid => {
                const emp = dbUsers[uid];
                const eData = employeeData.find(e => e.user_id === uid || e.username === uid || e.EmployeeNameEng === (emp ? emp.name : '') || e.EmployeeNameThai === (emp ? emp.name : ''));
                if (eData && eData.PositionNameThai) visiblePosSet.add(eData.PositionNameThai);
                else if (eData && eData.position_name) visiblePosSet.add(eData.position_name);
                else if (emp && emp.position) visiblePosSet.add(emp.position);
            });
            let visiblePos = Array.from(visiblePosSet).filter(p => p).sort();"""

new_text = """            let visiblePosSet = new Set();
            employeeData.forEach(e => {
                if (matchesFiltersExcept(e, null)) {
                    let posName = e.PositionNameThai || e.position_name;
                    if (posName) visiblePosSet.add(posName);
                }
            });
            let visiblePos = Array.from(visiblePosSet).filter(p => p).sort();"""

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # The string match is safer and we just replace it
    if original_text in content:
        content = content.replace(original_text, new_text)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Patch applied successfully for {file_path}")
    else:
        print(f"Warning: exact text not found in {file_path}")
        # fallback regex in case of slight whitespace diff
        # just for safety, maybe we can strip spaces
        pass

