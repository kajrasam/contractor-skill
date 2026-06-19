import re

with open('build_frontend.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace renderEmployeeDataTab body
new_render_func = """        function renderEmployeeDataTab() {
            const tbody = document.getElementById('employee-data-tbody');
            if(!tbody) return;
            
            if(!employeeData || employeeData.length === 0) {
                tbody.innerHTML = `<tr><td colspan="14" class="text-center py-8 text-slate-500">ไม่พบข้อมูลพนักงาน หรือตารางยังไม่ได้ถูกสร้างขึ้นในฐานข้อมูล</td></tr>`;
                return;
            }

            // Inject FullNameThai for filtering and display
            employeeData.forEach(emp => {
                emp.FullNameThai = [emp.NamePrefixThai, emp.FirstNameThai, emp.LastNameThai].filter(Boolean).join(' ') || '-';
            });

            let html = '';
            employeeData.forEach(emp => {
                html += `
                    <tr class="hover:bg-slate-50 transition-colors">
                        <td class="py-3 px-6 border-r border-slate-100 text-scg-700 font-medium">${emp.user_id || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 text-slate-500">${emp.password || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.FullNameThai}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.PositionNameThai || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.SectionThai || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.DepartmentThai || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.Sub1DivisionThai || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.DivisionThai || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.Sub1CompanyThai || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.CompanyThai || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.PersonnelArea || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.ReportToName || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 text-blue-600 hover:underline"><a href="mailto:${emp.ReportToEmail || ''}">${emp.ReportToEmail || '-'}</a></td>
                        <td class="py-3 px-6 text-blue-600 hover:underline"><a href="mailto:${emp.EmailAddressBusiness || ''}">${emp.EmailAddressBusiness || '-'}</a></td>
                    </tr>
                `;
            });
            tbody.innerHTML = html;
            setTimeout(buildEmployeeFilters, 0); // wait for DOM update
        }"""

pattern_render = re.compile(r'        function renderEmployeeDataTab\(\) \{.*?setTimeout\(buildEmployeeFilters, 0\); // wait for DOM update\n        \}', re.DOTALL)
content = pattern_render.sub(new_render_func, content)

# Replace colKeys
new_col_keys = """            const colKeys = [
                'user_id', 'password', 'FullNameThai', 'PositionNameThai', 'SectionThai', 'DepartmentThai',
                'Sub1DivisionThai', 'DivisionThai', 'Sub1CompanyThai', 'CompanyThai', 'PersonnelArea',
                'ReportToName', 'ReportToEmail', 'EmailAddressBusiness'
            ];"""

pattern_cols = re.compile(r'            const colKeys = \[\n.*?\];', re.DOTALL)
content = pattern_cols.sub(new_col_keys, content)

with open('build_frontend.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated build_frontend.py")
