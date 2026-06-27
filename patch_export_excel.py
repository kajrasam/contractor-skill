import re

def fix_export_excel(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    old_func = """function exportAverageSkillChart() {
    if (!averageBarChartInstance) {
        if (typeof showToast === 'function') showToast("ไม่มีข้อมูลให Export");
        else alert("ไม่มีข้อมูลให Export");
        return;
    }
    const data = averageBarChartInstance.data;
    const labels = data.labels;
    const percentCompletes = data.datasets.find(d => d.label === '% Complete').data;
    const avgTargets = data.datasets.find(d => d.label === 'Average Expected').data;
    const avgActuals = data.datasets.find(d => d.label === 'Average Actual').data;

    let csvContent = "\\uFEFF" + "Employee Name,Average Expected,Average Actual,% Complete\\n";
    for (let i = 0; i < labels.length; i++) {
        csvContent += `"${labels[i]}",${avgTargets[i]},${avgActuals[i]},${percentCompletes[i]}%\\n`;
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
}"""

    # I'll use regex to match because the previous indentation might not be exactly 4 spaces
    # Let's write a robust regex
    pattern = r'function exportAverageSkillChart\(\)\s*\{[\s\S]*?document\.body\.removeChild\(link\);\s*\}'
    
    new_func = """function exportAverageSkillChart() {
    if (!averageBarChartInstance) {
        if (typeof showToast === 'function') showToast("ไม่มีข้อมูลให้ Export");
        else alert("ไม่มีข้อมูลให้ Export");
        return;
    }
    const data = averageBarChartInstance.data;
    const labels = data.labels;

    let csvContent = "\\uFEFF" + "Employee Name,Position name,Average Expected,Average Before,Average Self Eva,Average Actual,% Complete\\n";
    
    for (let i = 0; i < labels.length; i++) {
        const empName = labels[i];
        let position = "Unassigned";
        let avgT = "0.0";
        let avgB = "0.0";
        let avgS = "0.0";
        let avgA = "0.0";
        let percent = 0;

        const empId = Object.keys(dbUsers).find(id => dbUsers[id].name === empName);
        if (empId) {
            const emp = dbUsers[empId];
            position = emp.position || "Unassigned";
            
            const targets = positionTargets[emp.position] || [];
            let sumTarget = 0, sumActual = 0, sumSelf = 0, sumBefore = 0, validCompsCount = 0;
            
            for (let j = 0; j < competencies.length; j++) {
                if (selectedCompetencyGroupFilter.length > 0 && !selectedCompetencyGroupFilter.includes(competencies[j].group)) continue;
                if (selectedCompetenciesFilter.length > 0 && !selectedCompetenciesFilter.includes(competencies[j].name)) continue;

                const t = Array.isArray(targets) ? targets[j] : (targets[j] || 0);
                if (t === 0) continue;
                if (t > 0) {
                    sumTarget += t;
                    sumActual += (emp.actuals[j] || 0);
                    sumSelf += emp.self_evals ? (emp.self_evals[j] || 0) : 0;
                    sumBefore += emp.before_evals ? (emp.before_evals[j] || 0) : 0;
                    validCompsCount++;
                }
            }
            
            avgT = validCompsCount > 0 ? (sumTarget / validCompsCount).toFixed(1) : "0.0";
            avgA = validCompsCount > 0 ? (sumActual / validCompsCount).toFixed(1) : "0.0";
            avgS = validCompsCount > 0 ? (sumSelf / validCompsCount).toFixed(1) : "0.0";
            avgB = validCompsCount > 0 ? (sumBefore / validCompsCount).toFixed(1) : "0.0";
            percent = sumTarget > 0 ? Math.round((sumActual / sumTarget) * 100) : 0;
        }
        
        csvContent += `"${empName}","${position}",${avgT},${avgB},${avgS},${avgA},${percent}%\\n`;
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
}"""

    content, count = re.subn(pattern, new_func, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}, count={count}")

fix_export_excel('static/index.html')
fix_export_excel('index_render.html')
