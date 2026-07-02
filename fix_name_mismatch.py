import os

def patch_file(filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    target = "employeeData = employeeDataAll.filter(e => e.Pipeline === 'Evaluated');"
                
    replacement = """employeeData = employeeDataAll.filter(e => e.Pipeline === 'Evaluated');
                // Sync dbUsers names with official employeeData to fix filter/display mismatch
                Object.keys(dbUsers).forEach(id => {
                    let eData = employeeDataAll.find(e => e.username === id || e.user_id === id);
                    if (eData) {
                        let officialName = eData.FullNameTH || eData.FullName || eData.EmployeeNameThai || eData.EmployeeNameEng;
                        if (officialName) dbUsers[id].name = officialName;
                    }
                });"""

    if target in html:
        # Check if already patched
        if "Sync dbUsers names with official employeeData" not in html:
            html = html.replace(target, replacement)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"Patched {filepath}")
        else:
            print(f"Already patched {filepath}")
    else:
        print(f"Target not found in {filepath}")

patch_file('index_render.html')
patch_file('static/index.html')
