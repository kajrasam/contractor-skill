import re

path = "d:\\Work\\งานใหม่\\อบรม\\2026\\Vibe Coding Workshop\\Project\\competency-system\\build_frontend.py"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add state variables
state_vars = """        let selectedJobGroupFilter = [];
        let selectedSectionFilter = [];
        let selectedDepartmentFilter = [];
        let selectedSub1DivisionFilter = [];
        let selectedDivisionFilter = [];
        let selectedSub1CompanyFilter = [];
        let selectedCompanyFilter = [];"""
content = content.replace("        let selectedJobGroupFilter = [];", state_vars)

# 2. Update buildFiltersUI() top part
# We need to find `const posContainer = document.getElementById('position-filters');`
# and add the new containers.
containers_replacement = """            const posContainer = document.getElementById('position-filters');
            const sectionContainer = document.getElementById('section-filters');
            const departmentContainer = document.getElementById('department-filters');
            const sub1DivisionContainer = document.getElementById('sub1division-filters');
            const divisionContainer = document.getElementById('division-filters');
            const sub1CompanyContainer = document.getElementById('sub1company-filters');
            const companyContainer = document.getElementById('company-filters');"""
content = content.replace("            const posContainer = document.getElementById('position-filters');", containers_replacement)

# 3. Add logic to build HTML for new filters in buildFiltersUI
# Insert it after `jobGroupContainer.innerHTML = jobGroupHtml;` block
new_filters_html_logic = """
            // Build Org Filters
            let sectionsSet = new Set(), deptsSet = new Set(), sub1DivsSet = new Set(), divsSet = new Set(), sub1CompsSet = new Set(), compsSet = new Set();
            visiblePos.forEach(p => {
                const emps = employeeData.filter(e => e.position_name === p);
                emps.forEach(e => {
                    if(e.section) sectionsSet.add(e.section);
                    if(e.department) deptsSet.add(e.department);
                    if(e.sub1_division) sub1DivsSet.add(e.sub1_division);
                    if(e.division) divsSet.add(e.division);
                    if(e.sub1_company) sub1CompsSet.add(e.sub1_company);
                    if(e.company) compsSet.add(e.company);
                });
            });

            const buildFilterHtml = (items, selectedArr, toggleFn) => {
                let html = '';
                Array.from(items).sort().forEach(item => {
                    const isSelected = selectedArr.includes(item);
                    html += `<label class="flex items-center gap-3 px-3 py-2 hover:bg-slate-50 rounded-lg cursor-pointer transition-colors w-full">
                        <input type="checkbox" class="form-checkbox h-4 w-4 text-scg-600 rounded border-slate-300" ${isSelected ? 'checked' : ''} onchange="${toggleFn}('${item}')">
                        <span class="text-sm font-medium ${isSelected ? 'text-scg-700' : 'text-slate-600'}">${item}</span>
                    </label>`;
                });
                return html;
            };

            if(sectionContainer) sectionContainer.innerHTML = buildFilterHtml(sectionsSet, selectedSectionFilter, 'toggleSectionFilter');
            if(departmentContainer) departmentContainer.innerHTML = buildFilterHtml(deptsSet, selectedDepartmentFilter, 'toggleDepartmentFilter');
            if(sub1DivisionContainer) sub1DivisionContainer.innerHTML = buildFilterHtml(sub1DivsSet, selectedSub1DivisionFilter, 'toggleSub1DivisionFilter');
            if(divisionContainer) divisionContainer.innerHTML = buildFilterHtml(divsSet, selectedDivisionFilter, 'toggleDivisionFilter');
            if(sub1CompanyContainer) sub1CompanyContainer.innerHTML = buildFilterHtml(sub1CompsSet, selectedSub1CompanyFilter, 'toggleSub1CompanyFilter');
            if(companyContainer) companyContainer.innerHTML = buildFilterHtml(compsSet, selectedCompanyFilter, 'toggleCompanyFilter');
"""
target_job_group = "                jobGroupContainer.innerHTML = jobGroupHtml;\n            }"
if target_job_group in content:
    content = content.replace(target_job_group, target_job_group + "\n" + new_filters_html_logic)

# 4. Filter visiblePos for position dropdowns
# We need to add the org filters logic before populating posHtml.
org_filter_logic = """
            let orgFiltersActive = selectedSectionFilter.length > 0 || selectedDepartmentFilter.length > 0 || selectedSub1DivisionFilter.length > 0 || selectedDivisionFilter.length > 0 || selectedSub1CompanyFilter.length > 0 || selectedCompanyFilter.length > 0;
            if (orgFiltersActive) {
                filteredPositionsForDropdown = filteredPositionsForDropdown.filter(p => {
                    const emps = employeeData.filter(e => e.position_name === p);
                    if(emps.length === 0) return false;
                    return emps.some(e => {
                        let match = true;
                        if (selectedSectionFilter.length > 0 && !selectedSectionFilter.includes(e.section)) match = false;
                        if (selectedDepartmentFilter.length > 0 && !selectedDepartmentFilter.includes(e.department)) match = false;
                        if (selectedSub1DivisionFilter.length > 0 && !selectedSub1DivisionFilter.includes(e.sub1_division)) match = false;
                        if (selectedDivisionFilter.length > 0 && !selectedDivisionFilter.includes(e.division)) match = false;
                        if (selectedSub1CompanyFilter.length > 0 && !selectedSub1CompanyFilter.includes(e.sub1_company)) match = false;
                        if (selectedCompanyFilter.length > 0 && !selectedCompanyFilter.includes(e.company)) match = false;
                        return match;
                    });
                });
            }
"""
content = content.replace("            if(selectedJobGroupFilter.length > 0) {\n                filteredPositionsForDropdown = visiblePos.filter(p => selectedJobGroupFilter.includes(positionGroups[p]));\n            }", 
                         "            if(selectedJobGroupFilter.length > 0) {\n                filteredPositionsForDropdown = visiblePos.filter(p => selectedJobGroupFilter.includes(positionGroups[p]));\n            }\n" + org_filter_logic)

# 5. Update dropdown text indicators
update_text_logic = """
            const updateText = (id, arr, defaultText) => {
                const el = document.getElementById(id);
                if(el) {
                    if(arr.length === 0) el.textContent = defaultText;
                    else el.textContent = `เลือกแล้ว ${arr.length} รายการ`;
                }
            };
            updateText('section-dropdown-text', selectedSectionFilter, 'เลือก Section ทั้งหมด');
            updateText('department-dropdown-text', selectedDepartmentFilter, 'เลือก Department ทั้งหมด');
            updateText('sub1division-dropdown-text', selectedSub1DivisionFilter, 'เลือก Sub1-Division ทั้งหมด');
            updateText('division-dropdown-text', selectedDivisionFilter, 'เลือก Division ทั้งหมด');
            updateText('sub1company-dropdown-text', selectedSub1CompanyFilter, 'เลือก Sub1-Company ทั้งหมด');
            updateText('company-dropdown-text', selectedCompanyFilter, 'เลือก Company ทั้งหมด');
"""
content = content.replace("                if(selectedJobGroupFilter.length === 0) jobGroupText.textContent = 'เลือกกลุ่มงานทั้งหมด';", 
                          "                if(selectedJobGroupFilter.length === 0) jobGroupText.textContent = 'เลือกกลุ่มงานทั้งหมด';\n" + update_text_logic)

# 6. Add toggle functions for new filters
toggle_functions = """
        window.toggleSectionFilter = function(v) {
            if(selectedSectionFilter.includes(v)) selectedSectionFilter = selectedSectionFilter.filter(x => x !== v);
            else selectedSectionFilter.push(v);
            buildFiltersUI(); buildRoleResponseSection(); buildTrainingMatrix();
        }
        window.toggleDepartmentFilter = function(v) {
            if(selectedDepartmentFilter.includes(v)) selectedDepartmentFilter = selectedDepartmentFilter.filter(x => x !== v);
            else selectedDepartmentFilter.push(v);
            buildFiltersUI(); buildRoleResponseSection(); buildTrainingMatrix();
        }
        window.toggleSub1DivisionFilter = function(v) {
            if(selectedSub1DivisionFilter.includes(v)) selectedSub1DivisionFilter = selectedSub1DivisionFilter.filter(x => x !== v);
            else selectedSub1DivisionFilter.push(v);
            buildFiltersUI(); buildRoleResponseSection(); buildTrainingMatrix();
        }
        window.toggleDivisionFilter = function(v) {
            if(selectedDivisionFilter.includes(v)) selectedDivisionFilter = selectedDivisionFilter.filter(x => x !== v);
            else selectedDivisionFilter.push(v);
            buildFiltersUI(); buildRoleResponseSection(); buildTrainingMatrix();
        }
        window.toggleSub1CompanyFilter = function(v) {
            if(selectedSub1CompanyFilter.includes(v)) selectedSub1CompanyFilter = selectedSub1CompanyFilter.filter(x => x !== v);
            else selectedSub1CompanyFilter.push(v);
            buildFiltersUI(); buildRoleResponseSection(); buildTrainingMatrix();
        }
        window.toggleCompanyFilter = function(v) {
            if(selectedCompanyFilter.includes(v)) selectedCompanyFilter = selectedCompanyFilter.filter(x => x !== v);
            else selectedCompanyFilter.push(v);
            buildFiltersUI(); buildRoleResponseSection(); buildTrainingMatrix();
        }
"""
content = content.replace("        window.toggleJobGroupFilter = function(g) {", toggle_functions + "\n        window.toggleJobGroupFilter = function(g) {")

# 7. Apply org filters in buildRoleResponseSection and buildTrainingMatrix
org_filter_apply_logic = """
            let orgFiltersActive = selectedSectionFilter.length > 0 || selectedDepartmentFilter.length > 0 || selectedSub1DivisionFilter.length > 0 || selectedDivisionFilter.length > 0 || selectedSub1CompanyFilter.length > 0 || selectedCompanyFilter.length > 0;
            if (orgFiltersActive) {
                visiblePos = visiblePos.filter(p => {
                    const emps = employeeData.filter(e => e.position_name === p);
                    if(emps.length === 0) return false;
                    return emps.some(e => {
                        let match = true;
                        if (selectedSectionFilter.length > 0 && !selectedSectionFilter.includes(e.section)) match = false;
                        if (selectedDepartmentFilter.length > 0 && !selectedDepartmentFilter.includes(e.department)) match = false;
                        if (selectedSub1DivisionFilter.length > 0 && !selectedSub1DivisionFilter.includes(e.sub1_division)) match = false;
                        if (selectedDivisionFilter.length > 0 && !selectedDivisionFilter.includes(e.division)) match = false;
                        if (selectedSub1CompanyFilter.length > 0 && !selectedSub1CompanyFilter.includes(e.sub1_company)) match = false;
                        if (selectedCompanyFilter.length > 0 && !selectedCompanyFilter.includes(e.company)) match = false;
                        return match;
                    });
                });
            }
"""

content = content.replace("            if(selectedJobGroupFilter.length > 0) {\n                visiblePos = visiblePos.filter(p => selectedJobGroupFilter.includes(positionGroups[p]));\n            }", 
                          "            if(selectedJobGroupFilter.length > 0) {\n                visiblePos = visiblePos.filter(p => selectedJobGroupFilter.includes(positionGroups[p]));\n            }\n" + org_filter_apply_logic)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Patch successful!")
