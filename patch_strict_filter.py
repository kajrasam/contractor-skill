import re

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Change isEmployeeMatchingOrgFilters to strictly return false if eData is not found (meaning not in Evaluated list)
    old_logic = """if(!eData) {
                let posName = emp.position;
                if(selectedJobGroupFilter.length > 0 && (!posName || !selectedJobGroupFilter.includes(positionGroups[posName]))) return false;
                if(selectedPositionsFilter.length > 0 && (!posName || !selectedPositionsFilter.includes(posName))) return false;
                if(selectedEmployeeFilter.length > 0 || selectedSectionFilter.length > 0 || selectedDepartmentFilter.length > 0 || selectedSub1DivisionFilter.length > 0 || selectedDivisionFilter.length > 0 || selectedSub1CompanyFilter.length > 0 || selectedCompanyFilter.length > 0) return false;
                return true;
            }"""
    
    new_logic = """if(!eData) return false;"""
    
    html = html.replace(old_logic, new_logic)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Patched {filepath}")

patch_file('static/index.html')
patch_file('index_render.html')
