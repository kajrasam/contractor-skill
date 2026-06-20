files = [
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html',
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/index_render.html'
]

old_tail = """            updateEvalUI();
        }
            subs.forEach(id => { selectEl.innerHTML += `<option value="${id}">${dbUsers[id].name} (${dbUsers[id].position})</option>`; });
            updateEvalUI();
        }"""
        
new_tail = """            updateEvalUI();
        }"""

old_update = """            const emp = dbUsers[id];
            const targets = positionTargets[emp.position] || [];"""

new_update = """            if (!dbUsers[id]) {
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

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Clean the tail
    if old_tail in content:
        content = content.replace(old_tail, new_tail)
        print(f"Cleaned tail in {file_path}")
        
    # Replace updateEvalUI logic
    if old_update in content:
        content = content.replace(old_update, new_update)
        print(f"Patched updateEvalUI in {file_path}")
    else:
        print(f"WARNING: old_update not found in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Fix applied.")
