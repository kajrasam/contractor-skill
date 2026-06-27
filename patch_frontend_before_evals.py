import re

def patch_frontend(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update saveEvaluation payload to send beforeEvals
    # Look for: JSON.stringify({ userId: id, actuals, selfEvals, supervisorFeedbacks, evidences, additionalExpectations, learningTopics, evalDate: emp.evalDate, evalStatus: emp.eval_status, specialExpertise: emp.special_expertise, specialExpertiseDetail: emp.special_expertise_detail })
    pattern1 = r'JSON\.stringify\(\{\s*userId:\s*id,\s*actuals,\s*selfEvals,\s*supervisorFeedbacks,\s*evidences,\s*additionalExpectations,\s*learningTopics,\s*evalDate:'
    replacement1 = r'JSON.stringify({ userId: id, actuals, selfEvals, beforeEvals, supervisorFeedbacks, evidences, additionalExpectations, learningTopics, evalDate:'
    content = re.sub(pattern1, replacement1, content)

    # 2. Reorder activeDatasetsBar in drawAverageBarChart
    # The order of `activeDatasetsBar.push` determines the order in the chart.
    # Current order usually: Target, Actual, Self, Before.
    # New order: Target, Before, Self, Actual
    old_bar_pushes = """            if (activeFilters.includes('target')) activeDatasetsBar.push({ label: 'Average Expected', data: avgTargets, backgroundColor: '#cbd5e1', yAxisID: 'y', borderRadius: 6 });
            if (activeFilters.includes('actual')) activeDatasetsBar.push({ label: 'Average Actual', data: avgActuals, backgroundColor: '#ca3656', yAxisID: 'y', borderRadius: 6 });
            if (activeFilters.includes('self')) activeDatasetsBar.push({ label: 'Average Self', data: avgSelfs, backgroundColor: '#fbbf24', yAxisID: 'y', borderRadius: 6 });
            if (activeFilters.includes('before')) activeDatasetsBar.push({ label: 'Average Before', data: avgBefores, backgroundColor: '#9333ea', yAxisID: 'y', borderRadius: 6 });"""
            
    new_bar_pushes = """            if (activeFilters.includes('target')) activeDatasetsBar.push({ label: 'Average Expected', data: avgTargets, backgroundColor: '#cbd5e1', yAxisID: 'y', borderRadius: 6 });
            if (activeFilters.includes('before')) activeDatasetsBar.push({ label: 'Average Before', data: avgBefores, backgroundColor: '#9333ea', yAxisID: 'y', borderRadius: 6 });
            if (activeFilters.includes('self')) activeDatasetsBar.push({ label: 'Average Self', data: avgSelfs, backgroundColor: '#fbbf24', yAxisID: 'y', borderRadius: 6 });
            if (activeFilters.includes('actual')) activeDatasetsBar.push({ label: 'Average Actual', data: avgActuals, backgroundColor: '#ca3656', yAxisID: 'y', borderRadius: 6 });"""
    
    content = content.replace(old_bar_pushes, new_bar_pushes)

    # 3. Reorder activeDatasets in renderIndividualDashboards
    old_indiv_pushes = """                if (activeFilters.includes('target')) activeDatasets.push({ label: 'Target', data: cleanTargets, borderColor: '#94a3b8', backgroundColor: 'rgba(148, 163, 184, 0.2)' });
                if (activeFilters.includes('actual')) activeDatasets.push({ label: 'Actual', data: cleanActuals, borderColor: '#882239', backgroundColor: 'rgba(136, 34, 57, 0.3)' });
                if (activeFilters.includes('self')) activeDatasets.push({ label: 'Self Eva.', data: cleanSelfs, borderColor: '#fbbf24', backgroundColor: 'rgba(251, 191, 36, 0.2)' });
                if (activeFilters.includes('before')) activeDatasets.push({ label: 'Before', data: cleanBefores, borderColor: '#9333ea', backgroundColor: 'transparent', borderDash: [2, 2] });"""
                
    new_indiv_pushes = """                if (activeFilters.includes('target')) activeDatasets.push({ label: 'Target', data: cleanTargets, borderColor: '#94a3b8', backgroundColor: 'rgba(148, 163, 184, 0.2)' });
                if (activeFilters.includes('before')) activeDatasets.push({ label: 'Before', data: cleanBefores, borderColor: '#9333ea', backgroundColor: 'transparent', borderDash: [2, 2] });
                if (activeFilters.includes('self')) activeDatasets.push({ label: 'Self Eva.', data: cleanSelfs, borderColor: '#fbbf24', backgroundColor: 'rgba(251, 191, 36, 0.2)' });
                if (activeFilters.includes('actual')) activeDatasets.push({ label: 'Actual', data: cleanActuals, borderColor: '#882239', backgroundColor: 'rgba(136, 34, 57, 0.3)' });"""

    content = content.replace(old_indiv_pushes, new_indiv_pushes)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}")

patch_frontend('static/index.html')
patch_frontend('index_render.html')
