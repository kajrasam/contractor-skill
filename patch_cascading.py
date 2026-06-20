import re
import os

files = [
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html',
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/index_render.html'
]

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Navigation Active Class Fix
    old_nav = """            const activeBtn = document.getElementById(`nav-${tabId}`);
            if(activeBtn) {
                activeBtn.classList.add('bg-scg-800', 'text-white', 'shadow-md');
                activeBtn.classList.remove('text-slate-600', 'hover:bg-scg-50', 'text-scg-700', 'bg-scg-50');
            }"""
    new_nav = """            document.querySelectorAll('.nav-btn').forEach(btn => {
                btn.classList.remove('bg-scg-800', 'text-white', 'shadow-md', 'text-scg-700', 'bg-scg-50');
                btn.classList.add('text-slate-600', 'hover:bg-scg-50');
            });
            const activeBtn = document.getElementById(`nav-${tabId}`);
            if(activeBtn) {
                activeBtn.classList.add('bg-scg-800', 'text-white', 'shadow-md');
                activeBtn.classList.remove('text-slate-600', 'hover:bg-scg-50');
            }"""
    content = content.replace(old_nav, new_nav)

    # 2. Add matchesFiltersExcept and replace the top of buildFiltersUI
    matches_filters_except = """
        function matchesFiltersExcept(e, ignoreFilter) {
            if (ignoreFilter !== 'company' && selectedCompanyFilter.length > 0 && (!e.CompanyThai || !selectedCompanyFilter.includes(e.CompanyThai))) return false;
            if (ignoreFilter !== 'sub1company' && selectedSub1CompanyFilter.length > 0 && (!e.Sub1CompanyThai || !selectedSub1CompanyFilter.includes(e.Sub1CompanyThai))) return false;
            if (ignoreFilter !== 'division' && selectedDivisionFilter.length > 0 && (!e.DivisionThai || !selectedDivisionFilter.includes(e.DivisionThai))) return false;
            if (ignoreFilter !== 'sub1division' && selectedSub1DivisionFilter.length > 0 && (!e.Sub1DivisionThai || !selectedSub1DivisionFilter.includes(e.Sub1DivisionThai))) return false;
            if (ignoreFilter !== 'department' && selectedDepartmentFilter.length > 0 && (!e.DepartmentThai || !selectedDepartmentFilter.includes(e.DepartmentThai))) return false;
            if (ignoreFilter !== 'section' && selectedSectionFilter.length > 0 && (!e.SectionThai || !selectedSectionFilter.includes(e.SectionThai))) return false;
            
            let posName = e.PositionNameThai || e.position_name;
            if (ignoreFilter !== 'position' && selectedPositionsFilter.length > 0 && (!posName || !selectedPositionsFilter.includes(posName))) return false;
            
            if (ignoreFilter !== 'jobGroup' && selectedJobGroupFilter.length > 0) {
                let jg = posName ? positionGroups[posName] : null;
                if (!jg || !selectedJobGroupFilter.includes(jg)) return false;
            }
            return true;
        }

        function buildFiltersUI() {"""
        
    content = content.replace("        function buildFiltersUI() {", matches_filters_except)

    # Now replace the Sets building logic
    old_sets = """            // Build Job Groups
            let jobGroupsSet = new Set();
            visiblePos.forEach(p => {
                if(positionGroups[p]) jobGroupsSet.add(positionGroups[p]);
            });

            // Build Org Filters AND Position Filter
            let sectionsSet = new Set(), deptsSet = new Set(), sub1DivsSet = new Set(), divsSet = new Set(), sub1CompsSet = new Set(), compsSet = new Set(), posSet = new Set();
            employeeData.forEach(e => {
                if(e.SectionThai) sectionsSet.add(e.SectionThai);
                if(e.DepartmentThai) deptsSet.add(e.DepartmentThai);
                if(e.Sub1DivisionThai) sub1DivsSet.add(e.Sub1DivisionThai);
                if(e.DivisionThai) divsSet.add(e.DivisionThai);
                if(e.Sub1CompanyThai) sub1CompsSet.add(e.Sub1CompanyThai);
                if(e.CompanyThai) compsSet.add(e.CompanyThai);
                if(e.PositionNameThai) posSet.add(e.PositionNameThai);
            });"""
            
    new_sets = """            let sectionsSet = new Set(), deptsSet = new Set(), sub1DivsSet = new Set(), divsSet = new Set(), sub1CompsSet = new Set(), compsSet = new Set(), posSet = new Set(), jobGroupsSet = new Set();
            
            employeeData.forEach(e => {
                let posName = e.PositionNameThai || e.position_name;
                
                // Add org sets based on matchesFiltersExcept
                if (matchesFiltersExcept(e, 'section')) if(e.SectionThai) sectionsSet.add(e.SectionThai);
                if (matchesFiltersExcept(e, 'department')) if(e.DepartmentThai) deptsSet.add(e.DepartmentThai);
                if (matchesFiltersExcept(e, 'sub1division')) if(e.Sub1DivisionThai) sub1DivsSet.add(e.Sub1DivisionThai);
                if (matchesFiltersExcept(e, 'division')) if(e.DivisionThai) divsSet.add(e.DivisionThai);
                if (matchesFiltersExcept(e, 'sub1company')) if(e.Sub1CompanyThai) sub1CompsSet.add(e.Sub1CompanyThai);
                if (matchesFiltersExcept(e, 'company')) if(e.CompanyThai) compsSet.add(e.CompanyThai);
                
                if (posName && visiblePos.includes(posName)) {
                    if (matchesFiltersExcept(e, 'position')) posSet.add(posName);
                    if (matchesFiltersExcept(e, 'jobGroup')) {
                        let jg = positionGroups[posName];
                        if (jg) jobGroupsSet.add(jg);
                    }
                }
            });"""
            
    content = content.replace(old_sets, new_sets)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
print("Done!")
