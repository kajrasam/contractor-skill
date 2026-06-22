import re

with open('d:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

target = """            // Build Job Groups
            let jobGroupsSet = new Set();
            visiblePos.forEach(p => {
                if(positionGroups[p]) jobGroupsSet.add(positionGroups[p]);
            });

            // Build Org Filters AND Position Filter
            let sectionsSet = new Set(), deptsSet = new Set(), sub1DivsSet = new Set(), divsSet = new Set(), sub1CompsSet = new Set(), compsSet = new Set(), posSet = new Set(), employeesSet = new Set();
            visiblePos.forEach(p => {
                const emps = employeeData.filter(e => p.includes(e.position_name || e.PositionNameThai) || ((e.position_name || e.PositionNameThai) && (e.position_name || e.PositionNameThai).includes(p)));
                emps.forEach(e => {
                    if(e.section || e.SectionThai) sectionsSet.add(e.section || e.SectionThai);
                    if(e.department || e.DepartmentThai) deptsSet.add(e.department || e.DepartmentThai);
                    if(e.sub1_division || e.Sub1DivisionThai) sub1DivsSet.add(e.sub1_division || e.Sub1DivisionThai);
                    if(e.division || e.DivisionThai) divsSet.add(e.division || e.DivisionThai);
                    if(e.sub1_company || e.Sub1CompanyThai) sub1CompsSet.add(e.sub1_company || e.Sub1CompanyThai);
                    if(e.company || e.CompanyThai) compsSet.add(e.company || e.CompanyThai);
                    if(e.position_name || e.PositionNameThai) posSet.add(e.position_name || e.PositionNameThai);
                    let empName = e.FullNameTH || e.FullName || e.EmployeeNameThai || e.EmployeeNameEng;
                    if(empName) employeesSet.add(empName);
                });
            });"""

replacement = """            // Build Org Filters AND Position Filter with Hierarchy/Intersection
            let jobGroupsSet = new Set(), sectionsSet = new Set(), deptsSet = new Set(), sub1DivsSet = new Set(), divsSet = new Set(), sub1CompsSet = new Set(), compsSet = new Set(), posSet = new Set(), employeesSet = new Set();
            
            employeeData.forEach(e => {
                let posName = e.position_name || e.PositionNameThai;
                if (!posName) return;
                
                const isVisible = visiblePos.some(p => p.includes(posName) || posName.includes(p));
                if (!isVisible) return;
                
                if ((e.section || e.SectionThai) && matchesFiltersExcept(e, 'section')) sectionsSet.add(e.section || e.SectionThai);
                if ((e.department || e.DepartmentThai) && matchesFiltersExcept(e, 'department')) deptsSet.add(e.department || e.DepartmentThai);
                if ((e.sub1_division || e.Sub1DivisionThai) && matchesFiltersExcept(e, 'sub1division')) sub1DivsSet.add(e.sub1_division || e.Sub1DivisionThai);
                if ((e.division || e.DivisionThai) && matchesFiltersExcept(e, 'division')) divsSet.add(e.division || e.DivisionThai);
                if ((e.sub1_company || e.Sub1CompanyThai) && matchesFiltersExcept(e, 'sub1company')) sub1CompsSet.add(e.sub1_company || e.Sub1CompanyThai);
                if ((e.company || e.CompanyThai) && matchesFiltersExcept(e, 'company')) compsSet.add(e.company || e.CompanyThai);
                if (posName && matchesFiltersExcept(e, 'position')) posSet.add(posName);
                
                let empName = e.FullNameTH || e.FullName || e.EmployeeNameThai || e.EmployeeNameEng;
                if (empName && matchesFiltersExcept(e, 'employee')) employeesSet.add(empName);
                
                let jg = positionGroups[posName];
                if (jg && matchesFiltersExcept(e, 'jobGroup')) jobGroupsSet.add(jg);
            });"""

if target in content:
    content = content.replace(target, replacement)
    with open('d:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched buildFiltersUI successfully")
else:
    print("Could not find target block!")
