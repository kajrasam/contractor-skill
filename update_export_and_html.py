import re

# Update build_frontend.py
with open('build_frontend.py', 'r', encoding='utf-8') as f:
    content = f.read()

# We can just replace the whole body of exportEmployeeData
old_func_pattern = re.compile(r'        function exportEmployeeData\(\) \{.*?link\.click\(\);\n            document\.body\.removeChild\(link\);\n        \}', re.DOTALL)

# Find the match
match = old_func_pattern.search(content)

new_func = '''        function exportEmployeeData() {
            if(!employeeData || employeeData.length === 0) {
                showToast("ไม่มีข้อมูลให้ Export");
                return;
            }
            
            const headers = [
                "USER ID", "PASSWORD", "Full Name", "POSITION", "SECTION (TH)", 
                "DEPARTMENT (TH)", "SUB1-DIVISION (TH)", "DIVISION (TH)", "SUB1-COMPANY (TH)", 
                "COMPANY (TH)", "PERSONNEL AREA", "REPORT TO NAME", "REPORT TO EMAIL", 
                "EMAIL ADDRESS BUSINESS"
            ];
            
            let csvContent = "\\uFEFF" + headers.join(",") + "\\n";
            
            employeeData.forEach(emp => {
                const row = [
                    emp.user_id || '', emp.password || '', emp.FullName || '',
                    emp.PositionNameThai || '', emp.SectionThai || '', emp.DepartmentThai || '',
                    emp.Sub1DivisionThai || '', emp.DivisionThai || '', emp.Sub1CompanyThai || '',
                    emp.CompanyThai || '', emp.PersonnelArea || '', emp.ReportToName || '',
                    emp.ReportToEmail || '', emp.EmailAddressBusiness || ''
                ].map(val => `"${String(val).replace(/"/g, '""')}"`);
                
                csvContent += row.join(",") + "\\n";
            });
            
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement("a");
            const url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", `Employee_Data_Export_${new Date().getTime()}.csv`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }'''

if match:
    content = content[:match.start()] + new_func + content[match.end():]
    with open('build_frontend.py', 'w', encoding='utf-8') as f:
        f.write(content)
else:
    print("Could not find exportEmployeeData")

# Update HTML
html_path = '../competency_system_dynamic_rbac_hierarchy.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('ชื่อ-นามสกุล (TH)', 'Full Name')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated build_frontend.py and html")
