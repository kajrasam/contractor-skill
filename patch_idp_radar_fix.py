import re

def patch_idp_radar(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the loop block in drawIDPRadar
    pattern = r'(const s = emp\.self_evals \? \(emp\.self_evals\[i\] \|\| 0\) : 0;[\s\n]*cleanLabels\.push\(allLabels\[i\]\);[\s\n]*cleanTargets\.push\(t\);[\s\n]*actuals\.push\(a\);[\s\n]*selfEvals\.push\(s\);)'
    
    def replacer(match):
        return match.group(1) + '\n                window.beforeEvalsLocal.push(emp.before_evals ? (emp.before_evals[i] || 0) : 0);'
        
    new_content, count = re.subn(pattern, replacer, content)
    
    # Let's also make sure the datasets are added in the right order: Target, Before, Self, Actual
    pattern2 = r'(let activeDatasetsIDP = \[\];.*?)(idpRadarChartInstance = new Chart)'
    
    def dataset_replacer(match):
        code = match.group(1)
        new_code = """let activeDatasetsIDP = [];
            if (activeFilters.includes('target')) activeDatasetsIDP.push({ label: 'Target', data: cleanTargets, borderColor: '#cbd5e1', backgroundColor: 'transparent', borderDash: [5, 5], borderWidth: 2, pointRadius: 0 });
            if (activeFilters.includes('before')) activeDatasetsIDP.push({ label: 'Before', data: window.beforeEvalsLocal, borderColor: '#9333ea', backgroundColor: 'transparent', borderDash: [2, 2], borderWidth: 2, pointBackgroundColor: '#9333ea', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#9333ea', pointRadius: 4 });
            if (activeFilters.includes('self')) activeDatasetsIDP.push({ label: 'Self Eva.', data: selfEvals, borderColor: '#fbbf24', backgroundColor: 'rgba(251, 191, 36, 0.2)', borderWidth: 2, pointBackgroundColor: '#fbbf24', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#fbbf24', pointRadius: 4 });
            if (activeFilters.includes('actual')) activeDatasetsIDP.push({ label: 'Actual', data: actuals, borderColor: '#ca3656', backgroundColor: 'rgba(202, 54, 86, 0.25)', borderWidth: 2, pointBackgroundColor: '#ca3656', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#ca3656', pointRadius: 4 });

            """
        return new_code + match.group(2)

    new_content, count2 = re.subn(pattern2, dataset_replacer, new_content, flags=re.DOTALL)

    if count > 0 or count2 > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Patched {filepath} count1={count} count2={count2}")
    else:
        print(f"Failed to patch {filepath}")

patch_idp_radar('static/index.html')
patch_idp_radar('index_render.html')
