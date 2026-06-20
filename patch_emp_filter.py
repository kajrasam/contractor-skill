import re

files = [
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html',
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/index_render.html'
]

employee_filter_html = """                    <div class="w-full relative">
                        <label class="block text-sm font-bold text-slate-700 mb-2"><i class="fa-solid fa-user text-scg-500 mr-1"></i> ชื่อพนักงาน</label>
                        <button onclick="toggleFilterMenu('employee-menu')" class="w-full flex items-center justify-between bg-white border border-slate-300 px-4 py-2.5 rounded-xl text-left shadow-sm hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-scg-500 transition-colors">
                            <span class="text-sm font-medium text-slate-700 truncate" id="employee-dropdown-text">เลือกพนักงานทั้งหมด</span>
                            <i class="fa-solid fa-chevron-down text-slate-400 ml-2"></i>
                        </button>
                        <div id="employee-menu" class="filter-menu hidden absolute top-full left-0 w-full mt-2 bg-white border border-slate-200 rounded-xl shadow-xl z-30 max-h-64 overflow-y-auto">
                            <div id="employee-filters" class="p-2 flex flex-col gap-1">
                                <!-- Injected by JS -->
                            </div>
                        </div>
                    </div>"""

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add HTML
    old_grid = '<div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-100 mb-6 grid grid-cols-1 md:grid-cols-4 gap-6 relative z-20">'
    new_grid = """                <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-100 mb-6 relative z-20">
                    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-4 gap-2 border-b border-slate-100 pb-4">
                        <h3 class="text-sm font-bold text-slate-800"><i class="fa-solid fa-sliders text-scg-600 mr-2"></i>ตัวกรองข้อมูลองค์กรและพนักงาน</h3>
                        <button onclick="window.clearAllFilters()" class="px-4 py-2 bg-red-50 hover:bg-red-100 text-red-600 border border-red-200 text-sm font-medium rounded-xl transition-colors flex items-center gap-2 shadow-sm">
                            <i class="fa-solid fa-eraser"></i> ล้างตัวกรองทั้งหมด
                        </button>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-5 gap-4">"""
    content = content.replace(old_grid, new_grid)

    company_dropdown_end = """                        <div id="company-dropdown-menu" class="filter-menu hidden absolute top-full left-0 w-full mt-2 bg-white border border-slate-200 rounded-xl shadow-xl z-30 max-h-64 overflow-y-auto">
                            <div id="company-filters" class="p-2 flex flex-col gap-1">
                                <!-- Injected by JS -->
                            </div>
                        </div>
                    </div>"""
    
    # We replace `company_dropdown_end` followed by `</div>` to properly close the wrapper.
    content = re.sub(
        re.escape(company_dropdown_end) + r"\s*</div>\s*(?=<!--|</div>)", 
        company_dropdown_end + "\n" + employee_filter_html + "\n                    </div>\n                </div>\n",
        content,
        count=1
    )

    # Add selectedEmployeeFilter = []
    content = content.replace("let selectedCompanyFilter = [];", "let selectedCompanyFilter = [];\n        let selectedEmployeeFilter = [];")

    # matchesFiltersExcept
    old_matches = "if (ignoreFilter !== 'jobGroup' && selectedJobGroupFilter.length > 0) {"
    new_matches = """if (ignoreFilter !== 'employee' && selectedEmployeeFilter.length > 0) {
                let empName = e.FullName || e.EmployeeNameThai || e.EmployeeNameEng;
                if (!empName || !selectedEmployeeFilter.includes(empName)) return false;
            }
            if (ignoreFilter !== 'jobGroup' && selectedJobGroupFilter.length > 0) {"""
    content = content.replace(old_matches, new_matches)

    # buildFiltersUI sets
    content = content.replace(
        "const compContainer = document.getElementById('competency-filters');",
        "const compContainer = document.getElementById('competency-filters');\n            const employeeContainer = document.getElementById('employee-filters');"
    )

    content = content.replace(
        "let sectionsSet = new Set(), deptsSet = new Set(), sub1DivsSet = new Set(), divsSet = new Set(), sub1CompsSet = new Set(), compsSet = new Set(), posSet = new Set(), jobGroupsSet = new Set();",
        "let sectionsSet = new Set(), deptsSet = new Set(), sub1DivsSet = new Set(), divsSet = new Set(), sub1CompsSet = new Set(), compsSet = new Set(), posSet = new Set(), jobGroupsSet = new Set(), employeesSet = new Set();"
    )

    old_org_sets = "if (matchesFiltersExcept(e, 'company')) if(e.CompanyThai) compsSet.add(e.CompanyThai);"
    new_org_sets = "if (matchesFiltersExcept(e, 'company')) if(e.CompanyThai) compsSet.add(e.CompanyThai);\n                if (matchesFiltersExcept(e, 'employee')) {\n                    let empName = e.FullName || e.EmployeeNameThai || e.EmployeeNameEng;\n                    if(empName) employeesSet.add(empName);\n                }"
    content = content.replace(old_org_sets, new_org_sets)

    old_build_inner = "if(companyContainer) companyContainer.innerHTML = buildFilterHtml(compsSet, selectedCompanyFilter, 'company');"
    new_build_inner = "if(companyContainer) companyContainer.innerHTML = buildFilterHtml(compsSet, selectedCompanyFilter, 'company');\n            if(employeeContainer) employeeContainer.innerHTML = buildFilterHtml(employeesSet, selectedEmployeeFilter, 'employee');"
    content = content.replace(old_build_inner, new_build_inner)

    old_update_text = "updateText('company-dropdown-text', selectedCompanyFilter, 'เลือก Company ทั้งหมด');"
    new_update_text = "updateText('company-dropdown-text', selectedCompanyFilter, 'เลือก Company ทั้งหมด');\n            updateText('employee-dropdown-text', selectedEmployeeFilter, 'เลือกพนักงานทั้งหมด');"
    content = content.replace(old_update_text, new_update_text)

    # toggleFilterValue
    content = content.replace(
        "else if(type === 'company') arr = selectedCompanyFilter;",
        "else if(type === 'company') arr = selectedCompanyFilter;\n            else if(type === 'employee') arr = selectedEmployeeFilter;"
    )

    # setAllFilter
    content = content.replace(
        "else if(type === 'company') { arr = selectedCompanyFilter; containerId = 'company-filters'; }",
        "else if(type === 'company') { arr = selectedCompanyFilter; containerId = 'company-filters'; }\n            else if(type === 'employee') { arr = selectedEmployeeFilter; containerId = 'employee-filters'; }"
    )

    # isEmployeeMatchingOrgFilters
    content = content.replace(
        "if(selectedSectionFilter.length > 0 || selectedDepartmentFilter.length > 0 || selectedSub1DivisionFilter.length > 0 || selectedDivisionFilter.length > 0 || selectedSub1CompanyFilter.length > 0 || selectedCompanyFilter.length > 0) return false;",
        "if(selectedEmployeeFilter.length > 0 || selectedSectionFilter.length > 0 || selectedDepartmentFilter.length > 0 || selectedSub1DivisionFilter.length > 0 || selectedDivisionFilter.length > 0 || selectedSub1CompanyFilter.length > 0 || selectedCompanyFilter.length > 0) return false;"
    )
    
    old_isEmp = "if(selectedSectionFilter.length > 0 && (!eData.SectionThai || !selectedSectionFilter.includes(eData.SectionThai))) return false;"
    new_isEmp = """let empName = eData.FullName || eData.EmployeeNameThai || eData.EmployeeNameEng;
            if(selectedEmployeeFilter.length > 0 && (!empName || !selectedEmployeeFilter.includes(empName))) return false;
            
            if(selectedSectionFilter.length > 0 && (!eData.SectionThai || !selectedSectionFilter.includes(eData.SectionThai))) return false;"""
    content = content.replace(old_isEmp, new_isEmp)
    
    # clearAllFilters function
    clear_func = """
        window.clearAllFilters = function() {
            selectedJobGroupFilter = [];
            selectedPositionsFilter = [];
            selectedSectionFilter = [];
            selectedDepartmentFilter = [];
            selectedSub1DivisionFilter = [];
            selectedDivisionFilter = [];
            selectedSub1CompanyFilter = [];
            selectedCompanyFilter = [];
            selectedEmployeeFilter = [];
            
            selectedCompetencyGroupFilter = [];
            selectedCompetenciesFilter = [];
            
            buildFiltersUI();
            renderActiveTab();
        };"""
    content = content.replace("window.setAllFilter = function", clear_func + "\n\n        window.setAllFilter = function")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
print("Done!")
