import re

with open('d:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

target = """        function buildCompetencySection() {
            const container = document.getElementById('competency-target-container');
            if(!container) return;
            
            let visibleCompSet = new Set();
            visiblePos.forEach(p => {
                if (positionTargets[p]) {
                    positionTargets[p].forEach((t, i) => {
                        if (t > 0) visibleCompSet.add(i);
                    });
                }
            });"""

replacement = """        function buildCompetencySection() {
            const container = document.getElementById('competency-target-container');
            if(!container) return;
            
            let visibleCompSet = new Set();
            if (competencies) {
                competencies.forEach((c, i) => visibleCompSet.add(i));
            }"""

if target in content:
    content = content.replace(target, replacement)
    with open('d:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched buildCompetencySection successfully")
else:
    print("Could not find target block!")
