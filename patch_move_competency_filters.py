import re

files = [
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html',
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/index_render.html'
]

filters_html = """
                    <div class="w-full relative filter-dropdown-container">
                        <label class="block text-sm font-bold text-slate-700 mb-2"><i class="fa-solid fa-layer-group text-scg-500 mr-1"></i> กลุ่ม Competency</label>
                        <button onclick="toggleFilterMenu('comp-group-menu')" class="w-full flex items-center justify-between bg-white border border-slate-300 px-4 py-2.5 rounded-xl text-left shadow-sm hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-scg-500 transition-colors">
                            <span class="text-sm font-medium text-slate-700 truncate" id="comp-group-dropdown-text">เลือกกลุ่มทักษะทั้งหมด</span>
                            <i class="fa-solid fa-chevron-down text-slate-400 ml-2"></i>
                        </button>
                        <div id="comp-group-menu" class="filter-menu hidden absolute top-full left-0 w-full mt-2 bg-white border border-slate-200 rounded-xl shadow-xl z-30 max-h-64 overflow-y-auto">
                            <div id="comp-group-filters" class="p-2 flex flex-col gap-1">
                                <!-- Injected by JS -->
                            </div>
                        </div>
                    </div>

                    <div class="w-full relative filter-dropdown-container">
                        <label class="block text-sm font-bold text-slate-700 mb-2"><i class="fa-solid fa-filter text-scg-500 mr-1"></i> หัวข้อ Competency</label>
                        <button onclick="toggleFilterMenu('comp-dropdown-menu')" class="w-full flex items-center justify-between bg-white border border-slate-300 px-4 py-2.5 rounded-xl text-left shadow-sm hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-scg-500 transition-colors">
                            <span class="text-sm font-medium text-slate-700 truncate" id="comp-dropdown-text">เลือกทักษะทั้งหมด</span>
                            <i class="fa-solid fa-chevron-down text-slate-400 ml-2"></i>
                        </button>
                        <div id="comp-dropdown-menu" class="filter-menu hidden absolute top-full left-0 w-full mt-2 bg-white border border-slate-200 rounded-xl shadow-xl z-30 max-h-64 overflow-y-auto">
                            <div id="competency-filters" class="p-2 flex flex-col gap-1">
                                <!-- Injected by JS -->
                            </div>
                        </div>
                    </div>
"""

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Insert into Global Filters
    employee_div_end_pattern = re.compile(
        r'(<div id="employee-menu"[^>]*>\s*<div id="employee-filters"[^>]*>\s*<!-- Injected by JS -->\s*</div>\s*</div>\s*</div>)', 
        re.DOTALL
    )
    content = employee_div_end_pattern.sub(r'\1' + filters_html, content)

    # 2. Remove from Training Matrix
    training_matrix_filters_pattern = re.compile(
        r'<div class="grid grid-cols-1 md:grid-cols-2 gap-4 w-full xl:w-1/2">.*?<div id="competency-filters"[^>]*>\s*<!-- Injected by JS -->\s*</div>\s*</div>\s*</div>\s*</div>',
        re.DOTALL
    )
    content = training_matrix_filters_pattern.sub('', content)

    # 3. Update updateEvalUI()
    eval_ui_pattern = re.compile(r'for \(let i = 0; i < competencies\.length; i\+\+\) \{\s*const targetVal = targets\[i\] \|\| 0;', re.DOTALL)
    new_eval_ui = """for (let i = 0; i < competencies.length; i++) {
                if(selectedCompetencyGroupFilter.length > 0 && !selectedCompetencyGroupFilter.includes(competencies[i].group)) continue;
                if(selectedCompetenciesFilter.length > 0 && !selectedCompetenciesFilter.includes(competencies[i].name)) continue;
                
                const targetVal = targets[i] || 0;"""
    content = eval_ui_pattern.sub(new_eval_ui, content)

    # 4. Update renderEvalRadarChart()
    eval_radar_pattern = re.compile(r'for \(let i = 0; i < competencies\.length; i\+\+\) \{\s*const t = targets\[i\] \|\| 0;', re.DOTALL)
    new_eval_radar = """for (let i = 0; i < competencies.length; i++) {
                if(selectedCompetencyGroupFilter.length > 0 && !selectedCompetencyGroupFilter.includes(competencies[i].group)) continue;
                if(selectedCompetenciesFilter.length > 0 && !selectedCompetenciesFilter.includes(competencies[i].name)) continue;
                
                const t = targets[i] || 0;"""
    content = eval_radar_pattern.sub(new_eval_radar, content)

    # 5. Fix toggle functions to call renderActiveTab instead of buildTrainingMatrix
    def repl_comp_group(m):
        return m.group(0).replace('buildTrainingMatrix();', 'renderActiveTab();')
    content = re.sub(r'window\.toggleCompGroupFilter = function.*?\s*buildTrainingMatrix\(\);\s*\}', repl_comp_group, content, flags=re.DOTALL)

    def repl_comp(m):
        return m.group(0).replace('buildTrainingMatrix();', 'renderActiveTab();')
    content = re.sub(r'window\.toggleCompetencyFilter = function.*?\s*buildTrainingMatrix\(\);\s*\}', repl_comp, content, flags=re.DOTALL)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Patch applied.")
