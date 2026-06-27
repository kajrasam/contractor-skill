import re

def fix_org_filters_2(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r'(if\s*\(!eData\)\s*\{\s*)(let\s*empName\s*=\s*emp\.name;\s*if\s*\(selectedEmployeeFilter\.length\s*>\s*0\s*&&\s*\(!empName\s*\|\|\s*!selectedEmployeeFilter\.includes\(empName\)\)\)\s*return\s*false;\s*if\s*\(selectedSectionFilter\.length\s*>\s*0\s*\|\|\s*selectedDepartmentFilter\.length\s*>\s*0\s*\|\|\s*selectedReportToFilter\.length\s*>\s*0\s*\)\s*return\s*false;\s*return\s*true;\s*\})'
    
    new_inner_logic = """let hasScopeRestriction = false;
        if (currentUser.scope_division && currentUser.scope_division.length > 0) hasScopeRestriction = true;
        if (currentUser.scope_department && currentUser.scope_department !== 'ALL') hasScopeRestriction = true;
        if (currentUser.scope_section && currentUser.scope_section !== 'ALL') hasScopeRestriction = true;
        
        const isAdmin = (currentUser.id === 'Admin' || currentUser.id.toLowerCase().includes('admin') || (currentUser.role && (currentUser.role === 'Admin' || currentUser.role === 'Super Admin')));
        if (hasScopeRestriction && isAdmin) {
            return false;
        }

        """
    
    def replacer(match):
        return match.group(1) + new_inner_logic + match.group(2)
        
    content, count = re.subn(pattern, replacer, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}, count={count}")

fix_org_filters_2('static/index.html')
fix_org_filters_2('index_render.html')
