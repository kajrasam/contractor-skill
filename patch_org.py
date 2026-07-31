import re

with open('static/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add nav button
if 'nav-orgchart' not in content:
    nav_btn = """                html += `<button onclick="switchTab('employee-data')" id="nav-employee-data" class="nav-btn w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all text-left"><i class="fa-solid fa-users w-5 text-center"></i> Employee Data</button>`;
                html += `<button onclick="switchTab('orgchart')" id="nav-orgchart" class="nav-btn w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all text-left"><i class="fa-solid fa-sitemap w-5 text-center"></i> ผังองค์กร</button>`;"""
    content = re.sub(r'html \+= `<button onclick="switchTab\(\'employee-data\'\).*?`;', nav_btn, content)

# 2. Add to tabsWithFilters
if "'orgchart'" not in content:
    content = content.replace(
        "const tabsWithFilters = ['training', 'evaluation', 'dashboard', 'idp', 'analytic', 'admin', 'tracking'];",
        "const tabsWithFilters = ['training', 'evaluation', 'dashboard', 'idp', 'analytic', 'admin', 'tracking', 'orgchart'];"
    )

# 3. Add tab-orgchart section
orgchart_section = """
            <section id="tab-orgchart" class="tab-content hidden animate-fadeIn pb-12">
                <div class="mb-6 flex justify-between items-end">
                    <div>
                        <h2 class="text-xl font-bold text-scg-900 mb-1"><i class="fa-solid fa-sitemap mr-2 text-scg-600"></i>ผังองค์กร (Organization Chart)</h2>
                        <p class="text-sm text-slate-500">แสดงโครงสร้างองค์กรตามสายบังคับบัญชา สามารถกรองข้อมูลจากแถบด้านบนได้</p>
                    </div>
                    <div>
                        <button onclick="renderOrgChart()" class="px-4 py-2 bg-slate-100 text-slate-700 rounded-lg hover:bg-slate-200 text-sm font-medium transition-colors shadow-sm">
                            <i class="fa-solid fa-rotate mr-1"></i> รีเฟรชผังองค์กร
                        </button>
                    </div>
                </div>
                
                <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6">
                    <div id="orgchart-container" class="overflow-x-auto custom-scrollbar p-2">
                        <!-- Org Chart will be rendered here -->
                    </div>
                </div>
            </section>
"""
if 'id="tab-orgchart"' not in content:
    content = content.replace('<section id="tab-admin-manual"', orgchart_section + '\n            <section id="tab-admin-manual"')

# 4. Add renderOrgChart function
orgchart_script = """
        // ==========================================
        // Organization Chart Logic
        // ==========================================
        
        function toggleOrgNode(elementId, iconId) {
            const el = document.getElementById(elementId);
            const icon = document.getElementById(iconId);
            if (el.classList.contains('hidden')) {
                el.classList.remove('hidden');
                icon.classList.remove('fa-chevron-right');
                icon.classList.add('fa-chevron-down');
            } else {
                el.classList.add('hidden');
                icon.classList.remove('fa-chevron-down');
                icon.classList.add('fa-chevron-right');
            }
        }

        function renderOrgChart() {
            const container = document.getElementById('orgchart-container');
            if (!container) return;
            
            // Filter employeeDataAll using the same global filter logic
            // The global filter uses isEmployeeMatchingOrgFilters(userId)
            let dataToUse = [];
            if (typeof employeeDataAll !== 'undefined' && employeeDataAll.length > 0) {
                // If the user has global filters, they apply to dbUsers
                // But employeeDataAll is an array of raw objects
                dataToUse = employeeDataAll.filter(emp => {
                    const userId = emp.user_id || emp.USER || emp.username;
                    if (!userId) return false;
                    return isEmployeeMatchingOrgFilters(userId);
                });
            }
            
            if (dataToUse.length === 0) {
                container.innerHTML = '<div class="text-center py-8 text-slate-500"><i class="fa-solid fa-folder-open text-3xl mb-3 text-slate-300 block"></i>ไม่พบข้อมูลสำหรับผังองค์กร (โปรดตรวจสอบตัวกรอง)</div>';
                return;
            }

            // Build Hierarchy
            // Levels:
            // 1. Sub11BusinessUnitThai
            // 2. Sub1CompanyThai
            // 3. DivisionThai
            // 4. Sub1DivisionThai
            // 5. DepartmentThai
            // 6. SectionThai
            // 7. ShiftThai
            // 8. CostCenterPayment (Leaf containing array of employees)

            const tree = {};

            dataToUse.forEach(emp => {
                const l1 = emp.Sub11BusinessUnitThai || '(ไม่ระบุ Business Unit)';
                const l2 = emp.Sub1CompanyThai || '(ไม่ระบุ Sub1-Company)';
                const l3 = emp.DivisionThai || '(ไม่ระบุ Division)';
                const l4 = emp.Sub1DivisionThai || '(ไม่ระบุ Sub1-Division)';
                const l5 = emp.DepartmentThai || '(ไม่ระบุ Department)';
                const l6 = emp.SectionThai || '(ไม่ระบุ Section)';
                const l7 = emp.ShiftThai || '(ไม่ระบุ Shift)';
                const l8 = emp.CostCenterPayment || '(ไม่ระบุ Cost Center)';
                
                if (!tree[l1]) tree[l1] = {};
                if (!tree[l1][l2]) tree[l1][l2] = {};
                if (!tree[l1][l2][l3]) tree[l1][l2][l3] = {};
                if (!tree[l1][l2][l3][l4]) tree[l1][l2][l3][l4] = {};
                if (!tree[l1][l2][l3][l4][l5]) tree[l1][l2][l3][l4][l5] = {};
                if (!tree[l1][l2][l3][l4][l5][l6]) tree[l1][l2][l3][l4][l5][l6] = {};
                if (!tree[l1][l2][l3][l4][l5][l6][l7]) tree[l1][l2][l3][l4][l5][l6][l7] = {};
                if (!tree[l1][l2][l3][l4][l5][l6][l7][l8]) tree[l1][l2][l3][l4][l5][l6][l7][l8] = [];
                
                tree[l1][l2][l3][l4][l5][l6][l7][l8].push(emp);
            });

            // Recursive HTML generator
            let idCounter = 0;
            function generateHTML(node, levelIndex) {
                const isLeafLevel = (levelIndex === 7); // Cost Center level
                let html = '<ul class="pl-6 border-l border-slate-200 ml-3 space-y-1 my-1">';
                
                const keys = Object.keys(node).sort();
                
                keys.forEach(key => {
                    idCounter++;
                    const nodeId = `org-node-${idCounter}`;
                    const iconId = `org-icon-${idCounter}`;
                    
                    if (isLeafLevel) {
                        const employees = node[key];
                        html += `
                            <li class="relative">
                                <div class="flex items-center gap-2 py-1.5 px-2 hover:bg-slate-50 rounded-lg cursor-pointer group text-sm" onclick="toggleOrgNode('${nodeId}', '${iconId}')">
                                    <i id="${iconId}" class="fa-solid fa-chevron-right text-xs text-slate-400 w-3 transition-transform group-hover:text-scg-500"></i>
                                    <i class="fa-solid fa-wallet text-amber-500"></i>
                                    <span class="font-semibold text-slate-700">Cost Center: ${key}</span>
                                    <span class="text-xs bg-slate-100 text-slate-500 px-2 py-0.5 rounded-full ml-1">${employees.length} คน</span>
                                </div>
                                <ul id="${nodeId}" class="hidden pl-8 border-l border-slate-200 ml-3 py-1 space-y-1">
                        `;
                        
                        employees.forEach(emp => {
                            const empName = emp.FullName || (emp.FirstNameThai + ' ' + emp.LastNameThai);
                            const empPos = emp.PositionNameThai || emp.PositionName || '';
                            html += `
                                <li class="flex items-center gap-2 py-1 text-sm text-slate-600 hover:text-scg-600">
                                    <i class="fa-regular fa-circle-user text-slate-400"></i>
                                    <span>${empName} ${empPos ? '<span class="text-xs text-slate-400 ml-1">(' + empPos + ')</span>' : ''}</span>
                                </li>
                            `;
                        });
                        
                        html += `</ul></li>`;
                    } else {
                        // Intermediate folder
                        html += `
                            <li class="relative">
                                <div class="flex items-center gap-2 py-1.5 px-2 hover:bg-slate-50 rounded-lg cursor-pointer group text-sm" onclick="toggleOrgNode('${nodeId}', '${iconId}')">
                                    <i id="${iconId}" class="fa-solid fa-chevron-right text-xs text-slate-400 w-3 transition-transform group-hover:text-scg-500"></i>
                                    <i class="fa-regular fa-folder text-scg-500"></i>
                                    <span class="font-medium text-slate-700">${key}</span>
                                </div>
                                <div id="${nodeId}" class="hidden">
                                    ${generateHTML(node[key], levelIndex + 1)}
                                </div>
                            </li>
                        `;
                    }
                });
                
                html += '</ul>';
                return html;
            }

            // Generate root
            let rootHtml = '<ul class="space-y-2">';
            const rootKeys = Object.keys(tree).sort();
            rootKeys.forEach(rootKey => {
                idCounter++;
                const nodeId = `org-node-${idCounter}`;
                const iconId = `org-icon-${idCounter}`;
                rootHtml += `
                    <li class="relative">
                        <div class="flex items-center gap-2 py-2 px-2 hover:bg-slate-50 rounded-lg cursor-pointer group" onclick="toggleOrgNode('${nodeId}', '${iconId}')">
                            <i id="${iconId}" class="fa-solid fa-chevron-down text-xs text-slate-400 w-3 transition-transform group-hover:text-scg-500"></i>
                            <i class="fa-solid fa-building text-scg-600"></i>
                            <span class="font-bold text-scg-900">${rootKey}</span>
                        </div>
                        <div id="${nodeId}" class="block">
                            ${generateHTML(tree[rootKey], 1)}
                        </div>
                    </li>
                `;
            });
            rootHtml += '</ul>';

            container.innerHTML = rootHtml;
        }
"""
if 'function renderOrgChart()' not in content:
    content = content.replace('function closeAdminManualModal() {', orgchart_script + '\n        function closeAdminManualModal() {')


# 5. Make sure renderOrgChart is called when we switch to the tab or filter applies
if "if (id === 'orgchart') renderOrgChart();" not in content:
    content = content.replace("if (id === 'tracking') renderTrackingTable();", "if (id === 'tracking') renderTrackingTable();\n            if (id === 'orgchart') renderOrgChart();")

# We also need to hook into switchTab
if "if (tabId === 'orgchart')" not in content:
    switch_tab_hook = """
            if (tabId === 'orgchart') {
                renderOrgChart();
            }
"""
    content = content.replace("document.getElementById(`tab-${tabId}`).classList.add('active');", "document.getElementById(`tab-${tabId}`).classList.add('active');\n" + switch_tab_hook)

with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch applied to static/index.html successfully.")
