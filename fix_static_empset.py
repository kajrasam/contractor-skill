import re

with open('d:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the missing employeesSet declaration
content = content.replace(
    "let sectionsSet = new Set(), deptsSet = new Set(), sub1DivsSet = new Set(), divsSet = new Set(), sub1CompsSet = new Set(), compsSet = new Set(), posSet = new Set();",
    "let sectionsSet = new Set(), deptsSet = new Set(), sub1DivsSet = new Set(), divsSet = new Set(), sub1CompsSet = new Set(), compsSet = new Set(), posSet = new Set(), employeesSet = new Set();"
)

# Add employees to employeesSet in the loop
old_loop = """                    if(e.company || e.CompanyThai) compsSet.add(e.company || e.CompanyThai);
                    if(e.position_name || e.PositionNameThai) posSet.add(e.position_name || e.PositionNameThai);
                });"""
new_loop = """                    if(e.company || e.CompanyThai) compsSet.add(e.company || e.CompanyThai);
                    if(e.position_name || e.PositionNameThai) posSet.add(e.position_name || e.PositionNameThai);
                    let empName = e.FullNameTH || e.FullName || e.EmployeeNameThai || e.EmployeeNameEng;
                    if(empName) employeesSet.add(empName);
                });"""
content = content.replace(old_loop, new_loop)

with open('d:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("static/index.html fixed employeesSet")
