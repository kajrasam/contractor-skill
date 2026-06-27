import re

def fix_org_filters(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    old_code = """    if (!eData) {
        let empName = emp.name;
        if (selectedEmployeeFilter.length > 0 && (!empName || !selectedEmployeeFilter.includes(empName))) return false;
        if (selectedSectionFilter.length > 0 || selectedDepartmentFilter.length > 0 || selectedReportToFilter.length > 0) return false;
        return true;
    }"""

    new_code = """    if (!eData) {
        let hasScopeRestriction = false;
        if (currentUser.scope_division && currentUser.scope_division.length > 0) hasScopeRestriction = true;
        if (currentUser.scope_department && currentUser.scope_department !== 'ALL') hasScopeRestriction = true;
        if (currentUser.scope_section && currentUser.scope_section !== 'ALL') hasScopeRestriction = true;
        
        const isAdmin = (currentUser.id === 'Admin' || currentUser.id.toLowerCase().includes('admin') || (currentUser.role && (currentUser.role === 'Admin' || currentUser.role === 'Super Admin')));
        if (hasScopeRestriction && isAdmin) {
            return false;
        }

        let empName = emp.name;
        if (selectedEmployeeFilter.length > 0 && (!empName || !selectedEmployeeFilter.includes(empName))) return false;
        if (selectedSectionFilter.length > 0 || selectedDepartmentFilter.length > 0 || selectedReportToFilter.length > 0) return false;
        return true;
    }"""
    
    content = content.replace(old_code, new_code)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}")

fix_org_filters('static/index.html')
fix_org_filters('index_render.html')
