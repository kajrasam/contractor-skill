import os

def patch_file(filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # First replace the specific longer string
    html = html.replace('Training Need & Competency Mapping', 'Role & Competency Mapping')
    
    # Then replace the shorter string everywhere else
    html = html.replace('Training Need', 'Role & Competency')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Patched {filepath}")

patch_file('index_render.html')
patch_file('static/index.html')
