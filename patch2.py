import re

with open(r'd:\Work\งานใหม่\อบรม\2026\Vibe Coding Workshop\Project\contractor-skill\static\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

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
            
            let dataToUse = [];
            if (typeof employeeDataAll !== 'undefined' && employeeDataAll.length > 0) {
                dataToUse = employeeDataAll.filter(emp => matchesOrgFiltersData(emp));
            }
            
            if (dataToUse.length === 0) {
                container.innerHTML = '<div class="text-center py-8 text-slate-500"><i class="fa-solid fa-folder-open text-3xl mb-3 text-slate-300 block"></i>ไม่พบข้อมูลสำหรับผังองค์กร (โปรดตรวจสอบตัวกรอง)</div>';
                return;
            }

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
    content = content.replace('function renderActiveTab() {', orgchart_script + '\n        function renderActiveTab() {')
    with open(r'd:\Work\งานใหม่\อบรม\2026\Vibe Coding Workshop\Project\contractor-skill\static\index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Successfully injected renderOrgChart before renderActiveTab.')
else:
    print('renderOrgChart is already present.')
