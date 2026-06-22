import re

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update tabsWithFilters to include 'admin'
    html = re.sub(r"const tabsWithFilters = \['training', 'evaluation', 'dashboard', 'idp', 'analytic'\];",
                  r"const tabsWithFilters = ['training', 'evaluation', 'dashboard', 'idp', 'analytic', 'admin'];", html)

    # 2. Extract matchesOrgFiltersData and update isEmployeeMatchingOrgFilters
    filter_logic = """
        function matchesOrgFiltersData(eData) {
            if(!eData) return true;
            let posName = eData.PositionNameThai || eData.position_name || eData.position;
            if(selectedJobGroupFilter.length > 0 && (!posName || !selectedJobGroupFilter.includes(positionGroups[posName]))) return false;
            if(selectedPositionsFilter.length > 0 && (!posName || !selectedPositionsFilter.includes(posName))) return false;
            
            if(selectedEmployeeFilter.length > 0) {
                let empName = eData.FullNameTH || eData.FullName || eData.EmployeeNameThai || eData.EmployeeNameEng;
                if(!empName || !selectedEmployeeFilter.includes(empName)) return false;
            }
            
            if(selectedSectionFilter.length > 0 && !selectedSectionFilter.includes(eData.SectionThai)) return false;
            if(selectedDepartmentFilter.length > 0 && !selectedDepartmentFilter.includes(eData.DepartmentThai)) return false;
            if(selectedSub1DivisionFilter.length > 0 && !selectedSub1DivisionFilter.includes(eData.Sub1DivisionThai)) return false;
            if(selectedDivisionFilter.length > 0 && !selectedDivisionFilter.includes(eData.DivisionThai)) return false;
            if(selectedSub1CompanyFilter.length > 0 && !selectedSub1CompanyFilter.includes(eData.Sub1CompanyThai)) return false;
            if(selectedCompanyFilter.length > 0 && !selectedCompanyFilter.includes(eData.CompanyThai)) return false;
            
            return true;
        }

        function isEmployeeMatchingOrgFilters(empId) {
            let emp = dbUsers[empId];
            if(!emp) return false;
            
            let eData = employeeData.find(e => e.username === empId || e.user_id === empId || e.EmployeeNameEng === emp.name || e.EmployeeNameThai === emp.name || e.FullNameTH === emp.name);
            
            if(!eData) {
                let posName = emp.position;
                if(selectedJobGroupFilter.length > 0 && (!posName || !selectedJobGroupFilter.includes(positionGroups[posName]))) return false;
                if(selectedPositionsFilter.length > 0 && (!posName || !selectedPositionsFilter.includes(posName))) return false;
                if(selectedEmployeeFilter.length > 0 || selectedSectionFilter.length > 0 || selectedDepartmentFilter.length > 0 || selectedSub1DivisionFilter.length > 0 || selectedDivisionFilter.length > 0 || selectedSub1CompanyFilter.length > 0 || selectedCompanyFilter.length > 0) return false;
                return true;
            }
            return matchesOrgFiltersData(eData);
        }
"""
    # Replace the old isEmployeeMatchingOrgFilters
    html = re.sub(r'function isEmployeeMatchingOrgFilters\(empId\) \{.*?return true;\n        \}', filter_logic, html, count=1, flags=re.DOTALL)

    # 3. Update renderAdminTable to use matchesOrgFiltersData
    admin_table_logic = """
            adminTempData.forEach((emp, index) => {
                const searchStr = `${emp.person_id} ${emp.name_th} ${emp.name_en} ${emp.user_id}`.toLowerCase();
                if(search && !searchStr.includes(search)) return;
                
                const eData = employeeDataAll[index];
                if(eData && !matchesOrgFiltersData(eData)) return;
                
                count++;
"""
    html = html.replace("""
            adminTempData.forEach((emp, index) => {
                const searchStr = `${emp.person_id} ${emp.name_th} ${emp.name_en} ${emp.user_id}`.toLowerCase();
                if(search && !searchStr.includes(search)) return;
                
                count++;
""", admin_table_logic)

    # 4. Update toggleAdminSelectAll to also use the global filter
    admin_select_logic = """
        function toggleAdminSelectAll(cb) {
            const search = document.getElementById('admin-search').value.toLowerCase();
            adminTempData.forEach((emp, index) => {
                const searchStr = `${emp.person_id} ${emp.name_th} ${emp.name_en} ${emp.user_id}`.toLowerCase();
                if(search && !searchStr.includes(search)) return;
                
                const eData = employeeDataAll[index];
                if(eData && !matchesOrgFiltersData(eData)) return;
                
                emp.is_evaluated = cb.checked;
            });
            renderAdminTable();
        }
"""
    html = re.sub(r'function toggleAdminSelectAll\(cb\) \{.*?\n        \}', admin_select_logic, html, count=1, flags=re.DOTALL)

    # 5. Update renderActiveTab to call renderAdminTable
    render_active_tab = """
        function renderActiveTab() {
            const activeTab = document.querySelector('.tab-content.active');
            if(!activeTab) return;
            const id = activeTab.id.replace('tab-', '');
            if(id === 'training') buildTrainingMatrix();
            if(id === 'dashboard') setupDashboardTab();
            if(id === 'idp') renderIDPContent();
            if(id === 'analytic') renderAnalyticTab();
            if(id === 'admin') renderAdminTable();
        }
"""
    html = re.sub(r'function renderActiveTab\(\) \{.*?\n        \}', render_active_tab, html, count=1, flags=re.DOTALL)

    # 6. Change buildFiltersUI to use employeeDataAll so we get ALL departments/sections
    # Find let allSections = [...new Set(employeeData.map(e => e.SectionThai))] etc.
    # We can just replace employeeData.map( with employeeDataAll.map( inside buildFiltersUI
    idx_build = html.find('function buildFiltersUI()')
    end_build = html.find('}', html.find('let allCompanies', idx_build))
    build_code = html[idx_build:end_build]
    build_code = build_code.replace('employeeData.map(', 'employeeDataAll.map(')
    # Also replace employeeData.filter( inside buildFiltersUI if any
    build_code = build_code.replace('employeeData.filter(', 'employeeDataAll.filter(')
    html = html[:idx_build] + build_code + html[end_build:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Patched {filepath}")

patch_file('static/index.html')
patch_file('index_render.html')
