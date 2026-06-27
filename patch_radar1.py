import re

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add global state and functions
    js_logic = """
        // --- Radar Chart Multi-Select Filter Logic ---
        let activeRadarFilters = {
            'eval': ['target', 'self', 'before', 'actual'],
            'dashboard': ['target', 'self', 'before', 'actual'],
            'idp': ['target', 'self', 'before', 'actual'],
            'analytic': ['target', 'self', 'before', 'actual']
        };

        function toggleRadarFilterDropdown(type) {
            const dropdown = document.getElementById(`${type}-radar-filter-dropdown`);
            if (dropdown) {
                dropdown.classList.toggle('hidden');
            }
        }

        function updateRadarFilter(type) {
            const checkboxes = document.querySelectorAll(`.${type}-radar-cb`);
            let checkedVals = [];
            checkboxes.forEach(cb => {
                if (cb.checked) checkedVals.push(cb.value);
            });
            activeRadarFilters[type] = checkedVals;
            
            const textEl = document.getElementById(`${type}-radar-filter-text`);
            if (textEl) {
                if (checkedVals.length === 4) {
                    textEl.textContent = 'แสดงทั้งหมด';
                } else if (checkedVals.length === 0) {
                    textEl.textContent = 'ซ่อนทั้งหมด';
                } else {
                    const labels = {
                        'target': 'Target',
                        'self': 'Self',
                        'before': 'Before',
                        'actual': 'Actual'
                    };
                    textEl.textContent = checkedVals.map(v => labels[v]).join(', ');
                }
            }
            
            if (type === 'eval') drawEvalRadar();
            if (type === 'dashboard') setupDashboardTab();
            if (type === 'idp') drawIDPRadar();
            if (type === 'analytic') {
                if (typeof renderAnalyticTab === 'function') renderAnalyticTab();
            }
        }

        // Close dropdowns when clicking outside
        document.addEventListener('click', function(e) {
            ['eval', 'dashboard', 'idp', 'analytic'].forEach(type => {
                const dropdown = document.getElementById(`${type}-radar-filter-dropdown`);
                const container = dropdown ? dropdown.parentElement : null;
                if (container && !container.contains(e.target)) {
                    dropdown.classList.add('hidden');
                }
            });
        });
        // ---------------------------------------------
"""
    if "let activeRadarFilters =" not in html:
        html = html.replace("let currentEditIndex = -1;", js_logic + "\n        let currentEditIndex = -1;")

    # 2. Evaluation Tab Replacement
    old_eval_filter = """<select id="radar-filter" onchange="updateEvalUI()" class="w-full text-sm p-2 border border-slate-200 rounded-lg outline-none">
                                    <option value="all">แสดงทั้งหมด</option>
                                    <option value="target">Level Expect (Target) อย่างเดียว</option>
                                    <option value="self">Self Eva. อย่างเดียว</option>
                                    <option value="before">Before (ประเมินก่อน) อย่างเดียว</option>
                                    <option value="actual">Actual (ประเมินหลัง) อย่างเดียว</option>
                                </select>"""
    
    new_eval_filter = """<div class="relative w-full text-sm">
                                    <div onclick="toggleRadarFilterDropdown('eval')" class="w-full p-2 border border-slate-200 rounded-lg bg-white flex justify-between items-center cursor-pointer hover:bg-slate-50 transition-colors">
                                        <span id="eval-radar-filter-text" class="text-slate-700 truncate font-medium">แสดงทั้งหมด</span>
                                        <i class="fa-solid fa-chevron-down text-slate-400 text-xs"></i>
                                    </div>
                                    <div id="eval-radar-filter-dropdown" class="absolute z-50 w-full mt-1 bg-white border border-slate-200 rounded-lg shadow-lg hidden flex-col py-1">
                                        <label class="flex items-center gap-2 px-3 py-2 hover:bg-slate-50 cursor-pointer">
                                            <input type="checkbox" value="target" checked class="eval-radar-cb rounded border-slate-300 text-scg-600 focus:ring-scg-500" onchange="updateRadarFilter('eval')">
                                            <span class="text-slate-700">Level Expect (Target)</span>
                                        </label>
                                        <label class="flex items-center gap-2 px-3 py-2 hover:bg-slate-50 cursor-pointer">
                                            <input type="checkbox" value="self" checked class="eval-radar-cb rounded border-slate-300 text-scg-600 focus:ring-scg-500" onchange="updateRadarFilter('eval')">
                                            <span class="text-slate-700">Self Eva.</span>
                                        </label>
                                        <label class="flex items-center gap-2 px-3 py-2 hover:bg-slate-50 cursor-pointer">
                                            <input type="checkbox" value="before" checked class="eval-radar-cb rounded border-slate-300 text-scg-600 focus:ring-scg-500" onchange="updateRadarFilter('eval')">
                                            <span class="text-slate-700">Before (ประเมินก่อน)</span>
                                        </label>
                                        <label class="flex items-center gap-2 px-3 py-2 hover:bg-slate-50 cursor-pointer">
                                            <input type="checkbox" value="actual" checked class="eval-radar-cb rounded border-slate-300 text-scg-600 focus:ring-scg-500" onchange="updateRadarFilter('eval')">
                                            <span class="text-slate-700">Actual (ประเมินจริง)</span>
                                        </label>
                                    </div>
                                </div>"""
    
    html = html.replace(old_eval_filter, new_eval_filter)

    # Eval Tab Logic
    old_eval_logic = """            let activeDatasets = [];
            const rFilter = document.getElementById('radar-filter');
            const fVal = rFilter ? rFilter.value : 'all';
            
            if (fVal === 'all' || fVal === 'target') {
                activeDatasets.push({ label: 'Target', data: cleanTargets, borderColor: '#cbd5e1', backgroundColor: 'transparent', borderDash: [5, 5] });
            }
            if (fVal === 'all' || fVal === 'self') {
                activeDatasets.push({ label: 'Self Eva.', data: selfEvals, borderColor: '#fbbf24', backgroundColor: 'rgba(251, 191, 36, 0.2)' });
            }
            if (fVal === 'all' || fVal === 'before') {
                activeDatasets.push({ label: 'Before', data: beforeEvals, borderColor: '#9333ea', backgroundColor: 'transparent', borderDash: [2, 2] });
            }
            if (fVal === 'all' || fVal === 'actual') {
                activeDatasets.push({ label: 'Actual', data: actuals, borderColor: '#ca3656', backgroundColor: 'rgba(202, 54, 86, 0.2)' });
            }"""
    
    new_eval_logic = """            let activeDatasets = [];
            const filters = activeRadarFilters['eval'];
            
            if (filters.includes('target')) {
                activeDatasets.push({ label: 'Target', data: cleanTargets, borderColor: '#cbd5e1', backgroundColor: 'transparent', borderDash: [5, 5] });
            }
            if (filters.includes('self')) {
                activeDatasets.push({ label: 'Self Eva.', data: selfEvals, borderColor: '#fbbf24', backgroundColor: 'rgba(251, 191, 36, 0.2)' });
            }
            if (filters.includes('before')) {
                activeDatasets.push({ label: 'Before', data: beforeEvals, borderColor: '#9333ea', backgroundColor: 'transparent', borderDash: [2, 2] });
            }
            if (filters.includes('actual')) {
                activeDatasets.push({ label: 'Actual', data: actuals, borderColor: '#ca3656', backgroundColor: 'rgba(202, 54, 86, 0.2)' });
            }"""
    
    html = html.replace(old_eval_logic, new_eval_logic)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"{filepath} patched Eval successfully!")

patch_file('static/index.html')
patch_file('index_render.html')
