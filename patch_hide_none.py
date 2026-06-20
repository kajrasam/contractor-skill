import re

files = [
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html',
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/index_render.html'
]

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update updateEvalUI & renderIDPTab
    content = content.replace(
        "const targetVal = targets[i] || 0;",
        "const targetVal = targets[i] || 0;\n                if (targetVal === 0) continue;"
    )

    # 2. Update Radars
    content = content.replace(
        "const t = targets[i] || 0;",
        "const t = targets[i] || 0;\n                if (t === 0) continue;"
    )

    # 3. Update buildTrainingMatrix
    old_tm = """                if(selectedCompetencyGroupFilter.length > 0 && !selectedCompetencyGroupFilter.includes(comp.group)) return;
                if(selectedCompetenciesFilter.length > 0 && !selectedCompetenciesFilter.includes(comp.name)) return;"""
    
    new_tm = """                if(selectedCompetencyGroupFilter.length > 0 && !selectedCompetencyGroupFilter.includes(comp.group)) return;
                if(selectedCompetenciesFilter.length > 0 && !selectedCompetenciesFilter.includes(comp.name)) return;
                
                if (!isAdmin || !isEditMode) {
                    let hasTarget = false;
                    visiblePos.forEach(pos => {
                        const t = positionTargets[pos] && positionTargets[pos][compIndex] ? positionTargets[pos][compIndex] : 0;
                        if (t > 0) hasTarget = true;
                    });
                    if (!hasTarget) return;
                }"""
    
    content = content.replace(old_tm, new_tm)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Patched {len(files)} files to hide unmapped competencies.")
