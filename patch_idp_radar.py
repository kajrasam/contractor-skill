import re

files = [
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html',
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/index_render.html'
]

# We will just replace the drawIDPRadar function
for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the drawIDPRadar function and replace the whole thing
    pattern = r"function drawIDPRadar\(emp, targets\) \{.*?options: \{.*?scales: \{"
    
    replacement = """function drawIDPRadar(emp, targets) {
            let actuals = [];
            let cleanLabels = [];
            let cleanTargets = [];
            let cleanDescs = [];
            let cleanEvidences = [];
            
            const allLabels = getLabels().map(l => {
                const parts = l.split('. ');
                return parts.length > 1 ? parts.slice(1).join('. ') : l;
            });

            for (let i = 0; i < competencies.length; i++) {
                if(selectedCompetencyGroupFilter.length > 0 && !selectedCompetencyGroupFilter.includes(competencies[i].group)) continue;
                if(selectedCompetenciesFilter.length > 0 && !selectedCompetenciesFilter.includes(competencies[i].name)) continue;
                
                const t = targets[i] || 0;
                if (t === 0) continue;
                
                const a = emp.actuals[i] || 0;
                cleanLabels.push(allLabels[i]);
                cleanTargets.push(t);
                actuals.push(a);
                cleanDescs.push(competencies[i].levels[a] || "ไม่มีคำอธิบาย");
                cleanEvidences.push(emp.evidences[i] || "ไม่มีหลักฐานที่ระบุ");
            }

            if(idpRadarChartInstance) idpRadarChartInstance.destroy();
            const ctx = document.getElementById('idpRadarChart').getContext('2d');

            idpRadarChartInstance = new Chart(ctx, {
                type: 'radar',
                data: {
                    labels: cleanLabels, 
                    datasets: [
                        { label: 'Target', data: cleanTargets, borderColor: '#cbd5e1', backgroundColor: 'transparent', borderDash: [5,5], borderWidth: 2, pointRadius: 0 },
                        { label: 'Actual', data: actuals, borderColor: '#ca3656', backgroundColor: 'rgba(202, 54, 86, 0.25)', borderWidth: 2, pointBackgroundColor: '#ca3656', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#ca3656', pointRadius: 4 }
                    ]
                },
                options: { 
                    responsive: true, 
                    maintainAspectRatio: false, 
                    plugins: {
                        legend: { display: true, position: 'bottom' },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return context.dataset.label + ': Level ' + context.raw;
                                },
                                afterLabel: function(context) {
                                    if(context.dataset.label === 'Actual') {
                                        const idx = context.dataIndex;
                                        
                                        // Wrap text function to prevent extremely wide tooltips
                                        const wrapText = (text, maxLineLen) => {
                                            const words = text.split(' ');
                                            let lines = [];
                                            let currentLine = '';
                                            words.forEach(word => {
                                                if((currentLine + word).length > maxLineLen) {
                                                    lines.push(currentLine.trim());
                                                    currentLine = word + ' ';
                                                } else {
                                                    currentLine += word + ' ';
                                                }
                                            });
                                            if(currentLine) lines.push(currentLine.trim());
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
                    scales: {"""
    
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Patched {len(files)} files with new Tooltip feature.")
