import os
import re

orig_file = r"d:\Work\งานใหม่\อบรม\2026\Vibe Coding Workshop\Project\competency_system_dynamic_rbac_hierarchy.html"
dest_file = r"d:\Work\งานใหม่\อบรม\2026\Vibe Coding Workshop\Project\competency-system\static\index.html"

with open(orig_file, 'r', encoding='utf-8') as f:
    content = f.read()

# We want to replace the hardcoded DB definitions and update the functions.
# The hardcoded data block starts from `let competencies = [` and ends at `let dbUsers = { ... };`
# We'll just replace the whole `<script>` block with a new one.

script_start = content.find('<script>\n        // --- System Functions ---')
if script_start == -1:
    script_start = content.find('<script>') # Find the last one
    
# Actually, there are multiple <script> tags. The one we want is the last one.
parts = content.split('<!-- ========================================== -->\n    <!-- JAVASCRIPT LOGIC -->\n    <!-- ========================================== -->')

html_part = parts[0] + '<!-- ========================================== -->\n    <!-- JAVASCRIPT LOGIC -->\n    <!-- ========================================== -->\n    <script>\n'

new_js = """
        const API_BASE = '/api';

        // --- System Functions ---
        function showToast(message) {
            const container = document.getElementById('toast-container');
            const toast = document.createElement('div');
            toast.className = 'toast';
            toast.innerHTML = `<i class="fa-solid fa-circle-check"></i> <span>${message}</span>`;
            container.appendChild(toast);
            
            setTimeout(() => toast.classList.add('show'), 10);
            setTimeout(() => {
                toast.classList.remove('show');
                setTimeout(() => toast.remove(), 300);
            }, 3000);
        }

        // Global State
        let competencies = [];
        let positions = [];
        let positionTargets = {};
        let roleResponses = {};
        let positionGroups = {};
        let dbUsers = {};
        let currentUser = null; 
        let actingAsRole = null; 
        let evalRadarChartInstance = null;
        let averageBarChartInstance = null;
        let individualCharts = [];
        let isEditMode = false;
        let selectedPositionsFilter = [];
        let selectedCompetenciesFilter = [];
        let selectedJobGroupFilter = [];
        let selectedCompetencyGroupFilter = [];

        async function fetchInitialData(silent = false) {
            try {
                const res = await fetch(`${API_BASE}/data`);
                const data = await res.json();
                competencies = data.competencies;
                positions = data.positions;
                positionTargets = data.positionTargets || {};
                roleResponses = data.roleResponses || {};
                positionGroups = data.positionGroups || {};
                dbUsers = data.dbUsers || {};
                if (!silent) {
                    checkLoginState();
                }
            } catch (err) {
                console.error("Error fetching data", err);
                showToast("Failed to load database");
            }
        }

        function getLabels() {
            return competencies.map(c => c.name);
        }

        // --- Recursive Hierarchy Logic ---
        function getSubordinates(managerId) {
            let subs = new Set();
            
            function findSubs(mgrId) {
                for (let id in dbUsers) {
                    if (dbUsers[id].managerIds && dbUsers[id].managerIds.includes(mgrId)) {
                        if (!subs.has(id)) {
                            subs.add(id);
                            findSubs(id);
                        }
                    }
                }
            }
            
            findSubs(managerId);
            return Array.from(subs);
        }

        // --- 2. Authentication & Navigation ---
        window.onload = fetchInitialData;

        function handleLogin() {
            const user = document.getElementById('login-username').value;
            const pass = document.getElementById('login-password').value;
            if (dbUsers[user] && dbUsers[user].pass === pass) {
                localStorage.setItem('comp_sys_user', user);
                checkLoginState();
            } else {
                document.getElementById('login-error').classList.remove('hidden');
            }
        }

        function handleLogout() {
            localStorage.removeItem('comp_sys_user');
            currentUser = null;
            actingAsRole = null;
            isEditMode = false;
            checkLoginState();
        }

        function checkLoginState() {
            const loggedInUserId = localStorage.getItem('comp_sys_user');
            const loginContainer = document.getElementById('login-container');
            const appContainer = document.getElementById('app-container');

            if (loggedInUserId && dbUsers[loggedInUserId]) {
                currentUser = dbUsers[loggedInUserId];
                currentUser.id = loggedInUserId;
                actingAsRole = currentUser.id; 
                
                loginContainer.classList.add('hidden');
                appContainer.classList.remove('hidden');
                appContainer.classList.add('flex');
                
                document.getElementById('nav-user-name').textContent = currentUser.name;
                document.getElementById('nav-user-role').textContent = currentUser.id;

                buildNavigationByRole();
                switchTab('home');
            } else {
                loginContainer.classList.remove('hidden');
                appContainer.classList.add('hidden');
                appContainer.classList.remove('flex');
            }
        }

        function buildNavigationByRole() {
            const navContainer = document.getElementById('nav-tabs-container');
            let html = `<button onclick="switchTab('home')" id="nav-home" class="nav-btn px-3 py-2 rounded-lg text-sm font-medium"><i class="fa-solid fa-house mr-1"></i> หน้าแรก</button>`;
            html += `<button onclick="switchTab('training')" id="nav-training" class="nav-btn px-3 py-2 rounded-lg text-sm font-medium"><i class="fa-solid fa-book mr-1"></i> Training Need</button>`;
            
            const hasSubs = getSubordinates(currentUser.id).length > 0;
            if (currentUser.id === 'Admin' || hasSubs) {
                html += `<button onclick="switchTab('evaluation')" id="nav-evaluation" class="nav-btn px-3 py-2 rounded-lg text-sm font-medium"><i class="fa-solid fa-clipboard-check mr-1"></i> การประเมิน</button>`;
            }
            
            html += `<button onclick="switchTab('dashboard')" id="nav-dashboard" class="nav-btn px-3 py-2 rounded-lg text-sm font-medium"><i class="fa-solid fa-chart-pie mr-1"></i> Dashboard</button>`;
            if (currentUser.id === 'Admin') {
                html += `<button onclick="switchTab('admin')" id="nav-admin" class="nav-btn px-3 py-2 rounded-lg text-sm font-bold border border-scg-200 shadow-sm ml-2"><i class="fa-solid fa-gear mr-1"></i> Admin</button>`;
            }
            navContainer.innerHTML = html;
        }

        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
            document.getElementById(`tab-${tabId}`).classList.add('active');

            document.querySelectorAll('.nav-btn').forEach(btn => {
                btn.className = btn.id === 'nav-admin' 
                    ? 'nav-btn px-3 py-2 rounded-lg text-sm font-bold text-scg-700 bg-scg-50 border border-scg-200 shadow-sm hover:bg-scg-100 ml-2' 
                    : 'nav-btn px-3 py-2 rounded-lg text-sm font-medium transition-colors text-slate-600 hover:text-scg-800 hover:bg-scg-50';
            });
            
            const activeBtn = document.getElementById(`nav-${tabId}`);
            if(activeBtn) {
                activeBtn.classList.add('bg-scg-800', 'text-white', 'shadow-md');
                activeBtn.classList.remove('text-slate-600', 'hover:bg-scg-50', 'text-scg-700', 'bg-scg-50');
            }

            if(tabId === 'training') {
                const toggleContainer = document.getElementById('admin-edit-toggle-container');
                if(currentUser.id === 'Admin') toggleContainer.classList.remove('hidden');
                else toggleContainer.classList.add('hidden');
                
                isEditMode = false;
                updateEditModeButton();
                buildFiltersUI();
                buildRoleResponseSection();
                buildTrainingMatrix();
            }
            if(tabId === 'evaluation') setupEvaluationTab();
            if(tabId === 'dashboard') setupDashboardTab();
            if(tabId === 'admin') setupAdminTab();
        }

        function toggleEditMode() {
            isEditMode = !isEditMode;
            updateEditModeButton();
            buildRoleResponseSection();
            buildTrainingMatrix();
        }

        function updateEditModeButton() {
            const btn = document.getElementById('edit-mode-btn');
            if(!btn) return;
            if(isEditMode) {
                btn.innerHTML = `<i class="fa-solid fa-check mr-2"></i> ปิดโหมดแก้ไข (Done)`;
                btn.classList.replace('bg-white', 'bg-scg-800');
                btn.classList.replace('text-slate-700', 'text-white');
                btn.classList.replace('border-slate-300', 'border-scg-900');
            } else {
                btn.innerHTML = `<i class="fa-solid fa-pen-to-square mr-2"></i> เปิดโหมดแก้ไขโครงสร้าง (Edit Mode)`;
                btn.classList.replace('bg-scg-800', 'bg-white');
                btn.classList.replace('text-white', 'text-slate-700');
                btn.classList.replace('border-scg-900', 'border-slate-300');
            }
        }

        function getVisiblePositions(userId) {
            if (userId === 'Admin') return positions;
            let visible = new Set();
            if(dbUsers[userId] && dbUsers[userId].position) visible.add(dbUsers[userId].position);
            getSubordinates(userId).forEach(subId => {
                if(dbUsers[subId] && dbUsers[subId].position) visible.add(dbUsers[subId].position);
            });
            return Array.from(visible).filter(p => p !== undefined);
        }

        async function addNewPosition() {
            const newPos = "ตำแหน่งใหม่ " + (positions.length + 1);
            if (positions.includes(newPos)) return;
            
            await fetch(`${API_BASE}/positions`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: newPos, num_comps: competencies.length })
            });
            await fetchInitialData(true);
            showToast("เพิ่มตำแหน่งใหม่สำเร็จ");
            buildRoleResponseSection();
            buildTrainingMatrix();
        }

        async function deletePosition(posName) {
            if (!confirm(`คุณต้องการลบตำแหน่ง "${posName}" ใช่หรือไม่? พนักงานที่อยู่ในตำแหน่งนี้จะถูกนำตำแหน่งออก`)) return;
            await fetch(`${API_BASE}/positions/${encodeURIComponent(posName)}`, {
                method: 'DELETE'
            });
            await fetchInitialData(true);
            showToast("ลบตำแหน่งสำเร็จ");
            buildRoleResponseSection();
            buildTrainingMatrix();
        }

        async function addNewCompetency() {
            const nextIndex = competencies.length + 1;
            const newCompName = nextIndex + ". ทักษะใหม่";
            
            await fetch(`${API_BASE}/competencies`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: newCompName, id: "c" + nextIndex })
            });
            await fetchInitialData(true);
            showToast("เพิ่ม Competency ใหม่สำเร็จ");
            buildTrainingMatrix();
        }

        async function handlePositionChange(oldName, newName) {
            if(oldName === newName || !newName) return;
            
            await fetch(`${API_BASE}/positions/name`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ oldName: oldName, newName: newName })
            });
            
            showToast("เปลี่ยนชื่อตำแหน่งสำเร็จ");
            fetchInitialData(true);
        }

        async function handlePositionGroupChange(pos, groupName) {
            positionGroups[pos] = groupName;
            await fetch(`${API_BASE}/positions/group`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ position: pos, group: groupName })
            });
            showToast("อัปเดตกลุ่มงานสำเร็จ");
        }

        async function handleRoleResponseChange(pos, response) {
            roleResponses[pos] = response;
            await fetch(`${API_BASE}/positions/role`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ position: pos, roleResponse: response })
            });
            showToast("อัปเดตหน้าที่สำเร็จ");
        }

        async function handleCompetencyChange(index, newName) {
            if(!newName) return;
            
            await fetch(`${API_BASE}/competencies/name`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ index, name: newName })
            });
            competencies[index].name = newName;
            showToast("เปลี่ยนชื่อ Competency สำเร็จ");
            buildTrainingMatrix();
        }
        async function handleCompetencyGroupChange(index, groupName) {
            competencies[index].group = groupName;
            await fetch(`${API_BASE}/competencies/group`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ index, group: groupName })
            });
            showToast("อัปเดตกลุ่มทักษะสำเร็จ");
        }


        window.toggleFilterMenu = function(menuId) {
            const menus = ['job-group-menu', 'pos-dropdown-menu', 'comp-group-menu', 'comp-dropdown-menu'];
            menus.forEach(m => {
                const el = document.getElementById(m);
                if(el) {
                    if(m === menuId) el.classList.toggle('hidden');
                    else el.classList.add('hidden');
                }
            });
        };

        // Close dropdowns when clicking outside
        document.addEventListener('click', function(e) {
            if(!e.target.closest('.relative.z-20')) {
                const menus = ['job-group-menu', 'pos-dropdown-menu', 'comp-group-menu', 'comp-dropdown-menu'];
                menus.forEach(m => {
                    const el = document.getElementById(m);
                    if(el) el.classList.add('hidden');
                });
            }
        });

        function buildFiltersUI() {
            const jobGroupContainer = document.getElementById('job-group-filters');
            const posContainer = document.getElementById('position-filters');
            const compGroupContainer = document.getElementById('comp-group-filters');
            const compContainer = document.getElementById('competency-filters');
            if(!posContainer || !compContainer) return;
            
            const visiblePos = getVisiblePositions(currentUser.id);
            
            // Build Job Groups
            let jobGroupsSet = new Set();
            visiblePos.forEach(p => {
                if(positionGroups[p]) jobGroupsSet.add(positionGroups[p]);
            });
            let jobGroups = Array.from(jobGroupsSet).sort();
            
            if(jobGroupContainer) {
                let jobGroupHtml = '';
                jobGroups.forEach(g => {
                    const isSelected = selectedJobGroupFilter.includes(g);
                    jobGroupHtml += `<label class="flex items-center gap-3 px-3 py-2 hover:bg-slate-50 rounded-lg cursor-pointer transition-colors w-full">
                        <input type="checkbox" class="form-checkbox h-4 w-4 text-scg-600 rounded border-slate-300" ${isSelected ? 'checked' : ''} onchange="toggleJobGroupFilter('${g}')">
                        <span class="text-sm font-medium ${isSelected ? 'text-scg-700' : 'text-slate-600'}">${g}</span>
                    </label>`;
                });
                jobGroupContainer.innerHTML = jobGroupHtml;
            }
            
            let posHtml = '';
            let filteredPositionsForDropdown = visiblePos;
            if(selectedJobGroupFilter.length > 0) {
                filteredPositionsForDropdown = visiblePos.filter(p => selectedJobGroupFilter.includes(positionGroups[p]));
            }
            filteredPositionsForDropdown.forEach(p => {
                const isSelected = selectedPositionsFilter.includes(p);
                posHtml += `<label class="flex items-center gap-3 px-3 py-2 hover:bg-slate-50 rounded-lg cursor-pointer transition-colors w-full">
                    <input type="checkbox" class="form-checkbox h-4 w-4 text-scg-600 rounded border-slate-300" ${isSelected ? 'checked' : ''} onchange="togglePosFilter('${p}')">
                    <span class="text-sm font-medium ${isSelected ? 'text-scg-700' : 'text-slate-600'}">${p}</span>
                </label>`;
            });
            posContainer.innerHTML = posHtml;
            
            // Build Competency Groups
            let compGroupsSet = new Set();
            competencies.forEach(c => {
                if(c.group) compGroupsSet.add(c.group);
            });
            let compGroups = Array.from(compGroupsSet).sort();

            if(compGroupContainer) {
                let compGroupHtml = '';
                compGroups.forEach(g => {
                    const isSelected = selectedCompetencyGroupFilter.includes(g);
                    compGroupHtml += `<label class="flex items-center gap-3 px-3 py-2 hover:bg-slate-50 rounded-lg cursor-pointer transition-colors w-full">
                        <input type="checkbox" class="form-checkbox h-4 w-4 text-scg-600 rounded border-slate-300" ${isSelected ? 'checked' : ''} onchange="toggleCompGroupFilter('${g}')">
                        <span class="text-sm font-medium ${isSelected ? 'text-scg-700' : 'text-slate-600'}">${g}</span>
                    </label>`;
                });
                compGroupContainer.innerHTML = compGroupHtml;
            }

            let compHtml = '';
            let filteredCompetenciesForDropdown = competencies;
            if(selectedCompetencyGroupFilter.length > 0) {
                filteredCompetenciesForDropdown = competencies.filter(c => selectedCompetencyGroupFilter.includes(c.group));
            }
            filteredCompetenciesForDropdown.forEach(c => {
                const isSelected = selectedCompetenciesFilter.includes(c.name);
                compHtml += `<label class="flex items-center gap-3 px-3 py-2 hover:bg-slate-50 rounded-lg cursor-pointer transition-colors w-full">
                    <input type="checkbox" class="form-checkbox h-4 w-4 text-scg-600 rounded border-slate-300" ${isSelected ? 'checked' : ''} onchange="toggleCompFilter('${c.name}')">
                    <span class="text-sm font-medium ${isSelected ? 'text-scg-700' : 'text-slate-600'}">${c.name}</span>
                </label>`;
            });
            compContainer.innerHTML = compHtml;

            // Update texts
            const jobGroupText = document.getElementById('job-group-dropdown-text');
            if(jobGroupText) {
                if(selectedJobGroupFilter.length === 0) jobGroupText.textContent = 'เลือกกลุ่มงานทั้งหมด';
                else jobGroupText.textContent = `เลือกแล้ว ${selectedJobGroupFilter.length} กลุ่ม`;
            }

            const compGroupText = document.getElementById('comp-group-dropdown-text');
            if(compGroupText) {
                if(selectedCompetencyGroupFilter.length === 0) compGroupText.textContent = 'เลือกกลุ่มทักษะทั้งหมด';
                else compGroupText.textContent = `เลือกแล้ว ${selectedCompetencyGroupFilter.length} กลุ่ม`;
            }

            const posText = document.getElementById('pos-dropdown-text');
            if(posText) {
                if(selectedPositionsFilter.length === 0) posText.textContent = 'เลือกตำแหน่งทั้งหมด';
                else posText.textContent = `เลือกแล้ว ${selectedPositionsFilter.length} ตำแหน่ง`;
            }

            const compText = document.getElementById('comp-dropdown-text');
            if(compText) {
                if(selectedCompetenciesFilter.length === 0) compText.textContent = 'เลือกทักษะทั้งหมด';
                else compText.textContent = `เลือกแล้ว ${selectedCompetenciesFilter.length} ทักษะ`;
            }
        }
        
        window.toggleJobGroupFilter = function(g) {
            if(selectedJobGroupFilter.includes(g)) selectedJobGroupFilter = selectedJobGroupFilter.filter(x => x !== g);
            else selectedJobGroupFilter.push(g);
            buildFiltersUI();
            buildRoleResponseSection();
            buildTrainingMatrix();
        }

        window.togglePosFilter = function(p) {
            if(selectedPositionsFilter.includes(p)) selectedPositionsFilter = selectedPositionsFilter.filter(x => x !== p);
            else selectedPositionsFilter.push(p);
            buildFiltersUI();
            buildRoleResponseSection();
            buildTrainingMatrix();
        }
        
        window.toggleCompGroupFilter = function(g) {
            if(selectedCompetencyGroupFilter.includes(g)) selectedCompetencyGroupFilter = selectedCompetencyGroupFilter.filter(x => x !== g);
            else selectedCompetencyGroupFilter.push(g);
            buildFiltersUI();
            buildTrainingMatrix();
        }

        window.toggleCompFilter = function(c) {
            if(selectedCompetenciesFilter.includes(c)) selectedCompetenciesFilter = selectedCompetenciesFilter.filter(x => x !== c);
            else selectedCompetenciesFilter.push(c);
            buildFiltersUI();
            buildTrainingMatrix();
        }

        function buildRoleResponseSection() {
            const container = document.getElementById('role-response-container');
            let visiblePos = getVisiblePositions(currentUser.id);
            if(selectedJobGroupFilter.length > 0) {
                visiblePos = visiblePos.filter(p => selectedJobGroupFilter.includes(positionGroups[p]));
            }
            if(selectedPositionsFilter.length > 0) {
                visiblePos = visiblePos.filter(p => selectedPositionsFilter.includes(p));
            }
            const isAdmin = currentUser.id === 'Admin';
            
            let html = '';
            visiblePos.forEach(pos => {
                const response = roleResponses[pos] || "ยังไม่ระบุหน้าที่ความรับผิดชอบ...";
                html += `
                <div class="bg-white p-5 rounded-2xl border ${isAdmin && isEditMode ? 'border-amber-200 bg-amber-50/10' : 'border-slate-100'} hover:shadow-md transition-shadow">
                    <div class="flex items-start gap-3">
                        <div class="bg-scg-50 p-2.5 rounded-xl shrink-0"><i class="fa-solid fa-user-gear text-scg-500"></i></div>
                        <div class="w-full">
                            `;
                            
                if(isAdmin && isEditMode) {
                    html += `
                        <input type="text" value="${pos}" onchange="handlePositionChange('${pos}', this.value)" class="w-full font-bold text-scg-900 text-sm mb-2 border-b border-scg-300 bg-transparent px-1 py-1 focus:border-scg-600 outline-none" title="แก้ไขชื่อตำแหน่ง">
                        <div class="mb-2">
                            <label class="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-1 block">กลุ่มงาน (Job Group)</label>
                            <input type="text" value="${positionGroups[pos] || ''}" onchange="handlePositionGroupChange('${pos}', this.value)" placeholder="ระบุกลุ่มงาน..." class="w-full text-xs text-slate-700 p-1.5 border border-slate-200 rounded outline-none focus:border-scg-500 bg-white">
                        </div>
                        <div class="flex justify-between items-start w-full gap-2">
                            <textarea rows="3" onchange="handleRoleResponseChange('${pos}', this.value)" class="w-full text-xs text-slate-600 p-2 border border-slate-200 rounded outline-none focus:border-scg-500 resize-none bg-white">${response}</textarea>
                            <button onclick="deletePosition('${pos}')" class="text-red-400 hover:text-white hover:bg-red-500 p-2 rounded-lg transition-colors border border-red-100 flex-shrink-0" title="ลบตำแหน่งนี้"><i class="fa-solid fa-trash"></i></button>
                        </div>
                    `;
                } else {
                    html += `
                        <h4 class="font-bold text-scg-900 text-sm mb-1">${pos}</h4>
                        <p class="text-xs text-slate-500 leading-relaxed whitespace-pre-wrap">${response}</p>
                    `;
                }
                
                html += `</div></div></div>`;
            });
            
            if (isAdmin && isEditMode) {
                html += `
                <div onclick="addNewPosition()" class="bg-slate-50 border-2 border-dashed border-slate-300 rounded-2xl flex flex-col items-center justify-center p-6 cursor-pointer hover:border-scg-400 hover:bg-scg-50 transition-colors group">
                    <div class="w-10 h-10 rounded-full bg-white shadow-sm flex items-center justify-center mb-2 group-hover:scale-110 transition-transform"><i class="fa-solid fa-plus text-scg-500"></i></div>
                    <span class="text-sm font-bold text-slate-500 group-hover:text-scg-700">เพิ่มตำแหน่งใหม่</span>
                </div>`;
            }
            container.innerHTML = html;
        }

        function buildTrainingMatrix() {
            const container = document.getElementById('training-matrix-container');
            let visiblePos = getVisiblePositions(currentUser.id);
            if(selectedJobGroupFilter.length > 0) {
                visiblePos = visiblePos.filter(p => selectedJobGroupFilter.includes(positionGroups[p]));
            }
            if(selectedPositionsFilter.length > 0) {
                visiblePos = visiblePos.filter(p => selectedPositionsFilter.includes(p));
            }
            const isAdmin = currentUser.id === 'Admin';
            
            let html = `<table class="w-full text-left border-collapse text-sm"><thead><tr class="bg-slate-50 border-b border-slate-100 text-slate-600"><th class="p-4 font-semibold min-w-[200px] w-1/4">Competency</th>`;
            
            visiblePos.forEach(pos => {
                if(isAdmin && isEditMode) {
                    html += `<th class="p-4 font-semibold text-center align-top min-w-[150px] whitespace-nowrap bg-amber-50/30 border-l border-white">
                                <input type="text" value="${pos}" onchange="handlePositionChange('${pos}', this.value)" class="w-full border-b border-scg-300 bg-transparent px-1 py-1 text-sm font-bold text-scg-900 focus:border-scg-600 outline-none text-center" title="แก้ไขชื่อตำแหน่ง">
                             </th>`;
                } else {
                    html += `<th class="p-4 font-semibold text-center align-top whitespace-pre-wrap min-w-[120px] border-l border-white">${pos}</th>`;
                }
            });
            html += `<th class="w-full"></th></tr></thead><tbody class="divide-y divide-slate-100 text-slate-700">`;

            competencies.forEach((comp, compIndex) => {
                if(selectedCompetencyGroupFilter.length > 0 && !selectedCompetencyGroupFilter.includes(comp.group)) return;
                if(selectedCompetenciesFilter.length > 0 && !selectedCompetenciesFilter.includes(comp.name)) return;

                html += `<tr class="hover:bg-slate-50">`;
                
                if(isAdmin && isEditMode) {
                    html += `<td class="p-4 font-medium align-top bg-amber-50/30">
                                <div class="flex flex-col gap-2">
                                    <div class="flex items-start gap-2">
                                        <i class="fa-solid ${comp.icon} text-scg-400 w-5 mt-1"></i>
                                        <textarea rows="2" onchange="handleCompetencyChange(${compIndex}, this.value)" class="w-full border border-scg-200 rounded px-2 py-1 text-sm font-bold text-scg-900 focus:ring-1 focus:ring-scg-500 outline-none resize-none leading-tight" title="แก้ไขชื่อ Competency">${comp.name}</textarea>
                                    </div>
                                    <div class="mb-1">
                                        <label class="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-1 block">กลุ่มทักษะ (Group)</label>
                                        <input type="text" value="${comp.group || ''}" onchange="handleCompetencyGroupChange(${compIndex}, this.value)" placeholder="ระบุกลุ่มทักษะ..." class="w-full text-xs text-slate-700 p-1 border border-slate-200 rounded outline-none focus:border-scg-500 bg-white">
                                    </div>
                                    <button onclick="openLevelEditModal(${compIndex})" class="text-xs bg-white hover:bg-slate-100 text-scg-700 px-2 py-1.5 rounded border border-slate-200 w-full flex items-center justify-center gap-1 shadow-sm transition-colors">
                                        <i class="fa-solid fa-list-ol"></i> แก้ไขความหมาย Level
                                    </button>
                                </div>
                             </td>`;
                } else {
                    html += `<td class="p-4 font-medium"><i class="fa-solid ${comp.icon} text-scg-400 w-6"></i> ${comp.name}</td>`;
                }
                
                visiblePos.forEach(pos => {
                    const t = positionTargets[pos] && positionTargets[pos][compIndex] ? positionTargets[pos][compIndex] : 0;
                    const safeId = `target-${pos.replace(/[^a-zA-Z0-9]/g, '')}-${compIndex}`;
                    
                    if (isAdmin) {
                        let selectHtml = `<select id="${safeId}" onchange="updateMatrixTarget('${pos}', ${compIndex}, this.value)" class="border border-slate-200 rounded px-2 py-1.5 font-bold outline-none focus:border-scg-500 text-xs w-full max-w-[140px] bg-white cursor-pointer ${t>=4?'text-scg-800':'text-slate-600'} ${isEditMode ? 'border-amber-200' : ''}">`;
                        selectHtml += `<option value="0" ${t===0?'selected':''}>None</option>`;
                        for(let i=1; i<=5; i++) {
                            const desc = comp.levels[i] || "";
                            selectHtml += `<option value="${i}" ${t===i?'selected':''}>L${i}: ${desc}</option>`;
                        }
                        selectHtml += `</select>`;
                        html += `<td class="p-3 text-center border-l border-slate-100 ${isEditMode ? 'bg-amber-50/10' : ''}">${selectHtml}</td>`;
                    } else {
                        const levelText = t === 0 ? 'None' : `L${t}`;
                        const desc = t === 0 ? "ไม่มีความคาดหวังในทักษะนี้" : comp.levels[t];
                        const badgeClass = t === 0 ? 'bg-slate-100 text-slate-500 border border-slate-200' : (t >= 4 ? 'bg-scg-50 text-scg-800 border border-scg-200 shadow-sm' : 'bg-white text-slate-700 border border-slate-200 shadow-sm');
                        html += `<td class="p-4 text-center border-l border-slate-100">
                                    <div class="group relative inline-block w-full">
                                        <div class="px-3 py-2 rounded-lg font-bold text-xs truncate ${badgeClass}">
                                            ${levelText}${t>0 ? ': ' + desc : ''}
                                        </div>
                                        <div class="hidden group-hover:block absolute z-10 w-48 p-2 bg-slate-800 text-white text-xs rounded shadow-lg -top-10 left-1/2 transform -translate-x-1/2 whitespace-normal break-words">
                                            ${desc}
                                        </div>
                                    </div>
                                 </td>`;
                    }
                });
                html += `<td class="w-full"></td></tr>`;
            });

            if (isAdmin && isEditMode) {
                html += `
                <tr class="bg-slate-50/50">
                    <td colspan="${visiblePos.length + 2}" class="p-6 text-center border-t border-dashed border-slate-300">
                        <button onclick="addNewCompetency()" class="text-sm font-bold text-scg-700 hover:text-scg-900 bg-white border border-scg-200 px-6 py-3 rounded-xl shadow-sm hover:shadow transition-all flex items-center justify-center gap-2 mx-auto">
                            <i class="fa-solid fa-plus"></i> เพิ่ม Competency ใหม่
                        </button>
                    </td>
                </tr>`;
            }

            html += `</tbody></table>`;
            container.innerHTML = html;
        }

        async function updateMatrixTarget(pos, compIndex, value) {
            const val = parseInt(value);
            positionTargets[pos][compIndex] = val;
            
            await fetch(`${API_BASE}/positions/targets`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ position: pos, compIndex, value: val })
            });
            
            const selectEl = document.getElementById(`target-${pos.replace(/[^a-zA-Z0-9]/g, '')}-${compIndex}`);
            if (val >= 4) {
                selectEl.classList.add('text-scg-800'); selectEl.classList.remove('text-slate-600');
            } else {
                selectEl.classList.add('text-slate-600'); selectEl.classList.remove('text-scg-800');
            }
            showToast("อัปเดตเป้าหมายสำเร็จ");
        }

        // --- Level Edit Modal Functions ---
        let currentEditCompIndex = -1;

        function openLevelEditModal(index) {
            currentEditCompIndex = index;
            const comp = competencies[index];
            document.getElementById('modal-comp-name').textContent = comp.name;
            
            let html = '';
            for(let i = 1; i <= 5; i++) {
                html += `
                <div class="bg-white p-3 rounded-xl border border-slate-200">
                    <label class="block text-xs font-bold text-scg-800 mb-1.5 bg-scg-50 w-fit px-2 py-0.5 rounded">Level ${i}</label>
                    <textarea id="modal-l${i}" rows="2" class="w-full text-sm p-2 border border-slate-100 rounded-lg outline-none focus:border-scg-500 focus:ring-1 focus:ring-scg-500 resize-none" placeholder="ระบุความหมายพฤติกรรมของ Level ${i}">${comp.levels[i] || ""}</textarea>
                </div>`;
            }
            document.getElementById('modal-levels-container').innerHTML = html;
            document.getElementById('level-edit-modal').classList.remove('hidden');
        }

        function closeLevelEditModal() {
            document.getElementById('level-edit-modal').classList.add('hidden');
            currentEditCompIndex = -1;
        }

        async function saveLevelEdits() {
            if(currentEditCompIndex === -1) return;
            const comp = competencies[currentEditCompIndex];
            
            const levels = {};
            for(let i = 1; i <= 5; i++) {
                levels[i] = document.getElementById(`modal-l${i}`).value;
                comp.levels[i] = levels[i];
            }
            
            await fetch(`${API_BASE}/competencies/levels`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ index: currentEditCompIndex, levels })
            });
            
            closeLevelEditModal();
            buildTrainingMatrix(); 
            showToast("บันทึกคำอธิบาย Level สำเร็จ");
        }

        // --- 4. Evaluation Logic ---
        function setupEvaluationTab() {
            if (currentUser.id === 'Admin') {
                document.getElementById('admin-override-container').classList.remove('hidden');
                
                const overrideSelect = document.getElementById('admin-override-select');
                const prevVal = overrideSelect.value;
                overrideSelect.innerHTML = '<option value="Admin">-- เลือกสวมสิทธิหัวหน้า --</option>';
                for(let id in dbUsers) {
                    if (id !== 'Admin') overrideSelect.innerHTML += `<option value="${id}">สวมสิทธิ: ${dbUsers[id].name}</option>`;
                }
                overrideSelect.value = prevVal || 'Admin';
                
                actingAsRole = overrideSelect.value;
            } else {
                document.getElementById('admin-override-container').classList.add('hidden');
                actingAsRole = currentUser.id;
            }
            populateEvalDropdown();
        }

        function applyAdminOverride() {
            actingAsRole = document.getElementById('admin-override-select').value;
            populateEvalDropdown();
        }

        function populateEvalDropdown() {
            const selectEl = document.getElementById('eval-employee-select');
            selectEl.innerHTML = '';
            
            const subs = actingAsRole === 'Admin' ? [] : getSubordinates(actingAsRole);
            
            if (subs.length === 0) {
                selectEl.innerHTML = '<option value="">-- ไม่มีผู้ใต้บังคับบัญชา --</option>';
                document.getElementById('sliders-container').innerHTML = '<div class="text-center text-slate-400 py-10">ไม่พบข้อมูลให้ประเมิน</div>';
                if(evalRadarChartInstance) evalRadarChartInstance.destroy();
                return;
            }
            subs.forEach(id => { selectEl.innerHTML += `<option value="${id}">${dbUsers[id].name} (${dbUsers[id].position})</option>`; });
            updateEvalUI();
        }

        function updateEvalUI() {
            const id = document.getElementById('eval-employee-select').value;
            if(!id) return;
            const emp = dbUsers[id];
            const targets = positionTargets[emp.position] || [];
            const currentLabels = getLabels();

            document.getElementById('eval-emp-name').textContent = emp.name;
            document.getElementById('eval-emp-position').textContent = emp.position;

            let html = '';
            for (let i = 0; i < competencies.length; i++) {
                const targetVal = targets[i] || 0;
                if (targetVal === 0) continue; // Skip competencies with target 0
                
                const targetText = targetVal === 0 ? 'None' : `L${targetVal}`;
                const currentVal = emp.actuals[i] === 0 ? 1 : emp.actuals[i];
                const currentDesc = competencies[i].levels[currentVal] || "";

                html += `
                <div class="bg-white p-6 rounded-2xl border border-slate-200 mb-6 shadow-sm">
                    <div class="flex justify-between items-center mb-4">
                        <label class="font-bold text-lg text-slate-800">${currentLabels[i]}</label>
                        <span class="text-xs font-medium text-slate-500 bg-slate-50 px-3 py-1.5 rounded-lg border border-slate-200">เป้าหมายตำแหน่ง: <strong class="text-scg-800 text-sm ml-1">${targetText}</strong></span>
                    </div>
                    
                    <div class="flex items-center gap-4 mb-4">
                        <input type="range" id="eval-val-${i}" min="1" max="5" value="${currentVal}" 
                            class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-scg-700" 
                            oninput="updateEvalSliderDisplay(${i}, this.value)">
                        <div id="disp-${i}" class="w-12 h-12 flex items-center justify-center bg-scg-800 text-white font-black text-xl rounded-xl shadow-inner shrink-0">${currentVal}</div>
                    </div>
                    
                    <div class="bg-slate-50 p-3.5 rounded-xl border border-slate-100 text-sm mb-4 flex items-start gap-3">
                        <span id="badge-${i}" class="font-bold text-scg-700 bg-scg-100/50 px-2.5 py-1 rounded-md shrink-0 border border-scg-200/50">Level ${currentVal}</span>
                        <span id="desc-${i}" class="text-slate-600 leading-relaxed mt-0.5">${currentDesc}</span>
                    </div>
                    
                    <div class="pt-4 border-t border-slate-200 border-dashed">
                        <label class="block text-xs font-bold text-slate-500 mb-2"><i class="fa-regular fa-comment-dots text-scg-500 mr-1"></i> คำอธิบาย/หลักฐานอ้างอิง (Evidence)</label>
                        <textarea id="eval-evi-${i}" rows="2" class="w-full text-sm p-3 border border-slate-200 rounded-xl outline-none focus:border-scg-500 focus:ring-1 focus:ring-scg-500 resize-none transition-colors" placeholder="ระบุพฤติกรรมหรือผลงานที่สนับสนุนคะแนนนี้...">${emp.evidences[i] || ''}</textarea>
                    </div>
                    
                    <div class="pt-4 mt-2 border-t border-slate-200 border-dashed grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-xs font-bold text-slate-500 mb-2"><i class="fa-solid fa-bullseye text-scg-500 mr-1"></i> ความคาดหวังเพิ่มเติม</label>
                            <textarea id="eval-add-exp-${i}" rows="2" class="w-full text-sm p-3 border border-slate-200 rounded-xl outline-none focus:border-scg-500 focus:ring-1 focus:ring-scg-500 resize-none transition-colors" placeholder="สิ่งที่คาดหวังให้พัฒนาเพิ่มเติม...">${(emp.additional_expectations && emp.additional_expectations[i]) || ''}</textarea>
                        </div>
                        <div>
                            <label class="block text-xs font-bold text-slate-500 mb-2"><i class="fa-solid fa-book-open text-scg-500 mr-1"></i> หัวข้อที่อยากให้เรียนรู้เพิ่มเติม</label>
                            <textarea id="eval-lrn-top-${i}" rows="2" class="w-full text-sm p-3 border border-slate-200 rounded-xl outline-none focus:border-scg-500 focus:ring-1 focus:ring-scg-500 resize-none transition-colors" placeholder="ระบุหัวข้อที่ควรส่งไปอบรม...">${(emp.learning_topics && emp.learning_topics[i]) || ''}</textarea>
                        </div>
                    </div>
                </div>`;
            }
            
            html += `
                <div class="bg-white p-6 rounded-2xl border border-scg-200 mb-6 shadow-md relative overflow-hidden">
                    <div class="absolute top-0 right-0 w-24 h-24 bg-scg-50 rounded-bl-full z-0"></div>
                    <h3 class="font-bold text-lg text-scg-900 mb-4 relative z-10"><i class="fa-solid fa-star text-amber-400 mr-2"></i> ความเชี่ยวชาญพิเศษของพนักงาน</h3>
                    
                    <div class="space-y-4 relative z-10">
                        <div>
                            <label class="block text-sm font-bold text-slate-700 mb-2">กลุ่มความเชี่ยวชาญ</label>
                            <select id="eval-spec-exp" class="w-full md:w-1/2 text-sm p-3 border border-slate-300 rounded-xl outline-none focus:border-scg-500 focus:ring-1 focus:ring-scg-500 bg-white">
                                <option value="" ${!emp.special_expertise ? 'selected' : ''}>-- เลือกความเชี่ยวชาญ --</option>
                                <option value="Technical" ${emp.special_expertise === 'Technical' ? 'selected' : ''}>Technical</option>
                                <option value="Leadership" ${emp.special_expertise === 'Leadership' ? 'selected' : ''}>Leadership</option>
                                <option value="IT" ${emp.special_expertise === 'IT' ? 'selected' : ''}>IT</option>
                                <option value="Digital" ${emp.special_expertise === 'Digital' ? 'selected' : ''}>Digital</option>
                                <option value="AI" ${emp.special_expertise === 'AI' ? 'selected' : ''}>AI</option>
                                <option value="Analytic" ${emp.special_expertise === 'Analytic' ? 'selected' : ''}>Analytic</option>
                                <option value="Other" ${emp.special_expertise === 'Other' ? 'selected' : ''}>Other</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-slate-700 mb-2">คำอธิบายเพิ่มเติม / ตัวอย่างผลงานที่เชี่ยวชาญ</label>
                            <textarea id="eval-spec-dtl" rows="3" class="w-full text-sm p-3 border border-slate-300 rounded-xl outline-none focus:border-scg-500 focus:ring-1 focus:ring-scg-500 resize-none transition-colors" placeholder="ระบุรายละเอียดความเชี่ยวชาญพิเศษที่โดดเด่น...">${emp.special_expertise_detail || ''}</textarea>
                        </div>
                    </div>
                </div>
            `;
            
            document.getElementById('sliders-container').innerHTML = html;
            drawEvalRadar();
        }

        function updateEvalSliderDisplay(index, val) {
            document.getElementById(`disp-${index}`).textContent = val;
            document.getElementById(`badge-${index}`).textContent = `Level ${val}`;
            document.getElementById(`desc-${index}`).textContent = competencies[index].levels[val];
            drawEvalRadar();
        }

        function drawEvalRadar() {
            const id = document.getElementById('eval-employee-select').value;
            const emp = dbUsers[id];
            const targets = positionTargets[emp.position] || [];
            let actuals = [];
            let cleanLabels = [];
            let cleanTargets = [];
            
            const allLabels = getLabels().map(l => {
                const parts = l.split('. ');
                return parts.length > 1 ? parts.slice(1).join('. ') : l;
            });

            for (let i = 0; i < competencies.length; i++) {
                const t = targets[i] || 0;
                if (t === 0) continue; // Only show on radar if target > 0
                
                cleanLabels.push(allLabels[i]);
                cleanTargets.push(t);
                
                const el = document.getElementById(`eval-val-${i}`);
                actuals.push(el ? parseInt(el.value) : (emp.actuals[i] || 0));
            }

            if(evalRadarChartInstance) evalRadarChartInstance.destroy();
            const ctx = document.getElementById('evalRadarChart').getContext('2d');

            evalRadarChartInstance = new Chart(ctx, {
                type: 'radar',
                data: {
                    labels: cleanLabels, 
                    datasets: [
                        { label: 'Target', data: cleanTargets, borderColor: '#cbd5e1', backgroundColor: 'transparent', borderDash: [5,5] },
                        { label: 'Actual', data: actuals, borderColor: '#ca3656', backgroundColor: 'rgba(202, 54, 86, 0.2)' }
                    ]
                },
                options: { responsive: true, maintainAspectRatio: false, scales: { r: { min: 0, max: 5, ticks:{display:false} } } }
            });
        }

        async function saveEvaluation() {
            const id = document.getElementById('eval-employee-select').value;
            const emp = dbUsers[id];
            
            if (!emp.additional_expectations) emp.additional_expectations = new Array(competencies.length).fill('');
            if (!emp.learning_topics) emp.learning_topics = new Array(competencies.length).fill('');
            
            for (let i = 0; i < competencies.length; i++) {
                const elVal = document.getElementById(`eval-val-${i}`);
                const elEvi = document.getElementById(`eval-evi-${i}`);
                const elAddExp = document.getElementById(`eval-add-exp-${i}`);
                const elLrnTop = document.getElementById(`eval-lrn-top-${i}`);
                
                if (elVal && elEvi) {
                    emp.actuals[i] = parseInt(elVal.value);
                    emp.evidences[i] = elEvi.value;
                }
                if (elAddExp) emp.additional_expectations[i] = elAddExp.value;
                if (elLrnTop) emp.learning_topics[i] = elLrnTop.value;
            }
            
            const specExp = document.getElementById('eval-spec-exp') ? document.getElementById('eval-spec-exp').value : '';
            const specDtl = document.getElementById('eval-spec-dtl') ? document.getElementById('eval-spec-dtl').value : '';
            
            emp.special_expertise = specExp;
            emp.special_expertise_detail = specDtl;
            emp.evalDate = new Date().toLocaleDateString('th-TH');
            
            await fetch(`${API_BASE}/evaluations`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    userId: id,
                    actuals: emp.actuals,
                    evidences: emp.evidences,
                    additionalExpectations: emp.additional_expectations,
                    learningTopics: emp.learning_topics,
                    specialExpertise: emp.special_expertise,
                    specialExpertiseDetail: emp.special_expertise_detail,
                    evalDate: emp.evalDate
                })
            });
            
            showToast("บันทึกประเมินสำเร็จ");
            setTimeout(() => { switchTab('dashboard'); }, 1000);
        }

        // --- 5. Dashboard Logic ---
        function setupDashboardTab() {
            const currentUserId = currentUser.id;
            const subs = getSubordinates(currentUserId);
            
            let toShow = [];
            if (currentUserId === 'Admin') {
                toShow = Object.keys(dbUsers).filter(id => id !== 'Admin');
                document.getElementById('dash-manager-view').style.display = 'block';
            } else if (subs.length === 0) {
                toShow = [currentUserId];
                document.getElementById('dash-manager-view').style.display = 'none';
            } else {
                toShow = subs;
                document.getElementById('dash-manager-view').style.display = 'block';
            }

            if(toShow.length === 0) {
                 document.getElementById('dash-individual-cards-container').innerHTML = '<div class="text-center bg-white p-10 rounded-3xl border border-slate-100 text-slate-400">ไม่พบข้อมูลให้แสดงผล</div>';
                 return;
            }

            if(subs.length > 0 || currentUserId === 'Admin') {
                drawAverageBarChart(toShow);
            }
            renderIndividualDashboards(toShow);
        }

        function drawAverageBarChart(subIds) {
            const names = []; const avgTargets = []; const avgActuals = []; const percentCompletes = [];

            subIds.forEach(id => {
                const emp = dbUsers[id];
                const targets = positionTargets[emp.position] || [];
                names.push(emp.name); 
                
                const sumTarget = targets.reduce((a, b) => a + b, 0);
                const sumActual = emp.actuals.reduce((a, b) => a + b, 0);
                
                const avgT = sumTarget / (competencies.length || 1);
                const avgA = sumActual / (competencies.length || 1);
                
                avgTargets.push(avgT.toFixed(1));
                avgActuals.push(avgA.toFixed(1));
                
                // Calculate % Complete
                const percent = avgT > 0 ? Math.round((avgA / avgT) * 100) : 0;
                percentCompletes.push(percent);
            });

            if(averageBarChartInstance) averageBarChartInstance.destroy();
            const ctx = document.getElementById('averageBarChart').getContext('2d');
            averageBarChartInstance = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: names,
                    datasets: [
                        { 
                            type: 'line',
                            label: '% Complete', 
                            data: percentCompletes, 
                            borderColor: '#eab308',
                            backgroundColor: '#eab308',
                            borderWidth: 2,
                            pointRadius: 6,
                            pointHoverRadius: 8,
                            showLine: false,
                            yAxisID: 'y1'
                        },
                        { label: 'Average Expected', data: avgTargets, backgroundColor: '#cbd5e1', yAxisID: 'y' },
                        { label: 'Average Actual', data: avgActuals, backgroundColor: '#ca3656', yAxisID: 'y' }
                    ]
                },
                options: { 
                    responsive: true, 
                    maintainAspectRatio: false, 
                    scales: { 
                        y: { min: 0, max: 5, position: 'left' },
                        y1: { 
                            min: 0, 
                            max: 120,
                            position: 'right',
                            grid: { drawOnChartArea: false },
                            ticks: { callback: function(value) { return value + '%'; } }
                        }
                    },
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    let label = context.dataset.label || '';
                                    if (label) { label += ': '; }
                                    if (context.dataset.yAxisID === 'y1') {
                                        label += context.parsed.y + '%';
                                    } else {
                                        label += context.parsed.y;
                                    }
                                    return label;
                                }
                            }
                        }
                    }
                },
                plugins: [{
                    id: 'customDataLabels',
                    afterDatasetsDraw(chart, args, pluginOptions) {
                        const { ctx, data } = chart;
                        ctx.save();
                        
                        // Dataset 0 is the % Complete line
                        chart.getDatasetMeta(0).data.forEach((datapoint, index) => {
                            const value = data.datasets[0].data[index] + '%';
                            ctx.fillStyle = '#b45309';
                            ctx.font = 'bold 12px sans-serif';
                            ctx.textAlign = 'center';
                            ctx.textBaseline = 'bottom';
                            ctx.fillText(value, datapoint.x, datapoint.y - 10);
                        });
                        
                        ctx.restore();
                    }
                }]
            });
        }

        function renderIndividualDashboards(subIds) {
            const container = document.getElementById('dash-individual-cards-container');
            container.innerHTML = '';
            individualCharts.forEach(chart => chart.destroy()); individualCharts = [];
            const currentLabels = getLabels();

            subIds.forEach(id => {
                const emp = dbUsers[id];
                const targets = positionTargets[emp.position] || [];
                let totalTarget = 0; let totalActual = 0; let gaps = [];
                
                for(let i=0; i<competencies.length; i++) {
                    const t = targets[i] || 0;
                    const a = emp.actuals[i] || 0;
                    totalTarget += t;
                    totalActual += a;
                    let diff = a - t;
                    if (diff < 0 && t > 0) gaps.push({ skill: currentLabels[i], gap: diff, index: i });
                }

                const readiness = totalTarget === 0 ? 0 : Math.round((totalActual / totalTarget) * 100);
                const safeReadiness = readiness > 100 ? 100 : readiness;
                let readinessColor = safeReadiness >= 100 ? "text-green-400" : (safeReadiness >= 80 ? "text-yellow-400" : "text-red-400");
                const gapText = gaps.length === 0 ? "พร้อมสมบูรณ์ (ไม่มี Gap)" : `พบ ${gaps.length} ทักษะที่ต้องพัฒนา`;

                let recsHtml = '';
                if (gaps.length === 0) {
                    recsHtml = `<div class="bg-green-50 p-3 rounded-xl border border-green-100 flex items-start gap-3"><i class="fa-solid fa-medal text-green-500 mt-0.5"></i><div><p class="text-sm font-bold text-green-800">ทักษะผ่านเกณฑ์ทั้งหมด</p></div></div>`;
                } else {
                    gaps.forEach(gap => {
                        let courseName = "หลักสูตรพัฒนาทักษะ (OJT)"; let icon = "fa-book";
                        if (gap.skill.includes("ไฟฟ้า")) { courseName = "เทคนิคตู้ MDB และมอเตอร์ 3 เฟส"; icon="fa-bolt"; }
                        else if (gap.skill.includes("เครื่องกล")) { courseName = "ซ่อมบำรุงปั๊มน้ำและระบบนิวเมติกส์"; icon="fa-gear"; }
                        else if (gap.skill.includes("วิเคราะห์")) { courseName = "การอ่านแบบ Schematic Diagram"; icon="fa-magnifying-glass-chart"; }
                        recsHtml += `
                        <div class="flex items-center gap-3 p-3 bg-white border border-slate-100 rounded-xl shadow-sm">
                            <div class="bg-scg-50 p-2 rounded-lg text-scg-600 flex-shrink-0"><i class="fa-solid ${icon}"></i></div>
                            <div>
                                <p class="text-[10px] text-slate-500 font-medium">${gap.skill.substring(3)} <span class="text-red-500 font-bold">(Gap ${gap.gap})</span></p>
                                <p class="text-xs font-bold text-slate-800 leading-tight mt-0.5">${courseName}</p>
                            </div>
                        </div>`;
                    });
                }

                const html = `
                <div class="bg-white p-6 md:p-8 rounded-3xl shadow-sm border border-slate-100">
                    <div class="flex items-center justify-between mb-6 border-b border-slate-100 pb-4">
                        <h3 class="font-bold text-xl text-scg-900">${emp.name}</h3>
                        <span class="bg-scg-50 text-scg-700 text-xs px-3 py-1 rounded-full font-bold border border-scg-100">${emp.position}</span>
                    </div>
                    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                        <div class="lg:col-span-2 relative h-[320px] w-full flex justify-center"><canvas id="radar-${id}"></canvas></div>
                        <div class="space-y-6">
                            <div class="bg-scg-800 rounded-2xl p-6 text-white shadow-md">
                                <h3 class="font-medium text-scg-100 mb-1">ความพร้อมโดยรวม</h3>
                                <div class="flex items-baseline gap-2"><span class="text-5xl font-bold ${readinessColor}">${safeReadiness}%</span><span class="text-sm text-scg-200">จากเป้าหมาย</span></div>
                                <div class="mt-4 pt-4 border-t border-scg-700/50"><p class="text-sm text-scg-100">Gap:</p><p class="text-lg font-bold text-white">${gapText}</p></div>
                            </div>
                            <div class="bg-slate-50 rounded-2xl p-5 border border-slate-100 shadow-inner">
                                <h3 class="font-bold text-slate-800 mb-4 text-sm"><i class="fa-solid fa-lightbulb text-amber-500 mr-2"></i>คอร์สเรียนแนะนำ</h3>
                                <div class="space-y-3 max-h-[160px] overflow-y-auto pr-2">${recsHtml}</div>
                            </div>
                        </div>
                    </div>
                </div>`;
                container.innerHTML += html;
            });

            subIds.forEach(id => {
                const emp = dbUsers[id];
                const ctx = document.getElementById(`radar-${id}`).getContext('2d');
                
                const tData = positionTargets[emp.position] || [];
                const aData = emp.actuals || [];
                
                const cleanLabels = [];
                const cleanTargets = [];
                const cleanActuals = [];
                
                for (let i = 0; i < currentLabels.length; i++) {
                    if (tData[i] && tData[i] > 0) {
                        const parts = currentLabels[i].split('. ');
                        cleanLabels.push(parts.length > 1 ? parts.slice(1).join('. ') : currentLabels[i]);
                        cleanTargets.push(tData[i]);
                        cleanActuals.push(aData[i] || 0);
                    }
                }

                const chart = new Chart(ctx, {
                    type: 'radar',
                    data: {
                        labels: cleanLabels,
                        datasets: [
                            { label: 'Target', data: cleanTargets, borderColor: '#94a3b8', backgroundColor: 'rgba(148, 163, 184, 0.2)' },
                            { label: 'Actual', data: cleanActuals, borderColor: '#882239', backgroundColor: 'rgba(136, 34, 57, 0.3)' }
                        ]
                    },
                    options: { responsive: true, maintainAspectRatio: false, scales: { r: { min: 0, max: 5, ticks:{display:false} } } }
                });
                individualCharts.push(chart);
            });
        }

        // --- 6. Admin Panel Export & Management ---
        function setupAdminTab() {
            const posSelect = document.getElementById('new-user-pos');
            posSelect.innerHTML = '';
            positions.forEach(p => posSelect.innerHTML += `<option value="${p}">${p}</option>`);

            const mgrSelect = document.getElementById('new-user-mgr');
            mgrSelect.innerHTML = '';
            for(let id in dbUsers) {
                if (id !== 'Admin') mgrSelect.innerHTML += `<option value="${id}">${dbUsers[id].name}</option>`;
            }

            let hHtml = '';
            for(let id in dbUsers) {
                if(id !== 'Admin') {
                    let mgrOptions = '';
                    for(let potentialMgr in dbUsers) {
                        if (potentialMgr !== 'Admin' && potentialMgr !== id) {
                            const selected = dbUsers[id].managerIds && dbUsers[id].managerIds.includes(potentialMgr) ? 'selected' : '';
                            mgrOptions += `<option value="${potentialMgr}" ${selected}>${dbUsers[potentialMgr].name}</option>`;
                        }
                    }

                    hHtml += `
                    <div class="bg-slate-50 p-5 rounded-2xl border border-slate-200 flex flex-col items-start gap-4 text-sm shadow-sm">
                        <div class="w-full flex justify-between items-start border-b border-slate-200 pb-3">
                            <div>
                                <span class="font-bold text-scg-800 block text-base leading-tight">${dbUsers[id].name}</span>
                                <span class="text-xs text-slate-500 font-medium">Username: ${id}</span>
                            </div>
                            <span class="text-[10px] text-scg-600 font-bold bg-scg-50 border border-scg-100 px-2 py-0.5 rounded">${dbUsers[id].position}</span>
                        </div>
                        <div class="w-full">
                            <label class="text-xs font-bold text-slate-500 block mb-1.5"><i class="fa-solid fa-sitemap mr-1"></i> สายบังคับบัญชา (เลือกได้หลายคน):</label>
                            <select multiple onchange="updateUserManager('${id}', this)" class="w-full text-xs p-1.5 border border-slate-300 rounded-lg focus:border-scg-500 outline-none bg-white font-bold text-slate-700 h-20 shadow-inner">
                                ${mgrOptions}
                            </select>
                            <p class="text-[9px] text-slate-400 mt-1 text-right">Ctrl/Cmd + คลิก เพื่อเลือกหลายคน</p>
                        </div>
                    </div>`;
                }
            }
            document.getElementById('admin-hierarchy-list').innerHTML = hHtml;
        }

        async function updateUserManager(userId, selectElement) {
            const selectedManagers = Array.from(selectElement.selectedOptions).map(opt => opt.value);
            dbUsers[userId].managerIds = selectedManagers;
            
            await fetch(`${API_BASE}/users/${userId}/manager`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ managers: selectedManagers })
            });
            
            showToast(`อัปเดตสายบังคับบัญชาของ ${userId} สำเร็จ`);
        }

        async function addNewUser() {
            const uid = document.getElementById('new-user-id').value.trim();
            const pass = document.getElementById('new-user-pass').value.trim();
            const name = document.getElementById('new-user-name').value.trim();
            const pos = document.getElementById('new-user-pos').value;
            const selectMgrs = document.getElementById('new-user-mgr');
            const mgrs = Array.from(selectMgrs.selectedOptions).map(opt => opt.value);

            if (!uid || !pass || !name) {
                alert("กรุณากรอกข้อมูล Username, Password และ ชื่อ-นามสกุล ให้ครบถ้วน");
                return;
            }

            if (dbUsers[uid] || uid.toLowerCase() === 'admin') {
                alert("Username นี้มีอยู่ในระบบแล้ว กรุณาใช้ชื่ออื่น");
                return;
            }

            try {
                const res = await fetch(`${API_BASE}/users`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        uid, pass, name, pos, mgrs, num_comps: competencies.length
                    })
                });
                
                if (!res.ok) throw new Error("Failed to create user");
                
                await fetchInitialData(true);

                showToast(`เพิ่มผู้ใช้งาน ${name} สำเร็จ`);
                
                document.getElementById('new-user-id').value = '';
                document.getElementById('new-user-pass').value = '';
                document.getElementById('new-user-name').value = '';
                selectMgrs.selectedIndex = -1;
                
                setupAdminTab(); 
            } catch (err) {
                alert("Failed to create user.");
                console.error(err);
            }
        }

        function exportToExcel() {
            let csvContent = "\\ufeff"; 
            csvContent += "ชื่อพนักงาน,ตำแหน่ง,ผู้บังคับบัญชา,Competency,Skill level ที่คาดหวัง,skill Level ที่ประเมินจริง,คำอธิบาย Evidence ที่ผู้บังคับบัญชาใส่,วันที่ประเมิน,ความหมาย skill level ที่คาดหวัง,ความหมาย skill level ที่ประเมินจริง\\n";
            const currentLabels = getLabels();

            for (let id in dbUsers) {
                if (id === 'Admin') continue;
                const emp = dbUsers[id];
                const targets = positionTargets[emp.position] || [];
                
                let mgrNames = "None";
                if (emp.managerIds && emp.managerIds.length > 0) {
                    mgrNames = emp.managerIds.map(mId => dbUsers[mId] ? dbUsers[mId].name : mId).join(' และ ');
                }

                for (let i = 0; i < competencies.length; i++) {
                    const targetVal = targets[i] || 0;
                    const actualVal = emp.actuals[i] || 0;
                    
                    const targetDesc = targetVal === 0 ? "ไม่มีเป้าหมายที่คาดหวัง" : (competencies[i].levels[targetVal] || "-");
                    const actualDesc = actualVal === 0 ? "-" : (competencies[i].levels[actualVal] || "-");
                    
                    const row = [
                        `"${emp.name}"`, `"${emp.position}"`, `"${mgrNames}"`,
                        `"${currentLabels[i]}"`, targetVal, actualVal,
                        `"${emp.evidences[i] || '-'}"`, `"${emp.evalDate || 'ยังไม่ถูกประเมิน'}"`,
                        `"${targetDesc}"`, `"${actualDesc}"`
                    ];
                    csvContent += row.join(",") + "\\n";
                }
            }

            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement("a");
            const url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", `Competency_Export_${new Date().getTime()}.csv`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    </script>
</body>
</html>
"""

final_content = html_part + new_js

os.makedirs(os.path.dirname(dest_file), exist_ok=True)
with open(dest_file, 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Build frontend successfully.")
