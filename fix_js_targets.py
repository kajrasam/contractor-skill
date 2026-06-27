import re

def fix_position_targets_js(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix the object initialization
    old_init = "if (!positionTargets[pos]) positionTargets[pos] = {};"
    new_init = "if (!positionTargets[pos]) positionTargets[pos] = Array(competencies.length).fill(0);"
    content = content.replace(old_init, new_init)

    # To be extremely safe for existing data (since users might not reload the page or clear cache), 
    # we should also ensure targets is converted to an array if it's an object in updateEvalUI and other radar chart places.
    # But replacing `const targets = positionTargets[pName] || [];` is tricky if there are many of them.
    # Let's just fix updateEvalUI specifically, as that is where it crashes:
    
    old_has_mapped = "const hasMappedCompetency = targets.some(t => t > 0);"
    new_has_mapped = "const hasMappedCompetency = Array.isArray(targets) ? targets.some(t => t > 0) : Object.values(targets).some(t => t > 0);"
    content = content.replace(old_has_mapped, new_has_mapped)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}")

fix_position_targets_js('static/index.html')
fix_position_targets_js('index_render.html')
