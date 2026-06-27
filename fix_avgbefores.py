import re

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # We use regex to safely insert avgBefores
    pattern = r'(const avgSelfs = dataToSort\.map\(d => d\.avgS\);)'
    replacement = r'\1\n            const avgBefores = dataToSort.map(d => d.avgB);'
    
    html = re.sub(pattern, replacement, html)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Patched avgBefores into {filepath}")

patch_file('static/index.html')
patch_file('index_render.html')
