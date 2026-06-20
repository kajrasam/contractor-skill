import re
import os

files_to_process = [
    'd:\\Work\\งานใหม่\\อบรม\\2026\\Vibe Coding Workshop\\Project\\competency-system\\static\\index.html',
    'd:\\Work\\งานใหม่\\อบรม\\2026\\Vibe Coding Workshop\\Project\\competency-system\\index_render.html'
]

js_helper = """
        function isEmployeeMatchingOrgFilters(empId) {
            let emp = dbUsers[empId];
            if(!emp) return false;
            
            if(selectedJobGroupFilter.length > 0 && (!emp.position || !selectedJobGroupFilter.includes(positionGroups[emp.position]))) return false;
            if(selectedPositionsFilter.length > 0 && (!emp.position || !selectedPositionsFilter.includes(emp.position))) return false;
            
            let eData = employeeData.find(e => e.username === empId || e.EmployeeNameEng === emp.name || e.EmployeeNameThai === emp.name);
            if(!eData) {
                if(selectedSectionFilter.length > 0 || selectedDepartmentFilter.length > 0 || selectedSub1DivisionFilter.length > 0 || selectedDivisionFilter.length > 0 || selectedSub1CompanyFilter.length > 0 || selectedCompanyFilter.length > 0) return false;
                return true;
            }
            
            if(selectedSectionFilter.length > 0 && !selectedSectionFilter.includes(eData.SectionThai)) return false;
            if(selectedDepartmentFilter.length > 0 && !selectedDepartmentFilter.includes(eData.DepartmentThai)) return false;
            if(selectedSub1DivisionFilter.length > 0 && !selectedSub1DivisionFilter.includes(eData.Sub1DivisionThai)) return false;
            if(selectedDivisionFilter.length > 0 && !selectedDivisionFilter.includes(eData.DivisionThai)) return false;
            if(selectedSub1CompanyFilter.length > 0 && !selectedSub1CompanyFilter.includes(eData.Sub1CompanyThai)) return false;
            if(selectedCompanyFilter.length > 0 && !selectedCompanyFilter.includes(eData.CompanyThai)) return false;
            
            return true;
        }

        function applyGlobalFiltersToSubIds(subIds) {
            return subIds.filter(id => isEmployeeMatchingOrgFilters(id));
        }

        function renderActiveTab() {
            if(document.getElementById('tab-training').classList.contains('active')) { buildRoleResponseSection(); buildTrainingMatrix(); }
            if(document.getElementById('tab-evaluation').classList.contains('active')) updateEvalUI();
            if(document.getElementById('tab-dashboard').classList.contains('active')) buildDashboard();
            if(document.getElementById('tab-idp').classList.contains('active')) buildIDP();
            if(document.getElementById('tab-analytic').classList.contains('active')) buildAnalytic();
        }
"""

for filepath in files_to_process:
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Move Filters Section
    # Find the block from <!-- Filters Section --> to just before <!-- Role & Response Section (Vertical Layout) -->
    filter_block_pattern = re.compile(r'(<!-- Filters Section -->.*?)(?=<!-- Role & Response Section \(Vertical Layout\) -->)', re.DOTALL)
    match = filter_block_pattern.search(content)
    if match:
        filter_html = match.group(1)
        # Remove from original location
        content = content.replace(filter_html, '')
        
        # Wrap in global container
        global_filter_html = f'''
            <!-- GLOBAL FILTERS (Shared across tabs) -->
            <div id="global-filters-container" class="hidden">
{filter_html}
            </div>
'''
        # Insert after <main ...>
        main_pattern = r'(<main[^>]*>)'
        content = re.sub(main_pattern, r'\1\n' + global_filter_html, content, count=1)
        print(f"Moved filter block in {os.path.basename(filepath)}")

    # 2. Update switchTab logic
    # Find switchTab function
    switch_tab_pattern = re.compile(r'(function switchTab\(tabId\) \{.*?document\.getElementById\(`tab-\$\{tabId\}`\)\.classList\.add\(\'active\'\);)(.*?)(        \})', re.DOTALL)
    def switch_tab_repl(m):
        prefix = m.group(1)
        suffix = m.group(3)
        new_logic = """
            const tabsWithFilters = ['training', 'evaluation', 'dashboard', 'idp', 'analytic'];
            const globalFilters = document.getElementById('global-filters-container');
            if(globalFilters) {
                if (tabsWithFilters.includes(tabId)) {
                    globalFilters.classList.remove('hidden');
                } else {
                    globalFilters.classList.add('hidden');
                }
            }

            renderActiveTab();
"""
        return prefix + "\n" + new_logic + suffix
    content = switch_tab_pattern.sub(switch_tab_repl, content)

    # 3. Inject js_helper
    # Put it before window.toggleFilterValue
    if 'function isEmployeeMatchingOrgFilters' not in content:
        content = content.replace('window.toggleFilterValue = function(type, v) {', js_helper + '\n        window.toggleFilterValue = function(type, v) {')

    # 4. Update window.toggleFilterValue and window.setAllFilter to call renderActiveTab()
    content = content.replace('buildFiltersUI(); buildRoleResponseSection(); buildTrainingMatrix();', 'buildFiltersUI(); renderActiveTab();')

    # 5. Inject filter application into updateEvalUI, buildDashboard, buildIDP, buildAnalytic
    # For updateEvalUI: let subIds = getSubordinates(currentUser.id); -> let subIds = applyGlobalFiltersToSubIds(getSubordinates(currentUser.id));
    content = content.replace('let subIds = getSubordinates(currentUser.id);', 'let subIds = applyGlobalFiltersToSubIds(getSubordinates(currentUser.id));')
    
    # For buildDashboard: let subIds = getSubordinates(currentUser.id); -> let subIds = applyGlobalFiltersToSubIds(getSubordinates(currentUser.id));
    # Wait, buildDashboard might use const subIds = ...
    content = content.replace('const subIds = getSubordinates(currentUser.id);', 'const subIds = applyGlobalFiltersToSubIds(getSubordinates(currentUser.id));')
    
    # Let's ensure we catch variations:
    content = re.sub(r'let\s+subIds\s*=\s*getSubordinates\(currentUser\.id\);', r'let subIds = applyGlobalFiltersToSubIds(getSubordinates(currentUser.id));', content)
    content = re.sub(r'const\s+subIds\s*=\s*getSubordinates\(currentUser\.id\);', r'const subIds = applyGlobalFiltersToSubIds(getSubordinates(currentUser.id));', content)

    # Note: Training matrix might also need adjustment if it uses getSubordinates? No, it uses visiblePos.
    # We should update `visiblePos` filtering too if needed?
    # In buildRoleResponseSection and buildTrainingMatrix, they iterate over `visiblePos`.
    # Wait, the global filter uses selectedSectionFilter, etc. which already works for Training Need!
    # Because Training Need logic already checks `selectedSectionFilter.length > 0` etc.
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Processed {os.path.basename(filepath)}")
