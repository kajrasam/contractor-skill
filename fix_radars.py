import re

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. drawAverageBarChart
    old_avg_loop = """                let sumTarget = 0;
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

            // §ӴѺҡ % Completed ҡ仹
            dataToSort.sort((a, b) => b.percent - a.percent);

            const names = dataToSort.map(d => d.name);
            const avgTargets = dataToSort.map(d => d.avgT);
            const avgActuals = dataToSort.map(d => d.avgA);
            const avgSelfs = dataToSort.map(d => d.avgS);
            const percentCompletes = dataToSort.map(d => d.percent);"""
    
    new_avg_loop = """                let sumTarget = 0;
                let sumActual = 0;
                let sumSelf = 0;
                let sumBefore = 0;
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
                        sumBefore += emp.before_evals ? (emp.before_evals[i] || 0) : 0;
                        validCompsCount++;
                    }
                }

                const avgT = validCompsCount > 0 ? sumTarget / validCompsCount : 0;
                const avgA = validCompsCount > 0 ? sumActual / validCompsCount : 0;
                const avgS = validCompsCount > 0 ? sumSelf / validCompsCount : 0;
                const avgB = validCompsCount > 0 ? sumBefore / validCompsCount : 0;

                // Calculate % Complete
                const percent = sumTarget > 0 ? Math.round((sumActual / sumTarget) * 100) : 0;

                dataToSort.push({
                    name: emp.name,
                    avgT: avgT.toFixed(1),
                    avgA: avgA.toFixed(1),
                    avgS: avgS.toFixed(1),
                    avgB: avgB.toFixed(1),
                    percent: percent
                });
            });

            // §ӴѺҡ % Completed ҡ仹
            dataToSort.sort((a, b) => b.percent - a.percent);

            const names = dataToSort.map(d => d.name);
            const avgTargets = dataToSort.map(d => d.avgT);
            const avgActuals = dataToSort.map(d => d.avgA);
            const avgSelfs = dataToSort.map(d => d.avgS);
            const avgBefores = dataToSort.map(d => d.avgB);
            const percentCompletes = dataToSort.map(d => d.percent);"""
    
    html = html.replace(old_avg_loop, new_avg_loop)

    old_avg_chart = """            averageBarChartInstance = new Chart(ctx, {
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
                },"""
    
    new_avg_chart = """
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
                },"""
    html = html.replace(old_avg_chart, new_avg_chart)

    # 2. renderIndividualDashboards
    old_dash_indiv = """                const tData = positionTargets[emp.position] || [];
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

                const chart = new Chart(ctx, {"""
    
    new_dash_indiv = """                const tData = positionTargets[emp.position] || [];
                const aData = emp.actuals || [];
                const sData = emp.self_evals || [];
                const bData = emp.before_evals || [];

                const cleanLabels = [];
                const cleanTargets = [];
                const cleanActuals = [];
                const cleanSelfs = [];
                const cleanBefores = [];

                for (let i = 0; i < currentLabels.length; i++) {
                    if (selectedCompetencyGroupFilter.length > 0 && !selectedCompetencyGroupFilter.includes(competencies[i].group)) continue;
                    if (selectedCompetenciesFilter.length > 0 && !selectedCompetenciesFilter.includes(competencies[i].name)) continue;

                    if (tData[i] && tData[i] > 0) {
                        const parts = currentLabels[i].split('. ');
                        cleanLabels.push(parts.length > 1 ? parts.slice(1).join('. ') : currentLabels[i]);
                        cleanTargets.push(tData[i]);
                        cleanActuals.push(aData[i] || 0);
                        cleanSelfs.push(sData[i] || 0);
                        cleanBefores.push(bData[i] || 0);
                    }
                }
                
                const activeFilters = activeRadarFilters['dashboard'] || ['target', 'self', 'before', 'actual'];
                let activeDatasets = [];
                if (activeFilters.includes('target')) activeDatasets.push({ label: 'Target', data: cleanTargets, borderColor: '#94a3b8', backgroundColor: 'rgba(148, 163, 184, 0.2)' });
                if (activeFilters.includes('actual')) activeDatasets.push({ label: 'Actual', data: cleanActuals, borderColor: '#882239', backgroundColor: 'rgba(136, 34, 57, 0.3)' });
                if (activeFilters.includes('self')) activeDatasets.push({ label: 'Self Eva.', data: cleanSelfs, borderColor: '#fbbf24', backgroundColor: 'rgba(251, 191, 36, 0.2)' });
                if (activeFilters.includes('before')) activeDatasets.push({ label: 'Before', data: cleanBefores, borderColor: '#9333ea', backgroundColor: 'transparent', borderDash: [2, 2] });

                const chart = new Chart(ctx, {"""
    html = html.replace(old_dash_indiv, new_dash_indiv)

    # Note: the Chart code in renderIndividualDashboards is still old (data: { labels: cleanLabels, datasets: [ ... ] }) from the user's current index.html because patch_radar2 failed.
    old_dash_indiv_chart = """                    data: {
                        labels: cleanLabels,
                        datasets: [
                            { label: 'Target', data: cleanTargets, borderColor: '#94a3b8', backgroundColor: 'rgba(148, 163, 184, 0.2)' },
                            { label: 'Actual', data: cleanActuals, borderColor: '#882239', backgroundColor: 'rgba(136, 34, 57, 0.3)' },
                            { label: 'Self Eva.', data: cleanSelfs, borderColor: '#fbbf24', backgroundColor: 'rgba(251, 191, 36, 0.2)' }
                        ]
                    },"""
    new_dash_indiv_chart = """                    data: {
                        labels: cleanLabels,
                        datasets: activeDatasets
                    },"""
    html = html.replace(old_dash_indiv_chart, new_dash_indiv_chart)

    # 3. IDP Tab (setupIDPTab/renderIDPContent uses idpRadarChartInstance)
    old_idp_loop = """                const a = emp.actuals[i] || 0;
                const s = emp.self_evals ? (emp.self_evals[i] || 0) : 0;
                cleanLabels.push(allLabels[i]);
                cleanTargets.push(t);
                actuals.push(a);
                selfEvals.push(s);
                cleanDescs.push(competencies[i].levels[a] || "դ͸Ժ");"""
    
    new_idp_loop = """                const a = emp.actuals[i] || 0;
                const s = emp.self_evals ? (emp.self_evals[i] || 0) : 0;
                const b = emp.before_evals ? (emp.before_evals[i] || 0) : 0;
                cleanLabels.push(allLabels[i]);
                cleanTargets.push(t);
                actuals.push(a);
                selfEvals.push(s);
                if (typeof beforeEvals === 'undefined') { window.beforeEvalsLocal = []; }
                window.beforeEvalsLocal.push(b);
                cleanDescs.push(competencies[i].levels[a] || "դ͸Ժ");"""
    
    html = html.replace("            let selfEvals = [];\n", "            let selfEvals = [];\n            window.beforeEvalsLocal = [];\n")
    html = html.replace(old_idp_loop, new_idp_loop)

    old_idp_chart = """            idpRadarChartInstance = new Chart(ctx, {
                type: 'radar',
                data: {
                    labels: cleanLabels,
                    datasets: [
                        { label: 'Target', data: cleanTargets, borderColor: '#cbd5e1', backgroundColor: 'transparent', borderDash: [5, 5], borderWidth: 2, pointRadius: 0 },
                        { label: 'Actual', data: actuals, borderColor: '#ca3656', backgroundColor: 'rgba(202, 54, 86, 0.25)', borderWidth: 2, pointBackgroundColor: '#ca3656', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#ca3656', pointRadius: 4 },
                        { label: 'Self Eva.', data: selfEvals, borderColor: '#fbbf24', backgroundColor: 'rgba(251, 191, 36, 0.2)', borderWidth: 2, pointBackgroundColor: '#fbbf24', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#fbbf24', pointRadius: 4 }
                    ]
                },"""
    new_idp_chart = """            const activeFilters = activeRadarFilters['idp'] || ['target', 'self', 'before', 'actual'];
            let activeDatasetsIDP = [];
            if (activeFilters.includes('target')) activeDatasetsIDP.push({ label: 'Target', data: cleanTargets, borderColor: '#cbd5e1', backgroundColor: 'transparent', borderDash: [5, 5], borderWidth: 2, pointRadius: 0 });
            if (activeFilters.includes('actual')) activeDatasetsIDP.push({ label: 'Actual', data: actuals, borderColor: '#ca3656', backgroundColor: 'rgba(202, 54, 86, 0.25)', borderWidth: 2, pointBackgroundColor: '#ca3656', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#ca3656', pointRadius: 4 });
            if (activeFilters.includes('self')) activeDatasetsIDP.push({ label: 'Self Eva.', data: selfEvals, borderColor: '#fbbf24', backgroundColor: 'rgba(251, 191, 36, 0.2)', borderWidth: 2, pointBackgroundColor: '#fbbf24', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#fbbf24', pointRadius: 4 });
            if (activeFilters.includes('before')) activeDatasetsIDP.push({ label: 'Before', data: window.beforeEvalsLocal, borderColor: '#9333ea', backgroundColor: 'transparent', borderDash: [2, 2], borderWidth: 2, pointBackgroundColor: '#9333ea', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#9333ea', pointRadius: 4 });

            idpRadarChartInstance = new Chart(ctx, {
                type: 'radar',
                data: {
                    labels: cleanLabels,
                    datasets: activeDatasetsIDP
                },"""
    html = html.replace(old_idp_chart, new_idp_chart)

    # 4. Analytic Tab
    old_analytic_loop = """                    let labels = [];
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

                    const chart = new Chart(ctx, {"""
    
    new_analytic_loop = """                    let labels = [];
                    let targetData = [];
                    let actualsData = [];

                    const topEmp = dbUsers[topUsers[0]];
                    let selfData = [];
                    let beforeData = [];

                    compIndices.forEach(idx => {
                        const t = targets[idx] || 0;
                        if (t > 0) {
                            labels.push(competencies[idx].name.replace(/^[0-9\.\s]+/, ''));
                            targetData.push(t);
                            actualsData.push(topEmp.actuals[idx] || 0);
                            selfData.push(topEmp.self_evals ? (topEmp.self_evals[idx] || 0) : 0);
                            beforeData.push(topEmp.before_evals ? (topEmp.before_evals[idx] || 0) : 0);
                        }
                    });

                    const activeFilters = activeRadarFilters['analytic'] || ['target', 'self', 'before', 'actual'];
                    let activeDatasetsAnalytic = [];
                    if (activeFilters.includes('target')) activeDatasetsAnalytic.push({ label: 'Target', data: targetData, borderColor: '#cbd5e1', backgroundColor: 'transparent', borderDash: [5, 5], borderWidth: 2, pointRadius: 0 });
                    if (activeFilters.includes('actual')) activeDatasetsAnalytic.push({ label: 'Actual', data: actualsData, borderColor: '#ca3656', backgroundColor: 'rgba(202, 54, 86, 0.25)', borderWidth: 2, pointBackgroundColor: '#ca3656', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#ca3656', pointRadius: 3 });
                    if (activeFilters.includes('self')) activeDatasetsAnalytic.push({ label: 'Self Eva.', data: selfData, borderColor: '#fbbf24', backgroundColor: 'rgba(251, 191, 36, 0.2)', borderWidth: 2, pointBackgroundColor: '#fbbf24', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#fbbf24', pointRadius: 3 });
                    if (activeFilters.includes('before')) activeDatasetsAnalytic.push({ label: 'Before', data: beforeData, borderColor: '#9333ea', backgroundColor: 'transparent', borderDash: [2, 2], borderWidth: 2, pointBackgroundColor: '#9333ea', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#9333ea', pointRadius: 3 });

                    const chart = new Chart(ctx, {"""
    
    html = html.replace(old_analytic_loop, new_analytic_loop)

    old_analytic_chart = """                    data: {
                            labels: labels,
                            datasets: [
                                { label: 'Target', data: targetData, borderColor: '#cbd5e1', backgroundColor: 'transparent', borderDash: [5, 5], borderWidth: 2, pointRadius: 0 },
                                { label: 'Actual', data: actualsData, borderColor: '#ca3656', backgroundColor: 'rgba(202, 54, 86, 0.25)', borderWidth: 2, pointBackgroundColor: '#ca3656', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#ca3656', pointRadius: 3 },
                                { label: 'Self Eva.', data: selfData, borderColor: '#fbbf24', backgroundColor: 'rgba(251, 191, 36, 0.2)', borderWidth: 2, pointBackgroundColor: '#fbbf24', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#fbbf24', pointRadius: 3 }
                            ]
                        },"""
    new_analytic_chart = """                    data: {
                            labels: labels,
                            datasets: activeDatasetsAnalytic
                        },"""
    html = html.replace(old_analytic_chart, new_analytic_chart)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Patched {filepath} successfully!")

patch_file('static/index.html')
patch_file('index_render.html')
