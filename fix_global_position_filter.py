import os

def patch_file(filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    target = """        let empName = emp.name;
                if (selectedEmployeeFilter.length > 0 && (!empName || !selectedEmployeeFilter.includes(empName))) return false;
                if (selectedSectionFilter.length > 0 || selectedDepartmentFilter.length > 0 || selectedReportToFilter.length > 0) return false;
                return true;"""
                
    replacement = """        let empName = emp.name;
                if (selectedEmployeeFilter.length > 0 && (!empName || !selectedEmployeeFilter.includes(empName))) return false;
                if (selectedSectionFilter.length > 0 || selectedDepartmentFilter.length > 0 || selectedReportToFilter.length > 0) return false;
                
                let posName = emp.position || emp.PositionNameThai || emp.position_name;
                if (selectedPositionsFilter.length > 0 && (!posName || !selectedPositionsFilter.includes(posName))) return false;
                if (typeof hasCompetencyFilterMatch === 'function' && !hasCompetencyFilterMatch(posName)) return false;
                let jg = emp.job_group || (typeof positionGroups !== 'undefined' ? positionGroups[posName] : null);
                if (selectedJobGroupFilter.length > 0 && (!jg || !selectedJobGroupFilter.includes(jg))) return false;

                return true;"""

    if target in html:
        html = html.replace(target, replacement)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Patched {filepath}")
    else:
        print(f"Target not found in {filepath}")

patch_file('index_render.html')
patch_file('static/index.html')
