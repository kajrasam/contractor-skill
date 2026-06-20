import re

files = [
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html',
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/index_render.html'
]

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update isEmployeeMatchingOrgFilters
    # Replace the body of isEmployeeMatchingOrgFilters
    func_pattern = re.compile(r'function isEmployeeMatchingOrgFilters\(empId\)\s*\{.*?\n        \}', re.DOTALL)
    new_func = """function isEmployeeMatchingOrgFilters(empId) {
            let emp = dbUsers[empId];
            if(!emp) return false;
            
            let eData = employeeData.find(e => e.username === empId || e.user_id === empId || e.EmployeeNameEng === emp.name || e.EmployeeNameThai === emp.name);
            
            let posName = emp.position;
            if(eData && eData.PositionNameThai) posName = eData.PositionNameThai;
            else if(eData && eData.position_name) posName = eData.position_name;
            
            if(selectedJobGroupFilter.length > 0 && (!posName || !selectedJobGroupFilter.includes(positionGroups[posName]))) return false;
            if(selectedPositionsFilter.length > 0 && (!posName || !selectedPositionsFilter.includes(posName))) return false;
            
            if(!eData) {
                if(selectedEmployeeFilter.length > 0 || selectedSectionFilter.length > 0 || selectedDepartmentFilter.length > 0 || selectedSub1DivisionFilter.length > 0 || selectedDivisionFilter.length > 0 || selectedSub1CompanyFilter.length > 0 || selectedCompanyFilter.length > 0) return false;
                return true;
            }
            
            if(selectedEmployeeFilter.length > 0) {
                let empName = eData.FullName || eData.EmployeeNameThai || eData.EmployeeNameEng;
                if(!empName || !selectedEmployeeFilter.includes(empName)) return false;
            }
            
            if(selectedSectionFilter.length > 0 && !selectedSectionFilter.includes(eData.SectionThai)) return false;
            if(selectedDepartmentFilter.length > 0 && !selectedDepartmentFilter.includes(eData.DepartmentThai)) return false;
            if(selectedSub1DivisionFilter.length > 0 && !selectedSub1DivisionFilter.includes(eData.Sub1DivisionThai)) return false;
            if(selectedDivisionFilter.length > 0 && !selectedDivisionFilter.includes(eData.DivisionThai)) return false;
            if(selectedSub1CompanyFilter.length > 0 && !selectedSub1CompanyFilter.includes(eData.Sub1CompanyThai)) return false;
            if(selectedCompanyFilter.length > 0 && !selectedCompanyFilter.includes(eData.CompanyThai)) return false;
            
            return true;
        }"""
    content = func_pattern.sub(new_func, content)

    # 2. Update buildRoleResponseSection
    role_pattern = re.compile(r'function buildRoleResponseSection\(\)\s*\{.*?container\.innerHTML = html;\n        \}', re.DOTALL)
    new_role = """function buildRoleResponseSection() {
            const container = document.getElementById('role-response-container');
            
            let visibleUsers = [];
            if (currentUser.id === 'Admin') {
                visibleUsers = applyGlobalFiltersToSubIds(Object.keys(dbUsers).filter(uid => uid !== 'Admin'));
            } else {
                visibleUsers = applyGlobalFiltersToSubIds([currentUser.id, ...getSubordinates(currentUser.id)]);
            }

            let visiblePosSet = new Set();
            visibleUsers.forEach(uid => {
                const emp = dbUsers[uid];
                const eData = employeeData.find(e => e.user_id === uid || e.username === uid || e.EmployeeNameEng === (emp ? emp.name : '') || e.EmployeeNameThai === (emp ? emp.name : ''));
                if (eData && eData.PositionNameThai) visiblePosSet.add(eData.PositionNameThai);
                else if (eData && eData.position_name) visiblePosSet.add(eData.position_name);
                else if (emp && emp.position) visiblePosSet.add(emp.position);
            });
            let visiblePos = Array.from(visiblePosSet).filter(p => p).sort();

            const isAdmin = currentUser.id === 'Admin';
            
            let html = '<div class="flex flex-col gap-3">';
            if (visiblePos.length === 0) {
                html += '<p class="text-slate-400 text-sm py-4">ไม่พบตำแหน่งที่ตรงกับเงื่อนไข</p>';
            }
            
            visiblePos.forEach(pos => {
                const response = roleResponses[pos] || "ยังไม่ระบุหน้าที่ความรับผิดชอบ...";
                const group = positionGroups[pos] || '-';
                
                if(isAdmin && isEditMode) {
                    html += `
                    <div class="bg-white p-4 rounded-xl border border-amber-200 bg-amber-50/10 hover:shadow-md transition-shadow">
                        <div class="flex flex-col md:flex-row items-start gap-4">
                            <div class="flex items-center gap-3 md:w-1/3">
                                <div class="w-10 h-10 rounded-full bg-amber-100 text-amber-600 flex items-center justify-center shrink-0">
                                    <i class="fa-solid fa-user-gear"></i>
                                </div>
                                <div class="w-full">
                                    <input type="text" value="${pos}" onchange="handlePositionChange('${pos}', this.value)" class="w-full font-bold text-scg-900 text-sm mb-1 border-b border-amber-300 bg-transparent px-1 py-1 focus:border-scg-600 outline-none" title="แก้ไขชื่อตำแหน่ง">
                                    <input type="text" value="${group}" onchange="handlePositionGroupChange('${pos}', this.value)" placeholder="ระบุกลุ่มงาน..." class="w-full text-xs text-slate-700 p-1 border border-slate-200 rounded outline-none focus:border-amber-500 bg-white">
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
                                <span class="text-[10px] bg-slate-100 text-slate-500 px-2 py-0.5 rounded-full font-medium inline-block mt-1">${group}</span>
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
        }"""
    content = role_pattern.sub(new_role, content)

    # 3. Update buildTrainingMatrix to use same visiblePos logic
    matrix_pattern = re.compile(r'function buildTrainingMatrix\(\)\s*\{.*?const isAdmin = currentUser\.id === \'Admin\';', re.DOTALL)
    new_matrix = """function buildTrainingMatrix() {
            const container = document.getElementById('training-matrix-container');
            
            let visibleUsers = [];
            if (currentUser.id === 'Admin') {
                visibleUsers = applyGlobalFiltersToSubIds(Object.keys(dbUsers).filter(uid => uid !== 'Admin'));
            } else {
                visibleUsers = applyGlobalFiltersToSubIds([currentUser.id, ...getSubordinates(currentUser.id)]);
            }

            let visiblePosSet = new Set();
            visibleUsers.forEach(uid => {
                const emp = dbUsers[uid];
                const eData = employeeData.find(e => e.user_id === uid || e.username === uid || e.EmployeeNameEng === (emp ? emp.name : '') || e.EmployeeNameThai === (emp ? emp.name : ''));
                if (eData && eData.PositionNameThai) visiblePosSet.add(eData.PositionNameThai);
                else if (eData && eData.position_name) visiblePosSet.add(eData.position_name);
                else if (emp && emp.position) visiblePosSet.add(emp.position);
            });
            let visiblePos = Array.from(visiblePosSet).filter(p => p).sort();

            const isAdmin = currentUser.id === 'Admin';"""
    content = matrix_pattern.sub(new_matrix, content)

    # We also need to change the grid layout in HTML to just block (remove grid classes)
    content = content.replace('id="role-response-container" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"', 'id="role-response-container" class="w-full"')
    content = content.replace('id="role-response-container" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4"', 'id="role-response-container" class="w-full"')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Patch applied for Role Response section.")
