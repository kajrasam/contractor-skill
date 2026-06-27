import re

def fix_position_targets_app(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    old_logic = """# 3. positionTargets
    pt_res = supabase.table("position_targets").select("*").order("position_name").order("competency_idx").execute()
    positionTargets = {}
    for pt in pt_res.data:
        pos = pt["position_name"]
        if pos not in positionTargets:
            positionTargets[pos] = []
        positionTargets[pos].append(pt["target_level"])"""

    new_logic = """# 3. positionTargets
    pt_res = supabase.table("position_targets").select("*").order("position_name").order("competency_idx").execute()
    positionTargets = {}
    for pt in pt_res.data:
        pos = pt["position_name"]
        if pos not in positionTargets:
            positionTargets[pos] = [0] * len(competencies)
        idx = pt["competency_idx"]
        if idx < len(competencies):
            positionTargets[pos][idx] = pt["target_level"]"""
            
    content = content.replace(old_logic, new_logic)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}")

fix_position_targets_app('app.py')
