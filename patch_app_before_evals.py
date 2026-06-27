import re

def patch_app_py(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update get_data to fetch before_level
    # Locate: self_evals = [a.get("self_level") for a in user_acts]
    pattern1 = r'self_evals = \[a\.get\("self_level"\) for a in user_acts\]'
    replacement1 = r'self_evals = [a.get("self_level") for a in user_acts]\n        before_evals = [a.get("before_level") for a in user_acts]'
    content = re.sub(pattern1, replacement1, content)
    
    # Locate: "self_evals": self_evals,
    pattern2 = r'"self_evals": self_evals,'
    replacement2 = r'"self_evals": self_evals,\n            "before_evals": before_evals,'
    content = re.sub(pattern2, replacement2, content)

    # 2. Update update_evaluation to save before_level
    # Locate: self_evals = data.get('selfEvals', [])
    pattern3 = r'self_evals = data\.get\(\'selfEvals\', \[\]\)'
    replacement3 = r'self_evals = data.get(\'selfEvals\', [])\n    before_evals = data.get(\'beforeEvals\', [])'
    content = re.sub(pattern3, replacement3, content)
    
    # Locate: sval = self_evals[idx] if idx < len(self_evals) else None
    pattern4 = r'sval = self_evals\[idx\] if idx < len\(self_evals\) else None'
    replacement4 = r'sval = self_evals[idx] if idx < len(self_evals) else None\n        bval = before_evals[idx] if idx < len(before_evals) else None'
    content = re.sub(pattern4, replacement4, content)
    
    # Locate: "self_level": sval, (in both insert and update)
    pattern5 = r'"self_level": sval,'
    replacement5 = r'"self_level": sval,\n                    "before_level": bval,'
    content = re.sub(pattern5, replacement5, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched app.py")

patch_app_py('app.py')
