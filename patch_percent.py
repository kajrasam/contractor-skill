import re

def fix_percent_completed(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We need to replace the logic in two places (drawAverageBarChart and exportAverageSkillChart).
    # Since they have very similar loops, let's use a regex that matches the variable declarations, loop, and calculations.

    old_logic_pattern = r'let sumTarget = 0;\s*let sumActual = 0;\s*let sumSelf = 0;\s*let sumBefore = 0;\s*let validCompsCount = 0;([\s\S]*?)const percent = sumTarget > 0 \? Math\.round\(\(sumActual / sumTarget\) \* 100\) : 0;'
    
    def replacer(match):
        body = match.group(1)
        
        # Modify the body to add sumPercent and calculate compPercent
        new_body = body.replace('let sumActual = 0;', 'let sumActual = 0;\n            let sumPercent = 0;')
        
        # Inside the loop:
        # sumActual += (emp.actuals[i] || 0); or (emp.actuals[j] || 0);
        # We need to capture the variable used for actuals.
        new_body = re.sub(
            r'sumActual \+= \((emp\.actuals\[[a-z]\] \|\| 0)\);', 
            r'const a = \1;\n                    sumActual += a;\n                    let compPercent = Math.min(100, (a / t) * 100);\n                    sumPercent += compPercent;', 
            new_body
        )
        
        # Finally, the percent calculation
        return "let sumTarget = 0;\n            let sumActual = 0;\n            let sumSelf = 0;\n            let sumBefore = 0;\n            let validCompsCount = 0;\n            let sumPercent = 0;" + new_body + "const percent = validCompsCount > 0 ? Math.round(sumPercent / validCompsCount) : 0;"
    
    content, count = re.subn(old_logic_pattern, replacer, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}, count={count}")

fix_percent_completed('static/index.html')
fix_percent_completed('index_render.html')
