import re

files = [
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html',
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/index_render.html'
]

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix buildFiltersUI
    old_build_filters = """                    let empName = e.FullName || e.EmployeeNameThai || e.EmployeeNameEng;
                    if(empName) employeesSet.add(empName);
                    if(e.section) sectionsSet.add(e.section);
                    if(e.department) deptsSet.add(e.department);
                    if(e.sub1_division) sub1DivsSet.add(e.sub1_division);
                    if(e.division) divsSet.add(e.division);
                    if(e.sub1_company) sub1CompsSet.add(e.sub1_company);
                    if(e.company) compsSet.add(e.company);
                    if(e.position_name) posSet.add(e.position_name);"""
                    
    new_build_filters = """                    let eName = e.name_th || e.FullName || e.EmployeeNameThai;
                    let eSect = e.section || e.SectionThai;
                    let eDept = e.department || e.DepartmentThai;
                    let eSub1Div = e.sub1_division || e.Sub1DivisionThai;
                    let eDiv = e.division || e.DivisionThai;
                    let eSub1Comp = e.sub1_company || e.Sub1CompanyThai;
                    let eComp = e.company || e.CompanyThai;
                    let ePos = e.position_name || e.PositionNameThai;
                    if(eName) employeesSet.add(eName);
                    if(eSect) sectionsSet.add(eSect);
                    if(eDept) deptsSet.add(eDept);
                    if(eSub1Div) sub1DivsSet.add(eSub1Div);
                    if(eDiv) divsSet.add(eDiv);
                    if(eSub1Comp) sub1CompsSet.add(eSub1Comp);
                    if(eComp) compsSet.add(eComp);
                    if(ePos) posSet.add(ePos);"""
                    
    content = content.replace(old_build_filters, new_build_filters)

    # 2. Fix renderEmployeeDataTab HTML
    old_render = """                        <td class="py-3 px-6 border-r border-slate-100 font-medium">${emp.person_id || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 text-scg-700 font-medium">${emp.employee_id || emp.SCGEmployeeID || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 text-scg-700 font-medium">${emp.user_id || emp.username || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 text-slate-500">${emp.password || '-'}</td>
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
                        <td class="py-3 px-6 border-r border-slate-100 text-center">${emp.years_of_service !== null && emp.years_of_service !== undefined ? emp.years_of_service : '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 text-center">${emp.age || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.report_to_name || emp.ManagerName || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.certificate_entry_degree || '-'}</td>
                        <td class="py-3 px-6 text-blue-600 hover:underline"><a href="mailto:${emp.email_address_business || ''}">${emp.email_address_business || '-'}</a></td>"""
                        
    new_render = """                        <td class="py-3 px-6 border-r border-slate-100 font-medium">${emp.person_id || emp.PersonID || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 text-scg-700 font-medium">${emp.employee_id || emp.SCGEmployeeID || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 text-scg-700 font-medium">${emp.user_id || emp.username || emp.USER || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 text-slate-500">${emp.password || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.name_th || emp.FullName || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.name_en || (emp.FirstNameEnglish ? emp.FirstNameEnglish + ' ' + (emp.LastNameEnglish || '') : '') || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.nick_name || emp.NickName || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.position_name || emp.PositionNameThai || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 text-center"><span class="bg-slate-100 text-slate-700 px-2 py-1 rounded font-bold text-xs">${emp.position_level || emp.PLGroup || '-'}</span></td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.section || emp.SectionThai || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.department || emp.DepartmentThai || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.sub1_division || emp.Sub1DivisionThai || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.division || emp.DivisionThai || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.sub1_company || emp.Sub1CompanyThai || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.company || emp.CompanyThai || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.sub1_1_business_unit || emp.Sub11BusinessUnitThai || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.working_location || emp.WorkingLocation || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 font-mono text-xs">${emp.cost_center_payment || emp.CostCenterPayment || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 font-mono text-xs">${emp.cost_center_organization || emp.CostCenterOrganization || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 text-center">${emp.retirement_year || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 text-center">${emp.years_of_service !== null && emp.years_of_service !== undefined ? emp.years_of_service : '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 text-center">${emp.age || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.report_to_name || emp.ManagerName || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.certificate_entry_degree || '-'}</td>
                        <td class="py-3 px-6 text-blue-600 hover:underline"><a href="mailto:${emp.email_address_business || emp.EmailAddressBusiness || ''}">${emp.email_address_business || emp.EmailAddressBusiness || '-'}</a></td>"""
                        
    content = content.replace(old_render, new_render)
    
    # 3. Fix exportEmployeeData HTML
    old_export = """                    emp.person_id || '', emp.employee_id || emp.SCGEmployeeID || '', emp.name_th || emp.EmployeeNameThai || emp.FullName || '', emp.name_en || emp.EmployeeNameEng || '',
                    emp.nick_name || '', emp.position_name || emp.PositionNameThai || '', emp.position_level || emp.PositionLevel || '',
                    emp.section || emp.SectionThai || '', emp.department || emp.DepartmentThai || '', emp.sub1_division || emp.Sub1DivisionThai || '',
                    emp.division || emp.DivisionThai || '', emp.sub1_company || emp.Sub1CompanyThai || '', emp.company || emp.CompanyThai || '',
                    emp.sub1_1_business_unit || '', emp.working_location || '',
                    emp.cost_center_payment || emp.CostCenter || '', emp.cost_center_organization || '',
                    emp.retirement_year || '', emp.years_of_service !== null && emp.years_of_service !== undefined ? emp.years_of_service : '',
                    emp.age || '', emp.report_to_name || emp.ManagerName || '', emp.certificate_entry_degree || '',
                    emp.email_address_business || ''"""
                    
    new_export = """                    emp.person_id || emp.PersonID || '', emp.employee_id || emp.SCGEmployeeID || '', emp.name_th || emp.FullName || '', emp.name_en || (emp.FirstNameEnglish ? emp.FirstNameEnglish + ' ' + (emp.LastNameEnglish || '') : '') || '',
                    emp.nick_name || emp.NickName || '', emp.position_name || emp.PositionNameThai || '', emp.position_level || emp.PLGroup || '',
                    emp.section || emp.SectionThai || '', emp.department || emp.DepartmentThai || '', emp.sub1_division || emp.Sub1DivisionThai || '',
                    emp.division || emp.DivisionThai || '', emp.sub1_company || emp.Sub1CompanyThai || '', emp.company || emp.CompanyThai || '',
                    emp.sub1_1_business_unit || emp.Sub11BusinessUnitThai || '', emp.working_location || emp.WorkingLocation || '',
                    emp.cost_center_payment || emp.CostCenterPayment || '', emp.cost_center_organization || emp.CostCenterOrganization || '',
                    emp.retirement_year || '', emp.years_of_service !== null && emp.years_of_service !== undefined ? emp.years_of_service : '',
                    emp.age || '', emp.report_to_name || emp.ManagerName || '', emp.certificate_entry_degree || '',
                    emp.email_address_business || emp.EmailAddressBusiness || ''"""
                    
    content = content.replace(old_export, new_export)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Fixed")
