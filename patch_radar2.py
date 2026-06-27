import re

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Dashboard Tab Filter
    dash_filter_html = """
                    <div class="mb-4 w-full md:w-64 ml-auto">
                        <label class="block text-xs font-bold text-slate-500 mb-1">แสดงข้อมูล (Filter)</label>
                        <div class="relative w-full text-sm">
                            <div onclick="toggleRadarFilterDropdown('dashboard')" class="w-full p-2 border border-slate-200 rounded-lg bg-white flex justify-between items-center cursor-pointer hover:bg-slate-50 transition-colors">
                                <span id="dashboard-radar-filter-text" class="text-slate-700 truncate font-medium">แสดงทั้งหมด</span>
                                <i class="fa-solid fa-chevron-down text-slate-400 text-xs"></i>
                            </div>
                            <div id="dashboard-radar-filter-dropdown" class="absolute z-50 w-full mt-1 bg-white border border-slate-200 rounded-lg shadow-lg hidden flex-col py-1">
                                <label class="flex items-center gap-2 px-3 py-2 hover:bg-slate-50 cursor-pointer">
                                    <input type="checkbox" value="target" checked class="dashboard-radar-cb rounded border-slate-300 text-scg-600 focus:ring-scg-500" onchange="updateRadarFilter('dashboard')">
                                    <span class="text-slate-700">Level Expect (Target)</span>
                                </label>
                                <label class="flex items-center gap-2 px-3 py-2 hover:bg-slate-50 cursor-pointer">
                                    <input type="checkbox" value="self" checked class="dashboard-radar-cb rounded border-slate-300 text-scg-600 focus:ring-scg-500" onchange="updateRadarFilter('dashboard')">
                                    <span class="text-slate-700">Self Eva.</span>
                                </label>
                                <label class="flex items-center gap-2 px-3 py-2 hover:bg-slate-50 cursor-pointer">
                                    <input type="checkbox" value="before" checked class="dashboard-radar-cb rounded border-slate-300 text-scg-600 focus:ring-scg-500" onchange="updateRadarFilter('dashboard')">
                                    <span class="text-slate-700">Before (ประเมินก่อน)</span>
                                </label>
                                <label class="flex items-center gap-2 px-3 py-2 hover:bg-slate-50 cursor-pointer">
                                    <input type="checkbox" value="actual" checked class="dashboard-radar-cb rounded border-slate-300 text-scg-600 focus:ring-scg-500" onchange="updateRadarFilter('dashboard')">
                                    <span class="text-slate-700">Actual (ประเมินจริง)</span>
                                </label>
                            </div>
                        </div>
                    </div>
"""
    if "dashboard-radar-filter-dropdown" not in html:
        target_dash = '</div>\n\n                    <!-- Manager Chart: Average Clustered Column -->'
        html = html.replace(target_dash, dash_filter_html + target_dash)

    # 2. Update Dashboard logic
    old_dash_logic = """                    const chart = new Chart(ctx, {
                        type: 'radar',
                        data: {
                            labels: cleanLabels,
                            datasets: [
                                { label: 'Target', data: cleanTargets, borderColor: '#94a3b8', backgroundColor: 'rgba(148, 163, 184, 0.2)' },
                                { label: 'Actual', data: cleanActuals, borderColor: '#882239', backgroundColor: 'rgba(136, 34, 57, 0.3)' },
                                { label: 'Self Eva.', data: cleanSelfs, borderColor: '#fbbf24', backgroundColor: 'rgba(251, 191, 36, 0.2)' },
                                { label: 'Before', data: cleanBefores, borderColor: '#9333ea', backgroundColor: 'transparent', borderDash: [2, 2] }
                            ]
                        }"""
    
    new_dash_logic = """                    const activeFilters = activeRadarFilters['dashboard'] || ['target', 'self', 'before', 'actual'];
                    let activeDatasets = [];
                    if (activeFilters.includes('target')) activeDatasets.push({ label: 'Target', data: cleanTargets, borderColor: '#94a3b8', backgroundColor: 'rgba(148, 163, 184, 0.2)' });
                    if (activeFilters.includes('actual')) activeDatasets.push({ label: 'Actual', data: cleanActuals, borderColor: '#882239', backgroundColor: 'rgba(136, 34, 57, 0.3)' });
                    if (activeFilters.includes('self')) activeDatasets.push({ label: 'Self Eva.', data: cleanSelfs, borderColor: '#fbbf24', backgroundColor: 'rgba(251, 191, 36, 0.2)' });
                    if (activeFilters.includes('before')) activeDatasets.push({ label: 'Before', data: cleanBefores, borderColor: '#9333ea', backgroundColor: 'transparent', borderDash: [2, 2] });

                    const chart = new Chart(ctx, {
                        type: 'radar',
                        data: {
                            labels: cleanLabels,
                            datasets: activeDatasets
                        }"""
    html = html.replace(old_dash_logic, new_dash_logic)

    # 3. IDP Tab Filter
    idp_filter_html = """
                                <div class="mb-4">
                                    <label class="block text-xs font-bold text-slate-500 mb-1">แสดงข้อมูล (Filter)</label>
                                    <div class="relative w-full text-sm">
                                        <div onclick="toggleRadarFilterDropdown('idp')" class="w-full p-2 border border-slate-200 rounded-lg bg-white flex justify-between items-center cursor-pointer hover:bg-slate-50 transition-colors">
                                            <span id="idp-radar-filter-text" class="text-slate-700 truncate font-medium">แสดงทั้งหมด</span>
                                            <i class="fa-solid fa-chevron-down text-slate-400 text-xs"></i>
                                        </div>
                                        <div id="idp-radar-filter-dropdown" class="absolute z-50 w-full mt-1 bg-white border border-slate-200 rounded-lg shadow-lg hidden flex-col py-1">
                                            <label class="flex items-center gap-2 px-3 py-2 hover:bg-slate-50 cursor-pointer">
                                                <input type="checkbox" value="target" checked class="idp-radar-cb rounded border-slate-300 text-scg-600 focus:ring-scg-500" onchange="updateRadarFilter('idp')">
                                                <span class="text-slate-700">Level Expect (Target)</span>
                                            </label>
                                            <label class="flex items-center gap-2 px-3 py-2 hover:bg-slate-50 cursor-pointer">
                                                <input type="checkbox" value="self" checked class="idp-radar-cb rounded border-slate-300 text-scg-600 focus:ring-scg-500" onchange="updateRadarFilter('idp')">
                                                <span class="text-slate-700">Self Eva.</span>
                                            </label>
                                            <label class="flex items-center gap-2 px-3 py-2 hover:bg-slate-50 cursor-pointer">
                                                <input type="checkbox" value="before" checked class="idp-radar-cb rounded border-slate-300 text-scg-600 focus:ring-scg-500" onchange="updateRadarFilter('idp')">
                                                <span class="text-slate-700">Before (ประเมินก่อน)</span>
                                            </label>
                                            <label class="flex items-center gap-2 px-3 py-2 hover:bg-slate-50 cursor-pointer">
                                                <input type="checkbox" value="actual" checked class="idp-radar-cb rounded border-slate-300 text-scg-600 focus:ring-scg-500" onchange="updateRadarFilter('idp')">
                                                <span class="text-slate-700">Actual (ประเมินจริง)</span>
                                            </label>
                                        </div>
                                    </div>
                                </div>
"""
    if "idp-radar-filter-dropdown" not in html:
        target_idp = '<h3 class="text-center font-bold text-scg-900 mb-4">Competency Radar</h3>'
        html = html.replace(target_idp, target_idp + idp_filter_html)

    # 4. Update IDP logic
    old_idp_logic = """            idpRadarChartInstance = new Chart(ctx, {
                type: 'radar',
                data: {
                    labels: cleanLabels,
                    datasets: [
                        { label: 'Target', data: cleanTargets, borderColor: '#cbd5e1', backgroundColor: 'transparent', borderDash: [5, 5], borderWidth: 2, pointRadius: 0 },
                        { label: 'Actual', data: actuals, borderColor: '#ca3656', backgroundColor: 'rgba(202, 54, 86, 0.25)', borderWidth: 2, pointBackgroundColor: '#ca3656', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#ca3656', pointRadius: 4 },
                        { label: 'Self Eva.', data: selfEvals, borderColor: '#fbbf24', backgroundColor: 'rgba(251, 191, 36, 0.2)', borderWidth: 2, pointBackgroundColor: '#fbbf24', pointBorderColor: '#fff', pointRadius: 3 }
                    ]
                }"""
    
    new_idp_logic = """            const activeFilters = activeRadarFilters['idp'] || ['target', 'self', 'before', 'actual'];
            let activeDatasets = [];
            if (activeFilters.includes('target')) activeDatasets.push({ label: 'Target', data: cleanTargets, borderColor: '#cbd5e1', backgroundColor: 'transparent', borderDash: [5, 5], borderWidth: 2, pointRadius: 0 });
            if (activeFilters.includes('actual')) activeDatasets.push({ label: 'Actual', data: actuals, borderColor: '#ca3656', backgroundColor: 'rgba(202, 54, 86, 0.25)', borderWidth: 2, pointBackgroundColor: '#ca3656', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#ca3656', pointRadius: 4 });
            if (activeFilters.includes('self')) activeDatasets.push({ label: 'Self Eva.', data: selfEvals, borderColor: '#fbbf24', backgroundColor: 'rgba(251, 191, 36, 0.2)', borderWidth: 2, pointBackgroundColor: '#fbbf24', pointBorderColor: '#fff', pointRadius: 3 });
            // Add 'before' if needed in IDP, assuming it doesn't exist for now or we leave it empty if not in cleanBefores
            // If before is added later, it will be injected here.

            idpRadarChartInstance = new Chart(ctx, {
                type: 'radar',
                data: {
                    labels: cleanLabels,
                    datasets: activeDatasets
                }"""
    html = html.replace(old_idp_logic, new_idp_logic)

    # 5. Analytic Tab Filter
    analytic_filter_html = """
                                <div class="mb-4">
                                    <label class="block text-xs font-bold text-slate-500 mb-1">แสดงข้อมูล (Filter)</label>
                                    <div class="relative w-full text-sm">
                                        <div onclick="toggleRadarFilterDropdown('analytic')" class="w-full p-2 border border-slate-200 rounded-lg bg-white flex justify-between items-center cursor-pointer hover:bg-slate-50 transition-colors">
                                            <span id="analytic-radar-filter-text" class="text-slate-700 truncate font-medium">แสดงทั้งหมด</span>
                                            <i class="fa-solid fa-chevron-down text-slate-400 text-xs"></i>
                                        </div>
                                        <div id="analytic-radar-filter-dropdown" class="absolute z-50 w-full mt-1 bg-white border border-slate-200 rounded-lg shadow-lg hidden flex-col py-1">
                                            <label class="flex items-center gap-2 px-3 py-2 hover:bg-slate-50 cursor-pointer">
                                                <input type="checkbox" value="target" checked class="analytic-radar-cb rounded border-slate-300 text-scg-600 focus:ring-scg-500" onchange="updateRadarFilter('analytic')">
                                                <span class="text-slate-700">Level Expect (Target)</span>
                                            </label>
                                            <label class="flex items-center gap-2 px-3 py-2 hover:bg-slate-50 cursor-pointer">
                                                <input type="checkbox" value="self" checked class="analytic-radar-cb rounded border-slate-300 text-scg-600 focus:ring-scg-500" onchange="updateRadarFilter('analytic')">
                                                <span class="text-slate-700">Self Eva.</span>
                                            </label>
                                            <label class="flex items-center gap-2 px-3 py-2 hover:bg-slate-50 cursor-pointer">
                                                <input type="checkbox" value="actual" checked class="analytic-radar-cb rounded border-slate-300 text-scg-600 focus:ring-scg-500" onchange="updateRadarFilter('analytic')">
                                                <span class="text-slate-700">Actual (ประเมินจริง)</span>
                                            </label>
                                        </div>
                                    </div>
                                </div>
"""
    if "analytic-radar-filter-dropdown" not in html:
        target_analytic = '<h3 class="font-bold text-slate-800 mb-4 flex items-center gap-2"><i class="fa-solid fa-star text-amber-400"></i> Top Performer Analysis</h3>'
        html = html.replace(target_analytic, target_analytic + analytic_filter_html)

    # 6. Update Analytic logic
    old_analytic_logic = """                    const chart = new Chart(ctx, {
                        type: 'radar',
                        data: {
                            labels: labels,
                            datasets: [
                                { label: 'Target', data: targetData, borderColor: '#cbd5e1', backgroundColor: 'transparent', borderDash: [5, 5], borderWidth: 2, pointRadius: 0 },
                                { label: 'Actual', data: actualsData, borderColor: '#ca3656', backgroundColor: 'rgba(202, 54, 86, 0.25)', borderWidth: 2, pointBackgroundColor: '#ca3656', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#ca3656', pointRadius: 3 },
                                { label: 'Self Eva.', data: selfData, borderColor: '#fbbf24', backgroundColor: 'rgba(251, 191, 36, 0.2)', borderWidth: 2, pointBackgroundColor: '#fbbf24', pointBorderColor: '#fff', pointRadius: 3 }
                            ]
                        }"""
    
    new_analytic_logic = """                    const activeFilters = activeRadarFilters['analytic'] || ['target', 'self', 'before', 'actual'];
                    let activeDatasets = [];
                    if (activeFilters.includes('target')) activeDatasets.push({ label: 'Target', data: targetData, borderColor: '#cbd5e1', backgroundColor: 'transparent', borderDash: [5, 5], borderWidth: 2, pointRadius: 0 });
                    if (activeFilters.includes('actual')) activeDatasets.push({ label: 'Actual', data: actualsData, borderColor: '#ca3656', backgroundColor: 'rgba(202, 54, 86, 0.25)', borderWidth: 2, pointBackgroundColor: '#ca3656', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#ca3656', pointRadius: 3 });
                    if (activeFilters.includes('self')) activeDatasets.push({ label: 'Self Eva.', data: selfData, borderColor: '#fbbf24', backgroundColor: 'rgba(251, 191, 36, 0.2)', borderWidth: 2, pointBackgroundColor: '#fbbf24', pointBorderColor: '#fff', pointRadius: 3 });

                    const chart = new Chart(ctx, {
                        type: 'radar',
                        data: {
                            labels: labels,
                            datasets: activeDatasets
                        }"""
    html = html.replace(old_analytic_logic, new_analytic_logic)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"{filepath} patched everything successfully!")

patch_file('static/index.html')
patch_file('index_render.html')
