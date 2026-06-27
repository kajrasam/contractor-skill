import re

def patch_chart_text(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match the text drawing block for '% Complete'
    pattern = r'(if\s*\(dataset\.label\s*===\s*\'%\s*Complete\'\)\s*\{\s*ctx\.fillStyle\s*=\s*)\'#[^\']+\'(.*?ctx\.fillText.*?datapoint\.y\s*-\s*)\d+(\);)'
    
    def replacer(match):
        return match.group(1) + "'#16a34a'" + match.group(2) + "8" + match.group(3)
        
    content, count = re.subn(pattern, replacer, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}, count={count}")

patch_chart_text('static/index.html')
patch_chart_text('index_render.html')
