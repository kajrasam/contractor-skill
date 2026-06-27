import re

def patch_radar_and_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Patch drawIDPRadar
    old_idp_radar = """            for (let i = 0; i < competencies.length; i++) {
                const t = targets[i] || 0;
                if (t === 0) continue; 
                cleanLabels.push(allLabels[i]);
                cleanTargets.push(t);
                actuals.push(emp.actuals[i] || 0);
            }

            if(idpRadarChartInstance) idpRadarChartInstance.destroy();
            const ctx = document.getElementById('idpRadarChart').getContext('2d');

            idpRadarChartInstance = new Chart(ctx, {
                type: 'radar',
                data: {
                    labels: cleanLabels, 
                    datasets: [
                        { label: 'Target', data: cleanTargets, borderColor: '#cbd5e1', backgroundColor: 'transparent', borderDash: [5,5], borderWidth: 2, pointRadius: 0 },
                        { label: 'Actual', data: actuals, borderColor: '#ca3656', backgroundColor: 'rgba(202, 54, 86, 0.25)', borderWidth: 2, pointBackgroundColor: '#ca3656', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#ca3656', pointRadius: 4 }
                    ]
                },"""
    new_idp_radar = """            let befores = [];
            let selfs = [];
            for (let i = 0; i < competencies.length; i++) {
                const t = targets[i] || 0;
                if (t === 0) continue; 
                cleanLabels.push(allLabels[i]);
                cleanTargets.push(t);
                actuals.push(emp.actuals[i] || 0);
                befores.push(emp.before_evals ? (emp.before_evals[i] || 0) : 0);
                selfs.push(emp.self_evals ? (emp.self_evals[i] || 0) : 0);
            }

            if(idpRadarChartInstance) idpRadarChartInstance.destroy();
            const ctx = document.getElementById('idpRadarChart').getContext('2d');
            
            const activeFilters = activeRadarFilters['idp'] || ['target', 'before', 'self', 'actual'];
            const datasets = [];

            if (activeFilters.includes('target')) {
                datasets.push({ label: 'Target', data: cleanTargets, borderColor: '#cbd5e1', backgroundColor: 'transparent', borderDash: [5,5], borderWidth: 2, pointRadius: 0 });
            }
            if (activeFilters.includes('before')) {
                datasets.push({ label: 'Before', data: befores, borderColor: '#a855f7', backgroundColor: 'transparent', borderDash: [3,3], borderWidth: 2, pointBackgroundColor: '#a855f7', pointBorderColor: '#fff', pointRadius: 3 });
            }
            if (activeFilters.includes('self')) {
                datasets.push({ label: 'Self Eva.', data: selfs, borderColor: '#f59e0b', backgroundColor: 'transparent', borderWidth: 2, pointBackgroundColor: '#f59e0b', pointBorderColor: '#fff', pointRadius: 3 });
            }
            if (activeFilters.includes('actual')) {
                datasets.push({ label: 'Actual', data: actuals, borderColor: '#ca3656', backgroundColor: 'rgba(202, 54, 86, 0.25)', borderWidth: 2, pointBackgroundColor: '#ca3656', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#ca3656', pointRadius: 4 });
            }

            idpRadarChartInstance = new Chart(ctx, {
                type: 'radar',
                data: {
                    labels: cleanLabels, 
                    datasets: datasets
                },"""
    content = content.replace(old_idp_radar, new_idp_radar)

    # 2. Patch renderIDPContent HTML
    old_idp_html = """                        <div class="absolute top-6 right-6 text-right">
                            <h4 class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">% Completed Skill Level</h4>
                            <div class="text-4xl font-black text-scg-700">${pctComplete}%</div>
                            <div class="text-xs text-slate-400 mt-1">อัปเดต: ${emp.evalDate || '-'}</div>
                        </div>
                        
                        <div class="w-full h-[400px] mt-16 lg:mt-10">"""
    
    filter_ui_idp = """
                        <div class="absolute top-6 right-6 text-right w-full sm:w-1/2 flex flex-col items-end">
                            <h4 class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">% Completed Skill Level</h4>
                            <div class="text-4xl font-black text-scg-700">${pctComplete}%</div>
                            <div class="text-xs text-slate-400 mt-1 mb-3">อัปเดต: ${emp.evalDate || '-'}</div>
                            
                            <div class="w-full max-w-xs text-left">
                                <label class="block text-[10px] font-bold text-slate-500 mb-1">แสดงข้อมูล (Filter)</label>
                                <div class="relative filter-dropdown">
                                    <div class="w-full px-3 py-1.5 border border-slate-200 rounded-lg text-xs bg-white flex justify-between items-center cursor-pointer hover:bg-slate-50 transition-colors" onclick="this.nextElementSibling.classList.toggle('hidden');">
                                        <span class="text-slate-600">แสดงทั้งหมด</span>
                                        <i class="fa-solid fa-chevron-down text-[10px] text-slate-400"></i>
                                    </div>
                                    <div class="absolute top-full left-0 right-0 mt-1 bg-white border border-slate-100 rounded-lg shadow-xl z-[60] hidden p-2">
                                        <label class="flex items-center gap-2 p-1.5 hover:bg-slate-50 rounded cursor-pointer text-xs">
                                            <input type="checkbox" checked value="target" onchange="toggleRadarFilter(this, 'idp')" class="w-3.5 h-3.5 rounded text-scg-600 border-slate-300 focus:ring-scg-500"> Target
                                        </label>
                                        <label class="flex items-center gap-2 p-1.5 hover:bg-slate-50 rounded cursor-pointer text-xs">
                                            <input type="checkbox" checked value="before" onchange="toggleRadarFilter(this, 'idp')" class="w-3.5 h-3.5 rounded text-purple-500 border-slate-300 focus:ring-purple-500"> Before
                                        </label>
                                        <label class="flex items-center gap-2 p-1.5 hover:bg-slate-50 rounded cursor-pointer text-xs">
                                            <input type="checkbox" checked value="self" onchange="toggleRadarFilter(this, 'idp')" class="w-3.5 h-3.5 rounded text-amber-500 border-slate-300 focus:ring-amber-500"> Self Eva.
                                        </label>
                                        <label class="flex items-center gap-2 p-1.5 hover:bg-slate-50 rounded cursor-pointer text-xs">
                                            <input type="checkbox" checked value="actual" onchange="toggleRadarFilter(this, 'idp')" class="w-3.5 h-3.5 rounded text-red-600 border-slate-300 focus:ring-red-600"> Actual
                                        </label>
                                    </div>
                                </div>
                            </div>
                        </div>
"""
    
    new_idp_html = filter_ui_idp + """                        <div class="w-full h-[400px] mt-24 lg:mt-32">"""
    content = content.replace(old_idp_html, new_idp_html)


    # 3. Patch drawAnalyticRadar
    old_analytic_radar = """            let groupActuals = [];

            const allLabels = getLabels();
            for (let i = 0; i < competencies.length; i++) {
                if (targets[i] > 0) {
                    let sum = 0;
                    let count = 0;
                    filteredUsers.forEach(u => {
                        sum += (u.actuals[i] || 0);
                        count++;
                    });
                    const avg = count > 0 ? (sum / count) : 0;
                    
                    groupLabels.push(allLabels[i]);
                    groupTargets.push(targets[i]);
                    groupActuals.push(avg);
                }
            }

            if(analyticRadarChartInstance) analyticRadarChartInstance.destroy();
            const ctx = document.getElementById('analyticRadarChart').getContext('2d');

            analyticRadarChartInstance = new Chart(ctx, {
                type: 'radar',
                data: {
                    labels: groupLabels,
                    datasets: [
                        { label: 'Target', data: groupTargets, borderColor: '#cbd5e1', backgroundColor: 'transparent', borderDash: [5,5], borderWidth: 2, pointRadius: 0 },
                        { label: 'Average Actual', data: groupActuals, borderColor: '#0ea5e9', backgroundColor: 'rgba(14, 165, 233, 0.25)', borderWidth: 2, pointBackgroundColor: '#0ea5e9', pointBorderColor: '#fff', pointRadius: 4 }
                    ]
                },"""
                
    new_analytic_radar = """            let groupActuals = [];
            let groupBefores = [];
            let groupSelfs = [];

            const allLabels = getLabels();
            for (let i = 0; i < competencies.length; i++) {
                if (targets[i] > 0) {
                    let sumA = 0, sumB = 0, sumS = 0, count = 0;
                    filteredUsers.forEach(u => {
                        sumA += (u.actuals[i] || 0);
                        sumB += u.before_evals ? (u.before_evals[i] || 0) : 0;
                        sumS += u.self_evals ? (u.self_evals[i] || 0) : 0;
                        count++;
                    });
                    
                    groupLabels.push(allLabels[i]);
                    groupTargets.push(targets[i]);
                    groupActuals.push(count > 0 ? (sumA / count) : 0);
                    groupBefores.push(count > 0 ? (sumB / count) : 0);
                    groupSelfs.push(count > 0 ? (sumS / count) : 0);
                }
            }

            if(analyticRadarChartInstance) analyticRadarChartInstance.destroy();
            const ctx = document.getElementById('analyticRadarChart').getContext('2d');
            
            const activeFilters = activeRadarFilters['analytic'] || ['target', 'before', 'self', 'actual'];
            const datasets = [];

            if (activeFilters.includes('target')) {
                datasets.push({ label: 'Target', data: groupTargets, borderColor: '#cbd5e1', backgroundColor: 'transparent', borderDash: [5,5], borderWidth: 2, pointRadius: 0 });
            }
            if (activeFilters.includes('before')) {
                datasets.push({ label: 'Average Before', data: groupBefores, borderColor: '#a855f7', backgroundColor: 'transparent', borderDash: [3,3], borderWidth: 2, pointBackgroundColor: '#a855f7', pointBorderColor: '#fff', pointRadius: 3 });
            }
            if (activeFilters.includes('self')) {
                datasets.push({ label: 'Average Self', data: groupSelfs, borderColor: '#f59e0b', backgroundColor: 'transparent', borderWidth: 2, pointBackgroundColor: '#f59e0b', pointBorderColor: '#fff', pointRadius: 3 });
            }
            if (activeFilters.includes('actual')) {
                datasets.push({ label: 'Average Actual', data: groupActuals, borderColor: '#0ea5e9', backgroundColor: 'rgba(14, 165, 233, 0.25)', borderWidth: 2, pointBackgroundColor: '#0ea5e9', pointBorderColor: '#fff', pointRadius: 4 });
            }

            analyticRadarChartInstance = new Chart(ctx, {
                type: 'radar',
                data: {
                    labels: groupLabels,
                    datasets: datasets
                },"""
    content = content.replace(old_analytic_radar, new_analytic_radar)

    # 4. Patch Analytic HTML
    old_analytic_html = """                        </div>
                        <div class="w-full h-[400px] mt-10">
                            <canvas id="analyticRadarChart"></canvas>"""
                            
    filter_ui_analytic = """
                            <div class="w-full max-w-xs ml-auto mt-4 mb-2 text-left">
                                <label class="block text-[10px] font-bold text-slate-500 mb-1">แสดงข้อมูล (Filter)</label>
                                <div class="relative filter-dropdown">
                                    <div class="w-full px-3 py-1.5 border border-slate-200 rounded-lg text-xs bg-white flex justify-between items-center cursor-pointer hover:bg-slate-50 transition-colors" onclick="this.nextElementSibling.classList.toggle('hidden');">
                                        <span class="text-slate-600">แสดงทั้งหมด</span>
                                        <i class="fa-solid fa-chevron-down text-[10px] text-slate-400"></i>
                                    </div>
                                    <div class="absolute top-full left-0 right-0 mt-1 bg-white border border-slate-100 rounded-lg shadow-xl z-[60] hidden p-2">
                                        <label class="flex items-center gap-2 p-1.5 hover:bg-slate-50 rounded cursor-pointer text-xs">
                                            <input type="checkbox" checked value="target" onchange="toggleRadarFilter(this, 'analytic')" class="w-3.5 h-3.5 rounded text-scg-600 border-slate-300 focus:ring-scg-500"> Target
                                        </label>
                                        <label class="flex items-center gap-2 p-1.5 hover:bg-slate-50 rounded cursor-pointer text-xs">
                                            <input type="checkbox" checked value="before" onchange="toggleRadarFilter(this, 'analytic')" class="w-3.5 h-3.5 rounded text-purple-500 border-slate-300 focus:ring-purple-500"> Average Before
                                        </label>
                                        <label class="flex items-center gap-2 p-1.5 hover:bg-slate-50 rounded cursor-pointer text-xs">
                                            <input type="checkbox" checked value="self" onchange="toggleRadarFilter(this, 'analytic')" class="w-3.5 h-3.5 rounded text-amber-500 border-slate-300 focus:ring-amber-500"> Average Self
                                        </label>
                                        <label class="flex items-center gap-2 p-1.5 hover:bg-slate-50 rounded cursor-pointer text-xs">
                                            <input type="checkbox" checked value="actual" onchange="toggleRadarFilter(this, 'analytic')" class="w-3.5 h-3.5 rounded text-sky-500 border-slate-300 focus:ring-sky-500"> Average Actual
                                        </label>
                                    </div>
                                </div>
                            </div>
"""
    new_analytic_html = """                        </div>""" + filter_ui_analytic + """
                        <div class="w-full h-[400px] mt-6">
                            <canvas id="analyticRadarChart"></canvas>"""
    content = content.replace(old_analytic_html, new_analytic_html)


    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Patched {filepath}')

patch_radar_and_html('static/index.html')
patch_radar_and_html('index_render.html')
