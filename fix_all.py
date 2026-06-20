import re

files = [
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html',
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/index_render.html'
]

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix matchesFiltersExcept
    old_matches = """        function matchesFiltersExcept(e, ignoreFilter) {
            if (ignoreFilter !== 'company' && selectedCompanyFilter.length > 0 && (!e.CompanyThai || !selectedCompanyFilter.includes(e.CompanyThai))) return false;
            if (ignoreFilter !== 'sub1company' && selectedSub1CompanyFilter.length > 0 && (!e.Sub1CompanyThai || !selectedSub1CompanyFilter.includes(e.Sub1CompanyThai))) return false;
            if (ignoreFilter !== 'division' && selectedDivisionFilter.length > 0 && (!e.DivisionThai || !selectedDivisionFilter.includes(e.DivisionThai))) return false;
            if (ignoreFilter !== 'sub1division' && selectedSub1DivisionFilter.length > 0 && (!e.Sub1DivisionThai || !selectedSub1DivisionFilter.includes(e.Sub1DivisionThai))) return false;
            if (ignoreFilter !== 'department' && selectedDepartmentFilter.length > 0 && (!e.DepartmentThai || !selectedDepartmentFilter.includes(e.DepartmentThai))) return false;
            if (ignoreFilter !== 'section' && selectedSectionFilter.length > 0 && (!e.SectionThai || !selectedSectionFilter.includes(e.SectionThai))) return false;"""
    
    new_matches = """        function matchesFiltersExcept(e, ignoreFilter) {
            let eComp = e.company || e.CompanyThai;
            if (ignoreFilter !== 'company' && selectedCompanyFilter.length > 0 && (!eComp || !selectedCompanyFilter.includes(eComp))) return false;
            let eSub1Comp = e.sub1_company || e.Sub1CompanyThai;
            if (ignoreFilter !== 'sub1company' && selectedSub1CompanyFilter.length > 0 && (!eSub1Comp || !selectedSub1CompanyFilter.includes(eSub1Comp))) return false;
            let eDiv = e.division || e.DivisionThai;
            if (ignoreFilter !== 'division' && selectedDivisionFilter.length > 0 && (!eDiv || !selectedDivisionFilter.includes(eDiv))) return false;
            let eSub1Div = e.sub1_division || e.Sub1DivisionThai;
            if (ignoreFilter !== 'sub1division' && selectedSub1DivisionFilter.length > 0 && (!eSub1Div || !selectedSub1DivisionFilter.includes(eSub1Div))) return false;
            let eDept = e.department || e.DepartmentThai;
            if (ignoreFilter !== 'department' && selectedDepartmentFilter.length > 0 && (!eDept || !selectedDepartmentFilter.includes(eDept))) return false;
            let eSect = e.section || e.SectionThai;
            if (ignoreFilter !== 'section' && selectedSectionFilter.length > 0 && (!eSect || !selectedSectionFilter.includes(eSect))) return false;"""
            
    content = content.replace(old_matches, new_matches)

    # 2. Fix document.addEventListener
    old_click = "const menus = ['job-group-menu', 'pos-dropdown-menu', 'comp-group-menu', 'comp-dropdown-menu', 'idp-pos-menu', 'idp-emp-menu', 'dash-job-group-menu', 'dash-pos-menu', 'analytic-job-group-menu', 'analytic-pos-menu', 'analytic-emp-menu', 'analytic-group-menu', 'analytic-skill-menu'];"
    new_click = "const menus = ['job-group-menu', 'pos-dropdown-menu', 'section-dropdown-menu', 'department-dropdown-menu', 'sub1division-dropdown-menu', 'division-dropdown-menu', 'sub1company-dropdown-menu', 'company-dropdown-menu', 'employee-menu', 'comp-group-menu', 'comp-dropdown-menu', 'idp-pos-menu', 'idp-emp-menu', 'dash-job-group-menu', 'dash-pos-menu', 'analytic-job-group-menu', 'analytic-pos-menu', 'analytic-emp-menu', 'analytic-group-menu', 'analytic-skill-menu'];"
    content = content.replace(old_click, new_click)

    # 3. Fix toggleFilterMenu to stop propagation if it's somehow bubbling
    # (Actually we just leave toggleFilterMenu as is, the syntax error was the main issue)
    
    # 4. Fix renderEmployeeDataTab (re-map fields)
    old_render = """                        <td class="py-3 px-6 border-r border-slate-100 font-medium">${emp.person_id || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 text-scg-700 font-medium">${emp.employee_id || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.name_th || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.name_en || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.nick_name || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.position_name || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 text-center"><span class="bg-slate-100 text-slate-700 px-2 py-1 rounded font-bold text-xs">${emp.position_level || '-'}</span></td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.section || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.department || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.sub1_division || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.division || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.sub1_company || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.company || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.sub1_1_business_unit || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.working_location || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 font-mono text-xs">${emp.cost_center_payment || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 font-mono text-xs">${emp.cost_center_organization || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 text-center">${emp.retirement_year || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 text-center">${emp.years_of_service !== null ? emp.years_of_service : '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 text-center">${emp.age || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.report_to_name || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.certificate_entry_degree || '-'}</td>
                        <td class="py-3 px-6 text-blue-600 hover:underline"><a href="mailto:${emp.email_address_business || ''}">${emp.email_address_business || '-'}</a></td>"""
                        
    new_render = """                        <td class="py-3 px-6 border-r border-slate-100 font-medium">${emp.person_id || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 text-scg-700 font-medium">${emp.employee_id || emp.SCGEmployeeID || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.name_th || emp.EmployeeNameThai || emp.FullName || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.name_en || emp.EmployeeNameEng || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.nick_name || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.position_name || emp.PositionNameThai || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 text-center"><span class="bg-slate-100 text-slate-700 px-2 py-1 rounded font-bold text-xs">${emp.position_level || emp.PositionLevel || '-'}</span></td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.section || emp.SectionThai || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.department || emp.DepartmentThai || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.sub1_division || emp.Sub1DivisionThai || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.division || emp.DivisionThai || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.sub1_company || emp.Sub1CompanyThai || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.company || emp.CompanyThai || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.sub1_1_business_unit || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.working_location || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 font-mono text-xs">${emp.cost_center_payment || emp.CostCenter || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 font-mono text-xs">${emp.cost_center_organization || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 text-center">${emp.retirement_year || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 text-center">${emp.years_of_service !== null ? emp.years_of_service : '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 text-center">${emp.age || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.report_to_name || emp.ManagerName || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.certificate_entry_degree || '-'}</td>
                        <td class="py-3 px-6 text-blue-600 hover:underline"><a href="mailto:${emp.email_address_business || ''}">${emp.email_address_business || '-'}</a></td>"""
                        
    content = content.replace(old_render, new_render)
    
    # 5. Fix exportEmployeeData
    old_export = """                    emp.person_id || '', emp.employee_id || '', emp.name_th || '', emp.name_en || '',
                    emp.nick_name || '', emp.position_name || '', emp.position_level || '',
                    emp.section || '', emp.department || '', emp.sub1_division || '',
                    emp.division || '', emp.sub1_company || '', emp.company || '',
                    emp.sub1_1_business_unit || '', emp.working_location || '',
                    emp.cost_center_payment || '', emp.cost_center_organization || '',
                    emp.retirement_year || '', emp.years_of_service !== null ? emp.years_of_service : '',
                    emp.age || '', emp.report_to_name || '', emp.certificate_entry_degree || '',
                    emp.email_address_business || ''"""
                    
    new_export = """                    emp.person_id || '', emp.employee_id || emp.SCGEmployeeID || '', emp.name_th || emp.EmployeeNameThai || emp.FullName || '', emp.name_en || emp.EmployeeNameEng || '',
                    emp.nick_name || '', emp.position_name || emp.PositionNameThai || '', emp.position_level || emp.PositionLevel || '',
                    emp.section || emp.SectionThai || '', emp.department || emp.DepartmentThai || '', emp.sub1_division || emp.Sub1DivisionThai || '',
                    emp.division || emp.DivisionThai || '', emp.sub1_company || emp.Sub1CompanyThai || '', emp.company || emp.CompanyThai || '',
                    emp.sub1_1_business_unit || '', emp.working_location || '',
                    emp.cost_center_payment || emp.CostCenter || '', emp.cost_center_organization || '',
                    emp.retirement_year || '', emp.years_of_service !== null ? emp.years_of_service : '',
                    emp.age || '', emp.report_to_name || emp.ManagerName || '', emp.certificate_entry_degree || '',
                    emp.email_address_business || ''"""
    
    content = content.replace(old_export, new_export)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Fixed fallbacks for filtering and Employee Data.")
