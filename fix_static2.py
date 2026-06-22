import re

with open('d:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# employee name in buildFiltersUI
content = content.replace("let empName = e.FullName || e.EmployeeNameThai || e.EmployeeNameEng;", "let empName = e.FullNameTH || e.FullName || e.EmployeeNameThai || e.EmployeeNameEng;")

# employee name in populateEmployeeSelects
content = content.replace("let empName = e.FullName || e.EmployeeNameThai || e.EmployeeNameEng;", "let empName = e.FullNameTH || e.FullName || e.EmployeeNameThai || e.EmployeeNameEng;")

with open('d:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("static/index.html fixed 2")
