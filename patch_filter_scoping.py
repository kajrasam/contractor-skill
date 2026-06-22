import re

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add ID to Competency Group
    # Find <!-- Competency Group -->\n                        <div class="xl:w-1/4...
    html = html.replace('<!-- Competency Group -->\n                        <div class="xl:w-1/4', '<!-- Competency Group -->\n                        <div id="global-competency-container" class="xl:w-1/4')

    # 2. Update switchTab(tabId)
    switch_tab_code = """function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
            document.getElementById(`tab-${tabId}`).classList.add('active');

            const tabsWithFilters = ['training', 'evaluation', 'dashboard', 'idp', 'analytic', 'admin'];
            const globalFilters = document.getElementById('global-filters-container');
            const compContainer = document.getElementById('global-competency-container');
            if(globalFilters) {
                if (tabsWithFilters.includes(tabId)) {
                    globalFilters.classList.remove('hidden');
                } else {
                    globalFilters.classList.add('hidden');
                }
            }
            if(compContainer) {
                if (tabId === 'admin') {
                    compContainer.classList.add('hidden');
                } else {
                    compContainer.classList.remove('hidden');
                }
            }
            
            // Rebuild filters based on tab context (admin vs others)
            buildFiltersUI(tabId);
            
            document.querySelectorAll('.nav-btn').forEach(btn => {"""
            
    html = re.sub(r"function switchTab\(tabId\) \{.*?document\.querySelectorAll\('\.nav-btn'\)\.forEach\(btn => \{", switch_tab_code, html, count=1, flags=re.DOTALL)

    # 3. Update buildFiltersUI signature and logic
    build_filters_code = """function buildFiltersUI(tabId = null) {
            if (!tabId) {
                const activeTab = document.querySelector('.tab-content.active');
                tabId = activeTab ? activeTab.id.replace('tab-', '') : 'dashboard';
            }
            const jobGroupContainer = document.getElementById('job-group-filters');"""
            
    html = html.replace("function buildFiltersUI() {\n            const jobGroupContainer = document.getElementById('job-group-filters');", build_filters_code)
    
    # 4. Change employeeDataAll.forEach back to conditional
    conditional_data = """// Build Org Filters AND Position Filter with Hierarchy/Intersection
            let jobGroupsSet = new Set(), sectionsSet = new Set(), deptsSet = new Set(), sub1DivsSet = new Set(), divsSet = new Set(), sub1CompsSet = new Set(), compsSet = new Set(), posSet = new Set(), employeesSet = new Set();
            
            const dataSource = (tabId === 'admin') ? employeeDataAll : employeeData;
            
            dataSource.forEach(e => {"""
            
    html = html.replace("""// Build Org Filters AND Position Filter with Hierarchy/Intersection
            let jobGroupsSet = new Set(), sectionsSet = new Set(), deptsSet = new Set(), sub1DivsSet = new Set(), divsSet = new Set(), sub1CompsSet = new Set(), compsSet = new Set(), posSet = new Set(), employeesSet = new Set();
            
            employeeDataAll.forEach(e => {""", conditional_data)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Patched {filepath}")

patch_file('static/index.html')
patch_file('index_render.html')
