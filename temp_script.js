

        const API_BASE = '/api';

        // --- System Functions ---
        function openQuickGuide() {
            document.getElementById('quick-guide-modal').classList.remove('hidden');
        }

        function closeQuickGuide() {
            document.getElementById('quick-guide-modal').classList.add('hidden');
        }

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
        let adminTempData = [];
        let deletedEmployeeIds = [];
        let currentUser = null;
        let actingAsRole = null;
        let evalRadarChartInstance = null;
        let averageBarChartInstance = null;
        let individualCharts = [];
        let isEditMode = false;
        let selectedPositionsFilter = [];
        let selectedCompetenciesFilter = [];
        let selectedJobGroupFilter = [];
        let selectedSectionFilter = [];
        let selectedDepartmentFilter = [];
        let selectedReportToFilter = [];
        let selectedEmployeeFilter = [];
        let selectedCompetencyGroupFilter = [];
        let idpRadarChartInstance = null;

        // Analytic Tab State
        let analyticRadarCharts = [];
        let analyticBarChartInstance = null;
        let employeeData = [];
        let employeeDataAll = [];

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
                employeeDataAll = data.employeeData || [];
                employeeData = employeeDataAll.filter(e => e.Pipeline === 'Evaluated');
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

            const matchedKeys = Object.keys(dbUsers).filter(k => k.toLowerCase() === user.toLowerCase());
            
            let validUserKey = null;
            for (let k of matchedKeys) {
                if (dbUsers[k].pass === pass) {
                    validUserKey = k;
                    break;
                }
            }

            if (validUserKey) {
                localStorage.setItem('comp_sys_user', validUserKey);
                checkLoginState();
            } else {
                document.getElementById('login-error').classList.remove('hidden');
            }
        }

                // Mobile menu toggle
        window.toggleMobileMenu = function() {
            const sidebar = document.getElementById('main-sidebar');
            const overlay = document.getElementById('mobile-overlay');
            if (sidebar.classList.contains('-translate-x-full')) {
                sidebar.classList.remove('-translate-x-full');
                overlay.classList.remove('hidden');
            } else {
                sidebar.classList.add('-translate-x-full');
                overlay.classList.add('hidden');
            }
        };

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

                if (currentUser.role === 'Super Admin') {
                    currentUser.scope_section = 'ALL';
                    currentUser.scope_department = 'ALL';
                    const btn = document.getElementById('btn-manage-admins');
                    if (btn) btn.classList.remove('hidden');
                } else if (currentUser.role === 'Admin') {
                    currentUser.scope_section = currentUser.scope_section || 'ALL';
                    currentUser.scope_department = currentUser.scope_department || 'ALL';
                    const btn = document.getElementById('btn-manage-admins');
                    if (btn) btn.classList.add('hidden');
                }

                loginContainer.classList.add('hidden');
                appContainer.classList.remove('hidden');
                appContainer.classList.add('flex');

                document.getElementById('nav-user-name').textContent = currentUser.name;
                document.getElementById('nav-user-role').textContent = currentUser.role === 'Super Admin' ? 'Super Admin' : (currentUser.role === 'Admin' ? 'Admin' : currentUser.id);

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
            let html = `<button onclick="switchTab('home')" id="nav-home" class="nav-btn w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all text-left"><i class="fa-solid fa-house w-5 text-center"></i> หน้าแรก</button>`;
            html += `<button onclick="switchTab('training')" id="nav-training" class="nav-btn w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all text-left"><i class="fa-solid fa-book w-5 text-center"></i> Training Need</button>`;

            const hasSubs = getSubordinates(currentUser.id).length > 0;
            html += `<button onclick="switchTab('evaluation')" id="nav-evaluation" class="nav-btn w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all text-left"><i class="fa-solid fa-clipboard-check w-5 text-center"></i> การประเมิน</button>`;

            html += `<button onclick="switchTab('dashboard')" id="nav-dashboard" class="nav-btn w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all text-left"><i class="fa-solid fa-chart-pie w-5 text-center"></i> Dashboard</button>`;
            html += `<button onclick="switchTab('idp')" id="nav-idp" class="nav-btn w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all text-left"><i class="fa-solid fa-address-card w-5 text-center"></i> IDP</button>`;
            if (currentUser.role === 'Admin' || currentUser.role === 'Super Admin' || currentUser.id === 'Admin') {
                html += `<button onclick="switchTab('analytic')" id="nav-analytic" class="nav-btn w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all text-left"><i class="fa-solid fa-chart-line w-5 text-center"></i> Competency Analytic</button>`;
                html += `<button onclick="switchTab('tracking')" id="nav-tracking" class="nav-btn w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all text-left"><i class="fa-solid fa-list-check w-5 text-center"></i> ติดตามการประเมิน</button>`;
                html += `<button onclick="switchTab('employee-data')" id="nav-employee-data" class="nav-btn w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all text-left"><i class="fa-solid fa-users w-5 text-center"></i> Employee Data</button>`;
                html += `<button onclick="switchTab('admin')" id="nav-admin" class="nav-btn w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold border border-scg-200 shadow-sm transition-all text-left mt-2"><i class="fa-solid fa-gear w-5 text-center"></i> Admin</button>`;
            }
            navContainer.innerHTML = html;
        }

        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
            document.getElementById(`tab-${tabId}`).classList.add('active');

            const tabsWithFilters = ['training', 'evaluation', 'dashboard', 'idp', 'analytic', 'admin', 'tracking'];
            const globalFilters = document.getElementById('global-filters-container');
            const compContainer = document.getElementById('global-competency-container');
            if (globalFilters) {
                if (tabsWithFilters.includes(tabId)) {
                    globalFilters.classList.remove('hidden');
                } else {
                    globalFilters.classList.add('hidden');
                }
            }
            if (compContainer) {
                if (tabId === 'admin') {
                    compContainer.classList.add('hidden');
                } else {
                    compContainer.classList.remove('hidden');
                }
            }

            // Rebuild filters based on tab context (admin vs others)
            buildFiltersUI(tabId);

            document.querySelectorAll('.nav-btn').forEach(btn => {
                btn.classList.remove('bg-scg-800', 'text-white', 'shadow-md', 'text-scg-700', 'bg-scg-50');
                btn.classList.add('text-slate-600', 'hover:bg-scg-50');
            });
            const activeBtn = document.getElementById(`nav-${tabId}`);
            if (activeBtn) {
                activeBtn.classList.add('bg-scg-800', 'text-white', 'shadow-md');
                activeBtn.classList.remove('text-slate-600', 'hover:bg-scg-50');
            }

            if (tabId === 'training') {
                const toggleContainer = document.getElementById('admin-edit-toggle-container');
                if (currentUser.id === 'Admin') toggleContainer.classList.remove('hidden');
                else toggleContainer.classList.add('hidden');

                isEditMode = false;
                updateEditModeButton();
                buildFiltersUI();
                buildRoleResponseSection();
                buildTrainingMatrix();
            }
            if (tabId === 'evaluation') setupEvaluationTab();
            if (tabId === 'dashboard') setupDashboardTab();
            if (tabId === 'idp') setupIDPTab();
            if (tabId === 'analytic') {
                renderAnalyticTab();
            }
            if (tabId === 'admin') setupAdminTab();
            if (tabId === 'tracking') renderTrackingTable();
            if (tabId === 'employee-data') renderEmployeeDataTab();
        }

        function toggleEditMode() {
            isEditMode = !isEditMode;
            updateEditModeButton();
            buildRoleResponseSection();
            buildTrainingMatrix();
        }

        function updateEditModeButton() {
            const btn = document.getElementById('edit-mode-btn');
            if (!btn) return;
            if (isEditMode) {
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
            if (userId === 'Admin') {
                const allPos = new Set(positions);
                employeeDataAll.forEach(e => {
                    const p = e.position_name || e.PositionNameThai;
                    if (p) allPos.add(p);
                });
                return Array.from(allPos);
            }
            let visible = new Set();
            if (dbUsers[userId] && dbUsers[userId].position) visible.add(dbUsers[userId].position);
            getSubordinates(userId).forEach(subId => {
                if (dbUsers[subId] && dbUsers[subId].position) visible.add(dbUsers[subId].position);
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
            if (oldName === newName || !newName) return;

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
            if (!newName) return;

            await fetch(`${API_BASE}/competencies/name`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ index, name: newName })
            });
            competencies[index].name = newName;
            showToast("เปลี่ยนชื่อ Competency สำเร็จ");
            buildTrainingMatrix();
        }
        async function deleteCompetency(index) {
            if (confirm("คุณต้องการลบทักษะนี้ใช่หรือไม่? ข้อมูลที่ถูกลบจะหายไปจากทุกตำแหน่งที่อ้างอิงถึงทักษะนี้")) {
                const compId = competencies[index].id;
                
                await fetch(`${API_BASE}/competencies/${index}`, {
                    method: 'DELETE'
                });
                
                competencies.splice(index, 1);
                for (const pos in positionTargets) {
                    if (positionTargets[pos][compId] !== undefined) {
                        delete positionTargets[pos][compId];
                    }
                }
                buildTrainingMatrix();
                showToast("ลบ Competency สำเร็จ");
            }
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


        window.toggleFilterMenu = function (menuId) { const allMenus = document.querySelectorAll('.filter-menu'); let found = false; allMenus.forEach(el => { if (el.id === menuId) { el.classList.toggle('hidden'); found = true; } else { el.classList.add('hidden'); } }); if (!found) { const target = document.getElementById(menuId); if (target) { target.classList.toggle('hidden'); } } };

        // Close dropdowns when clicking outside
        document.addEventListener('click', function (e) {
            if (!e.target.closest('.relative.z-20') && !e.target.closest('.filter-dropdown-container')) {
                const menus = ['job-group-menu', 'pos-dropdown-menu', 'section-dropdown-menu', 'department-dropdown-menu', 'report-to-menu', 'employee-menu', 'comp-group-menu', 'comp-dropdown-menu', 'idp-pos-menu', 'idp-emp-menu', 'dash-job-group-menu', 'dash-pos-menu', 'analytic-job-group-menu', 'analytic-pos-menu', 'analytic-emp-menu', 'analytic-group-menu', 'analytic-skill-menu'];
                menus.forEach(m => {
                    const el = document.getElementById(m);
                    if (el) el.classList.add('hidden');
                });
            }
        });


        function matchesFiltersExcept(e, ignoreFilter) {
            let eReportTo = e.report_to_name || e.ReportToName;
            if (ignoreFilter !== 'reportTo' && selectedReportToFilter.length > 0 && (!eReportTo || !selectedReportToFilter.includes(eReportTo))) return false;
            let eDept = e.department || e.DepartmentThai;
            if (ignoreFilter !== 'department' && selectedDepartmentFilter.length > 0 && (!eDept || !selectedDepartmentFilter.includes(eDept))) return false;
            let eSect = e.section || e.SectionThai;
            if (ignoreFilter !== 'section' && selectedSectionFilter.length > 0 && (!eSect || !selectedSectionFilter.includes(eSect))) return false;

            let posName = e.PositionNameThai || e.position_name;
            if (ignoreFilter !== 'competency' && !hasCompetencyFilterMatch(posName)) return false;
            if (ignoreFilter !== 'position' && selectedPositionsFilter.length > 0 && (!posName || !selectedPositionsFilter.includes(posName))) return false;

            if (ignoreFilter !== 'employee' && selectedEmployeeFilter.length > 0) {
                let empName = e.FullNameTH || e.FullName || e.EmployeeNameThai || e.EmployeeNameEng;
                if (!empName || !selectedEmployeeFilter.includes(empName)) return false;
            }
            if (ignoreFilter !== 'jobGroup' && selectedJobGroupFilter.length > 0) {
                let jg = e.JobGroup || positionGroups[posName] || e.job_group;
                if (!jg || !selectedJobGroupFilter.includes(jg)) return false;
            }
            return true;
        }

        function buildFiltersUI(tabId = null) {
            if (!tabId) {
                const activeTab = document.querySelector('.tab-content.active');
                tabId = activeTab ? activeTab.id.replace('tab-', '') : 'dashboard';
            }
            const jobGroupContainer = document.getElementById('job-group-filters');
            const posContainer = document.getElementById('position-filters');
            const sectionContainer = document.getElementById('section-filters');
            const departmentContainer = document.getElementById('department-filters');
            const reportToContainer = document.getElementById('report-to-filters');
            const compGroupContainer = document.getElementById('comp-group-filters');
            const compContainer = document.getElementById('competency-filters');
            const employeeContainer = document.getElementById('employee-filters');
            if (!posContainer || !compContainer) return;

            const visiblePos = getVisiblePositions(currentUser.id);

            // Build Org Filters AND Position Filter with Hierarchy/Intersection
            let jobGroupsSet = new Set(), sectionsSet = new Set(), deptsSet = new Set(), reportToSet = new Set(), posSet = new Set(), employeesSet = new Set();

            const dataSource = (tabId === 'admin') ? employeeDataAll : employeeData;

            dataSource.forEach(e => {
                let posName = e.position_name || e.PositionNameThai;
                if (!posName) return;

                const isVisible = visiblePos.some(p => p.includes(posName) || posName.includes(p));
                if (!isVisible) return;

                if ((e.section || e.SectionThai) && matchesFiltersExcept(e, 'section')) sectionsSet.add(e.section || e.SectionThai);
                if ((e.department || e.DepartmentThai) && matchesFiltersExcept(e, 'department')) deptsSet.add(e.department || e.DepartmentThai);
                if ((e.report_to_name || e.ReportToName) && matchesFiltersExcept(e, 'reportTo')) reportToSet.add(e.report_to_name || e.ReportToName);
                if (posName && matchesFiltersExcept(e, 'position')) posSet.add(posName);

                let empName = e.FullNameTH || e.FullName || e.EmployeeNameThai || e.EmployeeNameEng;
                if (empName && matchesFiltersExcept(e, 'employee')) employeesSet.add(empName);

                let jg = e.JobGroup || positionGroups[posName] || e.job_group;
                if (jg && matchesFiltersExcept(e, 'jobGroup')) jobGroupsSet.add(jg);
            });

            const buildFilterHtml = (items, selectedArr, filterType) => {
                let html = `
                <div class="p-2 border-b border-slate-100 flex gap-2 bg-slate-50 sticky top-0 z-10">
                    <button class="text-xs text-scg-600 font-medium hover:underline flex-1 text-left" onclick="window.setAllFilter('${filterType}', true)">Select All</button>
                    <button class="text-xs text-slate-500 hover:underline flex-1 text-right" onclick="window.setAllFilter('${filterType}', false)">Clear</button>
                </div>
                <div class="p-2 border-b border-slate-100 sticky top-[36px] z-10 bg-white">
                    <input type="text" class="w-full text-xs px-2 py-1.5 border border-slate-200 rounded search-filter focus:outline-none focus:ring-1 focus:ring-scg-500" placeholder="Search..." onkeyup="window.searchFilterList(this)">
                </div>
                <div class="filter-item-list p-1">
                `;
                Array.from(items).sort().forEach(item => {
                    if (!item) return;
                    const isSelected = selectedArr.includes(item);
                    html += `<label class="filter-item flex items-center gap-3 px-3 py-2 hover:bg-slate-50 rounded-lg cursor-pointer transition-colors w-full">
                        <input type="checkbox" class="form-checkbox h-4 w-4 text-scg-600 rounded border-slate-300" ${isSelected ? 'checked' : ''} onchange="window.toggleFilterValue('${filterType}', '${item}')">
                        <span class="text-sm font-medium ${isSelected ? 'text-scg-700' : 'text-slate-600'} item-text">${item}</span>
                    </label>`;
                });
                html += `</div>`;
                return html;
            };

            if (jobGroupContainer) jobGroupContainer.innerHTML = buildFilterHtml(jobGroupsSet, selectedJobGroupFilter, 'jobGroup');
            if (posContainer) posContainer.innerHTML = buildFilterHtml(posSet, selectedPositionsFilter, 'position');
            if (sectionContainer) sectionContainer.innerHTML = buildFilterHtml(sectionsSet, selectedSectionFilter, 'section');
            if (departmentContainer) departmentContainer.innerHTML = buildFilterHtml(deptsSet, selectedDepartmentFilter, 'department');
            if (reportToContainer) reportToContainer.innerHTML = buildFilterHtml(reportToSet, selectedReportToFilter, 'reportTo');
            if (employeeContainer) employeeContainer.innerHTML = buildFilterHtml(employeesSet, selectedEmployeeFilter, 'employee');

            // Build Competency Groups
            let compGroupsSet = new Set();
            competencies.forEach(c => {
                if (c.group) compGroupsSet.add(c.group);
            });
            let compGroups = Array.from(compGroupsSet).sort();

            if (compGroupContainer) {
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

            const compGroupText = document.getElementById('comp-group-dropdown-text');
            if (compGroupText) {
                if (selectedCompetencyGroupFilter.length === 0) compGroupText.textContent = 'เลือก Competency Group ทั้งหมด';
                else compGroupText.textContent = `เลือกแล้ว ${selectedCompetencyGroupFilter.length} กลุ่ม`;
            }

            const compFilterContainer = document.getElementById('competency-filters');
            let filteredComps = competencies;
            if (selectedCompetencyGroupFilter.length > 0) {
                filteredComps = competencies.filter(c => selectedCompetencyGroupFilter.includes(c.group));
            }
            if (compFilterContainer) {
                let compHtml = '';
                filteredComps.forEach(c => {
                    const isSelected = selectedCompetenciesFilter.includes(c.name);
                    compHtml += `<label class="flex items-center gap-3 px-3 py-2 hover:bg-slate-50 rounded-lg cursor-pointer transition-colors w-full">
                        <input type="checkbox" class="form-checkbox h-4 w-4 text-scg-600 rounded border-slate-300" ${isSelected ? 'checked' : ''} onchange="toggleCompFilter('${c.name}')">
                        <span class="text-sm font-medium ${isSelected ? 'text-scg-700' : 'text-slate-600'}">${c.name}</span>
                    </label>`;
                });
                compFilterContainer.innerHTML = compHtml;
            }

            const compText = document.getElementById('comp-dropdown-text');
            if (compText) {
                if (selectedCompetenciesFilter.length === 0) compText.textContent = 'เลือก Competency ทั้งหมด';
                else compText.textContent = `เลือกแล้ว ${selectedCompetenciesFilter.length} รายการ`;
            }

            // Update texts
            const updateText = (id, arr, defaultText) => {
                const el = document.getElementById(id);
                if (el) {
                    if (arr.length === 0) el.textContent = defaultText;
                    else el.textContent = `เลือกแล้ว ${arr.length} รายการ`;
                }
            };
            updateText('job-group-dropdown-text', selectedJobGroupFilter, 'เลือกกลุ่มงานทั้งหมด');
            updateText('position-dropdown-text', selectedPositionsFilter, 'เลือกตำแหน่งทั้งหมด');
            updateText('section-dropdown-text', selectedSectionFilter, 'เลือก Section ทั้งหมด');
            updateText('department-dropdown-text', selectedDepartmentFilter, 'เลือก Department ทั้งหมด');
            updateText('report-to-dropdown-text', selectedReportToFilter, 'เลือกหัวหน้างานทั้งหมด');
            updateText('employee-dropdown-text', selectedEmployeeFilter, 'เลือกพนักงานทั้งหมด');
        }



        function hasCompetencyFilterMatch(posName) {
            if (selectedCompetencyGroupFilter.length === 0 && selectedCompetenciesFilter.length === 0) return true;
            if (!posName || !positionTargets[posName]) return false;

            let filteredComps = competencies;
            if (selectedCompetencyGroupFilter.length > 0) {
                filteredComps = filteredComps.filter(c => selectedCompetencyGroupFilter.includes(c.group));
            }
            if (selectedCompetenciesFilter.length > 0) {
                filteredComps = filteredComps.filter(c => selectedCompetenciesFilter.includes(c.name));
            }

            const indices = filteredComps.map(c => competencies.findIndex(x => x.id === c.id));
            const targets = positionTargets[posName];

            for (let idx of indices) {
                if (targets[idx] && targets[idx] > 0) return true;
            }
            return false;
        }

        function matchesOrgFiltersData(eData) {
            if (!eData) return true;
            let posName = eData.PositionNameThai || eData.position_name || eData.position;
            if (!hasCompetencyFilterMatch(posName)) return false;
            let jg = eData.JobGroup || positionGroups[posName] || eData.job_group;
            if (selectedJobGroupFilter.length > 0 && !selectedJobGroupFilter.includes(jg)) return false;
            if (selectedPositionsFilter.length > 0 && (!posName || !selectedPositionsFilter.includes(posName))) return false;

            if (selectedEmployeeFilter.length > 0) {
                let empName = eData.FullNameTH || eData.FullName || eData.EmployeeNameThai || eData.EmployeeNameEng;
                if (!empName || !selectedEmployeeFilter.includes(empName)) return false;
            }

            if (selectedSectionFilter.length > 0 && !selectedSectionFilter.includes(eData.SectionThai)) return false;
            if (selectedDepartmentFilter.length > 0 && !selectedDepartmentFilter.includes(eData.DepartmentThai)) return false;
            if (selectedReportToFilter.length > 0 && !selectedReportToFilter.includes(eData.ReportToName)) return false;

            return true;
        }

        function isEmployeeMatchingOrgFilters(empId) {
            let emp = dbUsers[empId];
            if (!emp) return false;

            let eData = employeeData.find(e => e.username === empId || e.user_id === empId || e.EmployeeNameEng === emp.name || e.EmployeeNameThai === emp.name || e.FullNameTH === emp.name);

            if (!eData) {
                let empName = emp.name;
                if (selectedEmployeeFilter.length > 0 && (!empName || !selectedEmployeeFilter.includes(empName))) return false;
                if (selectedSectionFilter.length > 0 || selectedDepartmentFilter.length > 0 || selectedReportToFilter.length > 0) return false;
                return true;
            }
            return matchesOrgFiltersData(eData);
        }


        function applyGlobalFiltersToSubIds(subIds) {
            return subIds.filter(id => isEmployeeMatchingOrgFilters(id));
        }


        function renderActiveTab() {
            const activeTab = document.querySelector('.tab-content.active');
            if (!activeTab) return;
            const id = activeTab.id.replace('tab-', '');
            if (id === 'training') {
                buildRoleResponseSection();
                buildTrainingMatrix();
            }
            if (id === 'evaluation') setupEvaluationTab();
            if (id === 'dashboard') setupDashboardTab();
            if (id === 'idp') renderIDPContent();
            if (id === 'analytic') renderAnalyticTab();
            if (id === 'admin') renderAdminTable();
            if (id === 'tracking') renderTrackingTable();
        }


        window.toggleFilterValue = function (type, v) {
            let arr;
            if (type === 'jobGroup') arr = selectedJobGroupFilter;
            else if (type === 'position') arr = selectedPositionsFilter;
            else if (type === 'section') arr = selectedSectionFilter;
            else if (type === 'department') arr = selectedDepartmentFilter;
            else if (type === 'reportTo') arr = selectedReportToFilter;
            else if (type === 'employee') arr = selectedEmployeeFilter;

            if (arr) {
                const idx = arr.indexOf(v);
                if (idx > -1) arr.splice(idx, 1);
                else arr.push(v);
            }
            buildFiltersUI(); renderActiveTab();
        }


        window.clearAllFilters = function () {
            selectedJobGroupFilter = [];
            selectedPositionsFilter = [];
            selectedSectionFilter = [];
            selectedDepartmentFilter = [];
            selectedReportToFilter = [];
            selectedEmployeeFilter = [];

            selectedCompetencyGroupFilter = [];
            selectedCompetenciesFilter = [];

            buildFiltersUI();
            renderActiveTab();
        };

        window.setAllFilter = function (type, isSelectAll) {
            let arr;
            let containerId;
            if (type === 'jobGroup') { arr = selectedJobGroupFilter; containerId = 'job-group-filters'; }
            else if (type === 'position') { arr = selectedPositionsFilter; containerId = 'position-filters'; }
            else if (type === 'section') { arr = selectedSectionFilter; containerId = 'section-filters'; }
            else if (type === 'department') { arr = selectedDepartmentFilter; containerId = 'department-filters'; }
            else if (type === 'reportTo') { arr = selectedReportToFilter; containerId = 'report-to-filters'; }
            else if (type === 'employee') { arr = selectedEmployeeFilter; containerId = 'employee-filters'; }

            if (arr && containerId) {
                arr.length = 0; // Clear it
                if (isSelectAll) {
                    const container = document.getElementById(containerId);
                    if (container) {
                        container.querySelectorAll('.item-text').forEach(span => {
                            if (span.closest('.filter-item').style.display !== 'none') {
                                arr.push(span.innerText);
                            }
                        });
                    }
                }
            }
            buildFiltersUI(); renderActiveTab();
        }

        window.searchFilterList = function (input) {
            const q = input.value.toLowerCase();
            const list = input.closest('div').nextElementSibling;
            list.querySelectorAll('.filter-item').forEach(label => {
                const text = label.querySelector('.item-text').innerText.toLowerCase();
                label.style.display = text.includes(q) ? 'flex' : 'none';
            });
        }

        window.toggleCompGroupFilter = function (g) {
            if (selectedCompetencyGroupFilter.includes(g)) selectedCompetencyGroupFilter = selectedCompetencyGroupFilter.filter(x => x !== g);
            else selectedCompetencyGroupFilter.push(g);
            buildFiltersUI();
            renderActiveTab();
        }

        window.toggleCompFilter = function (c) {
            if (selectedCompetenciesFilter.includes(c)) selectedCompetenciesFilter = selectedCompetenciesFilter.filter(x => x !== c);
            else selectedCompetenciesFilter.push(c);
            buildFiltersUI();
            renderActiveTab();
        }

        function buildRoleResponseSection() {
            const container = document.getElementById('role-response-container');

            let visiblePosSet = new Set();
            employeeData.forEach(e => {
                if (matchesFiltersExcept(e, null)) {
                    let posName = e.PositionNameThai || e.position_name;
                    if (posName) visiblePosSet.add(posName);
                }
            });
            let visiblePos = Array.from(visiblePosSet).filter(p => p).sort();

            const isAdmin = currentUser.id === 'Admin';
            const subs = getSubordinates(currentUser.id);

            if (!isAdmin) {
                let allowedPos = new Set();
                let myEmpData = dbUsers[currentUser.id];
                if (myEmpData && myEmpData.position) {
                    allowedPos.add(myEmpData.position);
                }
                subs.forEach(subId => {
                    let subEmpData = dbUsers[subId];
                    if (subEmpData && subEmpData.position) {
                        allowedPos.add(subEmpData.position);
                    }
                });
                visiblePos = visiblePos.filter(p => allowedPos.has(p));
            }

            let html = '<div class="flex flex-col gap-3">';
            if (visiblePos.length === 0) {
                html += '<p class="text-slate-400 text-sm py-4">ไม่พบตำแหน่งที่ตรงกับเงื่อนไข</p>';
            }

            visiblePos.forEach(pos => {
                const response = roleResponses[pos] || "ยังไม่ระบุหน้าที่ความรับผิดชอบ...";
                const group = positionGroups[pos] || '-';

                if (isAdmin && isEditMode) {
                    html += `
                    <div class="bg-white p-4 rounded-xl border border-amber-200 bg-amber-50/10 hover:shadow-md transition-shadow">
                        <div class="flex flex-col md:flex-row items-start gap-4">
                            <div class="flex items-center gap-3 md:w-1/3">
                                <div class="w-10 h-10 rounded-full bg-amber-100 text-amber-600 flex items-center justify-center shrink-0">
                                    <i class="fa-solid fa-user-gear"></i>
                                </div>
                                <div class="w-full">
                                    <input type="text" value="${pos}" onchange="handlePositionChange('${pos}', this.value)" class="w-full font-bold text-scg-900 text-sm mb-1 border-b border-amber-300 bg-transparent px-1 py-1 focus:border-scg-600 outline-none" title="แก้ไขชื่อตำแหน่ง">
                                </div>
                            </div>
                            <div class="md:w-2/3 flex w-full gap-2">
                                <textarea rows="2" onchange="handleRoleResponseChange('${pos}', this.value)" class="w-full text-xs text-slate-600 p-2 border border-slate-200 rounded outline-none focus:border-amber-500 resize-none bg-white">${response}</textarea>
                                <button onclick="deletePosition('${pos}')" class="text-red-400 hover:text-white hover:bg-red-500 p-2 rounded-lg transition-colors border border-red-100 flex-shrink-0" title="ลบตำแหน่งนี้"><i class="fa-solid fa-trash"></i></button>
                            </div>
                        </div>
                    </div>`;
                } else {
                    html += `
                    <div class="bg-white p-4 rounded-xl border border-slate-100 flex flex-col md:flex-row items-start md:items-center gap-4 hover:shadow-md transition-all">
                        <div class="flex items-center gap-3 md:w-1/3 shrink-0">
                            <div class="w-10 h-10 rounded-full bg-scg-50 text-scg-500 flex items-center justify-center shrink-0">
                                <i class="fa-solid fa-briefcase"></i>
                            </div>
                            <div>
                                <h4 class="font-bold text-scg-900 text-sm">${pos}</h4>
                            </div>
                        </div>
                        <div class="md:w-2/3 w-full">
                            <p class="text-xs text-slate-500 leading-relaxed bg-slate-50 p-3 rounded-lg border border-slate-50 min-h-[40px] whitespace-pre-wrap">${response}</p>
                        </div>
                    </div>`;
                }
            });
            html += '</div>';

            if (isAdmin && isEditMode) {
                html += `
                <div onclick="addNewPosition()" class="mt-4 bg-slate-50 border-2 border-dashed border-slate-300 rounded-xl flex flex-col items-center justify-center p-4 cursor-pointer hover:border-scg-400 hover:bg-scg-50 transition-colors group">
                    <div class="w-8 h-8 rounded-full bg-white shadow-sm flex items-center justify-center mb-2 group-hover:scale-110 transition-transform"><i class="fa-solid fa-plus text-scg-500 text-sm"></i></div>
                    <span class="text-xs font-bold text-slate-500 group-hover:text-scg-700">เพิ่มตำแหน่งใหม่</span>
                </div>`;
            }
            container.innerHTML = html;
        }

        function buildTrainingMatrix() {
            const container = document.getElementById('training-matrix-container');

            let visiblePosSet = new Set();
            employeeData.forEach(e => {
                if (matchesFiltersExcept(e, null)) {
                    let posName = e.PositionNameThai || e.position_name;
                    if (posName) visiblePosSet.add(posName);
                }
            });
            let visiblePos = Array.from(visiblePosSet).filter(p => p).sort();

            const isAdmin = currentUser.id === 'Admin';
            const subs = getSubordinates(currentUser.id);

            if (!isAdmin) {
                let allowedPos = new Set();
                let myEmpData = dbUsers[currentUser.id];
                if (myEmpData && myEmpData.position) {
                    allowedPos.add(myEmpData.position);
                }
                subs.forEach(subId => {
                    let subEmpData = dbUsers[subId];
                    if (subEmpData && subEmpData.position) {
                        allowedPos.add(subEmpData.position);
                    }
                });
                visiblePos = visiblePos.filter(p => allowedPos.has(p));
            }

            let html = `<div class="overflow-x-auto w-full"><table class="w-full text-left border-collapse text-sm"><thead><tr class="bg-slate-50 border-b border-slate-100 text-slate-600"><th class="p-4 font-semibold min-w-[200px] w-1/4">Competency</th>`;

            visiblePos.forEach(pos => {
                if (isAdmin && isEditMode) {
                    html += `<th class="p-4 font-semibold text-center align-top min-w-[150px] whitespace-nowrap bg-amber-50/30 border-l border-white">
                                <input type="text" value="${pos}" onchange="handlePositionChange('${pos}', this.value)" class="w-full border-b border-scg-300 bg-transparent px-1 py-1 text-sm font-bold text-scg-900 focus:border-scg-600 outline-none text-center" title="แก้ไขชื่อตำแหน่ง">
                             </th>`;
                } else {
                    html += `<th class="p-4 font-semibold text-center align-top whitespace-pre-wrap min-w-[120px] border-l border-white">${pos}</th>`;
                }
            });
            html += `<th class="w-full"></th></tr></thead><tbody class="divide-y divide-slate-100 text-slate-700">`;

            competencies.forEach((comp, compIndex) => {
                if (selectedCompetencyGroupFilter.length > 0 && !selectedCompetencyGroupFilter.includes(comp.group)) return;
                if (selectedCompetenciesFilter.length > 0 && !selectedCompetenciesFilter.includes(comp.name)) return;

                // Removed hasTarget check to always display all competencies

                html += `<tr class="hover:bg-slate-50">`;

                if (isAdmin && isEditMode) {
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
                                    <div class="flex gap-1">
                                        <button onclick="openLevelEditModal(${compIndex})" class="text-xs bg-white hover:bg-slate-100 text-scg-700 px-2 py-1.5 rounded border border-slate-200 w-full flex items-center justify-center gap-1 shadow-sm transition-colors">
                                            <i class="fa-solid fa-list-ol"></i> แก้ไขความหมาย Level
                                        </button>
                                        <button onclick="deleteCompetency(${compIndex})" class="text-xs bg-red-50 hover:bg-red-100 text-red-600 px-2.5 py-1.5 rounded border border-red-200 flex items-center justify-center shadow-sm transition-colors" title="ลบทักษะนี้">
                                            <i class="fa-solid fa-trash"></i>
                                        </button>
                                    </div>
                                </div>
                             </td>`;
                } else {
                    html += `<td class="p-4 font-medium"><i class="fa-solid ${comp.icon} text-scg-400 w-6"></i> ${comp.name}</td>`;
                }

                visiblePos.forEach(pos => {
                    const t = positionTargets[pos] && positionTargets[pos][compIndex] ? positionTargets[pos][compIndex] : 0;
                    
                    if (isAdmin) {
                        let selectHtml = `<select onchange="updateMatrixTarget('${pos}', ${compIndex}, this)" class="border border-slate-200 rounded px-2 py-1.5 font-bold outline-none focus:border-scg-500 text-xs w-full max-w-[140px] bg-white cursor-pointer ${t >= 4 ? 'text-scg-800' : 'text-slate-600'} ${isEditMode ? 'border-amber-200' : ''}">`;
                        selectHtml += `<option value="0" ${t === 0 ? 'selected' : ''}>None</option>`;
                        for (let i = 1; i <= 5; i++) {
                            const desc = comp.levels[i] || "";
                            selectHtml += `<option value="${i}" ${t === i ? 'selected' : ''}>L${i}: ${desc}</option>`;
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
                                            ${levelText}${t > 0 ? ': ' + desc : ''}
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

            html += `</tbody></table></div>`;
            container.innerHTML = html;
        }

        async function updateMatrixTarget(pos, compIndex, selectEl) {
            const val = parseInt(selectEl.value);
            if (!positionTargets[pos]) positionTargets[pos] = {};
            positionTargets[pos][compIndex] = val;

            await fetch(`${API_BASE}/positions/target`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ position: pos, compIndex, value: val })
            });

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
            for (let i = 1; i <= 5; i++) {
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
            if (currentEditCompIndex === -1) return;
            const comp = competencies[currentEditCompIndex];

            const levels = {};
            for (let i = 1; i <= 5; i++) {
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
                for (let id in dbUsers) {
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

                function toggleEvalViewMode(mode) {
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
        
        function applyAdminOverride() {
            actingAsRole = document.getElementById('admin-override-select').value;
            populateEvalDropdown();
        }

        function populateEvalDropdown() {
            const selectEl = document.getElementById('eval-employee-select');
            const prevVal = selectEl.value;
            selectEl.innerHTML = '';

            let validEmps = [];
            let actingName = dbUsers[actingAsRole] ? dbUsers[actingAsRole].name : '';

            employeeData.forEach(e => {
                let empName = e.FullNameTH || e.FullName || e.EmployeeNameThai || e.EmployeeNameEng;
                let pName = e.PositionNameThai || e.position_name;
                let uid = e.user_id || e.username || e.SCGEmployeeID || empName;

                if (matchesFiltersExcept(e, null)) {
                    let isSub = false;
                    if (actingAsRole === 'Admin') {
                        isSub = true;
                    } else {
                        let mName = e.ManagerName || e.ReportToName || '';
                        if (actingName && mName.includes(actingName)) isSub = true;
                        if (!isSub && getSubordinates(actingAsRole).includes(uid)) isSub = true;
                        if (uid === actingAsRole) isSub = true; // Add self to list
                    }

                    if (isSub && empName) {
                        validEmps.push({ id: uid, name: empName, position: pName || 'Unassigned', raw: e });
                    }
                }
            });

            if (validEmps.length === 0) {
                selectEl.innerHTML = '<option value="">-- ไม่พบผู้ใต้บังคับบัญชา --</option>';
                document.getElementById('sliders-container').innerHTML = '<div class="text-center text-slate-400 py-10">ไม่พบข้อมูล หรือ ยังไม่ได้เริ่มประเมิน</div>';
                if (evalRadarChartInstance) evalRadarChartInstance.destroy();
                return;
            }

            // Remove duplicates by ID
            let uniqueEmps = [];
            let seenIds = new Set();
            validEmps.forEach(emp => {
                if (!seenIds.has(emp.id)) {
                    seenIds.add(emp.id);
                    uniqueEmps.push(emp);
                }
            });

            uniqueEmps.forEach(emp => {
                selectEl.innerHTML += `<option value="${emp.id}">${emp.name} (${emp.position})</option>`;
            });

            if (prevVal && Array.from(selectEl.options).some(o => o.value === prevVal)) {
                selectEl.value = prevVal;
            }

            updateEvalUI();
        }

        function updateEvalUI() {
            const id = document.getElementById('eval-employee-select').value;
            if (!id) return;
            if (!dbUsers[id]) {
                const rawEData = employeeData.find(e => e.user_id === id || e.username === id || e.SCGEmployeeID === id || (e.FullNameTH || e.FullName || e.EmployeeNameThai || e.EmployeeNameEng) === id);
                if (rawEData) {
                    const empName = rawEData.FullNameTH || rawEData.FullName || rawEData.EmployeeNameThai || rawEData.EmployeeNameEng;
                    const pName = rawEData.PositionNameThai || rawEData.position_name || 'Unassigned';
                    dbUsers[id] = {
                        name: empName,
                        position: pName,
                        actuals: [],
                        before_evals: [],
                        evidences: [],
                        additional_expectations: [],
                        learning_topics: [],
                        managerIds: []
                    };
                    // Auto create in backend
                    fetch(`${API_BASE}/users`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ uid: id, pass: 'Pass@1234', name: empName, pos: pName, mgrs: [], num_comps: competencies.length })
                    }).catch(e => console.error(e));
                }
            }

            const emp = dbUsers[id];
            const eData = employeeData.find(e => e.user_id === id || e.username === id || e.EmployeeNameEng === emp.name || e.EmployeeNameThai === emp.name || e.FullNameTH === emp.name);
            let pName = emp.position;
            if (eData && eData.PositionNameThai) pName = eData.PositionNameThai;
            else if (eData && eData.position_name) pName = eData.position_name;

            const targets = positionTargets[pName] || [];
            const hasMappedCompetency = targets.some(t => t > 0);

            if (!hasMappedCompetency) {
                document.getElementById('sliders-container').innerHTML = `<div class="text-center py-16 bg-slate-50 rounded-xl border border-slate-200 shadow-sm mt-4">
                    <i class="fa-solid fa-link-slash text-4xl text-amber-300 mb-4 block"></i>
                    <p class="text-slate-600 font-bold text-lg">กรุณาผูก Competency ในตำแหน่งนี้ ก่อน</p>
                    <p class="text-slate-400 text-sm mt-2">ผู้ดูแลระบบ (Admin) ต้องกำหนดความคาดหวังทักษะสำหรับตำแหน่ง "${pName}" ในหน้า Training Need ก่อนทำการประเมิน</p>
                </div>`;
                if (evalRadarChartInstance) evalRadarChartInstance.destroy();
                return;
            }
            const currentLabels = getLabels();

            document.getElementById('eval-emp-name').textContent = emp.name;
            document.getElementById('eval-emp-position').textContent = emp.position;

            const evalTitle = document.querySelector('#tab-evaluation h2');
            if (evalTitle) {
                if (currentUser.id === id) {
                    evalTitle.textContent = 'ประเมินตนเอง';
                } else {
                    evalTitle.textContent = 'ประเมินผลผู้ใต้บังคับบัญชา';
                }
            }

            let html = '';
            for (let i = 0; i < competencies.length; i++) {
                if (selectedCompetencyGroupFilter.length > 0 && !selectedCompetencyGroupFilter.includes(competencies[i].group)) continue;
                if (selectedCompetenciesFilter.length > 0 && !selectedCompetenciesFilter.includes(competencies[i].name)) continue;

                const targetVal = targets[i] || 0;
                if (targetVal === 0) continue;

                const targetText = targetVal === 0 ? 'None' : `L${targetVal}`;
                const currentVal = (emp.actuals[i] || 0) === 0 ? 1 : emp.actuals[i];
                const currentDesc = competencies[i].levels[currentVal] || "";
                
                const selfEvalVal = (emp.self_evals && emp.self_evals[i] !== undefined) ? emp.self_evals[i] : currentVal;
                const selfDesc = competencies[i].levels[selfEvalVal] || "";
                const supervisorFeedback = (emp.supervisor_feedback && emp.supervisor_feedback[i]) ? emp.supervisor_feedback[i] : '';

                html += `
                <div class="bg-white p-6 rounded-2xl border border-slate-200 mb-6 shadow-sm">
                    <div class="flex justify-between items-center mb-4">
                        <label class="font-bold text-lg text-slate-800">${currentLabels[i]}</label>
                        <span class="text-xs font-medium text-slate-500 bg-slate-50 px-3 py-1.5 rounded-lg border border-slate-200">เป้าหมายตำแหน่ง: <strong class="text-scg-800 text-sm ml-1">${targetText}</strong></span>
                    </div>
                `;

                if (currentUser.id === id) {
                    // Self Evaluation Mode
                    let statText = '';
                    if (emp.eval_status === 'Approved') statText = '<span class="text-green-600 font-bold ml-3 text-sm"><i class="fa-solid fa-circle-check"></i> Approved</span>';
                    else if (emp.eval_status === 'Waiting for Approval') statText = '<span class="text-amber-500 font-bold ml-3 text-sm"><i class="fa-solid fa-clock"></i> Waiting for Approval</span>';
                    
                    html += `
                    <div class="mb-4">
                        <label class="block text-sm font-bold text-blue-700 mb-2">ประเมินตนเอง (Self-Evaluation) ${statText}</label>
                        <div class="flex items-center gap-4 mb-2">
                            <input type="range" id="eval-self-${id}-${i}" min="1" max="5" value="${selfEvalVal}" 
                                class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-blue-600" 
                                oninput="updateEvalSliderDisplay(${i}, this.value, 'self')">
                            <div id="disp-self-${i}" class="w-12 h-12 flex items-center justify-center bg-blue-600 text-white font-black text-xl rounded-xl shadow-inner shrink-0">${selfEvalVal}</div>
                        </div>
                        <div class="bg-blue-50/50 p-3.5 rounded-xl border border-blue-100 text-sm flex items-start gap-3">
                            <span id="badge-self-${i}" class="font-bold text-blue-700 bg-blue-100 px-2.5 py-1 rounded-md shrink-0 border border-blue-200">Level ${selfEvalVal}</span>
                            <span id="desc-self-${i}" class="text-slate-600 leading-relaxed mt-0.5">${selfDesc}</span>
                        </div>
                    </div>`;
                    

                } else {
                    // Supervisor Mode
                    html += `
                    <div class="bg-blue-50/30 p-4 rounded-xl border border-blue-100 mb-6 flex justify-between items-center">
                        <div>
                            <span class="block text-xs font-bold text-blue-700 mb-1">พนักงานประเมินตนเอง:</span>
                            <span class="text-sm text-slate-600">${selfDesc}</span>
                        </div>
                        <div class="w-10 h-10 flex items-center justify-center bg-blue-100 text-blue-700 font-black text-lg rounded-lg shadow-inner shrink-0">${selfEvalVal}</div>
                    </div>
                    
                    const beforeVal = (emp.before_evals && emp.before_evals[i]) ? emp.before_evals[i] : 1;
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
                    </div>`;`;
                }

                html += `
                    <div class="pt-4 border-t border-slate-200 border-dashed mt-4">
                        <label class="block text-xs font-bold text-slate-500 mb-2"><i class="fa-regular fa-folder-open text-scg-500 w-5 text-center"></i> หลักฐานอ้างอิง (Evidence)</label>
                        <textarea id="eval-evi-${i}" rows="2" class="w-full text-sm p-3 border border-slate-200 rounded-xl outline-none focus:border-scg-500 focus:ring-1 focus:ring-scg-500 resize-none transition-colors" placeholder="ระบุพฤติกรรมหรือผลงานที่สนับสนุนคะแนนนี้...">${emp.evidences[i] || ''}</textarea>
                    </div>
                    
                    <div class="pt-4 mt-2 border-t border-slate-200 border-dashed grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-xs font-bold text-slate-500 mb-2"><i class="fa-solid fa-bullseye text-scg-500 w-5 text-center"></i> ความคาดหวังเพิ่มเติม</label>
                            <textarea id="eval-add-exp-${i}" rows="2" class="w-full text-sm p-3 border border-slate-200 rounded-xl outline-none focus:border-scg-500 focus:ring-1 focus:ring-scg-500 resize-none transition-colors" placeholder="สิ่งที่คาดหวังให้พัฒนาเพิ่มเติม...">${(emp.additional_expectations && emp.additional_expectations[i]) || ''}</textarea>
                        </div>
                        <div>
                            <label class="block text-xs font-bold text-slate-500 mb-2"><i class="fa-solid fa-book-open text-scg-500 w-5 text-center"></i> หัวข้อที่อยากให้เรียนรู้เพิ่มเติม</label>
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

        function updateEvalSliderDisplay(index, val, type) {
            const idPrefix = type === 'self' ? 'self-' : (type === 'actual' ? 'actual-' : '');
            
            const id = document.getElementById('eval-employee-select').value;
            
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
            drawEvalRadar();
        }

        function drawEvalRadar() {
            const id = document.getElementById('eval-employee-select').value;
            if (!dbUsers[id]) {
                const rawEData = employeeData.find(e => e.user_id === id || e.username === id || e.SCGEmployeeID === id || (e.FullNameTH || e.FullName || e.EmployeeNameThai || e.EmployeeNameEng) === id);
                if (rawEData) {
                    const empName = rawEData.FullNameTH || rawEData.FullName || rawEData.EmployeeNameThai || rawEData.EmployeeNameEng;
                    const pName = rawEData.PositionNameThai || rawEData.position_name || 'Unassigned';
                    dbUsers[id] = {
                        name: empName,
                        position: pName,
                        actuals: [],
                        before_evals: [],
                        evidences: [],
                        additional_expectations: [],
                        learning_topics: [],
                        managerIds: []
                    };
                    // Auto create in backend
                    fetch(`${API_BASE}/users`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ uid: id, pass: 'Pass@1234', name: empName, pos: pName, mgrs: [], num_comps: competencies.length })
                    }).catch(e => console.error(e));
                }
            }

            const emp = dbUsers[id];
            const eData = employeeData.find(e => e.user_id === id || e.username === id || e.EmployeeNameEng === emp.name || e.EmployeeNameThai === emp.name || e.FullNameTH === emp.name);
            let pName = emp.position;
            if (eData && eData.PositionNameThai) pName = eData.PositionNameThai;
            else if (eData && eData.position_name) pName = eData.position_name;

            const targets = positionTargets[pName] || [];
            const hasMappedCompetency = targets.some(t => t > 0);

            if (!hasMappedCompetency) {
                document.getElementById('sliders-container').innerHTML = `<div class="text-center py-16 bg-slate-50 rounded-xl border border-slate-200 shadow-sm mt-4">
                    <i class="fa-solid fa-link-slash text-4xl text-amber-300 mb-4 block"></i>
                    <p class="text-slate-600 font-bold text-lg">กรุณาผูก Competency ในตำแหน่งนี้ ก่อน</p>
                    <p class="text-slate-400 text-sm mt-2">ผู้ดูแลระบบ (Admin) ต้องกำหนดความคาดหวังทักษะสำหรับตำแหน่ง "${pName}" ในหน้า Training Need ก่อนทำการประเมิน</p>
                </div>`;
                if (evalRadarChartInstance) evalRadarChartInstance.destroy();
                return;
            }
            let actuals = [];
            let cleanLabels = [];
            let cleanTargets = [];
            let selfEvals = [];
            let beforeEvals = [];

            const allLabels = getLabels().map(l => {
                const parts = l.split('. ');
                return parts.length > 1 ? parts.slice(1).join('. ') : l;
            });

            for (let i = 0; i < competencies.length; i++) {
                if (selectedCompetencyGroupFilter.length > 0 && !selectedCompetencyGroupFilter.includes(competencies[i].group)) continue;
                if (selectedCompetenciesFilter.length > 0 && !selectedCompetenciesFilter.includes(competencies[i].name)) continue;

                const t = targets[i] || 0;
                if (t === 0) continue;

                cleanLabels.push(allLabels[i]);
                cleanTargets.push(t);

                const elActual = document.getElementById(`eval-actual-${id}-${i}`);
                actuals.push(elActual ? parseInt(elActual.value) : (emp.actuals[i] || 0));

                const elSelf = document.getElementById(`eval-self-${id}-${i}`);
                let defaultSelf = emp.self_evals ? (emp.self_evals[i] || 0) : 0;
                selfEvals.push(elSelf ? parseInt(elSelf.value) : defaultSelf);
                
                const elBefore = document.getElementById(`eval-before-${id}-${i}`);
                let defaultBefore = emp.before_evals ? (emp.before_evals[i] || 0) : 0;
                beforeEvals.push(elBefore ? parseInt(elBefore.value) : defaultBefore);
            }

            if (evalRadarChartInstance) evalRadarChartInstance.destroy();
            const ctx = document.getElementById('evalRadarChart').getContext('2d');

                        let activeDatasets = [];
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
                },
                options: { responsive: true, maintainAspectRatio: false, scales: { r: { min: 0, max: 5, ticks: { display: false } } } }
            });
        }

        async function saveEvaluation() {
            const id = document.getElementById('eval-employee-select').value;
            const emp = dbUsers[id];

            if (!emp.additional_expectations) emp.additional_expectations = new Array(competencies.length).fill('');
            if (!emp.learning_topics) emp.learning_topics = new Array(competencies.length).fill('');

            for (let i = 0; i < competencies.length; i++) {
                // Grab self eval if exists
                const elSelf = document.getElementById(`eval-self-${id}-${i}`);
                if (elSelf) {
                    if (!emp.self_evals) emp.self_evals = [];
                    emp.self_evals[i] = parseInt(elSelf.value);
                }

                // Grab actual eval if exists
                const elActual = document.getElementById(`eval-actual-${id}-${i}`);
                if (elActual) {
                    emp.actuals[i] = parseInt(elActual.value);
                }

                // Grab feedback if exists
                const elFeedback = document.getElementById(`eval-feedback-${id}-${i}`);
                if (elFeedback) {
                    if (!emp.supervisor_feedback) emp.supervisor_feedback = [];
                    emp.supervisor_feedback[i] = elFeedback.value;
                }

                const elEvi = document.getElementById(`eval-evi-${i}`);
                const elAddExp = document.getElementById(`eval-add-exp-${i}`);
                const elLrnTop = document.getElementById(`eval-lrn-top-${i}`);

                if (elEvi) emp.evidences[i] = elEvi.value;
                if (elAddExp) emp.additional_expectations[i] = elAddExp.value;
                if (elLrnTop) emp.learning_topics[i] = elLrnTop.value;
            }

            // Update evaluation status
            if (currentUser.id === id) {
                emp.eval_status = 'Waiting for Approval';
            } else {
                emp.eval_status = 'Approved';
            }

            const specExp = document.getElementById('eval-spec-exp') ? document.getElementById('eval-spec-exp').value : '';
            const specDtl = document.getElementById('eval-spec-dtl') ? document.getElementById('eval-spec-dtl').value : '';

            emp.special_expertise = specExp;
            emp.special_expertise_detail = specDtl;
            
            let datesObj = { self: '', mgr: '' };
            try {
                if (emp.evalDate && emp.evalDate.startsWith('{')) {
                    datesObj = JSON.parse(emp.evalDate);
                }
            } catch (e) {}

            const todayStr = new Date().toLocaleDateString('th-TH');
            if (currentUser.id === id) {
                datesObj.self = todayStr;
            } else {
                datesObj.mgr = todayStr;
            }
            emp.evalDate = JSON.stringify(datesObj);

            await fetch(`${API_BASE}/evaluations`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    userId: id,
                    actuals: emp.actuals,
                    selfEvals: emp.self_evals,
                    supervisorFeedbacks: emp.supervisor_feedback,
                    evidences: emp.evidences,
                    additionalExpectations: emp.additional_expectations,
                    learningTopics: emp.learning_topics,
                    specialExpertise: emp.special_expertise,
                    specialExpertiseDetail: emp.special_expertise_detail,
                    evalDate: emp.evalDate,
                    evalStatus: emp.eval_status
                })
            });

            showToast("บันทึกประเมินสำเร็จ");
            setTimeout(() => { switchTab('dashboard'); }, 1000);
        }

        // --- 5. Dashboard Logic ---
        function setupDashboardTab() {

            const currentUserId = currentUser.id;
            const mySubs = getSubordinates(currentUserId);
            let toShow = [];

            if (currentUserId === 'Admin') {
                toShow = applyGlobalFiltersToSubIds(Object.keys(dbUsers).filter(id => id !== 'Admin'));
                document.getElementById('dash-manager-view').style.display = 'block';
            } else if (mySubs.length === 0) {
                toShow = applyGlobalFiltersToSubIds([currentUserId]);
                document.getElementById('dash-manager-view').style.display = 'none';
            } else {
                toShow = applyGlobalFiltersToSubIds(mySubs);
                document.getElementById('dash-manager-view').style.display = 'block';
            }


            if (toShow.length === 0) {
                document.getElementById('dash-individual-cards-container').innerHTML = '<div class="text-center bg-white p-10 rounded-3xl border border-slate-100 text-slate-400">ไม่พบข้อมูลให้แสดงผล</div>';
                if (averageBarChartInstance) averageBarChartInstance.destroy();
                return;
            }

            if (mySubs.length > 0 || currentUserId === 'Admin') {
                drawAverageBarChart(toShow);
            }
            renderIndividualDashboards(toShow);
            renderTeamHeatmap(toShow);
        }



        function drawAverageBarChart(subIds) {
            const dataToSort = [];

            subIds.forEach(id => {
                const emp = dbUsers[id];
                const targets = positionTargets[emp.position] || [];

                let sumTarget = 0;
                let sumActual = 0;
                let sumSelf = 0;
                let validCompsCount = 0;

                for (let i = 0; i < competencies.length; i++) {
                    if (selectedCompetencyGroupFilter.length > 0 && !selectedCompetencyGroupFilter.includes(competencies[i].group)) continue;
                    if (selectedCompetenciesFilter.length > 0 && !selectedCompetenciesFilter.includes(competencies[i].name)) continue;

                    const t = targets[i] || 0;
                    if (t === 0) continue;
                    if (t > 0) {
                        sumTarget += t;
                        sumActual += (emp.actuals[i] || 0);
                        sumSelf += emp.self_evals ? (emp.self_evals[i] || 0) : 0;
                        validCompsCount++;
                    }
                }

                const avgT = validCompsCount > 0 ? sumTarget / validCompsCount : 0;
                const avgA = validCompsCount > 0 ? sumActual / validCompsCount : 0;
                const avgS = validCompsCount > 0 ? sumSelf / validCompsCount : 0;

                // Calculate % Complete
                const percent = sumTarget > 0 ? Math.round((sumActual / sumTarget) * 100) : 0;

                dataToSort.push({
                    name: emp.name,
                    avgT: avgT.toFixed(1),
                    avgA: avgA.toFixed(1),
                    avgS: avgS.toFixed(1),
                    percent: percent
                });
            });

            // เรียงลำดับจาก % Completed มากไปน้อย
            dataToSort.sort((a, b) => b.percent - a.percent);

            const names = dataToSort.map(d => d.name);
            const avgTargets = dataToSort.map(d => d.avgT);
            const avgActuals = dataToSort.map(d => d.avgA);
            const avgSelfs = dataToSort.map(d => d.avgS);
            const percentCompletes = dataToSort.map(d => d.percent);

            // คำนวณ max ของกราฟเส้นเผื่อไว้ 20% ของค่า max เพื่อไม่ให้ตัวหนังสือตกขอบ
            const maxPercentVal = Math.max(...percentCompletes, 100);
            const y1Max = Math.ceil(maxPercentVal + (maxPercentVal * 0.2));

            if (averageBarChartInstance) averageBarChartInstance.destroy();
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
                        { label: 'Average Expected', data: avgTargets, backgroundColor: '#cbd5e1', yAxisID: 'y', borderRadius: 6 },
                        { label: 'Average Actual', data: avgActuals, backgroundColor: '#ca3656', yAxisID: 'y', borderRadius: 6 }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            grid: { display: false }
                        },
                        y: { min: 0, max: 5, position: 'left', grid: { display: false } },
                        y1: {
                            min: 0,
                            max: y1Max,
                            position: 'right',
                            grid: { drawOnChartArea: false, display: false },
                            ticks: { callback: function (value) { return value + '%'; } }
                        }
                    },
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: function (context) {
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

                        // Dataset 1 is the Average Expected
                        chart.getDatasetMeta(1).data.forEach((datapoint, index) => {
                            const value = data.datasets[1].data[index];
                            if (value > 0) {
                                ctx.fillStyle = '#64748b'; // slate-500
                                ctx.font = 'bold 11px sans-serif';
                                ctx.textAlign = 'center';
                                ctx.textBaseline = 'bottom';
                                ctx.fillText(value, datapoint.x, datapoint.y - 5);
                            }
                        });

                        // Dataset 2 is the Average Actual
                        chart.getDatasetMeta(2).data.forEach((datapoint, index) => {
                            const value = data.datasets[2].data[index];
                            if (value > 0) {
                                ctx.fillStyle = '#9f1239'; // rose-900
                                ctx.font = 'bold 11px sans-serif';
                                ctx.textAlign = 'center';
                                ctx.textBaseline = 'bottom';
                                ctx.fillText(value, datapoint.x, datapoint.y - 5);
                            }
                        });

                        ctx.restore();
                    }
                }]
            });
        }

        window.renderTeamHeatmap = function(subIds) {
            const container = document.getElementById('dashboard-heatmap-container');
            if (!container) return;
            
            if (subIds.length === 0) {
                container.classList.add('hidden');
                return;
            }
            container.classList.remove('hidden');

            let html = '<div class="flex justify-between items-start mb-4">';
            html += '<h3 class="text-lg font-bold text-scg-800">Team Skill Matrix</h3>';
            html += '<button onclick="exportTeamSkillMatrix()" class="bg-emerald-600 hover:bg-emerald-700 text-white px-3 py-1.5 rounded-lg text-xs font-bold flex items-center gap-2 transition-colors shrink-0"><i class="fa-solid fa-file-excel"></i> Export Excel</button>';
            html += '</div>';
            html += '<div class="overflow-x-auto pb-4">';
            html += '<div class="overflow-x-auto w-full"><table class="w-full text-left border-collapse min-w-[800px]">';
            html += '<thead><tr class="bg-slate-50 text-slate-600 text-xs uppercase tracking-wider">';
            html += '<th class="p-3 border-b border-slate-200 sticky left-0 bg-slate-50 z-10 w-48">Employee</th>';
            
            // Get visible competencies
            let activeComps = [];
            for (let i = 0; i < competencies.length; i++) {
                if (selectedCompetencyGroupFilter.length > 0 && !selectedCompetencyGroupFilter.includes(competencies[i].group)) continue;
                if (selectedCompetenciesFilter.length > 0 && !selectedCompetenciesFilter.includes(competencies[i].name)) continue;
                activeComps.push({ index: i, name: competencies[i].name });
            }
            
            activeComps.forEach(comp => {
                html += `<th class="p-3 border-b border-slate-200 align-top min-w-[140px] whitespace-normal leading-relaxed" title="${comp.name}">${comp.name}</th>`;
            });
            html += '</tr></thead><tbody>';

            subIds.forEach(id => {
                const emp = dbUsers[id];
                const targets = positionTargets[emp.position] || [];
                
                html += `<tr class="border-b border-slate-100 hover:bg-slate-50">`;
                html += `<td class="p-3 sticky left-0 bg-white group-hover:bg-slate-50 z-10 font-medium text-sm text-slate-800 shadow-[1px_0_0_0_#f1f5f9] truncate" title="${emp.name}">${emp.name}</td>`;
                
                activeComps.forEach(comp => {
                    const t = targets[comp.index] || 0;
                    const a = emp.actuals[comp.index] || 0;
                    
                    let bgClass = "bg-slate-50";
                    let textClass = "text-slate-400";
                    let content = "-";
                    
                    if (t > 0) {
                        const diff = a - t;
                        if (diff >= 0) {
                            bgClass = "bg-green-100";
                            textClass = "text-green-700 font-bold";
                            content = a;
                        } else if (diff === -1) {
                            bgClass = "bg-yellow-100";
                            textClass = "text-yellow-700 font-bold";
                            content = a;
                        } else {
                            bgClass = "bg-red-100";
                            textClass = "text-red-700 font-bold";
                            content = a;
                        }
                    }
                    
                    html += `<td class="p-2 border-r border-slate-50 text-center"><div class="w-8 h-8 flex items-center justify-center rounded mx-auto ${bgClass} ${textClass} text-xs" title="Target: ${t}, Actual: ${a}">${content}</div></td>`;
                });
                
                html += `</tr>`;
            });

            html += '</tbody></table></div>';
            container.innerHTML = html;
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

                for (let i = 0; i < competencies.length; i++) {
                    if (selectedCompetencyGroupFilter.length > 0 && !selectedCompetencyGroupFilter.includes(competencies[i].group)) continue;
                    if (selectedCompetenciesFilter.length > 0 && !selectedCompetenciesFilter.includes(competencies[i].name)) continue;

                    const t = targets[i] || 0;
                    if (t === 0) continue;
                    if (t > 0) {
                        const a = emp.actuals[i] || 0;
                        totalTarget += t;
                        totalActual += a;
                        let diff = a - t;
                        if (diff < 0) gaps.push({ skill: currentLabels[i], gap: diff, index: i });
                    }
                }

                const readiness = totalTarget === 0 ? 0 : Math.round((totalActual / totalTarget) * 100);
                const safeReadiness = readiness;
                let readinessColor = safeReadiness >= 100 ? "text-green-400" : (safeReadiness >= 80 ? "text-yellow-400" : "text-red-400");
                const gapText = gaps.length === 0 ? "พร้อมสมบูรณ์ (ไม่มี Gap)" : `พบ ${gaps.length} ทักษะที่ต้องพัฒนา`;

                let recsHtml = '';
                if (gaps.length === 0) {
                    recsHtml = `<div class="bg-green-50 p-3 rounded-xl border border-green-100 flex items-start gap-3"><i class="fa-solid fa-medal text-green-500 mt-0.5"></i><div><p class="text-sm font-bold text-green-800">ทักษะผ่านเกณฑ์ทั้งหมด</p></div></div>`;
                } else {
                    gaps.forEach(gap => {
                        let courseName = "หลักสูตรพัฒนาทักษะ (OJT)"; let icon = "fa-book";
                        if (gap.skill.includes("ไฟฟ้า")) { courseName = "เทคนิคตู้ MDB และมอเตอร์ 3 เฟส"; icon = "fa-bolt"; }
                        else if (gap.skill.includes("เครื่องกล")) { courseName = "ซ่อมบำรุงปั๊มน้ำและระบบนิวเมติกส์"; icon = "fa-gear"; }
                        else if (gap.skill.includes("วิเคราะห์")) { courseName = "การอ่านแบบ Schematic Diagram"; icon = "fa-magnifying-glass-chart"; }
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
                const sData = emp.self_evals || [];

                const cleanLabels = [];
                const cleanTargets = [];
                const cleanActuals = [];
                const cleanSelfs = [];

                for (let i = 0; i < currentLabels.length; i++) {
                    if (selectedCompetencyGroupFilter.length > 0 && !selectedCompetencyGroupFilter.includes(competencies[i].group)) continue;
                    if (selectedCompetenciesFilter.length > 0 && !selectedCompetenciesFilter.includes(competencies[i].name)) continue;

                    if (tData[i] && tData[i] > 0) {
                        const parts = currentLabels[i].split('. ');
                        cleanLabels.push(parts.length > 1 ? parts.slice(1).join('. ') : currentLabels[i]);
                        cleanTargets.push(tData[i]);
                        cleanActuals.push(aData[i] || 0);
                        cleanSelfs.push(sData[i] || 0);
                    }
                }

                const chart = new Chart(ctx, {
                    type: 'radar',
                    data: {
                        labels: cleanLabels,
                        datasets: [
                            { label: 'Target', data: cleanTargets, borderColor: '#94a3b8', backgroundColor: 'rgba(148, 163, 184, 0.2)' },
                            { label: 'Actual', data: cleanActuals, borderColor: '#882239', backgroundColor: 'rgba(136, 34, 57, 0.3)' },
                            { label: 'Self Eva.', data: cleanSelfs, borderColor: '#fbbf24', backgroundColor: 'rgba(251, 191, 36, 0.2)' }
                        ]
                    },
                    options: { responsive: true, maintainAspectRatio: false, scales: { r: { min: 0, max: 5, ticks: { display: false } } } }
                });
                individualCharts.push(chart);
            });
        }

        // --- 6. Admin Panel Export & Management ---

        function setupAdminTab() {
            let filteredEmployeeDataAll = employeeDataAll;
            if (currentUser && currentUser.role === 'Admin') {
                if (currentUser.scope_department && currentUser.scope_department !== 'ALL') {
                    filteredEmployeeDataAll = filteredEmployeeDataAll.filter(e => e.DepartmentThai === currentUser.scope_department || e.department === currentUser.scope_department);
                }
                if (currentUser.scope_section && currentUser.scope_section !== 'ALL') {
                    filteredEmployeeDataAll = filteredEmployeeDataAll.filter(e => e.SectionThai === currentUser.scope_section || e.section === currentUser.scope_section);
                }
                if (currentUser.scope_division && Array.isArray(currentUser.scope_division) && currentUser.scope_division.length > 0) {
                    filteredEmployeeDataAll = filteredEmployeeDataAll.filter(e => currentUser.scope_division.includes(e.DivisionThai) || currentUser.scope_division.includes(e.division));
                }
            }

            adminTempData = filteredEmployeeDataAll.map(e => {
                let n_en = e.name_en;
                if (!n_en) {
                    n_en = e.FullNameENG;
                    if (!n_en) {
                        const first = e.FirstNameEnglish;
                        if (first) {
                            const prefix = e.NamePrefixEnglish || '';
                            const last = e.LastNameEnglish || '';
                            n_en = (prefix ? prefix + ' ' : '') + first + ' ' + last;
                        } else {
                            n_en = '';
                        }
                    }
                }

                return {
                    pk_field: e.PersonID ? 'PersonID' : (e.id ? 'id' : 'person_id'),
                    pk_value: e.PersonID || e.id || e.person_id,
                    person_id: e.PersonnelNumber || e.PersonID || e.person_id || '-',
                    name_th: e.FullNameTH || e.name_th || e.FullName || '-',
                    name_en: n_en ? n_en.trim() : '-',
                    user_id: e.user_id || e.username || e.USER || '',
                    password: e.password || '',
                    report_to_name: e.ReportToName || e.report_to_name || '',
                    is_evaluated: e.Pipeline === 'Evaluated',
                    position: e.PositionNameThai || e.position_name || '',
                    position_level: e.PositionStructureLevel || e.position_level || '',
                    job_group: e.JobGroup || e.job_group || '',
                    section: e.SectionThai || e.section || '',
                    department: e.DepartmentThai || e.department || '',
                    sub1_division: e.Sub1DivisionThai || e.sub1_division || '',
                    division: e.DivisionThai || e.division || '',
                    sub1_company: e.Sub1CompanyThai || e.sub1_company || '',
                    company: e.CompanyThai || e.company || '',
                    certificate: e.Certificate || e.certificate || ''
                };
            });
            renderAdminTable();
        }

        function renderAdminTable() {
            const tbody = document.getElementById('admin-tbody');
            if (!tbody) return;

            const search = document.getElementById('admin-search').value.toLowerCase();

            // Build unique Thai names for the dropdown
            const allNames = [...new Set(adminTempData.map(e => e.name_th).filter(n => n && n !== '-'))].sort();
            let optionsHtml = `<option value="">-- ไม่ระบุ --</option>`;
            allNames.forEach(n => {
                optionsHtml += `<option value="${n}">${n}</option>`;
            });

            let html = '';
            let count = 0;

            adminTempData.forEach((emp, index) => {
                const searchStr = `${emp.person_id} ${emp.name_th} ${emp.name_en} ${emp.user_id}`.toLowerCase();
                if (search && !searchStr.includes(search)) return;

                const eData = employeeDataAll[index];
                if (eData && !matchesOrgFiltersData(eData)) return;

                count++;

                let rowOpts = optionsHtml;
                if (emp.report_to_name) {
                    rowOpts = rowOpts.replace(`value="${emp.report_to_name}"`, `value="${emp.report_to_name}" selected`);
                }

                html += `
                    <tr class="hover:bg-slate-50 transition-colors border-b border-slate-100">
                        <td class="py-2 px-4 border-r border-slate-100 text-center">
                            <input type="checkbox" class="w-5 h-5 rounded border-slate-300 text-scg-600 focus:ring-scg-500 cursor-pointer" 
                                   ${emp.is_evaluated ? 'checked' : ''} 
                                   onchange="adminTempData[${index}].is_evaluated = this.checked">
                        </td>
                        <td class="py-2 px-4 border-r border-slate-100 font-medium">${emp.person_id}</td>
                        <td class="py-2 px-4 border-r border-slate-100">${emp.name_th}</td>
                        <td class="py-2 px-4 border-r border-slate-100 text-xs text-slate-500">${emp.position || '-'}</td>
                        <td class="py-2 px-4 border-r border-slate-100">
                            <input type="text" class="px-2 py-1.5 border border-slate-200 rounded-lg w-full text-xs font-bold text-scg-700" 
                                   value="${emp.user_id}" 
                                   onchange="adminTempData[${index}].user_id = this.value">
                        </td>
                        <td class="py-2 px-4 border-r border-slate-100">
                            <input type="text" class="px-2 py-1.5 border border-slate-200 rounded-lg w-full text-xs" 
                                   value="${emp.password}" 
                                   onchange="adminTempData[${index}].password = this.value">
                        </td>
                        <td class="py-2 px-4 border-r border-slate-100">
                            <select class="px-2 py-1.5 border border-slate-200 rounded-lg w-full text-xs bg-white cursor-pointer" 
                                    onchange="adminTempData[${index}].report_to_name = this.value">
                                ${rowOpts}
                            </select>
                        </td>
                        <td class="py-2 px-4 text-center">
                            <div class="flex items-center gap-2 justify-center">
                                <button onclick="openEditEmployeeModal(${index})" class="text-amber-500 hover:text-amber-700 transition-colors" title="แก้ไขข้อมูล">
                                    <i class="fa-solid fa-pen-to-square"></i>
                                </button>
                                <button onclick="deleteAdminRow(${index})" class="text-red-500 hover:text-red-700 transition-colors" title="ลบพนักงาน">
                                    <i class="fa-solid fa-trash-can"></i>
                                </button>
                            </div>
                        </td>
                    </tr>
                `;
            });

            tbody.innerHTML = html;
            document.getElementById('admin-count-info').innerText = `แสดง ${count} รายการ`;
        }


        function toggleAdminSelectAll(cb) {
            const search = document.getElementById('admin-search').value.toLowerCase();
            adminTempData.forEach((emp, index) => {
                const searchStr = `${emp.person_id} ${emp.name_th} ${emp.name_en} ${emp.user_id}`.toLowerCase();
                if (search && !searchStr.includes(search)) return;

                const eData = employeeDataAll[index];
                if (eData && !matchesOrgFiltersData(eData)) return;

                emp.is_evaluated = cb.checked;
            });
            renderAdminTable();
        }


        async function saveAdminData() {
            const btn = document.querySelector('button[onclick="saveAdminData()"]');
            const oldHtml = btn.innerHTML;
            btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> กำลังบันทึก...`;
            btn.disabled = true;

            try {
                const response = await fetch(API_BASE + '/admin/sync_employees', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ employees: adminTempData, deleted_ids: deletedEmployeeIds })
                });

                const result = await response.json();
                if (result.status === 'success') {
                    alert('บันทึกข้อมูลและอัปเดตสิทธิการเข้าถึงเรียบร้อยแล้ว!');
                    deletedEmployeeIds = [];
                    await fetchInitialData(true);
                    setupAdminTab();
                } else {
                    alert('Error: ' + result.message);
                }
            } catch (err) {
                console.error(err);
                alert('Failed to save data. Check console.');
            } finally {
                btn.innerHTML = oldHtml;
                btn.disabled = false;
            }
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
            let csvContent = "\ufeff";
            csvContent += "ชื่อพนักงาน,ตำแหน่ง,ผู้บังคับบัญชา,Competency,Skill level ที่คาดหวัง,skill Level ที่ประเมินจริง,คำอธิบาย Evidence ที่ผู้บังคับบัญชาใส่,วันที่ประเมิน,ความหมาย skill level ที่คาดหวัง,ความหมาย skill level ที่ประเมินจริง\n";
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
                    if (selectedCompetencyGroupFilter.length > 0 && !selectedCompetencyGroupFilter.includes(competencies[i].group)) continue;
                    if (selectedCompetenciesFilter.length > 0 && !selectedCompetenciesFilter.includes(competencies[i].name)) continue;

                    const targetVal = targets[i] || 0;
                    if (targetVal === 0) continue;
                    const actualVal = emp.actuals[i] || 0;

                    const targetDesc = targetVal === 0 ? "ไม่มีเป้าหมายที่คาดหวัง" : (competencies[i].levels[targetVal] || "-");
                    const actualDesc = actualVal === 0 ? "-" : (competencies[i].levels[actualVal] || "-");

                    const row = [
                        `"${emp.name}"`, `"${emp.position}"`, `"${mgrNames}"`,
                        `"${currentLabels[i]}"`, targetVal, actualVal,
                        `"${emp.evidences[i] || '-'}"`, `"${emp.evalDate || 'ยังไม่ถูกประเมิน'}"`,
                        `"${targetDesc}"`, `"${actualDesc}"`
                    ];
                    csvContent += row.join(",") + "\n";
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

        // --- IDP Logic ---
        function setupIDPTab() {
            renderIDPContent();
        }

        function buildIDPFilters() {
            const posContainer = document.getElementById('idp-pos-filters');
            const empContainer = document.getElementById('idp-emp-filters');
            if (!posContainer || !empContainer) return;

            // Allowable positions and employees based on access
            let visibleUsers = [];
            if (currentUser.id === 'Admin') {
                visibleUsers = applyGlobalFiltersToSubIds(Object.keys(dbUsers).filter(uid => uid !== 'Admin'));
            } else {
                visibleUsers = applyGlobalFiltersToSubIds([currentUser.id, ...getSubordinates(currentUser.id)]);
            }

            let posSet = new Set();
            let emps = [];

            visibleUsers.forEach(uid => {
                const emp = dbUsers[uid];
                const eData = employeeData.find(e => e.user_id === uid || e.username === uid || e.EmployeeNameEng === (emp ? emp.name : '') || e.EmployeeNameThai === (emp ? emp.name : ''));
                if (emp) {
                    let pName = emp.position;
                    if (eData && eData.PositionNameThai) pName = eData.PositionNameThai;
                    else if (eData && eData.position_name) pName = eData.position_name;

                    if (pName) posSet.add(pName);
                    emps.push({ id: uid, name: emp.name, position: pName });
                }
            });

            let posList = Array.from(posSet).sort();

            let posHtml = `<label class="flex items-center gap-3 px-3 py-2 hover:bg-slate-50 rounded-lg cursor-pointer transition-colors w-full">
                    <input type="radio" name="idp-pos-radio" class="form-radio h-4 w-4 text-scg-600 border-slate-300" ${!selectedIDPPos ? 'checked' : ''} onchange="toggleIDPPosFilter('')">
                    <span class="text-sm font-medium ${!selectedIDPPos ? 'text-scg-700' : 'text-slate-600'}">-- แสดงทุกตำแหน่ง --</span>
                </label>`;

            posList.forEach(p => {
                const isSelected = selectedIDPPos === p;
                posHtml += `<label class="flex items-center gap-3 px-3 py-2 hover:bg-slate-50 rounded-lg cursor-pointer transition-colors w-full">
                    <input type="radio" name="idp-pos-radio" class="form-radio h-4 w-4 text-scg-600 border-slate-300" ${isSelected ? 'checked' : ''} onchange="toggleIDPPosFilter('${p}')">
                    <span class="text-sm font-medium ${isSelected ? 'text-scg-700' : 'text-slate-600'}">${p}</span>
                </label>`;
            });
            posContainer.innerHTML = posHtml;

            let filteredEmps = emps;
            if (selectedIDPPos) {
                filteredEmps = emps.filter(e => e.position === selectedIDPPos);
                // Auto clear employee if they don't match the position
                if (selectedIDPEmp && !filteredEmps.find(e => e.id === selectedIDPEmp)) {
                    selectedIDPEmp = null;
                }
            }

            let empHtml = '';
            filteredEmps.forEach(e => {
                const isSelected = selectedIDPEmp === e.id;
                empHtml += `<label class="flex items-center gap-3 px-3 py-2 hover:bg-slate-50 rounded-lg cursor-pointer transition-colors w-full">
                    <input type="radio" name="idp-emp-radio" class="form-radio h-4 w-4 text-scg-600 border-slate-300" ${isSelected ? 'checked' : ''} onchange="toggleIDPEmpFilter('${e.id}')">
                    <span class="text-sm font-medium ${isSelected ? 'text-scg-700' : 'text-slate-600'}">${e.name}</span>
                </label>`;
            });
            empContainer.innerHTML = empHtml;

            // Texts
            const posText = document.getElementById('idp-pos-text');
            posText.textContent = selectedIDPPos ? selectedIDPPos : 'เลือกตำแหน่ง';

            const empText = document.getElementById('idp-emp-text');
            const selectedEmpData = emps.find(e => e.id === selectedIDPEmp);
            empText.textContent = selectedEmpData ? selectedEmpData.name : 'เลือกพนักงาน';
        }

        window.toggleIDPPosFilter = function (p) {
            selectedIDPPos = p;
            renderIDPContent();
        }

        window.toggleIDPEmpFilter = function (uid) {
            selectedIDPEmp = uid;
            renderIDPContent();
        }

        function renderIDPContent() {
            const container = document.getElementById('idp-content-container');
            if (!container) return;

            let visibleUsers = [];
            if (currentUser.id === 'Admin') {
                visibleUsers = applyGlobalFiltersToSubIds(Object.keys(dbUsers).filter(uid => uid !== 'Admin'));
            } else {
                visibleUsers = applyGlobalFiltersToSubIds([currentUser.id, ...getSubordinates(currentUser.id)]);
            }

            if (visibleUsers.length === 0) {
                container.innerHTML = `
                    <div class="bg-white p-10 rounded-2xl border border-slate-100 shadow-sm text-center text-slate-500">
                        <i class="fa-solid fa-users-slash text-4xl mb-3 text-slate-300"></i>
                        <p>ไม่พบพนักงานที่ตรงกับเงื่อนไข</p>
                    </div>`;
                return;
            }

            if (visibleUsers.length > 1) {
                container.innerHTML = `
                    <div class="bg-white p-10 rounded-2xl border border-slate-100 shadow-sm text-center text-slate-500">
                        <i class="fa-solid fa-address-card text-4xl mb-3 text-slate-300"></i>
                        <p>กรุณาเลือกชื่อพนักงาน 1 ท่าน จากตัวกรองด้านบนเพื่อดูแผนพัฒนา (IDP)</p>
                    </div>`;
                return;
            }

            const empId = visibleUsers[0];
            const emp = dbUsers[empId];
            const targets = positionTargets[emp.position] || [];

            let totalTarget = 0;
            let totalActual = 0;

            let compRowsHtml = '';
            let gaps = [];

            const currentLabels = getLabels();

            for (let i = 0; i < competencies.length; i++) {
                if (selectedCompetencyGroupFilter.length > 0 && !selectedCompetencyGroupFilter.includes(competencies[i].group)) continue;
                if (selectedCompetenciesFilter.length > 0 && !selectedCompetenciesFilter.includes(competencies[i].name)) continue;

                const t = targets[i] || 0;
                if (t === 0) continue;
                if (t === 0) continue; // Only process relevant competencies

                const a = emp.actuals[i] || 0;
                totalTarget += t;
                totalActual += Math.min(a, t);

                let diff = a - t;
                if (diff < 0 && t > 0) gaps.push({ skill: currentLabels[i], gap: diff, index: i });

                const addExp = (emp.additional_expectations && emp.additional_expectations[i]) ? emp.additional_expectations[i] : '-';
                const lrnTop = (emp.learning_topics && emp.learning_topics[i]) ? emp.learning_topics[i] : '-';

                compRowsHtml += `
                    <div class="border border-slate-100 rounded-xl p-5 bg-slate-50 shadow-sm mb-4">
                        <div class="flex flex-col md:flex-row items-start md:items-center justify-between mb-3 border-b border-slate-200 pb-3 gap-3">
                            <h4 class="font-bold text-scg-800 text-base"><i class="fa-solid ${competencies[i].icon} mr-2 text-scg-400"></i> ${competencies[i].name}</h4>
                            <div class="flex gap-4 shrink-0">
                                <div class="text-center">
                                    <span class="block text-[10px] text-slate-500 font-bold uppercase tracking-wider">Target</span>
                                    <span class="block font-bold text-scg-700 bg-white px-2 py-1 rounded border border-scg-200 shadow-sm">L${t}</span>
                                </div>
                                <div class="text-center">
                                    <span class="block text-[10px] text-slate-500 font-bold uppercase tracking-wider">Actual</span>
                                    <span class="block font-bold ${a >= t ? 'text-green-600 bg-green-50 border-green-200' : 'text-amber-600 bg-amber-50 border-amber-200'} px-2 py-1 rounded border shadow-sm">L${a}</span>
                                </div>
                            </div>
                        </div>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div class="bg-white p-4 rounded-lg border border-slate-100 shadow-sm">
                                <label class="block text-xs font-bold text-slate-500 mb-2"><i class="fa-solid fa-bullseye text-scg-500 w-5 text-center"></i> ความคาดหวังเพิ่มเติม</label>
                                <p class="text-sm text-slate-700 whitespace-pre-wrap">${addExp}</p>
                            </div>
                            <div class="bg-white p-4 rounded-lg border border-slate-100 shadow-sm">
                                <label class="block text-xs font-bold text-slate-500 mb-2"><i class="fa-solid fa-book-open text-scg-500 w-5 text-center"></i> หัวข้อที่อยากให้เรียนรู้เพิ่มเติม</label>
                                <p class="text-sm text-slate-700 whitespace-pre-wrap">${lrnTop}</p>
                            </div>
                        </div>
                    </div>
                `;
            }

            // Generate Gaps and Recs
            const gapText = gaps.length === 0 ? "พร้อมสมบูรณ์ (ไม่มี Gap)" : `พบ ${gaps.length} ทักษะที่ต้องพัฒนา (GAP)`;
            let recsHtml = '';
            if (gaps.length === 0) {
                recsHtml = `<div class="bg-green-50 p-4 rounded-2xl border border-green-100 flex flex-col items-center justify-center h-full text-center">
                    <i class="fa-solid fa-medal text-4xl text-green-500 mb-3 drop-shadow-md"></i>
                    <p class="text-lg font-bold text-green-800 mb-1">ทักษะผ่านเกณฑ์ทั้งหมด</p>
                    <p class="text-sm text-green-600">พนักงานมีความพร้อม 100% ตามมาตรฐานตำแหน่ง</p>
                </div>`;
            } else {
                gaps.forEach(gap => {
                    let courseName = "หลักสูตรพัฒนาทักษะ (OJT)"; let icon = "fa-book";
                    if (gap.skill.includes("ไฟฟ้า")) { courseName = "เทคนิคตู้ MDB และมอเตอร์ 3 เฟส"; icon = "fa-bolt"; }
                    else if (gap.skill.includes("เครื่องกล")) { courseName = "ซ่อมบำรุงปั๊มน้ำและระบบนิวเมติกส์"; icon = "fa-gear"; }
                    else if (gap.skill.includes("วิเคราะห์")) { courseName = "การอ่านแบบ Schematic Diagram"; icon = "fa-magnifying-glass-chart"; }
                    let idpStatus = (emp.idp_status && emp.idp_status[gap.skill]) ? emp.idp_status[gap.skill] : 'Not Started';
                    let statusColor = idpStatus === 'Completed' ? 'bg-green-100 text-green-700' : (idpStatus === 'In Progress' ? 'bg-yellow-100 text-yellow-700' : 'bg-slate-100 text-slate-600');
                    
                    recsHtml += `
                    <div class="flex items-center justify-between p-3 bg-white border border-red-100 rounded-xl shadow-sm mb-3">
                        <div class="flex items-center gap-3">
                            <div class="bg-red-50 p-3 rounded-lg text-red-500 flex-shrink-0"><i class="fa-solid ${icon} text-lg"></i></div>
                            <div class="flex-grow">
                                <p class="text-xs text-slate-500 font-medium">${gap.skill.replace(/^[0-9\.\s]+/, '')} <span class="text-red-600 font-bold bg-red-50 px-2 py-0.5 rounded-full ml-1 text-[10px]">Gap ${gap.gap}</span></p>
                                <p class="text-sm font-bold text-scg-800 mt-1">${courseName}</p>
                            </div>
                        </div>
                        <div class="flex-shrink-0">
                            <select onchange="updateIDPStatus('${empId}', '${gap.skill}', this.value)" class="text-xs font-bold px-3 py-1.5 rounded-lg border-0 outline-none cursor-pointer ${statusColor}">
                                <option value="Not Started" ${idpStatus === 'Not Started' ? 'selected' : ''} class="bg-white text-slate-700">Not Started</option>
                                <option value="In Progress" ${idpStatus === 'In Progress' ? 'selected' : ''} class="bg-white text-slate-700">In Progress</option>
                                <option value="Completed" ${idpStatus === 'Completed' ? 'selected' : ''} class="bg-white text-slate-700">Completed</option>
                            </select>
                        </div>
                    </div>`;
                });
            }

            // Calculate % Complete (Sum of Actual / Sum of Target) * 100
            let totalActualForPct = 0;
            let totalTargetForPct = 0;
            for (let i = 0; i < competencies.length; i++) {
                if (targets[i] > 0) {
                    totalTargetForPct += targets[i];
                    totalActualForPct += (emp.actuals[i] || 0);
                }
            }
            let pctComplete = totalTargetForPct > 0 ? Math.round((totalActualForPct / totalTargetForPct) * 100) : 0;

            // Generate Special Expertise HTML
            let expertiseHtml = '';
            if (emp.special_expertise && emp.special_expertise !== '-' && emp.special_expertise !== '') {
                let badgeClass = "bg-blue-50 text-blue-600 border-blue-200";
                if (emp.special_expertise === 'Leadership') badgeClass = "bg-purple-50 text-purple-600 border-purple-200";
                else if (emp.special_expertise === 'Digital' || emp.special_expertise === 'AI') badgeClass = "bg-teal-50 text-teal-600 border-teal-200";
                else if (emp.special_expertise === 'Analytic') badgeClass = "bg-orange-50 text-orange-600 border-orange-200";

                expertiseHtml = `
                    <div class="mb-5 pb-5 border-b border-slate-100">
                        <h3 class="font-bold text-sm text-scg-900 mb-3">
                            <i class="fa-solid fa-star text-amber-400 mr-2"></i> ความเชี่ยวชาญพิเศษ
                        </h3>
                        <div class="flex flex-col gap-2">
                            <span class="inline-flex w-max items-center px-2.5 py-1 rounded-md text-xs font-bold border shadow-sm ${badgeClass}">
                                ${emp.special_expertise}
                            </span>
                            <p class="text-xs text-slate-600 leading-relaxed bg-slate-50 p-2.5 rounded-lg border border-slate-100 whitespace-pre-wrap break-all">${emp.special_expertise_detail || '-'}</p>
                        </div>
                    </div>
                `;
            }

            let formattedDate = emp.evalDate || '-';
            if (emp.evalDate && emp.evalDate.startsWith('{')) {
                try {
                    let parsed = JSON.parse(emp.evalDate);
                    formattedDate = parsed.mgr || parsed.self || '-';
                } catch(e) {}
            }

            container.innerHTML = `
                <!-- IDP Header Section -->
                <div class="flex flex-col xl:flex-row gap-6 mb-6">
                    
                    <!-- Left Column: Chart -->
                    <div class="xl:w-2/3 bg-white p-6 md:p-8 rounded-3xl shadow-sm border border-slate-100 flex flex-col items-center justify-center relative">
                        <div class="absolute top-6 left-6 flex items-center gap-4">
                            <div class="w-16 h-16 bg-scg-50 rounded-2xl flex items-center justify-center text-scg-400 text-3xl shadow-inner shrink-0">
                                <i class="fa-solid fa-user-graduate"></i>
                            </div>
                            <div>
                                <h3 class="text-2xl font-bold text-scg-900 mb-1">${emp.name}</h3>
                                <div class="inline-flex items-center bg-slate-100 px-3 py-1 rounded-full text-sm font-medium text-slate-600 border border-slate-200">
                                    <i class="fa-solid fa-briefcase text-scg-500 mr-2"></i> ${emp.position}
                                </div>
                            </div>
                        </div>
                        <div class="absolute top-6 right-6 text-right">
                            <h4 class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">% Completed Skill Level</h4>
                            <div class="text-4xl font-black text-scg-700">${pctComplete}%</div>
                            <div class="text-xs text-slate-400 mt-1">อัปเดต: ${formattedDate}</div>
                        </div>
                        
                        <div class="w-full h-[400px] mt-16 lg:mt-10">
                            <canvas id="idpRadarChart"></canvas>
                        </div>
                    </div>
                    
                    <!-- Right Column: GAP Summary -->
                    <div class="xl:w-1/3 bg-white p-6 md:p-8 rounded-3xl shadow-sm border border-slate-100 flex flex-col">
                        ${expertiseHtml}
                        <h3 class="font-bold text-lg text-scg-900 mb-4 border-b border-slate-100 pb-3">
                            <i class="fa-solid fa-graduation-cap text-scg-500 mr-2"></i> สรุปผลประเมิน & หลักสูตรแนะนำ
                        </h3>
                        <div class="mb-4">
                            <div class="text-sm font-bold ${gaps.length === 0 ? 'text-green-600' : 'text-red-500'} mb-3 bg-slate-50 p-2 rounded-lg text-center border border-slate-100">
                                ${gapText}
                            </div>
                        </div>
                        <div class="flex-grow overflow-y-auto pr-2" style="max-height: 350px;">
                            ${recsHtml}
                        </div>
                    </div>
                </div>
                
                <!-- IDP Details List -->
                <div class="bg-white p-6 md:p-8 rounded-3xl shadow-sm border border-slate-100">
                    <h3 class="font-bold text-lg text-scg-900 mb-6"><i class="fa-solid fa-list-check text-scg-500 mr-2"></i> รายละเอียดการพัฒนาทักษะ (Competency Details)</h3>
                    ${compRowsHtml || '<p class="text-slate-500 text-sm text-center py-4">ไม่พบข้อมูลเป้าหมายทักษะสำหรับตำแหน่งนี้</p>'}
                </div>
            `;

            drawIDPRadar(emp, targets);
        }

        function drawIDPRadar(emp, targets) {
            let actuals = [];
            let selfEvals = [];
            let cleanLabels = [];
            let cleanTargets = [];
            let cleanDescs = [];
            let cleanEvidences = [];

            const allLabels = getLabels().map(l => {
                const parts = l.split('. ');
                return parts.length > 1 ? parts.slice(1).join('. ') : l;
            });

            for (let i = 0; i < competencies.length; i++) {
                if (selectedCompetencyGroupFilter.length > 0 && !selectedCompetencyGroupFilter.includes(competencies[i].group)) continue;
                if (selectedCompetenciesFilter.length > 0 && !selectedCompetenciesFilter.includes(competencies[i].name)) continue;

                const t = targets[i] || 0;
                if (t === 0) continue;

                const a = emp.actuals[i] || 0;
                const s = emp.self_evals ? (emp.self_evals[i] || 0) : 0;
                cleanLabels.push(allLabels[i]);
                cleanTargets.push(t);
                actuals.push(a);
                selfEvals.push(s);
                cleanDescs.push(competencies[i].levels[a] || "ไม่มีคำอธิบาย");
                cleanEvidences.push(emp.evidences[i] || "ไม่มีหลักฐานที่ระบุ");
            }

            if (idpRadarChartInstance) idpRadarChartInstance.destroy();
            const ctx = document.getElementById('idpRadarChart').getContext('2d');

            idpRadarChartInstance = new Chart(ctx, {
                type: 'radar',
                data: {
                    labels: cleanLabels,
                    datasets: [
                        { label: 'Target', data: cleanTargets, borderColor: '#cbd5e1', backgroundColor: 'transparent', borderDash: [5, 5], borderWidth: 2, pointRadius: 0 },
                        { label: 'Actual', data: actuals, borderColor: '#ca3656', backgroundColor: 'rgba(202, 54, 86, 0.25)', borderWidth: 2, pointBackgroundColor: '#ca3656', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#ca3656', pointRadius: 4 },
                        { label: 'Self Eva.', data: selfEvals, borderColor: '#fbbf24', backgroundColor: 'rgba(251, 191, 36, 0.2)', borderWidth: 2, pointBackgroundColor: '#fbbf24', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#fbbf24', pointRadius: 4 }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: true, position: 'bottom' },
                        tooltip: {
                            callbacks: {
                                label: function (context) {
                                    return context.dataset.label + ': Level ' + context.raw;
                                },
                                afterLabel: function (context) {
                                    if (context.dataset.label === 'Actual') {
                                        const idx = context.dataIndex;

                                        // Wrap text function to prevent extremely wide tooltips
                                        const wrapText = (text, maxLineLen) => {
                                            const words = text.split(' ');
                                            let lines = [];
                                            let currentLine = '';
                                            words.forEach(word => {
                                                if ((currentLine + word).length > maxLineLen) {
                                                    lines.push(currentLine.trim());
                                                    currentLine = word + ' ';
                                                } else {
                                                    currentLine += word + ' ';
                                                }
                                            });
                                            if (currentLine) lines.push(currentLine.trim());
                                            return lines;
                                        };

                                        let result = [];
                                        result.push('ความหมาย:');
                                        result = result.concat(wrapText(cleanDescs[idx], 50).map(l => '  ' + l));
                                        result.push('หลักฐาน (Evidence):');
                                        result = result.concat(wrapText(cleanEvidences[idx], 50).map(l => '  ' + l));
                                        return result;
                                    }
                                    return '';
                                }
                            }
                        }
                    },
                    scales: {
                        r: {
                            min: 0,
                            max: 5,
                            ticks: { display: false, stepSize: 1 },
                            grid: { color: '#f1f5f9' },
                            angleLines: { color: '#f1f5f9' },
                            pointLabels: {
                                font: { size: 11, family: "'Sarabun', sans-serif" },
                                color: function (context) {
                                    const idx = context.index;
                                    const actual = actuals[idx] || 0;
                                    const target = cleanTargets[idx] || 0;
                                    return actual >= target ? '#16a34a' : '#991b1b';
                                }
                            }
                        }
                    }
                }
            });
        }

        // --- 8. COMPETENCY ANALYTIC TAB ---
        function setupAnalyticTab() {
            renderAnalyticTab();
        }

        function renderAnalyticTab() {
            let filteredComps = competencies;
            if (selectedCompetencyGroupFilter.length > 0) {
                filteredComps = filteredComps.filter(c => selectedCompetencyGroupFilter.includes(c.group));
            }
            if (selectedCompetenciesFilter.length > 0) {
                filteredComps = filteredComps.filter(c => selectedCompetenciesFilter.includes(c.name));
            }

            // Map Comp index
            const compIndices = filteredComps.map(c => competencies.findIndex(x => x.id === c.id));

            // Determine valid users
            let validUserIds = [];
            if (currentUser.id === 'Admin') {
                validUserIds = applyGlobalFiltersToSubIds(Object.keys(dbUsers).filter(uid => uid !== 'Admin'));
            } else {
                let subs = getSubordinates(currentUser.id);
                if (subs.length > 0) {
                    validUserIds = applyGlobalFiltersToSubIds(subs);
                } else {
                    validUserIds = applyGlobalFiltersToSubIds([currentUser.id]);
                }
            }

            // 1. Radar Charts (Top Performers Per Position)
            // Group by position
            let usersByPos = {};
            validUserIds.forEach(id => {
                const emp = dbUsers[id];
                if (!usersByPos[emp.position]) usersByPos[emp.position] = [];
                usersByPos[emp.position].push(id);
            });

            // Calculate readiness per user
            let userReadiness = {};
            validUserIds.forEach(id => {
                const emp = dbUsers[id];
                const targets = positionTargets[emp.position] || [];
                let totalT = 0; let totalA = 0;
                compIndices.forEach(idx => {
                    const t = targets[idx] || 0;
                    if (t > 0) {
                        totalT += t;
                        totalA += (emp.actuals[idx] || 0);
                    }
                });
                userReadiness[id] = totalT > 0 ? (totalA / totalT) * 100 : 0;
            });

            const radarContainer = document.getElementById('analytic-radar-container');
            radarContainer.innerHTML = '';

            // Destroy old charts
            analyticRadarCharts.forEach(c => c.destroy());
            analyticRadarCharts = [];

            // Identify top users per position
            Object.keys(usersByPos).sort().forEach((pos, posIdx) => {
                const usersInPos = usersByPos[pos];
                if (usersInPos.length === 0) return;

                // Find Max
                let maxVal = -1;
                usersInPos.forEach(id => {
                    if (userReadiness[id] > maxVal) maxVal = userReadiness[id];
                });

                // Top Users
                let topUsers = usersInPos.filter(id => userReadiness[id] === maxVal);
                if (topUsers.length === 0) return;

                // Build Card
                const topNames = topUsers.map(id => dbUsers[id].name).join(', ');
                const readPct = Math.round(maxVal);

                let evalDates = topUsers.map(id => {
                    let mgrDate = 'ยังไม่ประเมิน';
                    try {
                        let uDate = dbUsers[id].evalDate;
                        if (uDate) {
                            if (uDate.startsWith('{')) {
                                let obj = JSON.parse(uDate);
                                if(obj.mgr) mgrDate = obj.mgr;
                            } else {
                                mgrDate = uDate;
                            }
                        }
                    } catch(e) {}
                    return mgrDate;
                });
                let evalDateText = evalDates.join(', ');

                let cardHtml = `
                    <div class="border border-slate-200 rounded-2xl p-4 flex flex-col bg-slate-50">
                        <div class="mb-3 border-b border-slate-200 pb-2">
                            <p class="text-xs font-bold text-scg-600 mb-1">${pos}</p>
                            <h4 class="text-sm font-bold text-slate-800 line-clamp-2">${topNames}</h4>
                            <p class="text-xs text-slate-500 mt-1 flex justify-between">
                                <span>Readiness: <span class="font-bold text-scg-700">${readPct}%</span></span>
                            </p>
                            <p class="text-xs text-slate-500 mt-1">
                                ประเมินโดยหัวหน้า: <span class="font-bold text-slate-700">${evalDateText}</span>
                            </p>
                        </div>
                        <div class="relative w-full aspect-square">
                            <canvas id="analytic-radar-${posIdx}"></canvas>
                        </div>
                    </div>
                `;
                radarContainer.innerHTML += cardHtml;
            });

            // Draw Charts (Need a small timeout for DOM to render canvas)
            setTimeout(() => {
                Object.keys(usersByPos).sort().forEach((pos, posIdx) => {
                    const usersInPos = usersByPos[pos];
                    if (usersInPos.length === 0) return;
                    let maxVal = Math.max(...usersInPos.map(id => userReadiness[id]));
                    let topUsers = usersInPos.filter(id => userReadiness[id] === maxVal);
                    if (topUsers.length === 0) return;

                    const canvas = document.getElementById(`analytic-radar-${posIdx}`);
                    if (!canvas) return;

                    const ctx = canvas.getContext('2d');
                    const targets = positionTargets[pos] || [];

                    let labels = [];
                    let targetData = [];
                    let actualsData = [];

                    const topEmp = dbUsers[topUsers[0]];
                    let selfData = [];

                    compIndices.forEach(idx => {
                        const t = targets[idx] || 0;
                        if (t > 0) {
                            labels.push(competencies[idx].name.replace(/^[0-9\.\s]+/, ''));
                            targetData.push(t);
                            actualsData.push(topEmp.actuals[idx] || 0);
                            selfData.push(topEmp.self_evals ? (topEmp.self_evals[idx] || 0) : 0);
                        }
                    });

                    const chart = new Chart(ctx, {
                        type: 'radar',
                        data: {
                            labels: labels,
                            datasets: [
                                { label: 'Target', data: targetData, borderColor: '#cbd5e1', backgroundColor: 'transparent', borderDash: [5, 5], borderWidth: 2, pointRadius: 0 },
                                { label: 'Actual', data: actualsData, borderColor: '#ca3656', backgroundColor: 'rgba(202, 54, 86, 0.25)', borderWidth: 2, pointBackgroundColor: '#ca3656', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#ca3656', pointRadius: 3 },
                                { label: 'Self Eva.', data: selfData, borderColor: '#fbbf24', backgroundColor: 'rgba(251, 191, 36, 0.2)', borderWidth: 2, pointBackgroundColor: '#fbbf24', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#fbbf24', pointRadius: 3 }
                            ]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                legend: { display: false }
                            },
                            scales: {
                                r: {
                                    min: 0,
                                    max: 5,
                                    ticks: { display: false, stepSize: 1 },
                                    pointLabels: { font: { size: 9, family: "'Sarabun', sans-serif" }, color: '#64748b' }
                                }
                            }
                        }
                    });
                    analyticRadarCharts.push(chart);
                });
            }, 50);

            // 2. Bar Chart (Gap Frequency)
            let gapCounts = {};
            compIndices.forEach(idx => gapCounts[idx] = 0);

            validUserIds.forEach(id => {
                const emp = dbUsers[id];
                const targets = positionTargets[emp.position] || [];
                compIndices.forEach(idx => {
                    const t = targets[idx] || 0;
                    if (t > 0) {
                        const a = emp.actuals[idx] || 0;
                        if (a < t) {
                            gapCounts[idx]++;
                        }
                    }
                });
            });

            let gapData = [];
            compIndices.forEach(idx => {
                if (gapCounts[idx] > 0) {
                    gapData.push({
                        label: competencies[idx].name.replace(/^[0-9\.\s]+/, ''),
                        count: gapCounts[idx]
                    });
                }
            });

            gapData.sort((a, b) => b.count - a.count);

            const barLabels = gapData.map(d => d.label);
            const barCounts = gapData.map(d => d.count);

            if (analyticBarChartInstance) analyticBarChartInstance.destroy();
            const barCtx = document.getElementById('analytic-bar-chart').getContext('2d');

            analyticBarChartInstance = new Chart(barCtx, {
                type: 'bar',
                data: {
                    labels: barLabels,
                    datasets: [{
                        label: 'จำนวนพนักงานที่ยังไม่ถึงเป้าหมาย (Gap)',
                        data: barCounts,
                        backgroundColor: '#ca3656',
                        borderRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    indexAxis: 'y',
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            ticks: { stepSize: 1 }
                        },
                        y: {
                            ticks: { font: { family: "'Sarabun', sans-serif" } }
                        }
                    }
                }
            });
        }

        function renderTrackingTable() {
            const tbody = document.getElementById('tracking-data-tbody');
            if (!tbody) return;

            let html = '';
            
            // Collect tracking data from employeeData first
            let trackingList = [];
            let processedEmpNames = new Set();
            
            if (employeeData && employeeData.length > 0) {
                employeeData.forEach(e => {
                    if (!matchesOrgFiltersData(e)) return;
                    
                    const empId = e.username || e.user_id || e.USER;
                    if (empId === 'Admin' || empId === 'admin') return;

                    let mgrName = e.ReportToName || '';
                    let empName = e.FullNameTH || e.FullName || e.EmployeeNameThai || e.EmployeeNameEng || empId;
                    let posName = e.PositionNameThai || e.position_name || e.position || '';

                    processedEmpNames.add(empName);

                    let u = null;
                    if (empId && dbUsers[empId]) {
                        u = dbUsers[empId];
                    } else {
                        for (const key in dbUsers) {
                            if (dbUsers[key].name === empName) {
                                u = dbUsers[key];
                                break;
                            }
                        }
                    }
                    
                    let hasRole = (roleResponses[posName] && roleResponses[posName].trim() !== "" && roleResponses[posName] !== "ระบุหน้าที่ความรับผิดชอบ...") ? true : false;
                    
                    let hasTargets = false;
                    if (positionTargets[posName]) {
                        hasTargets = positionTargets[posName].some(t => t >= 1);
                    }
                    
                    let selfDate = '';
                    let mgrDate = '';
                    if (u) {
                        if (u.evalDate && u.evalDate.startsWith('{')) {
                            try {
                                let parsed = JSON.parse(u.evalDate);
                                selfDate = parsed.self || '';
                                mgrDate = parsed.mgr || '';
                            } catch(err) {}
                        } else if (u.evalDate) {
                            selfDate = u.evalDate;
                        }
                    }
                    
                    trackingList.push({
                        mgrName: mgrName,
                        empName: empName,
                        posName: posName,
                        hasRole: hasRole,
                        hasTargets: hasTargets,
                        selfDate: selfDate,
                        mgrDate: mgrDate
                    });
                });
            }
            

            if (trackingList.length === 0) {
                html += `<tr><td colspan="8" class="text-center py-8 text-slate-500">ไม่พบข้อมูล หรืออาจถูกกรอง (Filter) ออก</td></tr>`;
            } else {
                trackingList.forEach((t, i) => {
                    html += `<tr class="hover:bg-slate-50 transition-colors">
                        <td class="py-3 px-6 border-r border-slate-100 text-center font-medium">${i + 1}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${t.mgrName}</td>
                        <td class="py-3 px-6 border-r border-slate-100 font-bold">${t.empName}</td>
                        <td class="py-3 px-6 border-r border-slate-100"><span class="bg-slate-100 text-slate-700 px-2 py-1 rounded text-xs font-medium">${t.posName}</span></td>
                        <td class="py-3 px-6 border-r border-slate-100 text-center">${t.hasRole ? '<i class="fa-solid fa-check text-emerald-500"></i>' : ''}</td>
                        <td class="py-3 px-6 border-r border-slate-100 text-center">${t.hasTargets ? '<i class="fa-solid fa-check text-emerald-500"></i>' : ''}</td>
                        <td class="py-3 px-6 border-r border-slate-100 text-center text-xs text-slate-600">${t.selfDate || ''}</td>
                        <td class="py-3 px-6 text-center text-xs text-slate-600">${t.mgrDate || ''}</td>
                    </tr>`;
                });
            }
            tbody.innerHTML = html;
        }

        function exportTrackingData() {
            const tbody = document.getElementById('tracking-data-tbody');
            if (!tbody || tbody.children.length === 0) {
                showToast("ไม่มีข้อมูลให้ Export");
                return;
            }

            const headers = [
                "ชื่อผู้บังคับบัญชา", "ชื่อพนักงาน", "ตำแหน่ง", "จัดทำ R&R", "ผูก competency", "ประเมินตนเอง", "ผู้บังคับบัญชาประเมิน"
            ];

            let csvContent = "\uFEFF" + headers.join(",") + "\n";
            
            // Loop through all table rows
            const rows = tbody.querySelectorAll('tr');
            rows.forEach(tr => {
                const cols = tr.querySelectorAll('td');
                if (cols.length >= 8) {
                    const rowData = [
                        cols[1].innerText.trim(),
                        cols[2].innerText.trim(),
                        cols[3].innerText.trim(),
                        cols[4].querySelector('i') ? 'Yes' : '',
                        cols[5].querySelector('i') ? 'Yes' : '',
                        cols[6].innerText.trim(),
                        cols[7].innerText.trim()
                    ].map(val => `"${val.replace(/"/g, '""')}"`);
                    
                    csvContent += rowData.join(",") + "\n";
                }
            });

            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement("a");
            const url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", `Tracking_Evaluation_${new Date().getTime()}.csv`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        function exportAverageSkillChart() {
            if (!averageBarChartInstance) {
                if (typeof showToast === 'function') showToast("ไม่มีข้อมูลสำหรับ Export");
                else alert("ไม่มีข้อมูลสำหรับ Export");
                return;
            }
            const data = averageBarChartInstance.data;
            const labels = data.labels;
            const percentCompletes = data.datasets.find(d => d.label === '% Complete').data;
            const avgTargets = data.datasets.find(d => d.label === 'Average Expected').data;
            const avgActuals = data.datasets.find(d => d.label === 'Average Actual').data;

            let csvContent = "\uFEFF" + "Employee Name,Average Expected,Average Actual,% Complete\n";
            for (let i = 0; i < labels.length; i++) {
                csvContent += `"${labels[i]}",${avgTargets[i]},${avgActuals[i]},${percentCompletes[i]}%\n`;
            }

            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement("a");
            const url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", "Average_Skill_Level.csv");
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        function exportTeamSkillMatrix() {
            const container = document.getElementById('dashboard-heatmap-container');
            if (!container || container.classList.contains('hidden')) {
                if (typeof showToast === 'function') showToast("ไม่มีข้อมูลสำหรับ Export");
                else alert("ไม่มีข้อมูลสำหรับ Export");
                return;
            }
            const table = container.querySelector('table');
            if (!table) return;

            let csvContent = "\uFEFF";
            
            const ths = table.querySelectorAll('thead th');
            let headers = [];
            ths.forEach(th => {
                let text = th.innerText.replace(/,/g, " ").replace(/"/g, '""').trim();
                headers.push(`"${text}"`);
            });
            csvContent += headers.join(",") + "\n";
            
            const trs = table.querySelectorAll('tbody tr');
            trs.forEach(tr => {
                let row = [];
                const tds = tr.querySelectorAll('td');
                tds.forEach(td => {
                    let text = td.innerText.replace(/,/g, " ").replace(/"/g, '""').trim();
                    row.push(`"${text}"`);
                });
                csvContent += row.join(",") + "\n";
            });

            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement("a");
            const url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", "Team_Skill_Matrix.csv");
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        function renderEmployeeDataTab() {
            const tbody = document.getElementById('employee-data-tbody');
            if (!tbody) return;

            if (!employeeData || employeeData.length === 0) {
                tbody.innerHTML = `<tr><td colspan="15" class="text-center py-8 text-slate-500">ไม่พบข้อมูลพนักงาน หรือตารางยังไม่ได้ถูกสร้างขึ้นในฐานข้อมูล</td></tr>`;
                return;
            }

            let html = '';
            employeeData.forEach(emp => {
                html += `
                    <tr class="hover:bg-slate-50 transition-colors">
                        <td class="py-3 px-6 border-r border-slate-100 font-medium">${emp.PersonnelNumber || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 text-scg-700 font-medium">${emp.user_id || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 text-slate-500">${emp.password || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.FullName || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.PositionNameThai || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100 text-center"><span class="bg-slate-100 text-slate-700 px-2 py-1 rounded font-bold text-xs">${emp.PositionStructureLevel || '-'}</span></td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.SectionThai || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.DepartmentThai || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.Sub1DivisionThai || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.DivisionThai || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.Sub1CompanyThai || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.CompanyThai || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.ReportToName || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.Certificate || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.JobGroup || '-'}</td>
                        <td class="py-3 px-6 border-r border-slate-100">${emp.Email || '-'}</td>
                    </tr>
                `;
            });
            tbody.innerHTML = html;
            setTimeout(buildEmployeeFilters, 0); // wait for DOM update
        }

        let employeeFilters = {}; // { colIndex: new Set(['Val1', 'Val2']) }

        window.buildEmployeeFilters = function () {
            const tbody = document.querySelector('#employee-data-tbody');
            if (!tbody) return;
            const table = tbody.parentElement;
            const thead = table.querySelector('thead');
            const headers = thead.querySelectorAll('th');

            const colKeys = [
                'PersonnelNumber', 'user_id', 'password', 'FullName', 'PositionNameThai', 'PositionStructureLevel',
                'SectionThai', 'DepartmentThai', 'Sub1DivisionThai', 'DivisionThai', 'Sub1CompanyThai', 'CompanyThai',
                'ReportToName', 'Certificate', 'JobGroup', 'Email'
            ];

            headers.forEach((th, index) => {
                if (th.querySelector('.emp-filter-container')) {
                    th.querySelector('.emp-filter-container').remove();
                }

                const key = colKeys[index];
                if (!key) return;

                const trs = tbody.querySelectorAll('tr');
                if (trs.length === 1 && trs[0].cells.length === 1) return; // Empty message row
                const uniqueValues = [...new Set(Array.from(trs).map(tr => tr.cells[index] ? tr.cells[index].innerText.trim() : '-'))].sort();

                const container = document.createElement('div');
                container.className = 'emp-filter-container relative mt-2 font-normal text-slate-700';

                const btn = document.createElement('button');
                btn.className = 'w-full px-2 py-1 border border-slate-200 rounded text-xs text-left bg-white flex justify-between items-center hover:bg-slate-50';
                btn.innerHTML = `<span class="truncate text-slate-400">All</span> <i class="fa-solid fa-chevron-down ml-1 text-[10px]"></i>`;
                btn.onclick = (e) => {
                    e.stopPropagation();
                    document.querySelectorAll('.emp-filter-dropdown').forEach(d => {
                        if (d !== dropdown) d.classList.add('hidden');
                    });
                    dropdown.classList.toggle('hidden');
                };

                const dropdown = document.createElement('div');
                dropdown.className = 'emp-filter-dropdown hidden absolute top-full left-0 w-48 mt-1 bg-white border border-slate-200 rounded-lg shadow-lg z-50 max-h-48 overflow-y-auto p-2';
                dropdown.onclick = (e) => e.stopPropagation();

                const searchBox = document.createElement('input');
                searchBox.type = 'text';
                searchBox.placeholder = 'Search...';
                searchBox.className = 'w-full mb-2 px-2 py-1 text-xs border border-slate-200 rounded';
                searchBox.onclick = (e) => e.stopPropagation();
                searchBox.onkeyup = (e) => {
                    const val = e.target.value.toLowerCase();
                    dropdown.querySelectorAll('.checkbox-item').forEach(lbl => {
                        lbl.style.display = lbl.innerText.toLowerCase().includes(val) ? 'flex' : 'none';
                    });
                };
                dropdown.appendChild(searchBox);

                const selectAllLbl = document.createElement('label');
                selectAllLbl.className = 'flex items-center gap-2 px-2 py-1 text-xs hover:bg-slate-50 cursor-pointer border-b border-slate-100 mb-1';
                selectAllLbl.innerHTML = `<input type="checkbox" class="rounded border-slate-300" checked> <span class="font-bold">Select All</span>`;
                const selectAllCb = selectAllLbl.querySelector('input');
                selectAllCb.onclick = (e) => e.stopPropagation();
                selectAllCb.onchange = (e) => {
                    const checked = e.target.checked;
                    dropdown.querySelectorAll('.val-checkbox').forEach(cb => {
                        cb.checked = checked;
                    });
                    updateFilterState(index, btn, dropdown);
                };
                dropdown.appendChild(selectAllLbl);

                uniqueValues.forEach(val => {
                    const lbl = document.createElement('label');
                    lbl.className = 'checkbox-item flex items-center gap-2 px-2 py-1 text-xs hover:bg-slate-50 cursor-pointer';
                    lbl.innerHTML = `<input type="checkbox" value="${val}" class="val-checkbox rounded border-slate-300" checked> <span class="truncate" title="${val}">${val}</span>`;
                    const cb = lbl.querySelector('input');
                    cb.onclick = (e) => e.stopPropagation();
                    cb.onchange = () => {
                        const allChecked = Array.from(dropdown.querySelectorAll('.val-checkbox')).every(c => c.checked);
                        selectAllCb.checked = allChecked;
                        updateFilterState(index, btn, dropdown);
                    };
                    dropdown.appendChild(lbl);
                });

                container.appendChild(btn);
                container.appendChild(dropdown);
                th.appendChild(container);

                employeeFilters[index] = new Set(uniqueValues);
            });

            document.addEventListener('click', () => {
                document.querySelectorAll('.emp-filter-dropdown').forEach(d => d.classList.add('hidden'));
            });
        };

        function updateFilterState(index, btn, dropdown) {
            const checkboxes = dropdown.querySelectorAll('.val-checkbox');
            const checkedVals = [];
            checkboxes.forEach(cb => {
                if (cb.checked) checkedVals.push(cb.value);
            });

            employeeFilters[index] = new Set(checkedVals);

            if (checkedVals.length === checkboxes.length) {
                btn.querySelector('span').innerText = 'All';
                btn.querySelector('span').classList.add('text-slate-400');
                btn.querySelector('span').classList.remove('text-scg-700', 'font-bold');
            } else if (checkedVals.length === 0) {
                btn.querySelector('span').innerText = 'None';
                btn.querySelector('span').classList.remove('text-slate-400');
                btn.querySelector('span').classList.add('text-red-500', 'font-bold');
            } else {
                btn.querySelector('span').innerText = `${checkedVals.length} selected`;
                btn.querySelector('span').classList.remove('text-slate-400');
                btn.querySelector('span').classList.add('text-scg-700', 'font-bold');
            }

            applyEmployeeFilters();
        }

        function applyEmployeeFilters() {
            const trs = document.querySelectorAll('#employee-data-tbody tr');
            trs.forEach(tr => {
                let show = true;
                for (let i = 0; i < tr.cells.length; i++) {
                    if (employeeFilters[i]) {
                        const text = tr.cells[i].innerText;
                        if (!employeeFilters[i].has(text)) {
                            show = false;
                            break;
                        }
                    }
                }
                tr.style.display = show ? '' : 'none';
            });
        }

        function exportEmployeeData() {
            if (!employeeData || employeeData.length === 0) {
                showToast("ไม่มีข้อมูลให้ Export");
                return;
            }

            const headers = [
                "Employee ID", "User ID", "Password", "Name", "Position Name",
                "Position Level", "Section", "Department", "Sub1-Division", "Division",
                "Sub1-Company", "Company", "Report to Name", "Certificate", "Job Group", "Email"
            ];

            let csvContent = "\uFEFF" + headers.join(",") + "\n";

            employeeData.forEach(emp => {
                const row = [
                    emp.PersonnelNumber || '', emp.user_id || '', emp.password || '', emp.FullName || '',
                    emp.PositionNameThai || '', emp.PositionStructureLevel || '', emp.SectionThai || '',
                    emp.DepartmentThai || '', emp.Sub1DivisionThai || '', emp.DivisionThai || '',
                    emp.Sub1CompanyThai || '', emp.CompanyThai || '', emp.ReportToName || '',
                    emp.Certificate || '', emp.JobGroup || '', emp.Email || ''
                ].map(val => `"${String(val).replace(/"/g, '""')}"`);

                csvContent += row.join(",") + "\n";
            });

            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement("a");
            const url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", `Employee_Data_Export_${new Date().getTime()}.csv`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    