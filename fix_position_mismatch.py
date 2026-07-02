import os

def patch_file(filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    target = """// Sync dbUsers names with official employeeData to fix filter/display mismatch
                Object.keys(dbUsers).forEach(id => {
                    let eData = employeeDataAll.find(e => e.username === id || e.user_id === id);
                    if (eData) {
                        let officialName = eData.FullNameTH || eData.FullName || eData.EmployeeNameThai || eData.EmployeeNameEng;
                        if (officialName) dbUsers[id].name = officialName;
                    }
                });"""
                
    replacement = """// Sync dbUsers names with official employeeData to fix filter/display mismatch
                Object.keys(dbUsers).forEach(id => {
                    let eData = employeeDataAll.find(e => e.username === id || e.user_id === id);
                    if (eData) {
                        let officialName = eData.FullNameTH || eData.FullName || eData.EmployeeNameThai || eData.EmployeeNameEng;
                        if (officialName) dbUsers[id].name = officialName;
                        let officialPos = eData.PositionNameThai || eData.position_name || eData.position;
                        if (officialPos) dbUsers[id].position = officialPos;
                    }
                });"""

    if target in html:
        html = html.replace(target, replacement)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Patched {filepath}")
    else:
        # What if it's slightly different whitespace? Let's use a regex or just replace the inner part
        print(f"Target not found in {filepath}. Trying line by line...")
        lines = html.splitlines()
        new_lines = []
        in_patch = False
        for line in lines:
            new_lines.append(line)
            if 'if (officialName) dbUsers[id].name = officialName;' in line:
                new_lines.append('                        let officialPos = eData.PositionNameThai || eData.position_name || eData.position;')
                new_lines.append('                        if (officialPos) dbUsers[id].position = officialPos;')
        
        new_html = '\n'.join(new_lines)
        if new_html != html:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_html)
            print(f"Patched {filepath} using fallback.")
        else:
            print(f"Failed to patch {filepath}")

patch_file('index_render.html')
patch_file('static/index.html')
