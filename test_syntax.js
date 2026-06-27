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

            const activeFilters = activeRadarFilters['dashboard'] || ['target', 'self', 'before', 'actual'];
            let activeDatasetsBar = [
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
                }
            ];
            
            if (activeFilters.includes('target')) activeDatasetsBar.push({ label: 'Average Expected', data: avgTargets, backgroundColor: '#cbd5e1', yAxisID: 'y', borderRadius: 6 });
            if (activeFilters.includes('actual')) activeDatasetsBar.push({ label: 'Average Actual', data: avgActuals, backgroundColor: '#ca3656', yAxisID: 'y', borderRadius: 6 });
            if (activeFilters.includes('self')) activeDatasetsBar.push({ label: 'Average Self', data: avgSelfs, backgroundColor: '#fbbf24', yAxisID: 'y', borderRadius: 6 });
            if (activeFilters.includes('before')) activeDatasetsBar.push({ label: 'Average Before', data: avgBefores, backgroundColor: '#9333ea', yAxisID: 'y', borderRadius: 6 });

            averageBarChartInstance = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: names,
                    datasets: activeDatasetsBar
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

        