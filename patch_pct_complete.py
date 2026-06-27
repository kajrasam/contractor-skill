import re

def fix_pct_complete(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find:
    # let totalActualForPct = 0;
    # let totalTargetForPct = 0;
    # for (let i = 0; i < competencies.length; i++) {
    # if (targets[i] > 0) {
    # totalTargetForPct += targets[i];
    # totalActualForPct += (emp.actuals[i] || 0);
    # }
    # }
    # let pctComplete = totalTargetForPct > 0 ? Math.round((totalActualForPct / totalTargetForPct) * 100) : 0;
    
    old_pattern = r'(let totalActualForPct = 0;\s*let totalTargetForPct = 0;)([\s\S]*?)let pctComplete = totalTargetForPct > 0 \? Math\.round\(\(totalActualForPct / totalTargetForPct\) \* 100\) : 0;'
    
    def replacer(match):
        decls = "let totalActualForPct = 0;\nlet totalTargetForPct = 0;\nlet totalPercentForPct = 0;\nlet validCompsCountForPct = 0;"
        body = match.group(2)
        
        # Replace the assignments inside the loop
        # totalTargetForPct += targets[i];
        # totalActualForPct += (emp.actuals[i] || 0);
        
        body = re.sub(
            r'if\s*\(\s*targets\[i\] > 0\s*\)\s*\{',
            r'const t = targets[i] || 0;\nif (t > 0) {',
            body
        )
        body = re.sub(
            r'totalTargetForPct \+= targets\[i\];',
            r'totalTargetForPct += t;',
            body
        )
        body = re.sub(
            r'totalActualForPct \+= \(emp\.actuals\[i\] \|\| 0\);',
            r'const a = (emp.actuals[i] || 0);\ntotalActualForPct += a;\ntotalPercentForPct += Math.min(100, (a / t) * 100);\nvalidCompsCountForPct++;',
            body
        )
        
        return decls + body + "let pctComplete = validCompsCountForPct > 0 ? Math.round(totalPercentForPct / validCompsCountForPct) : 0;"
        
    content, count = re.subn(old_pattern, replacer, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}, count={count}")

fix_pct_complete('static/index.html')
fix_pct_complete('index_render.html')
