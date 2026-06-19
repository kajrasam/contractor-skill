import re

with open('build_frontend.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix filter matching
content = content.replace('e.section)', 'e.SectionThai)')
content = content.replace('e.department)', 'e.DepartmentThai)')
content = content.replace('e.sub1_division)', 'e.Sub1DivisionThai)')
content = content.replace('e.division)', 'e.DivisionThai)')
content = content.replace('e.sub1_company)', 'e.Sub1CompanyThai)')
content = content.replace('e.company)', 'e.CompanyThai)')
content = content.replace('e.position_name)', 'e.PositionNameThai)')

# Fix CSV Export
old_csv = """            const csvContent = [
                ['Person ID', 'Employee ID', 'User ID', 'Name (TH)', 'Name (EN)', 'Nick Name', 'Position Name', 'Position Level', 'Section', 'Department', 'Sub1-Division', 'Division', 'Sub1-Company', 'Company', 'Sub1-1 Business Unit', 'Working Location', 'Cost Center (Payment)', 'Cost Center (Organization)', 'Retirement Year', 'อายุงาน', 'Age', 'Report to Name', 'Certificate (Entry Degree)', 'Email Address Business'].join(','),
                ...employeeData.map(emp => [
                    emp.person_id || '', emp.employee_id || '', emp.user_id || '',
                    emp.name_th || '', emp.name_en || '', emp.nick_name || '',
                    emp.position_name || '', emp.position_level || '',
                    emp.section || '', emp.department || '', emp.sub1_division || '',
                    emp.division || '', emp.sub1_company || '', emp.company || '',
                    emp.sub1_1_business_unit || '', emp.working_location || '',
                    emp.cost_center_payment || '', emp.cost_center_organization || '',
                    emp.retirement_year || '', emp.years_of_service || '', emp.age || '',
                    emp.report_to_name || '', emp.certificate_entry_degree || '',
                    emp.email_address_business || ''
                ].map(v => `"${String(v).replace(/"/g, '""')}"`).join(','))
            ].join('\\n');"""

new_csv = """            const csvContent = [
                ['USER ID', 'PASSWORD', 'ชื่อ-นามสกุล (TH)', 'ตำแหน่ง (POSITION)', 'SECTION (TH)', 'DEPARTMENT (TH)', 'SUB1-DIVISION (TH)', 'DIVISION (TH)', 'SUB1-COMPANY (TH)', 'COMPANY (TH)', 'PERSONNEL AREA', 'REPORT TO NAME', 'REPORT TO EMAIL', 'EMAIL ADDRESS BUSINESS'].join(','),
                ...employeeData.map(emp => [
                    emp.user_id || '', emp.password || '', emp.FullNameThai || '',
                    emp.PositionNameThai || '', emp.SectionThai || '', emp.DepartmentThai || '',
                    emp.Sub1DivisionThai || '', emp.DivisionThai || '', emp.Sub1CompanyThai || '',
                    emp.CompanyThai || '', emp.PersonnelArea || '', emp.ReportToName || '',
                    emp.ReportToEmail || '', emp.EmailAddressBusiness || ''
                ].map(v => `"${String(v).replace(/"/g, '""')}"`).join(','))
            ].join('\\n');"""

# The script might not find the exact old_csv string because of formatting, so I'll use regex.
pattern_csv = re.compile(r'            const csvContent = \[\n                \[\'Person ID\'.*?\].join\(\'\\n\'\);', re.DOTALL)
content = pattern_csv.sub(new_csv, content)

with open('build_frontend.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated build_frontend.py filters and CSV export")
