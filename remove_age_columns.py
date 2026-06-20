import re

files = [
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html',
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/index_render.html'
]

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove table headers
    # <th class="py-3 px-6 text-left border-r border-slate-200">RETIREMENT YEAR</th>
    # <th class="py-3 px-6 text-left border-r border-slate-200">อายุงาน</th>
    # <th class="py-3 px-6 text-left border-r border-slate-200">AGE</th>
    content = re.sub(r'<th[^>]*>RETIREMENT YEAR</th>', '', content)
    content = re.sub(r'<th[^>]*>อายุงาน</th>', '', content)
    content = re.sub(r'<th[^>]*>AGE</th>', '', content)
    
    # 2. Remove table columns in render
    content = re.sub(r'<td[^>]*>\$\{emp\.retirement_year \|\| \'-\'\}</td>', '', content)
    content = re.sub(r'<td[^>]*>\$\{emp\.years_of_service !== null && emp\.years_of_service !== undefined \? emp\.years_of_service : \'-\'\}</td>', '', content)
    content = re.sub(r'<td[^>]*>\$\{emp\.age \|\| \'-\'\}</td>', '', content)
    
    # 3. Remove CSV headers
    content = content.replace("Cost Center (Organization),Retirement Year,Years of Service,Age,Report to Name", "Cost Center (Organization),Report to Name")
    
    # 4. Remove CSV data
    content = content.replace("emp.cost_center_organization || emp.CostCenterOrganization || '',\n                    emp.retirement_year || '', emp.years_of_service !== null && emp.years_of_service !== undefined ? emp.years_of_service : '',\n                    emp.age || '', emp.report_to_name || emp.ManagerName || ''", "emp.cost_center_organization || emp.CostCenterOrganization || '',\n                    emp.report_to_name || emp.ManagerName || ''")
    
    # 5. Remove filters UI
    # We will search for the filter container divs by label content, they look like:
    # <div class="w-full md:w-48"><label class="block text-xs font-bold text-slate-500 mb-1">RETIREMENT YEAR</label><select id="filter-retirement" ...>...</select></div>
    content = re.sub(r'<div class="w-full md:w-48(?: mb-4)?">\s*<label[^>]*>RETIREMENT YEAR</label>.*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div class="w-full md:w-48(?: mb-4)?">\s*<label[^>]*>อายุงาน</label>.*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div class="w-full md:w-48(?: mb-4)?">\s*<label[^>]*>AGE</label>.*?</div>', '', content, flags=re.DOTALL)
    
    # Also remove from buildFiltersUI
    content = re.sub(r'const retirementContainer = document\.getElementById\(\'filter-retirement\'\);', '', content)
    content = re.sub(r'const yearsOfServiceContainer = document\.getElementById\(\'filter-years-of-service\'\);', '', content)
    content = re.sub(r'const ageContainer = document\.getElementById\(\'filter-age\'\);', '', content)
    
    content = re.sub(r'let retirementSet = new Set\(\);', '', content)
    content = re.sub(r'let yearsOfServiceSet = new Set\(\);', '', content)
    content = re.sub(r'let ageSet = new Set\(\);', '', content)
    
    content = re.sub(r'if\(e\.retirement_year\) retirementSet\.add\(e\.retirement_year\);', '', content)
    content = re.sub(r'if\(e\.years_of_service !== null && e\.years_of_service !== undefined\) yearsOfServiceSet\.add\(e\.years_of_service\);', '', content)
    content = re.sub(r'if\(e\.age\) ageSet\.add\(e\.age\);', '', content)
    
    content = re.sub(r'populateSelect\(retirementContainer, retirementSet\);', '', content)
    content = re.sub(r'populateSelect\(yearsOfServiceContainer, yearsOfServiceSet\);', '', content)
    content = re.sub(r'populateSelect\(ageContainer, ageSet\);', '', content)
    
    # Remove from matchesFiltersExcept
    content = re.sub(r'const fRetirement = document\.getElementById\(\'filter-retirement\'\)\?.value;', '', content)
    content = re.sub(r'const fYears = document\.getElementById\(\'filter-years-of-service\'\)\?.value;', '', content)
    content = re.sub(r'const fAge = document\.getElementById\(\'filter-age\'\)\?.value;', '', content)
    
    content = re.sub(r'if\(skipId !== \'filter-retirement\' && fRetirement && String\(e\.retirement_year\) !== fRetirement\) return false;', '', content)
    content = re.sub(r'if\(skipId !== \'filter-years-of-service\' && fYears && String\(e\.years_of_service\) !== fYears\) return false;', '', content)
    content = re.sub(r'if\(skipId !== \'filter-age\' && fAge && String\(e\.age\) !== fAge\) return false;', '', content)
    
    # Remove from clear events
    content = re.sub(r'document\.getElementById\(\'filter-retirement\'\)\.value = \'\';', '', content)
    content = re.sub(r'document\.getElementById\(\'filter-years-of-service\'\)\.value = \'\';', '', content)
    content = re.sub(r'document\.getElementById\(\'filter-age\'\)\.value = \'\';', '', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Done")
