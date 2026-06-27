import re

def fix_readiness(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. updateIDPProfile logic
    # Find:
    # let totalTarget = 0;
    # let totalActual = 0;
    
    old_idp_pattern = r'(let totalTarget = 0;\s*let totalActual = 0;)([\s\S]*?)const readiness = totalTarget === 0 \? 0 : Math\.round\(\(totalActual / totalTarget\) \* 100\);'
    
    def replacer_idp(match):
        decls = "let totalTarget = 0;\n    let totalActual = 0;\n    let totalPercent = 0;\n    let validCompsCount = 0;"
        body = match.group(2)
        
        # In body, replace:
        # totalActual += a;
        body = re.sub(
            r'totalActual \+= a;', 
            r'totalActual += a;\n            totalPercent += Math.min(100, (a / t) * 100);\n            validCompsCount++;', 
            body
        )
        
        return decls + body + "const readiness = validCompsCount === 0 ? 0 : Math.round(totalPercent / validCompsCount);"
        
    content, c1 = re.subn(old_idp_pattern, replacer_idp, content)

    # 2. renderTopPerformers logic
    # Find:
    # let totalT = 0; let totalA = 0;
    # ...
    # userReadiness[id] = totalT > 0 ? (totalA / totalT) * 100 : 0;
    
    old_perf_pattern = r'(let totalT = 0; let totalA = 0;)([\s\S]*?)userReadiness\[id\] = totalT > 0 \? \(totalA / totalT\) \* 100 : 0;'
    
    def replacer_perf(match):
        decls = "let totalT = 0; let totalA = 0; let totalP = 0; let validCompsCount = 0;"
        body = match.group(2)
        
        # In body, replace:
        # totalA += (emp.actuals[idx] || 0);
        body = re.sub(
            r'totalA \+= \(emp\.actuals\[idx\] \|\| 0\);',
            r'const a = (emp.actuals[idx] || 0);\n                    totalA += a;\n                    totalP += Math.min(100, (a / t) * 100);\n                    validCompsCount++;',
            body
        )
        
        return decls + body + "userReadiness[id] = validCompsCount > 0 ? (totalP / validCompsCount) : 0;"
        
    content, c2 = re.subn(old_perf_pattern, replacer_perf, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}, IDP count={c1}, Perf count={c2}")

fix_readiness('static/index.html')
fix_readiness('index_render.html')
