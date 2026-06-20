import re

files = [
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html',
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/index_render.html'
]

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update the table logic
    old_logic = "emp.name_en || (emp.FirstNameEnglish ? emp.FirstNameEnglish + ' ' + (emp.LastNameEnglish || '') : '') || '-'"
    new_logic = "emp.name_en || emp.FullNameENG || (emp.FirstNameEnglish ? (emp.NamePrefixEnglish ? emp.NamePrefixEnglish + ' ' : '') + emp.FirstNameEnglish + ' ' + (emp.LastNameEnglish || '') : '') || '-'"
    content = content.replace(old_logic, new_logic)

    # 2. Update the export logic
    old_export_logic = "emp.name_en || (emp.FirstNameEnglish ? emp.FirstNameEnglish + ' ' + (emp.LastNameEnglish || '') : '') || ''"
    new_export_logic = "emp.name_en || emp.FullNameENG || (emp.FirstNameEnglish ? (emp.NamePrefixEnglish ? emp.NamePrefixEnglish + ' ' : '') + emp.FirstNameEnglish + ' ' + (emp.LastNameEnglish || '') : '') || ''"
    content = content.replace(old_export_logic, new_export_logic)
    
    # 3. Change header from NAME (EN) to FULLNAME ENG
    content = content.replace('NAME (EN)', 'FULLNAME ENG')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Done")
