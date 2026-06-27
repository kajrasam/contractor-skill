import re

def fix_grab(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    out = []
    in_save_eval = False
    for line in lines:
        if 'async function saveEvaluation()' in line:
            in_save_eval = True
        
        out.append(line)
        
        if in_save_eval and 'emp.actuals[i] = parseInt(elActual.value);' in line:
            # We are inside the if (elActual) block, so we inject after it closes.
            # Wait, better to just inject after the closing brace of if (elActual)
            pass
            
    # Actually, simpler: regex on the whole string
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    pattern = r"const elActual = document\.getElementById\(`eval-actual-\$\{id\}-\$\{i\}`\);\s*if \(elActual\) \{\s*emp\.actuals\[i\] = parseInt\(elActual\.value\);\s*\}"
    replacement = """const elActual = document.getElementById(`eval-actual-${id}-${i}`);
                if (elActual) {
                    emp.actuals[i] = parseInt(elActual.value);
                }

                // Grab before eval if exists
                const elBefore = document.getElementById(`eval-before-${id}-${i}`);
                if (elBefore) {
                    if (!emp.before_evals) emp.before_evals = [];
                    emp.before_evals[i] = parseInt(elBefore.value);
                }"""
                
    content = re.sub(pattern, replacement, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}")

fix_grab('static/index.html')
fix_grab('index_render.html')
