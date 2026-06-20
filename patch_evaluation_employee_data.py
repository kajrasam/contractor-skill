import re

files = [
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html',
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/index_render.html'
]

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update populateEvalDropdown
    pattern_populate = re.compile(r'function populateEvalDropdown\(\)\s*\{.*?\n\s*\}', re.DOTALL)
    
    new_populate = """function populateEvalDropdown() {
            const selectEl = document.getElementById('eval-employee-select');
            selectEl.innerHTML = '';
            
            let validEmps = [];
            let actingName = dbUsers[actingAsRole] ? dbUsers[actingAsRole].name : '';

            employeeData.forEach(e => {
                let empName = e.FullName || e.EmployeeNameThai || e.EmployeeNameEng;
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
                    }
                    
                    if (isSub && empName) {
                        validEmps.push({ id: uid, name: empName, position: pName || 'Unassigned', raw: e });
                    }
                }
            });

            if (validEmps.length === 0) {
                selectEl.innerHTML = '<option value="">-- ไม่พบผู้ใต้บังคับบัญชา --</option>';
                document.getElementById('sliders-container').innerHTML = '<div class="text-center text-slate-400 py-10">ไม่พบข้อมูล หรือ ยังไม่ได้เริ่มประเมิน</div>';
                if(evalRadarChartInstance) evalRadarChartInstance.destroy();
                return;
            }

            // Remove duplicates by ID
            let uniqueEmps = [];
            let seenIds = new Set();
            validEmps.forEach(emp => {
                if(!seenIds.has(emp.id)) {
                    seenIds.add(emp.id);
                    uniqueEmps.push(emp);
                }
            });

            uniqueEmps.forEach(emp => { 
                selectEl.innerHTML += `<option value="${emp.id}">${emp.name} (${emp.position})</option>`; 
            });
            updateEvalUI();
        }"""
        
    content = pattern_populate.sub(new_populate, content)
    
    # 2. Update updateEvalUI to auto-create missing dbUsers
    pattern_update = re.compile(r'const emp = dbUsers\[id\];\s*const eData = employeeData\.find\(e => e\.user_id === id \|\| e\.username === id \|\| e\.EmployeeNameEng === emp\.name \|\| e\.EmployeeNameThai === emp\.name\);\s*let pName = emp\.position;\s*if\(eData && eData\.PositionNameThai\) pName = eData\.PositionNameThai;\s*else if\(eData && eData\.position_name\) pName = eData\.position_name;\s*const targets = positionTargets\[pName\] \|\| \[\];')
    
    new_update = """if (!dbUsers[id]) {
                const rawEData = employeeData.find(e => e.user_id === id || e.username === id || e.SCGEmployeeID === id || (e.FullName || e.EmployeeNameThai || e.EmployeeNameEng) === id);
                if (rawEData) {
                    const empName = rawEData.FullName || rawEData.EmployeeNameThai || rawEData.EmployeeNameEng;
                    const pName = rawEData.PositionNameThai || rawEData.position_name || 'Unassigned';
                    dbUsers[id] = {
                        name: empName,
                        position: pName,
                        actuals: [],
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
            const eData = employeeData.find(e => e.user_id === id || e.username === id || e.EmployeeNameEng === emp.name || e.EmployeeNameThai === emp.name);
            let pName = emp.position;
            if(eData && eData.PositionNameThai) pName = eData.PositionNameThai;
            else if(eData && eData.position_name) pName = eData.position_name;

            const targets = positionTargets[pName] || [];
            const hasMappedCompetency = targets.some(t => t > 0);
            
            if (!hasMappedCompetency) {
                document.getElementById('sliders-container').innerHTML = `<div class="text-center py-16 bg-slate-50 rounded-xl border border-slate-200 shadow-sm mt-4">
                    <i class="fa-solid fa-link-slash text-4xl text-amber-300 mb-4 block"></i>
                    <p class="text-slate-600 font-bold text-lg">ผูก Competency ในตำแหน่งนี้ ก่อน</p>
                    <p class="text-slate-400 text-sm mt-2">ผู้ดูแลระบบ (Admin) ต้องกำหนดความคาดหวังทักษะสำหรับตำแหน่ง "${pName}" ในหน้า Training Need ก่อนทำการประเมิน</p>
                </div>`;
                if(evalRadarChartInstance) evalRadarChartInstance.destroy();
                return;
            }"""
            
    content = pattern_update.sub(new_update, content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Patch applied for evaluation employee data.")
