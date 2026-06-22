import re

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    helper_func = """function hasCompetencyFilterMatch(posName) {
            if (selectedCompetencyGroupFilter.length === 0 && selectedCompetenciesFilter.length === 0) return true;
            if (!posName || !trainingMatrix[posName]) return false;
            
            let filteredComps = competencies;
            if (selectedCompetencyGroupFilter.length > 0) {
                filteredComps = filteredComps.filter(c => selectedCompetencyGroupFilter.includes(c.group));
            }
            if (selectedCompetenciesFilter.length > 0) {
                filteredComps = filteredComps.filter(c => selectedCompetenciesFilter.includes(c.name));
            }
            
            const indices = filteredComps.map(c => competencies.findIndex(x => x.id === c.id));
            const targets = trainingMatrix[posName];
            
            for (let idx of indices) {
                if (targets[idx] && targets[idx] > 0) return true;
            }
            return false;
        }

        function matchesOrgFiltersData(eData) {"""
        
    html = html.replace('function matchesOrgFiltersData(eData) {', helper_func)

    # 1. Patch matchesOrgFiltersData
    org_patch = """let posName = eData.PositionNameThai || eData.position_name || eData.position;
            if (!hasCompetencyFilterMatch(posName)) return false;"""
    html = html.replace('let posName = eData.PositionNameThai || eData.position_name || eData.position;', org_patch)

    # 2. Patch matchesFiltersExcept
    except_patch = """let posName = e.PositionNameThai || e.position_name;
            if (ignoreFilter !== 'competency' && !hasCompetencyFilterMatch(posName)) return false;"""
    html = html.replace('let posName = e.PositionNameThai || e.position_name;', except_patch)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Patched {filepath}")

patch_file('static/index.html')
patch_file('index_render.html')
