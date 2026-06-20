import re

files = [
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html',
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/index_render.html'
]

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove variables
    content = re.sub(r'\s*let analyticJobGroupFilter = \[\];.*?\n\s*let analyticSkillFilter = \[\];\n', '\n', content, flags=re.DOTALL)

    # 2. Remove HTML Filters block
    html_pattern = re.compile(
        r'<!-- Filters -->\s*<div class="bg-white p-6 md:p-8 rounded-3xl shadow-sm border border-slate-100 relative z-20">\s*<h3 class="font-bold text-lg text-slate-800 mb-4 border-b pb-2"><i class="fa-solid fa-filter text-scg-600 mr-2"></i>.*?<div class="grid grid-cols-1 md:grid-cols-5 gap-4" id="analytic-filters">\s*<!-- Injected by JS -->\s*</div>\s*</div>',
        re.DOTALL
    )
    content = html_pattern.sub('', content)

    # 3. Remove setupAnalyticTab filter call
    content = content.replace('            buildAnalyticFiltersUI();\n', '')

    # 4. Remove toggle functions and buildAnalyticFiltersUI
    func_pattern = re.compile(r'window\.toggleAnalyticJobGroupFilter = function.*?function renderAnalyticTab\(\) \{', re.DOTALL)
    content = func_pattern.sub('function renderAnalyticTab() {', content)

    # 5. Replace renderAnalyticTab
    render_start_pattern = re.compile(r'function renderAnalyticTab\(\) \{.*?let validUserIds = Object\.keys\(dbUsers\)\.filter\(id => dbUsers\[id\]\.role !== \'Admin\'\);.*?if\s*\(analyticEmpFilter\.length > 0\)\s*\{\s*validUserIds = validUserIds\.filter\(id => analyticEmpFilter\.includes\(id\)\);\s*\}', re.DOTALL)
    
    new_render_start = """function renderAnalyticTab() {
            let filteredComps = competencies;
            if(selectedCompetencyGroupFilter.length > 0) {
                filteredComps = filteredComps.filter(c => selectedCompetencyGroupFilter.includes(c.group));
            }
            if(selectedCompetenciesFilter.length > 0) {
                filteredComps = filteredComps.filter(c => selectedCompetenciesFilter.includes(c.name));
            }
            
            // Map Comp index
            const compIndices = filteredComps.map(c => competencies.findIndex(x => x.id === c.id));

            // Determine valid users
            let validUserIds = [];
            if (currentUser.id === 'Admin') {
                validUserIds = applyGlobalFiltersToSubIds(Object.keys(dbUsers).filter(uid => uid !== 'Admin'));
            } else {
                validUserIds = applyGlobalFiltersToSubIds([currentUser.id, ...getSubordinates(currentUser.id)]);
            }"""
    
    content = render_start_pattern.sub(new_render_start, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Patch applied for Analytic Tab.")
