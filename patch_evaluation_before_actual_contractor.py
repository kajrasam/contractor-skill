import os

target_dir = r"d:\Work\งานใหม่\อบรม\2026\Vibe Coding Workshop\Project\contractor-skill"
files_to_patch = [
    os.path.join(target_dir, "index_render.html"), 
    os.path.join(target_dir, "static", "index.html"),
    os.path.join(target_dir, "scratch_html.html")
]

for filepath in files_to_patch:
    if not os.path.exists(filepath):
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add before_evals to dbUsers initialization
    if "before_evals: []," not in content:
        content = content.replace("actuals: [],", "actuals: [],\n                        before_evals: [],")

    # 2. Add eval-mode-toggle in the sliders container area
    if 'id="eval-mode-toggle"' not in content:
        toggle_html = """                            <div id="eval-mode-toggle" class="hidden mb-6 bg-slate-50 p-4 rounded-xl border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center gap-4 md:gap-6">
                                <span class="font-bold text-slate-800"><i class="fa-solid fa-sliders text-scg-500 mr-2"></i> เลือกโหมดการประเมิน:</span>
                                <label class="flex items-center gap-2 cursor-pointer font-bold text-purple-700">
                                    <input type="radio" name="evalModeToggle" value="before" class="w-4 h-4 accent-purple-600" onchange="toggleEvalViewMode(this.value)"> 
                                    ประเมินก่อน (Before)
                                </label>
                                <label class="flex items-center gap-2 cursor-pointer font-bold text-amber-700">
                                    <input type="radio" name="evalModeToggle" value="actual" checked class="w-4 h-4 accent-amber-600" onchange="toggleEvalViewMode(this.value)"> 
                                    ประเมินหลัง (Actual)
                                </label>
                            </div>
                            <div id="sliders-container" class="space-y-6"></div>"""
        content = content.replace('<div id="sliders-container" class="space-y-6"></div>', toggle_html)

    # 3. Add Filter Dropdown to Radar chart
    if 'id="radar-filter"' not in content:
        filter_html = """                            <div class="mb-4">
                                <label class="block text-xs font-bold text-slate-500 mb-1">แสดงข้อมูล (Filter)</label>
                                <select id="radar-filter" onchange="updateEvalUI()" class="w-full text-sm p-2 border border-slate-200 rounded-lg outline-none">
                                    <option value="all">แสดงทั้งหมด</option>
                                    <option value="target">Level Expect (Target) อย่างเดียว</option>
                                    <option value="self">Self Eva. อย่างเดียว</option>
                                    <option value="before">Before (ประเมินก่อน) อย่างเดียว</option>
                                    <option value="actual">Actual (ประเมินหลัง) อย่างเดียว</option>
                                </select>
                            </div>
                            <div class="relative h-64 w-full"><canvas id="evalRadarChart"></canvas></div>"""
        content = content.replace('<div class="relative h-64 w-full"><canvas id="evalRadarChart"></canvas></div>', filter_html)


    # 4. Modify supervisor mode block
    supervisor_old = """                    <div class="mb-4">
                        <label class="block text-sm font-bold text-amber-700 mb-2">หัวหน้าประเมินจริง (Supervisor Evaluation)</label>
                        <div class="flex items-center gap-4 mb-2">
                            <input type="range" id="eval-actual-${id}-${i}" min="1" max="5" value="${currentVal}" 
                                class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-amber-500" 
                                oninput="updateEvalSliderDisplay(${i}, this.value, 'actual')">
                            <div id="disp-actual-${i}" class="w-12 h-12 flex items-center justify-center bg-amber-500 text-white font-black text-xl rounded-xl shadow-inner shrink-0">${currentVal}</div>
                        </div>
                        <div class="bg-amber-50/30 p-3.5 rounded-xl border border-amber-100 text-sm flex items-start gap-3 mb-4">
                            <span id="badge-actual-${i}" class="font-bold text-amber-700 bg-amber-100 px-2.5 py-1 rounded-md shrink-0 border border-amber-200">Level ${currentVal}</span>
                            <span id="desc-actual-${i}" class="text-slate-600 leading-relaxed mt-0.5">${currentDesc}</span>
                        </div>
                        

                    </div>"""

    supervisor_new = """                    const beforeVal = (emp.before_evals && emp.before_evals[i]) ? emp.before_evals[i] : 1;
                    const beforeDesc = competencies[i].levels[beforeVal] || "";
                    
                    html += `
                    <div class="eval-before-block hidden mb-4">
                        <label class="block text-sm font-bold text-purple-700 mb-2">หัวหน้าประเมินก่อน (Before Evaluation)</label>
                        <div class="flex items-center gap-4 mb-2">
                            <input type="range" id="eval-before-${id}-${i}" min="1" max="5" value="${beforeVal}" 
                                class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-purple-500" 
                                oninput="updateEvalSliderDisplay(${i}, this.value, 'before')">
                            <div id="disp-before-${i}" class="w-12 h-12 flex items-center justify-center bg-purple-500 text-white font-black text-xl rounded-xl shadow-inner shrink-0">${beforeVal}</div>
                        </div>
                        <div class="bg-purple-50/30 p-3.5 rounded-xl border border-purple-100 text-sm flex items-start gap-3 mb-4">
                            <span id="badge-before-${i}" class="font-bold text-purple-700 bg-purple-100 px-2.5 py-1 rounded-md shrink-0 border border-purple-200">Level ${beforeVal}</span>
                            <span id="desc-before-${i}" class="text-slate-600 leading-relaxed mt-0.5">${beforeDesc}</span>
                        </div>
                    </div>

                    <div class="eval-actual-block mb-4">
                        <label class="block text-sm font-bold text-amber-700 mb-2">หัวหน้าประเมินจริง (Actual / Supervisor Evaluation)</label>
                        <div class="flex items-center gap-4 mb-2">
                            <input type="range" id="eval-actual-${id}-${i}" min="1" max="5" value="${currentVal}" 
                                class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-amber-500" 
                                oninput="updateEvalSliderDisplay(${i}, this.value, 'actual')">
                            <div id="disp-actual-${i}" class="w-12 h-12 flex items-center justify-center bg-amber-500 text-white font-black text-xl rounded-xl shadow-inner shrink-0">${currentVal}</div>
                        </div>
                        <div class="bg-amber-50/30 p-3.5 rounded-xl border border-amber-100 text-sm flex items-start gap-3 mb-4">
                            <span id="badge-actual-${i}" class="font-bold text-amber-700 bg-amber-100 px-2.5 py-1 rounded-md shrink-0 border border-amber-200">Level ${currentVal}</span>
                            <span id="desc-actual-${i}" class="text-slate-600 leading-relaxed mt-0.5">${currentDesc}</span>
                        </div>
                    </div>`;"""
                    
    content = content.replace(supervisor_old, supervisor_new)

    # 5. Add logic to hide/show toggle and restore mode
    toggle_logic_old = "document.getElementById('sliders-container').innerHTML = html;"
    toggle_logic_new = """document.getElementById('sliders-container').innerHTML = html;
            if (currentUser.id === id) {
                const modeToggle = document.getElementById('eval-mode-toggle');
                if (modeToggle) modeToggle.classList.add('hidden');
            } else {
                const modeToggle = document.getElementById('eval-mode-toggle');
                if (modeToggle) modeToggle.classList.remove('hidden');
                
                const modeRadio = document.querySelector('input[name="evalModeToggle"]:checked');
                if (modeRadio) toggleEvalViewMode(modeRadio.value);
            }"""
    if "toggleEvalViewMode(" not in content and toggle_logic_old in content:
        content = content.replace(toggle_logic_old, toggle_logic_new)

    # 6. Add beforeEvals array and radar chart logic
    radar_var_old = """            let actuals = [];
            let cleanLabels = [];
            let cleanTargets = [];
            let selfEvals = [];"""
    radar_var_new = """            let actuals = [];
            let cleanLabels = [];
            let cleanTargets = [];
            let selfEvals = [];
            let beforeEvals = [];"""
    if "let beforeEvals = [];" not in content:
        content = content.replace(radar_var_old, radar_var_new)

    radar_loop_old = """                const elSelf = document.getElementById(`eval-self-${id}-${i}`);
                let defaultSelf = emp.self_evals ? (emp.self_evals[i] || 0) : 0;
                selfEvals.push(elSelf ? parseInt(elSelf.value) : defaultSelf);"""
    radar_loop_new = """                const elSelf = document.getElementById(`eval-self-${id}-${i}`);
                let defaultSelf = emp.self_evals ? (emp.self_evals[i] || 0) : 0;
                selfEvals.push(elSelf ? parseInt(elSelf.value) : defaultSelf);
                
                const elBefore = document.getElementById(`eval-before-${id}-${i}`);
                let defaultBefore = emp.before_evals ? (emp.before_evals[i] || 0) : 0;
                beforeEvals.push(elBefore ? parseInt(elBefore.value) : defaultBefore);"""
    if "elBefore = document.getElementById(`eval-before" not in content:
        content = content.replace(radar_loop_old, radar_loop_new)

    radar_datasets_old = """                    datasets: [
                        { label: 'Target', data: cleanTargets, borderColor: '#cbd5e1', backgroundColor: 'transparent', borderDash: [5, 5] },
                        { label: 'Actual', data: actuals, borderColor: '#ca3656', backgroundColor: 'rgba(202, 54, 86, 0.2)' },
                        { label: 'Self Eva.', data: selfEvals, borderColor: '#fbbf24', backgroundColor: 'rgba(251, 191, 36, 0.2)' }
                    ]"""
    
    # Building datasets dynamically based on filter
    dataset_builder = """            let activeDatasets = [];
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
            }
            
            evalRadarChartInstance = new Chart(ctx, {
                type: 'radar',
                data: {
                    labels: cleanLabels,
                    datasets: activeDatasets
                },"""
                
    if "activeDatasets" not in content:
        content = content.replace(radar_datasets_old, "                    datasets: activeDatasets")
        content = content.replace("evalRadarChartInstance = new Chart(ctx, {", dataset_builder)


    # 7. updateEvalSliderDisplay patch
    slider_disp_old = """            // If the original UI is rendered (no type), idPrefix is empty.
            if (!type) {
                document.getElementById(`disp-${index}`).textContent = val;
                document.getElementById(`badge-${index}`).textContent = `Level ${val}`;
                document.getElementById(`desc-${index}`).textContent = competencies[index].levels[val];
            } else {
                document.getElementById(`disp-${idPrefix}${index}`).textContent = val;
                document.getElementById(`badge-${idPrefix}${index}`).textContent = `Level ${val}`;
                document.getElementById(`desc-${idPrefix}${index}`).textContent = competencies[index].levels[val];
            }
            drawEvalRadar();"""
    
    slider_disp_new = """            const id = document.getElementById('eval-employee-select').value;
            
            // If the original UI is rendered (no type), idPrefix is empty.
            if (!type) {
                document.getElementById(`disp-${index}`).textContent = val;
                document.getElementById(`badge-${index}`).textContent = `Level ${val}`;
                document.getElementById(`desc-${index}`).textContent = competencies[index].levels[val];
            } else {
                if(type === 'before') {
                    document.getElementById(`disp-before-${index}`).textContent = val;
                    document.getElementById(`badge-before-${index}`).textContent = `Level ${val}`;
                    document.getElementById(`desc-before-${index}`).textContent = competencies[index].levels[val];
                    if (id && dbUsers[id]) {
                        if(!dbUsers[id].before_evals) dbUsers[id].before_evals = [];
                        dbUsers[id].before_evals[index] = parseInt(val);
                    }
                } else {
                    document.getElementById(`disp-${idPrefix}${index}`).textContent = val;
                    document.getElementById(`badge-${idPrefix}${index}`).textContent = `Level ${val}`;
                    document.getElementById(`desc-${idPrefix}${index}`).textContent = competencies[index].levels[val];
                }
            }
            
            if (type === 'actual' && id && dbUsers[id]) {
                dbUsers[id].actuals[index] = parseInt(val);
            } else if (type === 'self' && id && dbUsers[id]) {
                if(!dbUsers[id].self_evals) dbUsers[id].self_evals = [];
                dbUsers[id].self_evals[index] = parseInt(val);
            }
            drawEvalRadar();"""
    if "type === 'before'" not in content:
        content = content.replace(slider_disp_old, slider_disp_new)

    # 8. saveEvaluation patch
    save_eval_old = """                // Grab actual eval if exists
                const elActual = document.getElementById(`eval-actual-${id}-${i}`);
                if (elActual) {
                    emp.actuals[i] = parseInt(elActual.value);
                }"""
    save_eval_new = """                // Grab actual eval if exists
                const elActual = document.getElementById(`eval-actual-${id}-${i}`);
                if (elActual) {
                    emp.actuals[i] = parseInt(elActual.value);
                }
                
                // Grab before eval if exists
                const elBefore = document.getElementById(`eval-before-${id}-${i}`);
                if (elBefore) {
                    if (!emp.before_evals) emp.before_evals = [];
                    emp.before_evals[i] = parseInt(elBefore.value);
                }"""
    if "const elBefore" not in content:
        content = content.replace(save_eval_old, save_eval_new)
    
    # 9. toggleEvalViewMode function
    if "function toggleEvalViewMode" not in content:
        toggle_func = """        function toggleEvalViewMode(mode) {
            const beforeBlocks = document.querySelectorAll('.eval-before-block');
            const actualBlocks = document.querySelectorAll('.eval-actual-block');
            if (mode === 'before') {
                beforeBlocks.forEach(el => el.classList.remove('hidden'));
                actualBlocks.forEach(el => el.classList.add('hidden'));
            } else {
                beforeBlocks.forEach(el => el.classList.add('hidden'));
                actualBlocks.forEach(el => el.classList.remove('hidden'));
            }
        }
        
        function applyAdminOverride"""
        content = content.replace("function applyAdminOverride", toggle_func)


    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("Patch applied to all target files in contractor-skill.")
