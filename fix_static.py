import re

with open('d:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix filter sets
content = content.replace("if(e.section) sectionsSet.add(e.section);", "if(e.section || e.SectionThai) sectionsSet.add(e.section || e.SectionThai);")
content = content.replace("if(e.department) deptsSet.add(e.department);", "if(e.department || e.DepartmentThai) deptsSet.add(e.department || e.DepartmentThai);")
content = content.replace("if(e.sub1_division) sub1DivsSet.add(e.sub1_division);", "if(e.sub1_division || e.Sub1DivisionThai) sub1DivsSet.add(e.sub1_division || e.Sub1DivisionThai);")
content = content.replace("if(e.division) divsSet.add(e.division);", "if(e.division || e.DivisionThai) divsSet.add(e.division || e.DivisionThai);")
content = content.replace("if(e.sub1_company) sub1CompsSet.add(e.sub1_company);", "if(e.sub1_company || e.Sub1CompanyThai) sub1CompsSet.add(e.sub1_company || e.Sub1CompanyThai);")
content = content.replace("if(e.company) compsSet.add(e.company);", "if(e.company || e.CompanyThai) compsSet.add(e.company || e.CompanyThai);")
content = content.replace("if(e.position_name) posSet.add(e.position_name);", "if(e.position_name || e.PositionNameThai) posSet.add(e.position_name || e.PositionNameThai);")

# Fix employee filter matching logic
content = content.replace("const emps = employeeData.filter(e => p.includes(e.position_name) || (e.position_name && e.position_name.includes(p)));", "const emps = employeeData.filter(e => p.includes(e.position_name || e.PositionNameThai) || ((e.position_name || e.PositionNameThai) && (e.position_name || e.PositionNameThai).includes(p)));")

with open('d:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("static/index.html fixed")
