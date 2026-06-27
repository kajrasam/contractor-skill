import re

def fix_position_targets_some(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    old_logic = "hasTargets = positionTargets[posName].some(t => t >= 1);"
    new_logic = "hasTargets = Array.isArray(positionTargets[posName]) ? positionTargets[posName].some(t => t >= 1) : Object.values(positionTargets[posName]).some(t => t >= 1);"
    
    content = content.replace(old_logic, new_logic)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}")

fix_position_targets_some('static/index.html')
fix_position_targets_some('index_render.html')
