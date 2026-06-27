import re

def fix_export_percent(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match in exportAverageSkillChart
    old_logic_pattern = r'let sumTarget = 0, sumActual = 0, sumSelf = 0, sumBefore = 0, validCompsCount = 0;([\s\S]*?)percent = sumTarget > 0 \? Math\.round\(\(sumActual / sumTarget\) \* 100\) : 0;'
    
    def replacer(match):
        body = match.group(1)
        
        # Inside the loop:
        # sumActual += (emp.actuals[j] || 0);
        new_body = re.sub(
            r'sumActual \+= \((emp\.actuals\[j\] \|\| 0)\);', 
            r'const a = \1;\n                    sumActual += a;\n                    let compPercent = Math.min(100, (a / t) * 100);\n                    sumPercent += compPercent;', 
            body
        )
        
        return "let sumTarget = 0, sumActual = 0, sumSelf = 0, sumBefore = 0, validCompsCount = 0, sumPercent = 0;" + new_body + "percent = validCompsCount > 0 ? Math.round(sumPercent / validCompsCount) : 0;"
    
    content, count = re.subn(old_logic_pattern, replacer, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}, count={count}")

fix_export_percent('static/index.html')
fix_export_percent('index_render.html')
