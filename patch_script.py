import os
import re

file_path = r'../competency_system_dynamic_rbac_hierarchy.html'

with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add dashboard heatmap container
heatmap_container_html = r'''
                        <!-- Heatmap Container -->
                        <div id="dashboard-heatmap-container" class="mt-8 overflow-x-auto bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hidden">
                        </div>
'''
html = html.replace('<div id="dash-individual-cards-container"', heatmap_container_html + '\n                    <div id="dash-individual-cards-container"')

# 2. Add updateIDPStatus function
update_idp_js = r'''
        window.updateIDPStatus = function(empId, skillName, status) {
            if (!dbUsers[empId]) return;
            if (!dbUsers[empId].idp_status) dbUsers[empId].idp_status = {};
            dbUsers[empId].idp_status[skillName] = status;
            showToast("บันทึกสถานะ IDP สำเร็จ!");
        }
'''
html = html.replace('window.toggleIDPEmpFilter = function', update_idp_js + '\n        window.toggleIDPEmpFilter = function')

# 3. Update renderIDPContent HTML
idp_new_html = r"""
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
                    </div>`;"""
html = re.sub(r'recsHtml \+= `\s*<div class="flex items-center gap-3 p-3 bg-white border border-red-100 rounded-xl shadow-sm mb-3">.*?</div>`;', lambda m: idp_new_html, html, flags=re.DOTALL)

# 4. Heatmap Rendering Logic
heatmap_js = r'''
        window.renderTeamHeatmap = function(subIds) {
            const container = document.getElementById('dashboard-heatmap-container');
            if (!container) return;
            
            if (subIds.length === 0) {
                container.classList.add('hidden');
                return;
            }
            container.classList.remove('hidden');

            let html = '<h3 class="text-lg font-bold text-scg-800 mb-4">Team Skill Matrix</h3>';
            html += '<table class="w-full text-left border-collapse min-w-[800px]">';
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
                html += `<th class="p-3 border-b border-slate-200 truncate max-w-[120px]" title="${comp.name}">${comp.name}</th>`;
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

            html += '</tbody></table>';
            container.innerHTML = html;
        }
'''
html = html.replace('function renderIndividualDashboards(subIds)', heatmap_js + '\n        function renderIndividualDashboards(subIds)')
html = html.replace('renderIndividualDashboards(toShow);', 'renderIndividualDashboards(toShow);\n            renderTeamHeatmap(toShow);')


# 5. Evaluation Workflow
new_eval_html = r"""
                let selfEvalVal = (emp.self_evals && emp.self_evals[i] !== undefined) ? emp.self_evals[i] : actual;
                let supervisorFeedback = (emp.supervisor_feedback && emp.supervisor_feedback[i]) ? emp.supervisor_feedback[i] : '';
                
                html += `<tr>
                    <td class="p-3 text-sm text-slate-800 border border-slate-200 max-w-[200px]"><span class="font-bold text-scg-700">${comp.name}</span><br><span class="text-xs text-slate-500">${comp.desc}</span></td>
                    <td class="p-3 text-center text-sm border border-slate-200">
                        <div class="inline-block w-8 h-8 leading-8 bg-slate-100 rounded font-bold text-slate-700">${target}</div>
                    </td>`;
                    
                if (currentUser.id === id) { // Self Evaluation
                    let statText = (emp.eval_status === 'Approved') ? '<span class="text-green-600 text-[10px] block mt-1">Approved</span>' : ((emp.eval_status === 'Waiting for Approval') ? '<span class="text-amber-500 text-[10px] block mt-1">Waiting</span>' : '');
                    html += `
                    <td class="p-3 text-center border border-slate-200 bg-blue-50/30">
                        <select id="eval-self-${id}-${i}" class="w-16 px-2 py-1 border border-blue-200 bg-white rounded text-center font-bold text-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500">
                            ${[0,1,2,3,4,5].map(v => `<option value="${v}" ${selfEvalVal === v ? 'selected' : ''}>${v}</option>`).join('')}
                        </select>
                        ${statText}
                    </td>
                    <td class="p-3 text-center border border-slate-200">
                        <div class="inline-block w-8 h-8 leading-8 bg-slate-50 rounded font-bold text-slate-400">${actual}</div>
                        ${supervisorFeedback ? `<div class="text-[10px] text-slate-500 mt-1 px-1 bg-slate-100 rounded text-left leading-tight break-words max-w-[100px]">${supervisorFeedback}</div>` : ''}
                    </td>`;
                } else { // Supervisor Evaluation
                    html += `
                    <td class="p-3 text-center border border-slate-200">
                        <div class="inline-block w-8 h-8 leading-8 bg-blue-50 text-blue-700 rounded font-bold">${selfEvalVal}</div>
                    </td>
                    <td class="p-3 border border-slate-200 bg-amber-50/30">
                        <div class="flex flex-col gap-2 items-center">
                            <select id="eval-actual-${id}-${i}" class="w-16 px-2 py-1 border border-amber-200 bg-white rounded text-center font-bold text-amber-700 focus:outline-none focus:ring-2 focus:ring-amber-500">
                                ${[0,1,2,3,4,5].map(v => `<option value="${v}" ${actual === v ? 'selected' : ''}>${v}</option>`).join('')}
                            </select>
                            <input type="text" id="eval-feedback-${id}-${i}" class="w-full text-xs px-2 py-1 border border-slate-200 rounded" placeholder="Feedback..." value="${supervisorFeedback}">
                        </div>
                    </td>`;
                }
                
                html += `</tr>`;
"""
html = re.sub(r'html \+= `<tr>\s*<td class="p-3 text-sm text-slate-800 border border-slate-200 max-w-\[200px\]"><span class="font-bold text-scg-700">\$\{comp\.name\}</span>.*?</tr>`;', lambda m: new_eval_html, html, flags=re.DOTALL)

header_old = r"""
                    <th class="p-3 border border-slate-200">Competency</th>
                    <th class="p-3 border border-slate-200 w-24">Target<br><span class="text-[10px] font-normal">(ความคาดหวัง)</span></th>
                    <th class="p-3 border border-slate-200 w-32">Actual<br><span class="text-[10px] font-normal">(ระดับปัจจุบัน)</span></th>
                </tr>
"""
header_new = r"""
                    <th class="p-3 border border-slate-200">Competency</th>
                    <th class="p-3 border border-slate-200 w-20">Target<br><span class="text-[10px] font-normal">(ความคาดหวัง)</span></th>
                    <th class="p-3 border border-slate-200 w-24">Self Eval<br><span class="text-[10px] font-normal text-blue-600">(ประเมินตนเอง)</span></th>
                    <th class="p-3 border border-slate-200 w-32">Supervisor Eval<br><span class="text-[10px] font-normal text-amber-600">(ประเมินจริง)</span></th>
                </tr>
"""
html = html.replace(header_old, header_new)

new_save_eval = r"""
        window.saveEvaluation = function (empId) {
            const emp = dbUsers[empId];
            if (!emp) return;
            
            if (!emp.self_evals) emp.self_evals = [...emp.actuals];
            if (!emp.supervisor_feedback) emp.supervisor_feedback = {};

            for (let i = 0; i < competencies.length; i++) {
                if (currentUser.id === empId) {
                    const selfSelect = document.getElementById(`eval-self-${empId}-${i}`);
                    if (selfSelect) {
                        emp.self_evals[i] = parseInt(selfSelect.value, 10);
                    }
                } else {
                    const actualSelect = document.getElementById(`eval-actual-${empId}-${i}`);
                    const feedbackInput = document.getElementById(`eval-feedback-${empId}-${i}`);
                    if (actualSelect) {
                        emp.actuals[i] = parseInt(actualSelect.value, 10);
                    }
                    if (feedbackInput) {
                        emp.supervisor_feedback[i] = feedbackInput.value;
                    }
                }
            }
            
            if (currentUser.id === empId) {
                emp.eval_status = 'Waiting for Approval';
            } else {
                emp.eval_status = 'Approved';
            }
"""
html = re.sub(r'window\.saveEvaluation = function \(empId\) \{.*?emp\.actuals\[i\] = parseInt\(select\.value, 10\);\s*\}\s*\}', lambda m: new_save_eval, html, flags=re.DOTALL)


with open(file_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("HTML file patched successfully.")
